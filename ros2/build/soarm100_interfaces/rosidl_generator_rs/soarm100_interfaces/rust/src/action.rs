
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to soarm100_interfaces__action__ExecuteGrasp_Goal

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteGrasp_Goal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target_prompt: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub enable_avoidance: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub approximate_target_pose: geometry_msgs::msg::PoseStamped,

}



impl Default for ExecuteGrasp_Goal {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecuteGrasp_Goal::default())
  }
}

impl rosidl_runtime_rs::Message for ExecuteGrasp_Goal {
  type RmwMsg = super::action::rmw::ExecuteGrasp_Goal;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_prompt: msg.target_prompt.as_str().into(),
        enable_avoidance: msg.enable_avoidance,
        approximate_target_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Owned(msg.approximate_target_pose)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_prompt: msg.target_prompt.as_str().into(),
      enable_avoidance: msg.enable_avoidance,
        approximate_target_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Borrowed(&msg.approximate_target_pose)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      target_prompt: msg.target_prompt.to_string(),
      enable_avoidance: msg.enable_avoidance,
      approximate_target_pose: geometry_msgs::msg::PoseStamped::from_rmw_message(msg.approximate_target_pose),
    }
  }
}


// Corresponds to soarm100_interfaces__action__ExecuteGrasp_Result

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteGrasp_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub final_grasp_pose: geometry_msgs::msg::PoseStamped,


    // This member is not documented.
    #[allow(missing_docs)]
    pub lift_height: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub attempts: u8,

}



impl Default for ExecuteGrasp_Result {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecuteGrasp_Result::default())
  }
}

impl rosidl_runtime_rs::Message for ExecuteGrasp_Result {
  type RmwMsg = super::action::rmw::ExecuteGrasp_Result;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        reason: msg.reason.as_str().into(),
        final_grasp_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Owned(msg.final_grasp_pose)).into_owned(),
        lift_height: msg.lift_height,
        attempts: msg.attempts,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        reason: msg.reason.as_str().into(),
        final_grasp_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Borrowed(&msg.final_grasp_pose)).into_owned(),
      lift_height: msg.lift_height,
      attempts: msg.attempts,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      reason: msg.reason.to_string(),
      final_grasp_pose: geometry_msgs::msg::PoseStamped::from_rmw_message(msg.final_grasp_pose),
      lift_height: msg.lift_height,
      attempts: msg.attempts,
    }
  }
}


// Corresponds to soarm100_interfaces__action__ExecuteGrasp_Feedback

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteGrasp_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub stage: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_visible_score: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub grasp_score: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub tcp_pos_err: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub tcp_ori_err: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sdf_min_dist: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub cbf_active: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub tracking_valid: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub replan_running: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: std::string::String,

}



impl Default for ExecuteGrasp_Feedback {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecuteGrasp_Feedback::default())
  }
}

impl rosidl_runtime_rs::Message for ExecuteGrasp_Feedback {
  type RmwMsg = super::action::rmw::ExecuteGrasp_Feedback;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stage: msg.stage.as_str().into(),
        target_visible_score: msg.target_visible_score,
        grasp_score: msg.grasp_score,
        tcp_pos_err: msg.tcp_pos_err,
        tcp_ori_err: msg.tcp_ori_err,
        sdf_min_dist: msg.sdf_min_dist,
        cbf_active: msg.cbf_active,
        tracking_valid: msg.tracking_valid,
        replan_running: msg.replan_running,
        reason: msg.reason.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stage: msg.stage.as_str().into(),
      target_visible_score: msg.target_visible_score,
      grasp_score: msg.grasp_score,
      tcp_pos_err: msg.tcp_pos_err,
      tcp_ori_err: msg.tcp_ori_err,
      sdf_min_dist: msg.sdf_min_dist,
      cbf_active: msg.cbf_active,
      tracking_valid: msg.tracking_valid,
      replan_running: msg.replan_running,
        reason: msg.reason.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      stage: msg.stage.to_string(),
      target_visible_score: msg.target_visible_score,
      grasp_score: msg.grasp_score,
      tcp_pos_err: msg.tcp_pos_err,
      tcp_ori_err: msg.tcp_ori_err,
      sdf_min_dist: msg.sdf_min_dist,
      cbf_active: msg.cbf_active,
      tracking_valid: msg.tracking_valid,
      replan_running: msg.replan_running,
      reason: msg.reason.to_string(),
    }
  }
}


// Corresponds to soarm100_interfaces__action__ExecuteGrasp_FeedbackMessage

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteGrasp_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::action::ExecuteGrasp_Feedback,

}



impl Default for ExecuteGrasp_FeedbackMessage {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecuteGrasp_FeedbackMessage::default())
  }
}

