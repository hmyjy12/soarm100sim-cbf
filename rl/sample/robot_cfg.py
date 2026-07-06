"""SO-100 Plus robot configuration for workspace sampling."""

from __future__ import annotations

from pathlib import Path

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets import ArticulationCfg, AssetBaseCfg
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.utils import configclass

from sample.constants import HOME_JOINT_POS, REACH_JOINT_NAMES

_RL_ROOT = Path(__file__).resolve().parents[1]
_REPO_ROOT = _RL_ROOT.parent


def default_usd_path() -> str:
    return str((_RL_ROOT / "assets" / "so100_plus.usd").resolve())


def default_urdf_path() -> str:
    return str(
        (
            _REPO_ROOT
            / "SO-ARM100"
            / "Simulation"
            / "SO100"
            / "mujoco"
            / "so100_plus.urdf"
        ).resolve()
    )


def build_so100_plus_cfg(usd_path: str, enable_self_collisions: bool = True) -> ArticulationCfg:
    joint_pos = {name: HOME_JOINT_POS[name] for name in HOME_JOINT_POS}
    return ArticulationCfg(
        spawn=sim_utils.UsdFileCfg(
            usd_path=usd_path,
            activate_contact_sensors=True,
            rigid_props=sim_utils.RigidBodyPropertiesCfg(
                max_depenetration_velocity=1.0,
            ),
            articulation_props=sim_utils.ArticulationRootPropertiesCfg(
                enabled_self_collisions=enable_self_collisions,
                fix_root_link=True,
                solver_position_iteration_count=8,
                solver_velocity_iteration_count=2,
            ),
        ),
        init_state=ArticulationCfg.InitialStateCfg(
            pos=(0.0, 0.0, 0.0),
            joint_pos=joint_pos,
            joint_vel={name: 0.0 for name in joint_pos},
        ),
        actuators={
            "arm": ImplicitActuatorCfg(
                joint_names_expr=list(REACH_JOINT_NAMES),
                stiffness=80.0,
                damping=8.0,
                velocity_limit=3.14,
                effort_limit=35.0,
            ),
        },
    )


@configclass
class SampleSceneCfg(InteractiveSceneCfg):
    ground = AssetBaseCfg(prim_path="/World/defaultGroundPlane", spawn=sim_utils.GroundPlaneCfg())
    dome_light = AssetBaseCfg(
        prim_path="/World/Light",
        spawn=sim_utils.DomeLightCfg(intensity=2500.0, color=(0.85, 0.85, 0.85)),
    )
    robot: ArticulationCfg = build_so100_plus_cfg(default_usd_path()).replace(
        prim_path="{ENV_REGEX_NS}/Robot"
    )
