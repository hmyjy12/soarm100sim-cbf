#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to soarm100_interfaces__srv__SegmentTarget_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SegmentTarget_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target_prompt: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub force_yolo: bool,

}



impl Default for SegmentTarget_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SegmentTarget_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SegmentTarget_Request {
  type RmwMsg = super::srv::rmw::SegmentTarget_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_prompt: msg.target_prompt.as_str().into(),
        force_yolo: msg.force_yolo,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        target_prompt: msg.target_prompt.as_str().into(),
      force_yolo: msg.force_yolo,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      target_prompt: msg.target_prompt.to_string(),
      force_yolo: msg.force_yolo,
    }
  }
}


// Corresponds to soarm100_interfaces__srv__SegmentTarget_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SegmentTarget_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_center: geometry_msgs::msg::PoseStamped,


    // This member is not documented.
    #[allow(missing_docs)]
    pub score: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub bbox_xyxy: [f32; 4],


    // This member is not documented.
    #[allow(missing_docs)]
    pub mask_topic: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub debug_json: std::string::String,

}



impl Default for SegmentTarget_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SegmentTarget_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SegmentTarget_Response {
  type RmwMsg = super::srv::rmw::SegmentTarget_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        reason: msg.reason.as_str().into(),
        target_center: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Owned(msg.target_center)).into_owned(),
        score: msg.score,
        bbox_xyxy: msg.bbox_xyxy,
        mask_topic: msg.mask_topic.as_str().into(),
        debug_json: msg.debug_json.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        reason: msg.reason.as_str().into(),
        target_center: geometry_msgs::msg::PoseStamped::into_rmw_message(std::borrow::Cow::Borrowed(&msg.target_center)).into_owned(),
      score: msg.score,
        bbox_xyxy: msg.bbox_xyxy,
        mask_topic: msg.mask_topic.as_str().into(),
        debug_json: msg.debug_json.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      reason: msg.reason.to_string(),
      target_center: geometry_msgs::msg::PoseStamped::from_rmw_message(msg.target_center),
      score: msg.score,
      bbox_xyxy: msg.bbox_xyxy,
      mask_topic: msg.mask_topic.to_string(),
      debug_json: msg.debug_json.to_string(),
    }
  }
}


// Corresponds to soarm100_interfaces__srv__SetAvoidance_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetAvoidance_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub enabled: bool,

}



impl Default for SetAvoidance_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetAvoidance_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetAvoidance_Request {
  type RmwMsg = super::srv::rmw::SetAvoidance_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        enabled: msg.enabled,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      enabled: msg.enabled,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      enabled: msg.enabled,
    }
  }
}


// Corresponds to soarm100_interfaces__srv__SetAvoidance_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetAvoidance_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: std::string::String,

}



impl Default for SetAvoidance_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetAvoidance_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetAvoidance_Response {
  type RmwMsg = super::srv::rmw::SetAvoidance_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        reason: msg.reason.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        reason: msg.reason.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      reason: msg.reason.to_string(),
    }
  }
}


// Corresponds to soarm100_interfaces__srv__MoveSingleJoint_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveSingleJoint_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub joint: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub delta_deg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub duration: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub hold: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub confirmation: std::string::String,

}



impl Default for MoveSingleJoint_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveSingleJoint_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveSingleJoint_Request {
  type RmwMsg = super::srv::rmw::MoveSingleJoint_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        joint: msg.joint.as_str().into(),
        delta_deg: msg.delta_deg,
        duration: msg.duration,
        hold: msg.hold,
        confirmation: msg.confirmation.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        joint: msg.joint.as_str().into(),
      delta_deg: msg.delta_deg,
      duration: msg.duration,
      hold: msg.hold,
        confirmation: msg.confirmation.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      joint: msg.joint.to_string(),
      delta_deg: msg.delta_deg,
      duration: msg.duration,
      hold: msg.hold,
      confirmation: msg.confirmation.to_string(),
    }
  }
}


// Corresponds to soarm100_interfaces__srv__MoveSingleJoint_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveSingleJoint_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub log_path: std::string::String,

}