impl rosidl_runtime_rs::Message for ExecuteGrasp_FeedbackMessage {
  type RmwMsg = super::action::rmw::ExecuteGrasp_FeedbackMessage;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        feedback: super::action::ExecuteGrasp_Feedback::into_rmw_message(std::borrow::Cow::Owned(msg.feedback)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        feedback: super::action::ExecuteGrasp_Feedback::into_rmw_message(std::borrow::Cow::Borrowed(&msg.feedback)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      feedback: super::action::ExecuteGrasp_Feedback::from_rmw_message(msg.feedback),
    }
  }
}


// Corresponds to soarm100_interfaces__action__ExecutePlannedGrasp_Goal

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecutePlannedGrasp_Goal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pregrasp_pose: geometry_msgs::msg::PoseStamped,


    // This member is not documented.
    #[allow(missing_docs)]
    pub grasp_pose: geometry_msgs::msg::PoseStamped,


    // This member is not documented.
    #[allow(missing_docs)]
    pub gripper_width: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub enable_avoidance: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_object: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_pos: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub traj_log: std::string::String,

}



impl Default for ExecutePlannedGrasp_Goal {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecutePlannedGrasp_Goal::default())
  }
}

impl rosidl_runtime_rs::Message for ExecutePlannedGrasp_Goal {
  type RmwMsg = super::action::rmw::ExecutePlannedGrasp_Goal;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pregrasp_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Owned(msg.pregrasp_pose)).into_owned(),
        grasp_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Owned(msg.grasp_pose)).into_owned(),
        gripper_width: msg.gripper_width,
        enable_avoidance: msg.enable_avoidance,
        target_object: msg.target_object.as_str().into(),
        target_pos: msg.target_pos.as_str().into(),
        traj_log: msg.traj_log.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pregrasp_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Borrowed(&msg.pregrasp_pose)).into_owned(),
        grasp_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Borrowed(&msg.grasp_pose)).into_owned(),
      gripper_width: msg.gripper_width,
      enable_avoidance: msg.enable_avoidance,
        target_object: msg.target_object.as_str().into(),
        target_pos: msg.target_pos.as_str().into(),
        traj_log: msg.traj_log.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pregrasp_pose: geometry_msgs::msg::PoseStamped::from_rmw_message(msg.pregrasp_pose),
      grasp_pose: geometry_msgs::msg::PoseStamped::from_rmw_message(msg.grasp_pose),
      gripper_width: msg.gripper_width,
      enable_avoidance: msg.enable_avoidance,
      target_object: msg.target_object.to_string(),
      target_pos: msg.target_pos.to_string(),
      traj_log: msg.traj_log.to_string(),
    }
  }
}


// Corresponds to soarm100_interfaces__action__ExecutePlannedGrasp_Result

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecutePlannedGrasp_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub lift_height: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub return_code: u8,

}



impl Default for ExecutePlannedGrasp_Result {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecutePlannedGrasp_Result::default())
  }
}

impl rosidl_runtime_rs::Message for ExecutePlannedGrasp_Result {
  type RmwMsg = super::action::rmw::ExecutePlannedGrasp_Result;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        reason: msg.reason.as_str().into(),
        lift_height: msg.lift_height,
        return_code: msg.return_code,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        reason: msg.reason.as_str().into(),
      lift_height: msg.lift_height,
      return_code: msg.return_code,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      reason: msg.reason.to_string(),
      lift_height: msg.lift_height,
      return_code: msg.return_code,
    }
  }
}


// Corresponds to soarm100_interfaces__action__ExecutePlannedGrasp_Feedback

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecutePlannedGrasp_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub stage: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub lift_height: f32,

}



impl Default for ExecutePlannedGrasp_Feedback {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecutePlannedGrasp_Feedback::default())
  }
}

impl rosidl_runtime_rs::Message for ExecutePlannedGrasp_Feedback {
  type RmwMsg = super::action::rmw::ExecutePlannedGrasp_Feedback;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stage: msg.stage.as_str().into(),
        reason: msg.reason.as_str().into(),
        lift_height: msg.lift_height,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stage: msg.stage.as_str().into(),
        reason: msg.reason.as_str().into(),
      lift_height: msg.lift_height,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      stage: msg.stage.to_string(),
      reason: msg.reason.to_string(),
      lift_height: msg.lift_height,
    }
  }
}


// Corresponds to soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecutePlannedGrasp_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::action::ExecutePlannedGrasp_Feedback,

}



impl Default for ExecutePlannedGrasp_FeedbackMessage {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecutePlannedGrasp_FeedbackMessage::default())
  }
}

impl rosidl_runtime_rs::Message for ExecutePlannedGrasp_FeedbackMessage {
  type RmwMsg = super::action::rmw::ExecutePlannedGrasp_FeedbackMessage;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        feedback: super::action::ExecutePlannedGrasp_Feedback::into_rmw_message(std::borrow::Cow::Owned(msg.feedback)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        feedback: super::action::ExecutePlannedGrasp_Feedback::into_rmw_message(std::borrow::Cow::Borrowed(&msg.feedback)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      feedback: super::action::ExecutePlannedGrasp_Feedback::from_rmw_message(msg.feedback),
    }
  }
}


