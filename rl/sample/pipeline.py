"""JSON stream / NPZ export / train-test split helpers for workspace sampling."""

from __future__ import annotations

import json
import math
import os
import time
from dataclasses import dataclass
from typing import Any, Iterable, Iterator

import numpy as np

from sample.constants import REACH_JOINT_NAMES

ALLOWED_SAVE_FORMATS = {"json", "jsonl", "npz"}


@dataclass
class PipelinePaths:
    output_json: str
    merged_npz: str
    train_npz: str
    test_npz: str

    @property
    def stream_dir(self) -> str:
        base_dir = os.path.dirname(os.path.abspath(self.output_json)) or "."
        stem = os.path.splitext(os.path.basename(self.output_json))[0]
        return os.path.join(base_dir, f"{stem}_stream")

    @property
    def manifest_path(self) -> str:
        return os.path.join(self.stream_dir, "manifest.json")


def _atomic_write_text(path: str, content: str) -> None:
    tmp = f"{path}.tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        handle.write(content)
    os.replace(tmp, path)


def _atomic_write_json(path: str, obj: dict | list) -> None:
    _atomic_write_text(path, json.dumps(obj, ensure_ascii=False, indent=2))


def parse_save_formats(raw: str) -> list[str]:
    parts = [item.strip().lower() for item in raw.split(",") if item.strip()]
    if not parts:
        raise ValueError("save_formats 不能为空")
    bad = [item for item in parts if item not in ALLOWED_SAVE_FORMATS]
    if bad:
        raise ValueError(f"不支持的保存格式: {bad}，允许: {sorted(ALLOWED_SAVE_FORMATS)}")
    out: list[str] = []
    seen: set[str] = set()
    for item in parts:
        if item not in seen:
            out.append(item)
            seen.add(item)
    return out


def validate_pipeline_config(
    *,
    enable_sample: bool,
    enable_split: bool,
    save_formats: list[str],
    paths: PipelinePaths,
) -> None:
    if not enable_sample and not enable_split:
        raise ValueError("必须至少启用 sample 或 split 之一")

    if enable_sample:
        if not any(fmt in save_formats for fmt in ("json", "npz")):
            raise ValueError("启用 sample 时，save_formats 必须包含 json 或 npz 至少一项")
    else:
        pass

    if enable_split and not enable_sample:
        if not os.path.isfile(paths.merged_npz):
            raise FileNotFoundError(
                "仅启用 split，但未找到合并 NPZ 文件: "
                f"{paths.merged_npz}\n"
                "请先运行一次采样生成该文件，或通过 --merged-npz 指定有效路径。"
            )


