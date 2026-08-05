#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to orbbec_camera_msgs__msg__DeviceInfo

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DeviceInfo {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub name: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub serial_number: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub firmware_version: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub supported_min_sdk_version: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub current_sdk_version: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub hardware_version: std::string::String,

}



impl Default for DeviceInfo {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::DeviceInfo::default())
  }
}

impl rosidl_runtime_rs::Message for DeviceInfo {
  type RmwMsg = super::msg::rmw::DeviceInfo;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        name: msg.name.as_str().into(),
        serial_number: msg.serial_number.as_str().into(),
        firmware_version: msg.firmware_version.as_str().into(),
        supported_min_sdk_version: msg.supported_min_sdk_version.as_str().into(),
        current_sdk_version: msg.current_sdk_version.as_str().into(),
        hardware_version: msg.hardware_version.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        name: msg.name.as_str().into(),
        serial_number: msg.serial_number.as_str().into(),
        firmware_version: msg.firmware_version.as_str().into(),
        supported_min_sdk_version: msg.supported_min_sdk_version.as_str().into(),
        current_sdk_version: msg.current_sdk_version.as_str().into(),
        hardware_version: msg.hardware_version.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      name: msg.name.to_string(),
      serial_number: msg.serial_number.to_string(),
      firmware_version: msg.firmware_version.to_string(),
      supported_min_sdk_version: msg.supported_min_sdk_version.to_string(),
      current_sdk_version: msg.current_sdk_version.to_string(),
      hardware_version: msg.hardware_version.to_string(),
    }
  }
}


// Corresponds to orbbec_camera_msgs__msg__DeviceStatus

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DeviceStatus {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,

    /// --- Color stream ---
    pub color_frame_rate_cur: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub color_frame_rate_avg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub color_frame_rate_min: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub color_frame_rate_max: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub color_delay_ms_cur: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub color_delay_ms_avg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub color_delay_ms_min: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub color_delay_ms_max: f64,

    /// --- Depth stream ---
    pub depth_frame_rate_cur: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub depth_frame_rate_avg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub depth_frame_rate_min: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub depth_frame_rate_max: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub depth_delay_ms_cur: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub depth_delay_ms_avg: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub depth_delay_ms_min: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub depth_delay_ms_max: f64,

    /// --- Device info ---
    pub device_online: bool,

    /// e.g. "USB2.0", "USB3.0", "GigE"
    pub connection_type: std::string::String,

    /// --- Calibration status ---
    pub customer_calibration_ready: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub calibration_from_factory: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub calibration_from_launch_param: bool,

}



impl Default for DeviceStatus {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::DeviceStatus::default())
  }
}

