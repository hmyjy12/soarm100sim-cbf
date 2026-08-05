#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to orbbec_camera_msgs__srv__GetBool_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetBool_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetBool_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetBool_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetBool_Request {
  type RmwMsg = super::srv::rmw::GetBool_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to orbbec_camera_msgs__srv__GetBool_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetBool_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub data: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for GetBool_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetBool_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetBool_Response {
  type RmwMsg = super::srv::rmw::GetBool_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        data: msg.data,
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      data: msg.data,
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      data: msg.data,
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to orbbec_camera_msgs__srv__GetDeviceInfo_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetDeviceInfo_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetDeviceInfo_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetDeviceInfo_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetDeviceInfo_Request {
  type RmwMsg = super::srv::rmw::GetDeviceInfo_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to orbbec_camera_msgs__srv__GetDeviceInfo_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetDeviceInfo_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub info: super::msg::DeviceInfo,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for GetDeviceInfo_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetDeviceInfo_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetDeviceInfo_Response {
  type RmwMsg = super::srv::rmw::GetDeviceInfo_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        info: super::msg::DeviceInfo::into_rmw_message(std::borrow::Cow::Owned(msg.info)).into_owned(),
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        info: super::msg::DeviceInfo::into_rmw_message(std::borrow::Cow::Borrowed(&msg.info)).into_owned(),
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      info: super::msg::DeviceInfo::from_rmw_message(msg.info),
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to orbbec_camera_msgs__srv__GetCameraInfo_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCameraInfo_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetCameraInfo_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCameraInfo_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetCameraInfo_Request {
  type RmwMsg = super::srv::rmw::GetCameraInfo_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to orbbec_camera_msgs__srv__GetCameraInfo_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCameraInfo_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub info: sensor_msgs::msg::CameraInfo,

}



impl Default for GetCameraInfo_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetCameraInfo_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetCameraInfo_Response {
  type RmwMsg = super::srv::rmw::GetCameraInfo_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        info: sensor_msgs::msg::CameraInfo::into_rmw_message(std::borrow::Cow::Owned(msg.info)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        info: sensor_msgs::msg::CameraInfo::into_rmw_message(std::borrow::Cow::Borrowed(&msg.info)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      info: sensor_msgs::msg::CameraInfo::from_rmw_message(msg.info),
    }
  }
}


// Corresponds to orbbec_camera_msgs__srv__GetInt32_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetInt32_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetInt32_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetInt32_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetInt32_Request {
  type RmwMsg = super::srv::rmw::GetInt32_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to orbbec_camera_msgs__srv__GetInt32_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetInt32_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub data: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for GetInt32_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetInt32_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetInt32_Response {
  type RmwMsg = super::srv::rmw::GetInt32_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        data: msg.data,
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      data: msg.data,
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      data: msg.data,
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to orbbec_camera_msgs__srv__GetString_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetString_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetString_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetString_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetString_Request {
  type RmwMsg = super::srv::rmw::GetString_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to orbbec_camera_msgs__srv__GetString_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetString_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub data: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for GetString_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetString_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetString_Response {
  type RmwMsg = super::srv::rmw::GetString_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        data: msg.data.as_str().into(),
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        data: msg.data.as_str().into(),
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      data: msg.data.to_string(),
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to orbbec_camera_msgs__srv__SetFilter_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetFilter_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub filter_name: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub filter_enable: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub filter_param: Vec<f32>,

}



impl Default for SetFilter_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetFilter_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetFilter_Request {
  type RmwMsg = super::srv::rmw::SetFilter_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        filter_name: msg.filter_name.as_str().into(),
        filter_enable: msg.filter_enable,
        filter_param: msg.filter_param.into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        filter_name: msg.filter_name.as_str().into(),
      filter_enable: msg.filter_enable,
        filter_param: msg.filter_param.as_slice().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      filter_name: msg.filter_name.to_string(),
      filter_enable: msg.filter_enable,
      filter_param: msg.filter_param
          .into_iter()
          .collect(),
    }
  }
}


// Corresponds to orbbec_camera_msgs__srv__SetFilter_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetFilter_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for SetFilter_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetFilter_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetFilter_Response {
  type RmwMsg = super::srv::rmw::SetFilter_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to orbbec_camera_msgs__srv__SetInt32_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetInt32_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub data: i32,

}



impl Default for SetInt32_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetInt32_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetInt32_Request {
  type RmwMsg = super::srv::rmw::SetInt32_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        data: msg.data,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      data: msg.data,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      data: msg.data,
    }
  }
}