// Corresponds to soarm100_interfaces__action__PlanGrasp_Goal

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlanGrasp_Goal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target_prompt: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub approximate_target_pose: geometry_msgs::msg::PoseStamped,


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_cloud: sensor_msgs::msg::PointCloud2,


    // This member is not documented.
    #[allow(missing_docs)]
    pub top_k: u16,

}



impl Default for PlanGrasp_Goal {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::PlanGrasp_Goal::default())
  }
}

impl rosidl_runtime_rs::Message for PlanGrasp_Goal {
  type RmwMsg = super::action::rmw::PlanGrasp_Goal;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_prompt: msg.target_prompt.as_str().into(),
        approximate_target_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Owned(msg.approximate_target_pose)).into_owned(),
        target_cloud: sensor_msgs::msg::PointCloud2::into_rmw_message(std::borrow::Cow::Owned(msg.target_cloud)).into_owned(),
        top_k: msg.top_k,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_prompt: msg.target_prompt.as_str().into(),
        approximate_target_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Borrowed(&msg.approximate_target_pose)).into_owned(),
        target_cloud: sensor_msgs::msg::PointCloud2::into_rmw_message(std::borrow::Cow::Borrowed(&msg.target_cloud)).into_owned(),
      top_k: msg.top_k,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      target_prompt: msg.target_prompt.to_string(),
      approximate_target_pose: geometry_msgs::msg::PoseStamped::from_rmw_message(msg.approximate_target_pose),
      target_cloud: sensor_msgs::msg::PointCloud2::from_rmw_message(msg.target_cloud),
      top_k: msg.top_k,
    }
  }
}


// Corresponds to soarm100_interfaces__action__PlanGrasp_Result

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlanGrasp_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub selected_grasp_pose: geometry_msgs::msg::PoseStamped,


    // This member is not documented.
    #[allow(missing_docs)]
    pub selected_pregrasp_pose: geometry_msgs::msg::PoseStamped,


    // This member is not documented.
    #[allow(missing_docs)]
    pub grasp_score: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub gripper_width: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub candidate_count: u16,

}



impl Default for PlanGrasp_Result {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::PlanGrasp_Result::default())
  }
}

impl rosidl_runtime_rs::Message for PlanGrasp_Result {
  type RmwMsg = super::action::rmw::PlanGrasp_Result;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        reason: msg.reason.as_str().into(),
        selected_grasp_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Owned(msg.selected_grasp_pose)).into_owned(),
        selected_pregrasp_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Owned(msg.selected_pregrasp_pose)).into_owned(),
        grasp_score: msg.grasp_score,
        gripper_width: msg.gripper_width,
        candidate_count: msg.candidate_count,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        reason: msg.reason.as_str().into(),
        selected_grasp_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Borrowed(&msg.selected_grasp_pose)).into_owned(),
        selected_pregrasp_pose: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Borrowed(&msg.selected_pregrasp_pose)).into_owned(),
      grasp_score: msg.grasp_score,
      gripper_width: msg.gripper_width,
      candidate_count: msg.candidate_count,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      reason: msg.reason.to_string(),
      selected_grasp_pose: geometry_msgs::msg::PoseStamped::from_rmw_message(msg.selected_grasp_pose),
      selected_pregrasp_pose: geometry_msgs::msg::PoseStamped::from_rmw_message(msg.selected_pregrasp_pose),
      grasp_score: msg.grasp_score,
      gripper_width: msg.gripper_width,
      candidate_count: msg.candidate_count,
    }
  }
}


// Corresponds to soarm100_interfaces__action__PlanGrasp_Feedback

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlanGrasp_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub stage: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub candidate_count: u16,


    // This member is not documented.
    #[allow(missing_docs)]
    pub best_score: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: std::string::String,

}



impl Default for PlanGrasp_Feedback {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::PlanGrasp_Feedback::default())
  }
}

impl rosidl_runtime_rs::Message for PlanGrasp_Feedback {
  type RmwMsg = super::action::rmw::PlanGrasp_Feedback;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stage: msg.stage.as_str().into(),
        candidate_count: msg.candidate_count,
        best_score: msg.best_score,
        reason: msg.reason.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        stage: msg.stage.as_str().into(),
      candidate_count: msg.candidate_count,
      best_score: msg.best_score,
        reason: msg.reason.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      stage: msg.stage.to_string(),
      candidate_count: msg.candidate_count,
      best_score: msg.best_score,
      reason: msg.reason.to_string(),
    }
  }
}


// Corresponds to soarm100_interfaces__action__PlanGrasp_FeedbackMessage

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlanGrasp_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::action::PlanGrasp_Feedback,

}