impl rosidl_runtime_rs::Message for DeviceStatus {
  type RmwMsg = super::msg::rmw::DeviceStatus;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        color_frame_rate_cur: msg.color_frame_rate_cur,
        color_frame_rate_avg: msg.color_frame_rate_avg,
        color_frame_rate_min: msg.color_frame_rate_min,
        color_frame_rate_max: msg.color_frame_rate_max,
        color_delay_ms_cur: msg.color_delay_ms_cur,
        color_delay_ms_avg: msg.color_delay_ms_avg,
        color_delay_ms_min: msg.color_delay_ms_min,
        color_delay_ms_max: msg.color_delay_ms_max,
        depth_frame_rate_cur: msg.depth_frame_rate_cur,
        depth_frame_rate_avg: msg.depth_frame_rate_avg,
        depth_frame_rate_min: msg.depth_frame_rate_min,
        depth_frame_rate_max: msg.depth_frame_rate_max,
        depth_delay_ms_cur: msg.depth_delay_ms_cur,
        depth_delay_ms_avg: msg.depth_delay_ms_avg,
        depth_delay_ms_min: msg.depth_delay_ms_min,
        depth_delay_ms_max: msg.depth_delay_ms_max,
        device_online: msg.device_online,
        connection_type: msg.connection_type.as_str().into(),
        customer_calibration_ready: msg.customer_calibration_ready,
        calibration_from_factory: msg.calibration_from_factory,
        calibration_from_launch_param: msg.calibration_from_launch_param,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
      color_frame_rate_cur: msg.color_frame_rate_cur,
      color_frame_rate_avg: msg.color_frame_rate_avg,
      color_frame_rate_min: msg.color_frame_rate_min,
      color_frame_rate_max: msg.color_frame_rate_max,
      color_delay_ms_cur: msg.color_delay_ms_cur,
      color_delay_ms_avg: msg.color_delay_ms_avg,
      color_delay_ms_min: msg.color_delay_ms_min,
      color_delay_ms_max: msg.color_delay_ms_max,
      depth_frame_rate_cur: msg.depth_frame_rate_cur,
      depth_frame_rate_avg: msg.depth_frame_rate_avg,
      depth_frame_rate_min: msg.depth_frame_rate_min,
      depth_frame_rate_max: msg.depth_frame_rate_max,
      depth_delay_ms_cur: msg.depth_delay_ms_cur,
      depth_delay_ms_avg: msg.depth_delay_ms_avg,
      depth_delay_ms_min: msg.depth_delay_ms_min,
      depth_delay_ms_max: msg.depth_delay_ms_max,
      device_online: msg.device_online,
        connection_type: msg.connection_type.as_str().into(),
      customer_calibration_ready: msg.customer_calibration_ready,
      calibration_from_factory: msg.calibration_from_factory,
      calibration_from_launch_param: msg.calibration_from_launch_param,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      color_frame_rate_cur: msg.color_frame_rate_cur,
      color_frame_rate_avg: msg.color_frame_rate_avg,
      color_frame_rate_min: msg.color_frame_rate_min,
      color_frame_rate_max: msg.color_frame_rate_max,
      color_delay_ms_cur: msg.color_delay_ms_cur,
      color_delay_ms_avg: msg.color_delay_ms_avg,
      color_delay_ms_min: msg.color_delay_ms_min,
      color_delay_ms_max: msg.color_delay_ms_max,
      depth_frame_rate_cur: msg.depth_frame_rate_cur,
      depth_frame_rate_avg: msg.depth_frame_rate_avg,
      depth_frame_rate_min: msg.depth_frame_rate_min,
      depth_frame_rate_max: msg.depth_frame_rate_max,
      depth_delay_ms_cur: msg.depth_delay_ms_cur,
      depth_delay_ms_avg: msg.depth_delay_ms_avg,
      depth_delay_ms_min: msg.depth_delay_ms_min,
      depth_delay_ms_max: msg.depth_delay_ms_max,
      device_online: msg.device_online,
      connection_type: msg.connection_type.to_string(),
      customer_calibration_ready: msg.customer_calibration_ready,
      calibration_from_factory: msg.calibration_from_factory,
      calibration_from_launch_param: msg.calibration_from_launch_param,
    }
  }
}


// Corresponds to orbbec_camera_msgs__msg__DepthFilterParam

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DepthFilterParam {

    // This member is not documented.
    #[allow(missing_docs)]
    pub name: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub value: std::string::String,

}



impl Default for DepthFilterParam {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::DepthFilterParam::default())
  }
}

impl rosidl_runtime_rs::Message for DepthFilterParam {
  type RmwMsg = super::msg::rmw::DepthFilterParam;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
        value: msg.value.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        name: msg.name.as_str().into(),
        value: msg.value.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      name: msg.name.to_string(),
      value: msg.value.to_string(),
    }
  }
}


// Corresponds to orbbec_camera_msgs__msg__DepthFilterState

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DepthFilterState {

    // This member is not documented.
    #[allow(missing_docs)]
    pub filter_name: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub enabled: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub params: Vec<super::msg::DepthFilterParam>,

}



impl Default for DepthFilterState {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::DepthFilterState::default())
  }
}

impl rosidl_runtime_rs::Message for DepthFilterState {
  type RmwMsg = super::msg::rmw::DepthFilterState;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        filter_name: msg.filter_name.as_str().into(),
        enabled: msg.enabled,
        params: msg.params
          .into_iter()
          .map(|elem| super::msg::DepthFilterParam::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        filter_name: msg.filter_name.as_str().into(),
      enabled: msg.enabled,
        params: msg.params
          .iter()
          .map(|elem| super::msg::DepthFilterParam::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      filter_name: msg.filter_name.to_string(),
      enabled: msg.enabled,
      params: msg.params
          .into_iter()
          .map(super::msg::DepthFilterParam::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to orbbec_camera_msgs__msg__DepthFiltersStatus

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DepthFiltersStatus {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub filters: Vec<super::msg::DepthFilterState>,

}



impl Default for DepthFiltersStatus {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::DepthFiltersStatus::default())
  }
}

impl rosidl_runtime_rs::Message for DepthFiltersStatus {
  type RmwMsg = super::msg::rmw::DepthFiltersStatus;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        filters: msg.filters
          .into_iter()
          .map(|elem| super::msg::DepthFilterState::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        filters: msg.filters
          .iter()
          .map(|elem| super::msg::DepthFilterState::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      filters: msg.filters
          .into_iter()
          .map(super::msg::DepthFilterState::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to orbbec_camera_msgs__msg__Extrinsics

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Extrinsics {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub rotation: [f64; 9],


    // This member is not documented.
    #[allow(missing_docs)]
    pub translation: [f64; 3],

}



impl Default for Extrinsics {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Extrinsics::default())
  }
}

impl rosidl_runtime_rs::Message for Extrinsics {
  type RmwMsg = super::msg::rmw::Extrinsics;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        rotation: msg.rotation,
        translation: msg.translation,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        rotation: msg.rotation,
        translation: msg.translation,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      rotation: msg.rotation,
      translation: msg.translation,
    }
  }
}


// Corresponds to orbbec_camera_msgs__msg__Metadata

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Metadata {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub json_data: std::string::String,

}



impl Default for Metadata {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Metadata::default())
  }
}