def normalize_quat_wxyz(quat: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(quat, axis=-1, keepdims=True)
    norm = np.clip(norm, 1e-8, None)
    return quat / norm


def quat_rotate_wxyz(quat: np.ndarray, vec: np.ndarray) -> np.ndarray:
    qw = quat[:, :1]
    qxyz = quat[:, 1:]
    t = 2.0 * np.cross(qxyz, vec, axis=-1)
    return vec + qw * t + np.cross(qxyz, t, axis=-1)


def iter_records_from_manifest(manifest_path: str) -> Iterator[dict[str, Any]]:
    with open(manifest_path, "r", encoding="utf-8") as handle:
        manifest = json.load(handle)
    chunk_files = manifest.get("chunk_files", {}).get("json", [])
    if not chunk_files:
        raise ValueError(f"manifest 中未找到 chunk_files['json']: {manifest_path}")
    base_dir = os.path.dirname(os.path.abspath(manifest_path))
    for rel in chunk_files:
        chunk_path = os.path.join(base_dir, rel)
        with open(chunk_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, list):
            continue
        for record in data:
            yield record


def iter_records_from_merged_json(json_path: str) -> Iterator[dict[str, Any]]:
    with open(json_path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError(f"合并 JSON 不是列表: {json_path}")
    yield from data


def extract_pose_from_record(
    record: dict[str, Any],
) -> tuple[np.ndarray, np.ndarray] | None:
    for key in ("tcp", "end_effector"):
        block = record.get(key, {})
        if not isinstance(block, dict):
            continue
        pos_d = block.get("pos", {})
        quat_d = block.get("quat", {})
        required_pos = ("x", "y", "z")
        required_quat = ("w", "x", "y", "z")
        if not all(k in pos_d for k in required_pos):
            continue
        if not all(k in quat_d for k in required_quat):
            continue
        pos = np.array([pos_d["x"], pos_d["y"], pos_d["z"]], dtype=np.float32)
        quat = np.array([quat_d["w"], quat_d["x"], quat_d["y"], quat_d["z"]], dtype=np.float32)
        return pos, quat
    return None


class ChunkedDataSink:
    """按块增量落盘 JSON，并支持中断恢复。"""

    def __init__(
        self,
        paths: PipelinePaths,
        save_formats: list[str],
        flush_every: int,
        resume: bool,
        merge_json_at_end: bool,
    ):
        self.paths = paths
        self.save_formats = save_formats
        self.flush_every = max(1, int(flush_every))
        self.resume = bool(resume)
        self.merge_json_at_end = bool(merge_json_at_end)

        self.run_dir = paths.stream_dir
        if os.path.exists(self.run_dir) and not self.resume:
            suffix = int(time.time())
            base_dir = os.path.dirname(self.run_dir)
            stem = os.path.basename(self.run_dir)
            self.run_dir = os.path.join(base_dir, f"{stem}_{suffix}")
            print(f"[INFO] 检测到已有流式目录，已新建: {self.run_dir}")
        os.makedirs(self.run_dir, exist_ok=True)

        self.manifest_path = os.path.join(self.run_dir, "manifest.json")
        self.pending: list[dict[str, Any]] = []
        self.chunk_id = 0
        self.total_records = 0
        self.chunk_files: dict[str, list[str]] = {fmt: [] for fmt in save_formats if fmt != "npz"}

        if self.resume and os.path.isfile(self.manifest_path):
            with open(self.manifest_path, "r", encoding="utf-8") as handle:
                manifest = json.load(handle)
            self.chunk_id = int(manifest.get("chunk_id", 0))
            self.total_records = int(manifest.get("total_records", 0))
            prev = manifest.get("chunk_files", {})
            if isinstance(prev, dict):
                for fmt in self.chunk_files:
                    self.chunk_files[fmt] = list(prev.get(fmt, []))
            print(
                f"[INFO] 续跑恢复：records={self.total_records}, chunk_id={self.chunk_id}"
            )

    def add(self, record: dict[str, Any]) -> None:
        self.pending.append(record)
        if len(self.pending) >= self.flush_every:
            self.flush()

    def _write_chunk_json(self, path: str, records: list[dict[str, Any]]) -> None:
        _atomic_write_json(path, records)

    def _write_chunk_jsonl(self, path: str, records: list[dict[str, Any]]) -> None:
        lines = "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n"
        _atomic_write_text(path, lines)

    def flush(self) -> None:
        if not self.pending:
            return
        self.chunk_id += 1
        chunk_tag = f"chunk_{self.chunk_id:06d}"
        records = self.pending

        for fmt in self.save_formats:
            if fmt == "npz":
                continue
            if fmt == "json":
                chunk_path = os.path.join(self.run_dir, f"{chunk_tag}.json")
                self._write_chunk_json(chunk_path, records)
            elif fmt == "jsonl":
                chunk_path = os.path.join(self.run_dir, f"{chunk_tag}.jsonl")
                self._write_chunk_jsonl(chunk_path, records)
            else:
                raise RuntimeError(f"未知保存格式: {fmt}")
            self.chunk_files[fmt].append(os.path.basename(chunk_path))

        self.total_records += len(records)
        self.pending = []
        manifest = {
            "chunk_id": self.chunk_id,
            "total_records": self.total_records,
            "save_formats": [fmt for fmt in self.save_formats if fmt != "npz"],
            "chunk_files": self.chunk_files,
            "output_path": self.paths.output_json,
            "merged_npz": self.paths.merged_npz,
        }
        _atomic_write_json(self.manifest_path, manifest)
        print(f"[INFO] 已落盘 {chunk_tag}，累计 records={self.total_records}", flush=True)

    def _merge_json_chunks(self) -> None:
        if "json" not in self.save_formats:
            return
        if not self.chunk_files.get("json"):
            _atomic_write_text(self.paths.output_json, "[]\n")
            return
        tmp = f"{self.paths.output_json}.tmp"
        with open(tmp, "w", encoding="utf-8") as out:
            out.write("[\n")
            first = True
            for filename in self.chunk_files["json"]:
                chunk_path = os.path.join(self.run_dir, filename)
                with open(chunk_path, "r", encoding="utf-8") as handle:
                    arr = json.load(handle)
                for record in arr:
                    if not first:
                        out.write(",\n")
                    out.write(json.dumps(record, ensure_ascii=False, indent=2))
                    first = False
            out.write("\n]\n")
        os.replace(tmp, self.paths.output_json)
        print(f"[INFO] 已合并 JSON 到: {self.paths.output_json}")

    def finalize(self) -> None:
        self.flush()
        if self.merge_json_at_end:
            self._merge_json_chunks()


def records_to_npz(
    records: Iterable[dict[str, Any]],
    output_path: str,
    *,
    skip_collision: bool = False,
    tcp_offset_local: tuple[float, float, float] = (0.0, 0.0, 0.0),
    max_samples: int = 0,
) -> int:
    pos_list: list[np.ndarray] = []
    quat_list: list[np.ndarray] = []
    joint_rows: list[np.ndarray] = []

    kept = 0
    scanned = 0
    for record in records:
        scanned += 1
        if skip_collision and float(record.get("collision_force", 0.0)) > 0.0:
            continue
        pose = extract_pose_from_record(record)
        if pose is None:
            continue
        pos, quat = pose
        pos_list.append(pos)
        quat_list.append(quat)
        arm = record.get("arm", {})
        if isinstance(arm, dict) and arm:
            joint_rows.append(
                np.array(
                    [float(arm.get(name, {}).get("pos", 0.0)) for name in REACH_JOINT_NAMES],
                    dtype=np.float32,
                )
            )
        kept += 1
        if max_samples > 0 and kept >= max_samples:
            break

    if kept == 0:
        raise RuntimeError("未提取到任何有效样本，请检查输入数据格式。")

    tcp_pos = np.stack(pos_list, axis=0).astype(np.float32, copy=False)
    tcp_quat = normalize_quat_wxyz(np.stack(quat_list, axis=0)).astype(np.float32, copy=False)
    if any(abs(v) > 1e-9 for v in tcp_offset_local):
        offset = np.asarray(tcp_offset_local, dtype=np.float32).reshape(1, 3)
        offset = np.repeat(offset, tcp_pos.shape[0], axis=0)
        tcp_pos = tcp_pos + quat_rotate_wxyz(tcp_quat, offset).astype(np.float32, copy=False)

    payload: dict[str, np.ndarray] = {
        "tcp": tcp_pos,
        "tcp_pos": tcp_pos,
        "tcp_quat_wxyz": tcp_quat,
    }
    if joint_rows and len(joint_rows) == kept:
        payload["joint_pos"] = np.stack(joint_rows, axis=0).astype(np.float32, copy=False)
        payload["joint_names"] = np.array(REACH_JOINT_NAMES)

    out_path = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    np.savez_compressed(out_path, **payload)
    print(
        f"[npz] scanned={scanned}, kept={kept}, output={out_path}, "
        f"keys={list(payload.keys())}"
    )
    return kept


def export_npz_from_sample_outputs(
    paths: PipelinePaths,
    *,
    skip_collision: bool = False,
    tcp_offset_local: tuple[float, float, float],
    max_samples: int = 0,
) -> int:
    if os.path.isfile(paths.manifest_path):
        records = iter_records_from_manifest(paths.manifest_path)
    elif os.path.isfile(paths.output_json):
        records = iter_records_from_merged_json(paths.output_json)
    else:
        raise FileNotFoundError(
            "无法导出 NPZ：未找到 manifest 或合并 JSON。\n"
            f"  manifest: {paths.manifest_path}\n"
            f"  json: {paths.output_json}"
        )
    return records_to_npz(
        records,
        paths.merged_npz,
        skip_collision=skip_collision,
        tcp_offset_local=tcp_offset_local,
        max_samples=max_samples,
    )


METADATA_NPZ_KEYS = frozenset({"joint_names"})


def split_npz(
    input_npz: str,
    train_output: str,
    test_output: str,
    *,
    train_ratio: float = 0.8,
    seed: int = 42,
) -> tuple[int, int, int]:
    if not (0.0 < train_ratio < 1.0):
        raise ValueError("train_ratio 必须在 (0, 1) 内")

    data = np.load(input_npz)
    keys = list(data.files)
    if not keys:
        raise RuntimeError("输入 NPZ 为空")

    sample_keys = [key for key in keys if key not in METADATA_NPZ_KEYS]
    if not sample_keys:
        raise RuntimeError("输入 NPZ 无样本数组")

    n = int(data[sample_keys[0]].shape[0])
    for key in sample_keys:
        if int(data[key].shape[0]) != n:
            raise RuntimeError(f"数组长度不一致: {key}")

    idx = np.arange(n)
    rng = np.random.default_rng(seed)
    rng.shuffle(idx)

    n_train = int(round(n * train_ratio))
    n_train = max(1, min(n - 1, n_train))
    train_idx = idx[:n_train]
    test_idx = idx[n_train:]

    train_dict: dict[str, np.ndarray] = {}
    test_dict: dict[str, np.ndarray] = {}
    for key in keys:
        if key in METADATA_NPZ_KEYS:
            train_dict[key] = data[key]
            test_dict[key] = data[key]
        else:
            train_dict[key] = data[key][train_idx]
            test_dict[key] = data[key][test_idx]

    train_out = os.path.abspath(train_output)
    test_out = os.path.abspath(test_output)
    os.makedirs(os.path.dirname(train_out) or ".", exist_ok=True)
    os.makedirs(os.path.dirname(test_out) or ".", exist_ok=True)
    np.savez_compressed(train_out, **train_dict)
    np.savez_compressed(test_out, **test_dict)
    print(
        f"[split] total={n}, train={len(train_idx)}, test={len(test_idx)}, "
        f"train_out={train_out}, test_out={test_out}"
    )
    return n, len(train_idx), len(test_idx)