impl Default for MoveSingleJoint_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveSingleJoint_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveSingleJoint_Response {
  type RmwMsg = super::srv::rmw::MoveSingleJoint_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        reason: msg.reason.as_str().into(),
        log_path: msg.log_path.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        reason: msg.reason.as_str().into(),
        log_path: msg.log_path.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      reason: msg.reason.to_string(),
      log_path: msg.log_path.to_string(),
    }
  }
}


// Corresponds to soarm100_interfaces__srv__MoveJointDelta_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveJointDelta_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub delta_rad: [f64; 7],


    // This member is not documented.
    #[allow(missing_docs)]
    pub duration: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub hold: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub keep_target: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub confirmation: std::string::String,

}



impl Default for MoveJointDelta_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveJointDelta_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveJointDelta_Request {
  type RmwMsg = super::srv::rmw::MoveJointDelta_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        delta_rad: msg.delta_rad,
        duration: msg.duration,
        hold: msg.hold,
        keep_target: msg.keep_target,
        confirmation: msg.confirmation.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        delta_rad: msg.delta_rad,
      duration: msg.duration,
      hold: msg.hold,
      keep_target: msg.keep_target,
        confirmation: msg.confirmation.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      delta_rad: msg.delta_rad,
      duration: msg.duration,
      hold: msg.hold,
      keep_target: msg.keep_target,
      confirmation: msg.confirmation.to_string(),
    }
  }
}


// Corresponds to soarm100_interfaces__srv__MoveJointDelta_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveJointDelta_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub log_path: std::string::String,

}



impl Default for MoveJointDelta_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveJointDelta_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveJointDelta_Response {
  type RmwMsg = super::srv::rmw::MoveJointDelta_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        reason: msg.reason.as_str().into(),
        log_path: msg.log_path.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        reason: msg.reason.as_str().into(),
        log_path: msg.log_path.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      reason: msg.reason.to_string(),
      log_path: msg.log_path.to_string(),
    }
  }
}


// Corresponds to soarm100_interfaces__srv__MoveNamedPose_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveNamedPose_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pose_name: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub duration: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub hold: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub confirmation: std::string::String,

}



impl Default for MoveNamedPose_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveNamedPose_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveNamedPose_Request {
  type RmwMsg = super::srv::rmw::MoveNamedPose_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pose_name: msg.pose_name.as_str().into(),
        duration: msg.duration,
        hold: msg.hold,
        confirmation: msg.confirmation.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pose_name: msg.pose_name.as_str().into(),
      duration: msg.duration,
      hold: msg.hold,
        confirmation: msg.confirmation.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pose_name: msg.pose_name.to_string(),
      duration: msg.duration,
      hold: msg.hold,
      confirmation: msg.confirmation.to_string(),
    }
  }
}


// Corresponds to soarm100_interfaces__srv__MoveNamedPose_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveNamedPose_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub log_path: std::string::String,

}



impl Default for MoveNamedPose_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveNamedPose_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveNamedPose_Response {
  type RmwMsg = super::srv::rmw::MoveNamedPose_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        reason: msg.reason.as_str().into(),
        log_path: msg.log_path.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        reason: msg.reason.as_str().into(),
        log_path: msg.log_path.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      reason: msg.reason.to_string(),
      log_path: msg.log_path.to_string(),
    }
  }
}


// Corresponds to soarm100_interfaces__srv__MoveJointTarget_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveJointTarget_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub position_rad: [f64; 7],


    // This member is not documented.
    #[allow(missing_docs)]
    pub duration: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub confirmation: std::string::String,

}



impl Default for MoveJointTarget_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveJointTarget_Request::default())
  }
}

impl rosidl_runtime_rs::Message for MoveJointTarget_Request {
  type RmwMsg = super::srv::rmw::MoveJointTarget_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        position_rad: msg.position_rad,
        duration: msg.duration,
        confirmation: msg.confirmation.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        position_rad: msg.position_rad,
      duration: msg.duration,
        confirmation: msg.confirmation.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      position_rad: msg.position_rad,
      duration: msg.duration,
      confirmation: msg.confirmation.to_string(),
    }
  }
}


// Corresponds to soarm100_interfaces__srv__MoveJointTarget_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveJointTarget_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub log_path: std::string::String,

}



impl Default for MoveJointTarget_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::MoveJointTarget_Response::default())
  }
}