impl rosidl_runtime_rs::Message for Metadata {
  type RmwMsg = super::msg::rmw::Metadata;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        json_data: msg.json_data.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        json_data: msg.json_data.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      json_data: msg.json_data.to_string(),
    }
  }
}


// Corresponds to orbbec_camera_msgs__msg__IMUInfo

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct IMUInfo {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub noise_density: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub random_walk: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reference_temperature: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub bias: [f64; 3],


    // This member is not documented.
    #[allow(missing_docs)]
    pub gravity: [f64; 3],


    // This member is not documented.
    #[allow(missing_docs)]
    pub scale_misalignment: [f64; 9],


    // This member is not documented.
    #[allow(missing_docs)]
    pub temperature_slope: [f64; 9],

}



impl Default for IMUInfo {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::IMUInfo::default())
  }
}

impl rosidl_runtime_rs::Message for IMUInfo {
  type RmwMsg = super::msg::rmw::IMUInfo;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        noise_density: msg.noise_density,
        random_walk: msg.random_walk,
        reference_temperature: msg.reference_temperature,
        bias: msg.bias,
        gravity: msg.gravity,
        scale_misalignment: msg.scale_misalignment,
        temperature_slope: msg.temperature_slope,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
      noise_density: msg.noise_density,
      random_walk: msg.random_walk,
      reference_temperature: msg.reference_temperature,
        bias: msg.bias,
        gravity: msg.gravity,
        scale_misalignment: msg.scale_misalignment,
        temperature_slope: msg.temperature_slope,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      noise_density: msg.noise_density,
      random_walk: msg.random_walk,
      reference_temperature: msg.reference_temperature,
      bias: msg.bias,
      gravity: msg.gravity,
      scale_misalignment: msg.scale_misalignment,
      temperature_slope: msg.temperature_slope,
    }
  }
}


// Corresponds to orbbec_camera_msgs__msg__RGBD
/// RGBD Message

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RGBD {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub rgb_camera_info: sensor_msgs::msg::CameraInfo,


    // This member is not documented.
    #[allow(missing_docs)]
    pub depth_camera_info: sensor_msgs::msg::CameraInfo,


    // This member is not documented.
    #[allow(missing_docs)]
    pub rgb: sensor_msgs::msg::Image,


    // This member is not documented.
    #[allow(missing_docs)]
    pub depth: sensor_msgs::msg::Image,

}



impl Default for RGBD {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::RGBD::default())
  }
}

impl rosidl_runtime_rs::Message for RGBD {
  type RmwMsg = super::msg::rmw::RGBD;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        rgb_camera_info: sensor_msgs::msg::CameraInfo::into_rmw_message(std::borrow::Cow::Owned(msg.rgb_camera_info)).into_owned(),
        depth_camera_info: sensor_msgs::msg::CameraInfo::into_rmw_message(std::borrow::Cow::Owned(msg.depth_camera_info)).into_owned(),
        rgb: sensor_msgs::msg::Image::into_rmw_message(std::borrow::Cow::Owned(msg.rgb)).into_owned(),
        depth: sensor_msgs::msg::Image::into_rmw_message(std::borrow::Cow::Owned(msg.depth)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        rgb_camera_info: sensor_msgs::msg::CameraInfo::into_rmw_message(std::borrow::Cow::Borrowed(&msg.rgb_camera_info)).into_owned(),
        depth_camera_info: sensor_msgs::msg::CameraInfo::into_rmw_message(std::borrow::Cow::Borrowed(&msg.depth_camera_info)).into_owned(),
        rgb: sensor_msgs::msg::Image::into_rmw_message(std::borrow::Cow::Borrowed(&msg.rgb)).into_owned(),
        depth: sensor_msgs::msg::Image::into_rmw_message(std::borrow::Cow::Borrowed(&msg.depth)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      rgb_camera_info: sensor_msgs::msg::CameraInfo::from_rmw_message(msg.rgb_camera_info),
      depth_camera_info: sensor_msgs::msg::CameraInfo::from_rmw_message(msg.depth_camera_info),
      rgb: sensor_msgs::msg::Image::from_rmw_message(msg.rgb),
      depth: sensor_msgs::msg::Image::from_rmw_message(msg.depth),
    }
  }
}


