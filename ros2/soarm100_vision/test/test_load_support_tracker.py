from pathlib import Path

import numpy as np

from soarm100_vision.control.load_support_tracker import PositionGravityBias


JOINTS = ("pan", "shoulder", "elbow")


def write_config(path: Path) -> None:
    path.write_text(
        """{
  "mode": "position_gravity_bias",
  "joints": {
    "shoulder": {
      "direction": -1,
      "bias_rad": 0.04,
      "max_bias_rad": 0.10,
      "ramp_rate_rad_s": 0.04
    }
  }
}
""",
        encoding="utf-8",
    )


def test_bias_ramps_in_configured_upward_direction(tmp_path):
    path = tmp_path / "support.json"
    write_config(path)
    support = PositionGravityBias.from_config(path, JOINTS)
    result = support.apply(np.zeros(3), np.full(3, -2.0), np.full(3, 2.0), 0.05)

    assert np.allclose(result["q_cmd"], [0.0, -0.002, 0.0])
    assert np.allclose(result["requested_bias_rad"], [0.0, -0.002, 0.0])


def test_bias_stops_at_requested_value_and_respects_joint_limit(tmp_path):
    path = tmp_path / "support.json"
    write_config(path)
    support = PositionGravityBias.from_config(path, JOINTS)
    result = None
    for _ in range(100):
        result = support.apply(
            np.array([0.0, -0.98, 0.0]),
            np.array([-2.0, -1.0, -2.0]),
            np.full(3, 2.0),
            0.05,
        )

    assert result is not None
    assert np.isclose(result["requested_bias_rad"][1], -0.04)
    assert np.isclose(result["applied_bias_rad"][1], -0.02)
    assert result["limit_clamped"][1]
