import importlib.util
import json
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = REPO_ROOT / "ros2/scripts/real/initialize_policy_ready_pose.py"
SPEC = importlib.util.spec_from_file_location("policy_pose_initializer", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def approved_pose() -> dict:
    return {
        "approved_for_recovery_motion": True,
        "policy_joint_order": list(MODULE.JOINT_ORDER),
        "policy_position_rad": [0.0, -1.5, 1.5, 0.0, 0.0, 0.0, 0.0],
    }


def write_pose(tmp_path: Path, payload: dict) -> Path:
    path = tmp_path / "pose.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_approved_interior_pose_is_loaded(tmp_path):
    values = MODULE.load_pose(write_pose(tmp_path, approved_pose()), margin=0.10)
    assert values == [0.0, -1.5, 1.5, 0.0, 0.0, 0.0, 0.0]


def test_unapproved_pose_is_rejected(tmp_path):
    payload = approved_pose()
    payload["approved_for_recovery_motion"] = False
    with pytest.raises(ValueError, match="not approved_for_recovery_motion"):
        MODULE.load_pose(write_pose(tmp_path, payload), margin=0.10)


def test_pose_inside_hard_limit_but_outside_training_margin_is_rejected(tmp_path):
    payload = approved_pose()
    payload["policy_position_rad"][1] = -3.10
    with pytest.raises(ValueError, match="shoulder_pitch_joint"):
        MODULE.load_pose(write_pose(tmp_path, payload), margin=0.10)
