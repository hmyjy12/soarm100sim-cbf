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