impl Default for PlanGrasp_FeedbackMessage {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::PlanGrasp_FeedbackMessage::default())
  }
}

impl rosidl_runtime_rs::Message for PlanGrasp_FeedbackMessage {
  type RmwMsg = super::action::rmw::PlanGrasp_FeedbackMessage;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        feedback: super::action::PlanGrasp_Feedback::into_rmw_message(std::borrow::Cow::Owned(msg.feedback)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        feedback: super::action::PlanGrasp_Feedback::into_rmw_message(std::borrow::Cow::Borrowed(&msg.feedback)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      feedback: super::action::PlanGrasp_Feedback::from_rmw_message(msg.feedback),
    }
  }
}






// Corresponds to soarm100_interfaces__action__ExecuteGrasp_SendGoal_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteGrasp_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::action::ExecuteGrasp_Goal,

}



impl Default for ExecuteGrasp_SendGoal_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecuteGrasp_SendGoal_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ExecuteGrasp_SendGoal_Request {
  type RmwMsg = super::action::rmw::ExecuteGrasp_SendGoal_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        goal: super::action::ExecuteGrasp_Goal::into_rmw_message(std::borrow::Cow::Owned(msg.goal)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        goal: super::action::ExecuteGrasp_Goal::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      goal: super::action::ExecuteGrasp_Goal::from_rmw_message(msg.goal),
    }
  }
}


// Corresponds to soarm100_interfaces__action__ExecuteGrasp_SendGoal_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteGrasp_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,

}



impl Default for ExecuteGrasp_SendGoal_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecuteGrasp_SendGoal_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ExecuteGrasp_SendGoal_Response {
  type RmwMsg = super::action::rmw::ExecuteGrasp_SendGoal_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      accepted: msg.accepted,
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
    }
  }
}


// Corresponds to soarm100_interfaces__action__ExecuteGrasp_GetResult_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteGrasp_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,

}



impl Default for ExecuteGrasp_GetResult_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecuteGrasp_GetResult_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ExecuteGrasp_GetResult_Request {
  type RmwMsg = super::action::rmw::ExecuteGrasp_GetResult_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
    }
  }
}


// Corresponds to soarm100_interfaces__action__ExecuteGrasp_GetResult_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteGrasp_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::action::ExecuteGrasp_Result,

}



impl Default for ExecuteGrasp_GetResult_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecuteGrasp_GetResult_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ExecuteGrasp_GetResult_Response {
  type RmwMsg = super::action::rmw::ExecuteGrasp_GetResult_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        status: msg.status,
        result: super::action::ExecuteGrasp_Result::into_rmw_message(std::borrow::Cow::Owned(msg.result)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      status: msg.status,
        result: super::action::ExecuteGrasp_Result::into_rmw_message(std::borrow::Cow::Borrowed(&msg.result)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      status: msg.status,
      result: super::action::ExecuteGrasp_Result::from_rmw_message(msg.result),
    }
  }
}


// Corresponds to soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecutePlannedGrasp_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::action::ExecutePlannedGrasp_Goal,

}



impl Default for ExecutePlannedGrasp_SendGoal_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecutePlannedGrasp_SendGoal_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ExecutePlannedGrasp_SendGoal_Request {
  type RmwMsg = super::action::rmw::ExecutePlannedGrasp_SendGoal_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        goal: super::action::ExecutePlannedGrasp_Goal::into_rmw_message(std::borrow::Cow::Owned(msg.goal)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        goal: super::action::ExecutePlannedGrasp_Goal::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      goal: super::action::ExecutePlannedGrasp_Goal::from_rmw_message(msg.goal),
    }
  }
}


// Corresponds to soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecutePlannedGrasp_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,

}



impl Default for ExecutePlannedGrasp_SendGoal_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecutePlannedGrasp_SendGoal_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ExecutePlannedGrasp_SendGoal_Response {
  type RmwMsg = super::action::rmw::ExecutePlannedGrasp_SendGoal_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      accepted: msg.accepted,
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
    }
  }
}


// Corresponds to soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecutePlannedGrasp_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,

}



impl Default for ExecutePlannedGrasp_GetResult_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecutePlannedGrasp_GetResult_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ExecutePlannedGrasp_GetResult_Request {
  type RmwMsg = super::action::rmw::ExecutePlannedGrasp_GetResult_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
    }
  }
}


// Corresponds to soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecutePlannedGrasp_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::action::ExecutePlannedGrasp_Result,

}



impl Default for ExecutePlannedGrasp_GetResult_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::ExecutePlannedGrasp_GetResult_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ExecutePlannedGrasp_GetResult_Response {
  type RmwMsg = super::action::rmw::ExecutePlannedGrasp_GetResult_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        status: msg.status,
        result: super::action::ExecutePlannedGrasp_Result::into_rmw_message(std::borrow::Cow::Owned(msg.result)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      status: msg.status,
        result: super::action::ExecutePlannedGrasp_Result::into_rmw_message(std::borrow::Cow::Borrowed(&msg.result)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      status: msg.status,
      result: super::action::ExecutePlannedGrasp_Result::from_rmw_message(msg.result),
    }
  }
}