// Corresponds to orbbec_camera_msgs__srv__SetInt32_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetInt32_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for SetInt32_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetInt32_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetInt32_Response {
  type RmwMsg = super::srv::rmw::SetInt32_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to orbbec_camera_msgs__srv__SetString_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetString_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub data: std::string::String,

}



impl Default for SetString_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetString_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetString_Request {
  type RmwMsg = super::srv::rmw::SetString_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        data: msg.data.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        data: msg.data.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      data: msg.data.to_string(),
    }
  }
}


// Corresponds to orbbec_camera_msgs__srv__SetString_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetString_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for SetString_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetString_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetString_Response {
  type RmwMsg = super::srv::rmw::SetString_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to orbbec_camera_msgs__srv__SetArrays_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetArrays_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub enable: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub data_param: Vec<f32>,

}



impl Default for SetArrays_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetArrays_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetArrays_Request {
  type RmwMsg = super::srv::rmw::SetArrays_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        enable: msg.enable,
        data_param: msg.data_param.into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      enable: msg.enable,
        data_param: msg.data_param.as_slice().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      enable: msg.enable,
      data_param: msg.data_param
          .into_iter()
          .collect(),
    }
  }
}


// Corresponds to orbbec_camera_msgs__srv__SetArrays_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetArrays_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for SetArrays_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetArrays_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetArrays_Response {
  type RmwMsg = super::srv::rmw::SetArrays_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to orbbec_camera_msgs__srv__GetUserCalibParams_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetUserCalibParams_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetUserCalibParams_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetUserCalibParams_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetUserCalibParams_Request {
  type RmwMsg = super::srv::rmw::GetUserCalibParams_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to orbbec_camera_msgs__srv__GetUserCalibParams_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetUserCalibParams_Response {
    /// Intrinsic camera matrix for the raw (distorted) images
    pub k: [f64; 9],

    /// The distortion parameters
    pub d: [f64; 8],

    /// Extrinsic rotation matrix
    pub rotation: [f64; 9],

    /// Extrinsic translation vector
    pub translation: [f64; 3],


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for GetUserCalibParams_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetUserCalibParams_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetUserCalibParams_Response {
  type RmwMsg = super::srv::rmw::GetUserCalibParams_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        k: msg.k,
        d: msg.d,
        rotation: msg.rotation,
        translation: msg.translation,
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        k: msg.k,
        d: msg.d,
        rotation: msg.rotation,
        translation: msg.translation,
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      k: msg.k,
      d: msg.d,
      rotation: msg.rotation,
      translation: msg.translation,
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to orbbec_camera_msgs__srv__SetUserCalibParams_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetUserCalibParams_Request {
    /// Intrinsic camera matrix for the raw (distorted) images
    pub k: [f64; 9],

    /// The distortion parameters
    pub d: [f64; 8],

    /// Extrinsic rotation matrix
    pub rotation: [f64; 9],

    /// Extrinsic translation vector
    pub translation: [f64; 3],

}



impl Default for SetUserCalibParams_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetUserCalibParams_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetUserCalibParams_Request {
  type RmwMsg = super::srv::rmw::SetUserCalibParams_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        k: msg.k,
        d: msg.d,
        rotation: msg.rotation,
        translation: msg.translation,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        k: msg.k,
        d: msg.d,
        rotation: msg.rotation,
        translation: msg.translation,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      k: msg.k,
      d: msg.d,
      rotation: msg.rotation,
      translation: msg.translation,
    }
  }
}


// Corresponds to orbbec_camera_msgs__srv__SetUserCalibParams_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetUserCalibParams_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for SetUserCalibParams_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetUserCalibParams_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetUserCalibParams_Response {
  type RmwMsg = super::srv::rmw::SetUserCalibParams_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}






#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__orbbec_camera_msgs__srv__GetBool() -> *const std::ffi::c_void;
}

// Corresponds to orbbec_camera_msgs__srv__GetBool
#[allow(missing_docs, non_camel_case_types)]
pub struct GetBool;

impl rosidl_runtime_rs::Service for GetBool {
    type Request = GetBool_Request;
    type Response = GetBool_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__orbbec_camera_msgs__srv__GetBool() }
    }
}




#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__orbbec_camera_msgs__srv__GetDeviceInfo() -> *const std::ffi::c_void;
}

// Corresponds to orbbec_camera_msgs__srv__GetDeviceInfo
#[allow(missing_docs, non_camel_case_types)]
pub struct GetDeviceInfo;