impl rosidl_runtime_rs::Message for MoveJointTarget_Response {
  type RmwMsg = super::srv::rmw::MoveJointTarget_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        reason: msg.reason.as_str().into(),
        log_path: msg.log_path.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        reason: msg.reason.as_str().into(),
        log_path: msg.log_path.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      reason: msg.reason.to_string(),
      log_path: msg.log_path.to_string(),
    }
  }
}


// Corresponds to soarm100_interfaces__srv__SetHardwareTorque_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetHardwareTorque_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub enabled: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub confirmation: std::string::String,

}



impl Default for SetHardwareTorque_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetHardwareTorque_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetHardwareTorque_Request {
  type RmwMsg = super::srv::rmw::SetHardwareTorque_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        enabled: msg.enabled,
        confirmation: msg.confirmation.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      enabled: msg.enabled,
        confirmation: msg.confirmation.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      enabled: msg.enabled,
      confirmation: msg.confirmation.to_string(),
    }
  }
}


// Corresponds to soarm100_interfaces__srv__SetHardwareTorque_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetHardwareTorque_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: std::string::String,

}



impl Default for SetHardwareTorque_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetHardwareTorque_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetHardwareTorque_Response {
  type RmwMsg = super::srv::rmw::SetHardwareTorque_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        reason: msg.reason.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        reason: msg.reason.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      reason: msg.reason.to_string(),
    }
  }
}






#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__srv__SegmentTarget() -> *const std::ffi::c_void;
}

// Corresponds to soarm100_interfaces__srv__SegmentTarget
#[allow(missing_docs, non_camel_case_types)]
pub struct SegmentTarget;

impl rosidl_runtime_rs::Service for SegmentTarget {
    type Request = SegmentTarget_Request;
    type Response = SegmentTarget_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__srv__SegmentTarget() }
    }
}




#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__srv__SetAvoidance() -> *const std::ffi::c_void;
}

// Corresponds to soarm100_interfaces__srv__SetAvoidance
#[allow(missing_docs, non_camel_case_types)]
pub struct SetAvoidance;

impl rosidl_runtime_rs::Service for SetAvoidance {
    type Request = SetAvoidance_Request;
    type Response = SetAvoidance_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__srv__SetAvoidance() }
    }
}




#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__srv__MoveSingleJoint() -> *const std::ffi::c_void;
}

// Corresponds to soarm100_interfaces__srv__MoveSingleJoint
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveSingleJoint;

impl rosidl_runtime_rs::Service for MoveSingleJoint {
    type Request = MoveSingleJoint_Request;
    type Response = MoveSingleJoint_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__srv__MoveSingleJoint() }
    }
}




#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__srv__MoveJointDelta() -> *const std::ffi::c_void;
}

// Corresponds to soarm100_interfaces__srv__MoveJointDelta
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveJointDelta;

impl rosidl_runtime_rs::Service for MoveJointDelta {
    type Request = MoveJointDelta_Request;
    type Response = MoveJointDelta_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__srv__MoveJointDelta() }
    }
}




#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__srv__MoveNamedPose() -> *const std::ffi::c_void;
}

// Corresponds to soarm100_interfaces__srv__MoveNamedPose
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveNamedPose;

impl rosidl_runtime_rs::Service for MoveNamedPose {
    type Request = MoveNamedPose_Request;
    type Response = MoveNamedPose_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__srv__MoveNamedPose() }
    }
}




#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__srv__MoveJointTarget() -> *const std::ffi::c_void;
}

// Corresponds to soarm100_interfaces__srv__MoveJointTarget
#[allow(missing_docs, non_camel_case_types)]
pub struct MoveJointTarget;

impl rosidl_runtime_rs::Service for MoveJointTarget {
    type Request = MoveJointTarget_Request;
    type Response = MoveJointTarget_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__srv__MoveJointTarget() }
    }
}




#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__srv__SetHardwareTorque() -> *const std::ffi::c_void;
}

// Corresponds to soarm100_interfaces__srv__SetHardwareTorque
#[allow(missing_docs, non_camel_case_types)]
pub struct SetHardwareTorque;

impl rosidl_runtime_rs::Service for SetHardwareTorque {
    type Request = SetHardwareTorque_Request;
    type Response = SetHardwareTorque_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__soarm100_interfaces__srv__SetHardwareTorque() }
    }
}