// Corresponds to soarm100_interfaces__action__PlanGrasp_SendGoal_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlanGrasp_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::action::PlanGrasp_Goal,

}



impl Default for PlanGrasp_SendGoal_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::PlanGrasp_SendGoal_Request::default())
  }
}

impl rosidl_runtime_rs::Message for PlanGrasp_SendGoal_Request {
  type RmwMsg = super::action::rmw::PlanGrasp_SendGoal_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
        goal: super::action::PlanGrasp_Goal::into_rmw_message(std::borrow::Cow::Owned(msg.goal)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
        goal: super::action::PlanGrasp_Goal::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
      goal: super::action::PlanGrasp_Goal::from_rmw_message(msg.goal),
    }
  }
}


// Corresponds to soarm100_interfaces__action__PlanGrasp_SendGoal_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlanGrasp_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::Time,

}



impl Default for PlanGrasp_SendGoal_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::PlanGrasp_SendGoal_Response::default())
  }
}

impl rosidl_runtime_rs::Message for PlanGrasp_SendGoal_Response {
  type RmwMsg = super::action::rmw::PlanGrasp_SendGoal_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.stamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      accepted: msg.accepted,
        stamp: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.stamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      accepted: msg.accepted,
      stamp: builtin_interfaces::msg::Time::from_rmw_message(msg.stamp),
    }
  }
}


// Corresponds to soarm100_interfaces__action__PlanGrasp_GetResult_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlanGrasp_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::UUID,

}



impl Default for PlanGrasp_GetResult_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::PlanGrasp_GetResult_Request::default())
  }
}

impl rosidl_runtime_rs::Message for PlanGrasp_GetResult_Request {
  type RmwMsg = super::action::rmw::PlanGrasp_GetResult_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Owned(msg.goal_id)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        goal_id: unique_identifier_msgs::msg::UUID::into_rmw_message(std::borrow::Cow::Borrowed(&msg.goal_id)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      goal_id: unique_identifier_msgs::msg::UUID::from_rmw_message(msg.goal_id),
    }
  }
}


// Corresponds to soarm100_interfaces__action__PlanGrasp_GetResult_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlanGrasp_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::action::PlanGrasp_Result,

}



impl Default for PlanGrasp_GetResult_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::action::rmw::PlanGrasp_GetResult_Response::default())
  }
}

impl rosidl_runtime_rs::Message for PlanGrasp_GetResult_Response {
  type RmwMsg = super::action::rmw::PlanGrasp_GetResult_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        status: msg.status,
        result: super::action::PlanGrasp_Result::into_rmw_message(std::borrow::Cow::Owned(msg.result)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      status: msg.status,
        result: super::action::PlanGrasp_Result::into_rmw_message(std::borrow::Cow::Borrowed(&msg.result)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      status: msg.status,
      result: super::action::PlanGrasp_Result::from_rmw_message(msg.result),
    }
  }
}






#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__action__ExecuteGrasp_SendGoal() -> *const std::ffi::c_void;
}

// Corresponds to soarm100_interfaces__action__ExecuteGrasp_SendGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct ExecuteGrasp_SendGoal;

impl rosidl_runtime_rs::Service for ExecuteGrasp_SendGoal {
    type Request = ExecuteGrasp_SendGoal_Request;
    type Response = ExecuteGrasp_SendGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__action__ExecuteGrasp_SendGoal() }
    }
}




#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__action__ExecuteGrasp_GetResult() -> *const std::ffi::c_void;
}

// Corresponds to soarm100_interfaces__action__ExecuteGrasp_GetResult
#[allow(missing_docs, non_camel_case_types)]
pub struct ExecuteGrasp_GetResult;

impl rosidl_runtime_rs::Service for ExecuteGrasp_GetResult {
    type Request = ExecuteGrasp_GetResult_Request;
    type Response = ExecuteGrasp_GetResult_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__action__ExecuteGrasp_GetResult() }
    }
}




#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal() -> *const std::ffi::c_void;
}

// Corresponds to soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct ExecutePlannedGrasp_SendGoal;

impl rosidl_runtime_rs::Service for ExecutePlannedGrasp_SendGoal {
    type Request = ExecutePlannedGrasp_SendGoal_Request;
    type Response = ExecutePlannedGrasp_SendGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal() }
    }
}




#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__action__ExecutePlannedGrasp_GetResult() -> *const std::ffi::c_void;
}

// Corresponds to soarm100_interfaces__action__ExecutePlannedGrasp_GetResult
#[allow(missing_docs, non_camel_case_types)]
pub struct ExecutePlannedGrasp_GetResult;