impl rosidl_runtime_rs::Service for GetDeviceInfo {
    type Request = GetDeviceInfo_Request;
    type Response = GetDeviceInfo_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__orbbec_camera_msgs__srv__GetDeviceInfo() }
    }
}




#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__orbbec_camera_msgs__srv__GetCameraInfo() -> *const std::ffi::c_void;
}

// Corresponds to orbbec_camera_msgs__srv__GetCameraInfo
#[allow(missing_docs, non_camel_case_types)]
pub struct GetCameraInfo;

impl rosidl_runtime_rs::Service for GetCameraInfo {
    type Request = GetCameraInfo_Request;
    type Response = GetCameraInfo_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__orbbec_camera_msgs__srv__GetCameraInfo() }
    }
}




#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__orbbec_camera_msgs__srv__GetInt32() -> *const std::ffi::c_void;
}

// Corresponds to orbbec_camera_msgs__srv__GetInt32
#[allow(missing_docs, non_camel_case_types)]
pub struct GetInt32;

impl rosidl_runtime_rs::Service for GetInt32 {
    type Request = GetInt32_Request;
    type Response = GetInt32_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__orbbec_camera_msgs__srv__GetInt32() }
    }
}




#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__orbbec_camera_msgs__srv__GetString() -> *const std::ffi::c_void;
}

// Corresponds to orbbec_camera_msgs__srv__GetString
#[allow(missing_docs, non_camel_case_types)]
pub struct GetString;

impl rosidl_runtime_rs::Service for GetString {
    type Request = GetString_Request;
    type Response = GetString_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__orbbec_camera_msgs__srv__GetString() }
    }
}




#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__orbbec_camera_msgs__srv__SetFilter() -> *const std::ffi::c_void;
}

// Corresponds to orbbec_camera_msgs__srv__SetFilter
#[allow(missing_docs, non_camel_case_types)]
pub struct SetFilter;

impl rosidl_runtime_rs::Service for SetFilter {
    type Request = SetFilter_Request;
    type Response = SetFilter_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__orbbec_camera_msgs__srv__SetFilter() }
    }
}




#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__orbbec_camera_msgs__srv__SetInt32() -> *const std::ffi::c_void;
}

// Corresponds to orbbec_camera_msgs__srv__SetInt32
#[allow(missing_docs, non_camel_case_types)]
pub struct SetInt32;

impl rosidl_runtime_rs::Service for SetInt32 {
    type Request = SetInt32_Request;
    type Response = SetInt32_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__orbbec_camera_msgs__srv__SetInt32() }
    }
}




#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__orbbec_camera_msgs__srv__SetString() -> *const std::ffi::c_void;
}

// Corresponds to orbbec_camera_msgs__srv__SetString
#[allow(missing_docs, non_camel_case_types)]
pub struct SetString;

impl rosidl_runtime_rs::Service for SetString {
    type Request = SetString_Request;
    type Response = SetString_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__orbbec_camera_msgs__srv__SetString() }
    }
}




#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__orbbec_camera_msgs__srv__SetArrays() -> *const std::ffi::c_void;
}

// Corresponds to orbbec_camera_msgs__srv__SetArrays
#[allow(missing_docs, non_camel_case_types)]
pub struct SetArrays;

impl rosidl_runtime_rs::Service for SetArrays {
    type Request = SetArrays_Request;
    type Response = SetArrays_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__orbbec_camera_msgs__srv__SetArrays() }
    }
}




#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__orbbec_camera_msgs__srv__GetUserCalibParams() -> *const std::ffi::c_void;
}

// Corresponds to orbbec_camera_msgs__srv__GetUserCalibParams
#[allow(missing_docs, non_camel_case_types)]
pub struct GetUserCalibParams;

impl rosidl_runtime_rs::Service for GetUserCalibParams {
    type Request = GetUserCalibParams_Request;
    type Response = GetUserCalibParams_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__orbbec_camera_msgs__srv__GetUserCalibParams() }
    }
}




#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__orbbec_camera_msgs__srv__SetUserCalibParams() -> *const std::ffi::c_void;
}

// Corresponds to orbbec_camera_msgs__srv__SetUserCalibParams
#[allow(missing_docs, non_camel_case_types)]
pub struct SetUserCalibParams;

impl rosidl_runtime_rs::Service for SetUserCalibParams {
    type Request = SetUserCalibParams_Request;
    type Response = SetUserCalibParams_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__orbbec_camera_msgs__srv__SetUserCalibParams() }
    }
}