impl rosidl_runtime_rs::Service for ExecutePlannedGrasp_GetResult {
    type Request = ExecutePlannedGrasp_GetResult_Request;
    type Response = ExecutePlannedGrasp_GetResult_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__action__ExecutePlannedGrasp_GetResult() }
    }
}




#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__action__PlanGrasp_SendGoal() -> *const std::ffi::c_void;
}

// Corresponds to soarm100_interfaces__action__PlanGrasp_SendGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct PlanGrasp_SendGoal;

impl rosidl_runtime_rs::Service for PlanGrasp_SendGoal {
    type Request = PlanGrasp_SendGoal_Request;
    type Response = PlanGrasp_SendGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__action__PlanGrasp_SendGoal() }
    }
}




#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__action__PlanGrasp_GetResult() -> *const std::ffi::c_void;
}

// Corresponds to soarm100_interfaces__action__PlanGrasp_GetResult
#[allow(missing_docs, non_camel_case_types)]
pub struct PlanGrasp_GetResult;

impl rosidl_runtime_rs::Service for PlanGrasp_GetResult {
    type Request = PlanGrasp_GetResult_Request;
    type Response = PlanGrasp_GetResult_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__action__PlanGrasp_GetResult() }
    }
}






#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_action_type_support_handle__soarm100_interfaces__action__ExecuteGrasp() -> *const std::ffi::c_void;
}

// Corresponds to soarm100_interfaces__action__ExecuteGrasp
#[allow(missing_docs, non_camel_case_types)]
pub struct ExecuteGrasp;

impl rosidl_runtime_rs::Action for ExecuteGrasp {
  // --- Associated types for client library users ---
  /// The goal message defined in the action definition.
  type Goal = ExecuteGrasp_Goal;

  /// The result message defined in the action definition.
  type Result = ExecuteGrasp_Result;

  /// The feedback message defined in the action definition.
  type Feedback = ExecuteGrasp_Feedback;

  // --- Associated types for client library implementation ---
  /// The feedback message with generic fields which wraps the feedback message.
  type FeedbackMessage = super::action::ExecuteGrasp_FeedbackMessage;

  /// The send_goal service using a wrapped version of the goal message as a request.
  type SendGoalService = super::action::ExecuteGrasp_SendGoal;

  /// The generic service to cancel a goal.
  type CancelGoalService = action_msgs::srv::rmw::CancelGoal;

  /// The get_result service using a wrapped version of the result message as a response.
  type GetResultService = super::action::ExecuteGrasp_GetResult;

  // --- Methods for client library implementation ---
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_action_type_support_handle__soarm100_interfaces__action__ExecuteGrasp() }
  }

  fn create_goal_request(
    goal_id: &[u8; 16],
    goal: super::action::rmw::ExecuteGrasp_Goal,
  ) -> super::action::rmw::ExecuteGrasp_SendGoal_Request {
   super::action::rmw::ExecuteGrasp_SendGoal_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
      goal,
    }
  }

  fn split_goal_request(
    request: super::action::rmw::ExecuteGrasp_SendGoal_Request,
  ) -> (
    [u8; 16],
   super::action::rmw::ExecuteGrasp_Goal,
  ) {
    (request.goal_id.uuid, request.goal)
  }

  fn create_goal_response(
    accepted: bool,
    stamp: (i32, u32),
  ) -> super::action::rmw::ExecuteGrasp_SendGoal_Response {
   super::action::rmw::ExecuteGrasp_SendGoal_Response {
      accepted,
      stamp: builtin_interfaces::msg::rmw::Time {
        sec: stamp.0,
        nanosec: stamp.1,
      },
    }
  }

  fn get_goal_response_accepted(
    response: &super::action::rmw::ExecuteGrasp_SendGoal_Response,
  ) -> bool {
    response.accepted
  }

  fn get_goal_response_stamp(
    response: &super::action::rmw::ExecuteGrasp_SendGoal_Response,
  ) -> (i32, u32) {
    (response.stamp.sec, response.stamp.nanosec)
  }

  fn create_feedback_message(
    goal_id: &[u8; 16],
    feedback: super::action::rmw::ExecuteGrasp_Feedback,
  ) -> super::action::rmw::ExecuteGrasp_FeedbackMessage {
    let mut message = super::action::rmw::ExecuteGrasp_FeedbackMessage::default();
    message.goal_id.uuid = *goal_id;
    message.feedback = feedback;
    message
  }

  fn split_feedback_message(
    feedback: super::action::rmw::ExecuteGrasp_FeedbackMessage,
  ) -> (
    [u8; 16],
   super::action::rmw::ExecuteGrasp_Feedback,
  ) {
    (feedback.goal_id.uuid, feedback.feedback)
  }

  fn create_result_request(
    goal_id: &[u8; 16],
  ) -> super::action::rmw::ExecuteGrasp_GetResult_Request {
   super::action::rmw::ExecuteGrasp_GetResult_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
    }
  }

  fn get_result_request_uuid(
    request: &super::action::rmw::ExecuteGrasp_GetResult_Request,
  ) -> &[u8; 16] {
    &request.goal_id.uuid
  }

  fn create_result_response(
    status: i8,
    result: super::action::rmw::ExecuteGrasp_Result,
  ) -> super::action::rmw::ExecuteGrasp_GetResult_Response {
   super::action::rmw::ExecuteGrasp_GetResult_Response {
      status,
      result,
    }
  }

  fn split_result_response(
    response: super::action::rmw::ExecuteGrasp_GetResult_Response
  ) -> (
    i8,
   super::action::rmw::ExecuteGrasp_Result,
  ) {
    (response.status, response.result)
  }
}




#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_action_type_support_handle__soarm100_interfaces__action__ExecutePlannedGrasp() -> *const std::ffi::c_void;
}

// Corresponds to soarm100_interfaces__action__ExecutePlannedGrasp
#[allow(missing_docs, non_camel_case_types)]
pub struct ExecutePlannedGrasp;

impl rosidl_runtime_rs::Action for ExecutePlannedGrasp {
  // --- Associated types for client library users ---
  /// The goal message defined in the action definition.
  type Goal = ExecutePlannedGrasp_Goal;

  /// The result message defined in the action definition.
  type Result = ExecutePlannedGrasp_Result;

  /// The feedback message defined in the action definition.
  type Feedback = ExecutePlannedGrasp_Feedback;

  // --- Associated types for client library implementation ---
  /// The feedback message with generic fields which wraps the feedback message.
  type FeedbackMessage = super::action::ExecutePlannedGrasp_FeedbackMessage;

  /// The send_goal service using a wrapped version of the goal message as a request.
  type SendGoalService = super::action::ExecutePlannedGrasp_SendGoal;

  /// The generic service to cancel a goal.
  type CancelGoalService = action_msgs::srv::rmw::CancelGoal;

  /// The get_result service using a wrapped version of the result message as a response.
  type GetResultService = super::action::ExecutePlannedGrasp_GetResult;

  // --- Methods for client library implementation ---
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_action_type_support_handle__soarm100_interfaces__action__ExecutePlannedGrasp() }
  }

  fn create_goal_request(
    goal_id: &[u8; 16],
    goal: super::action::rmw::ExecutePlannedGrasp_Goal,
  ) -> super::action::rmw::ExecutePlannedGrasp_SendGoal_Request {
   super::action::rmw::ExecutePlannedGrasp_SendGoal_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
      goal,
    }
  }

  fn split_goal_request(
    request: super::action::rmw::ExecutePlannedGrasp_SendGoal_Request,
  ) -> (
    [u8; 16],
   super::action::rmw::ExecutePlannedGrasp_Goal,
  ) {
    (request.goal_id.uuid, request.goal)
  }

  fn create_goal_response(
    accepted: bool,
    stamp: (i32, u32),
  ) -> super::action::rmw::ExecutePlannedGrasp_SendGoal_Response {
   super::action::rmw::ExecutePlannedGrasp_SendGoal_Response {
      accepted,
      stamp: builtin_interfaces::msg::rmw::Time {
        sec: stamp.0,
        nanosec: stamp.1,
      },
    }
  }

  fn get_goal_response_accepted(
    response: &super::action::rmw::ExecutePlannedGrasp_SendGoal_Response,
  ) -> bool {
    response.accepted
  }

  fn get_goal_response_stamp(
    response: &super::action::rmw::ExecutePlannedGrasp_SendGoal_Response,
  ) -> (i32, u32) {
    (response.stamp.sec, response.stamp.nanosec)
  }

  fn create_feedback_message(
    goal_id: &[u8; 16],
    feedback: super::action::rmw::ExecutePlannedGrasp_Feedback,
  ) -> super::action::rmw::ExecutePlannedGrasp_FeedbackMessage {
    let mut message = super::action::rmw::ExecutePlannedGrasp_FeedbackMessage::default();
    message.goal_id.uuid = *goal_id;
    message.feedback = feedback;
    message
  }

  fn split_feedback_message(
    feedback: super::action::rmw::ExecutePlannedGrasp_FeedbackMessage,
  ) -> (
    [u8; 16],
   super::action::rmw::ExecutePlannedGrasp_Feedback,
  ) {
    (feedback.goal_id.uuid, feedback.feedback)
  }

  fn create_result_request(
    goal_id: &[u8; 16],
  ) -> super::action::rmw::ExecutePlannedGrasp_GetResult_Request {
   super::action::rmw::ExecutePlannedGrasp_GetResult_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
    }
  }

  fn get_result_request_uuid(
    request: &super::action::rmw::ExecutePlannedGrasp_GetResult_Request,
  ) -> &[u8; 16] {
    &request.goal_id.uuid
  }

  fn create_result_response(
    status: i8,
    result: super::action::rmw::ExecutePlannedGrasp_Result,
  ) -> super::action::rmw::ExecutePlannedGrasp_GetResult_Response {
   super::action::rmw::ExecutePlannedGrasp_GetResult_Response {
      status,
      result,
    }
  }

  fn split_result_response(
    response: super::action::rmw::ExecutePlannedGrasp_GetResult_Response
  ) -> (
    i8,
   super::action::rmw::ExecutePlannedGrasp_Result,
  ) {
    (response.status, response.result)
  }
}




#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_action_type_support_handle__soarm100_interfaces__action__PlanGrasp() -> *const std::ffi::c_void;
}

// Corresponds to soarm100_interfaces__action__PlanGrasp
#[allow(missing_docs, non_camel_case_types)]
pub struct PlanGrasp;

impl rosidl_runtime_rs::Action for PlanGrasp {
  // --- Associated types for client library users ---
  /// The goal message defined in the action definition.
  type Goal = PlanGrasp_Goal;

  /// The result message defined in the action definition.
  type Result = PlanGrasp_Result;

  /// The feedback message defined in the action definition.
  type Feedback = PlanGrasp_Feedback;

  // --- Associated types for client library implementation ---
  /// The feedback message with generic fields which wraps the feedback message.
  type FeedbackMessage = super::action::PlanGrasp_FeedbackMessage;

  /// The send_goal service using a wrapped version of the goal message as a request.
  type SendGoalService = super::action::PlanGrasp_SendGoal;

  /// The generic service to cancel a goal.
  type CancelGoalService = action_msgs::srv::rmw::CancelGoal;

  /// The get_result service using a wrapped version of the result message as a response.
  type GetResultService = super::action::PlanGrasp_GetResult;

  // --- Methods for client library implementation ---
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_action_type_support_handle__soarm100_interfaces__action__PlanGrasp() }
  }

  fn create_goal_request(
    goal_id: &[u8; 16],
    goal: super::action::rmw::PlanGrasp_Goal,
  ) -> super::action::rmw::PlanGrasp_SendGoal_Request {
   super::action::rmw::PlanGrasp_SendGoal_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
      goal,
    }
  }

  fn split_goal_request(
    request: super::action::rmw::PlanGrasp_SendGoal_Request,
  ) -> (
    [u8; 16],
   super::action::rmw::PlanGrasp_Goal,
  ) {
    (request.goal_id.uuid, request.goal)
  }

  fn create_goal_response(
    accepted: bool,
    stamp: (i32, u32),
  ) -> super::action::rmw::PlanGrasp_SendGoal_Response {
   super::action::rmw::PlanGrasp_SendGoal_Response {
      accepted,
      stamp: builtin_interfaces::msg::rmw::Time {
        sec: stamp.0,
        nanosec: stamp.1,
      },
    }
  }

  fn get_goal_response_accepted(
    response: &super::action::rmw::PlanGrasp_SendGoal_Response,
  ) -> bool {
    response.accepted
  }

  fn get_goal_response_stamp(
    response: &super::action::rmw::PlanGrasp_SendGoal_Response,
  ) -> (i32, u32) {
    (response.stamp.sec, response.stamp.nanosec)
  }

  fn create_feedback_message(
    goal_id: &[u8; 16],
    feedback: super::action::rmw::PlanGrasp_Feedback,
  ) -> super::action::rmw::PlanGrasp_FeedbackMessage {
    let mut message = super::action::rmw::PlanGrasp_FeedbackMessage::default();
    message.goal_id.uuid = *goal_id;
    message.feedback = feedback;
    message
  }

  fn split_feedback_message(
    feedback: super::action::rmw::PlanGrasp_FeedbackMessage,
  ) -> (
    [u8; 16],
   super::action::rmw::PlanGrasp_Feedback,
  ) {
    (feedback.goal_id.uuid, feedback.feedback)
  }

  fn create_result_request(
    goal_id: &[u8; 16],
  ) -> super::action::rmw::PlanGrasp_GetResult_Request {
   super::action::rmw::PlanGrasp_GetResult_Request {
      goal_id: unique_identifier_msgs::msg::rmw::UUID { uuid: *goal_id },
    }
  }

  fn get_result_request_uuid(
    request: &super::action::rmw::PlanGrasp_GetResult_Request,
  ) -> &[u8; 16] {
    &request.goal_id.uuid
  }

  fn create_result_response(
    status: i8,
    result: super::action::rmw::PlanGrasp_Result,
  ) -> super::action::rmw::PlanGrasp_GetResult_Response {
   super::action::rmw::PlanGrasp_GetResult_Response {
      status,
      result,
    }
  }

  fn split_result_response(
    response: super::action::rmw::PlanGrasp_GetResult_Response
  ) -> (
    i8,
   super::action::rmw::PlanGrasp_Result,
  ) {
    (response.status, response.result)
  }
}


