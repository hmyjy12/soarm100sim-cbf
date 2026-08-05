#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetBool_Request() -> *const std::ffi::c_void;
}

#[link(name = "orbbec_camera_msgs__rosidl_generator_c")]
extern "C" {
    fn orbbec_camera_msgs__srv__GetBool_Request__init(msg: *mut GetBool_Request) -> bool;
    fn orbbec_camera_msgs__srv__GetBool_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetBool_Request>, size: usize) -> bool;
    fn orbbec_camera_msgs__srv__GetBool_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetBool_Request>);
    fn orbbec_camera_msgs__srv__GetBool_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetBool_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetBool_Request>) -> bool;
}

// Corresponds to orbbec_camera_msgs__srv__GetBool_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetBool_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetBool_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !orbbec_camera_msgs__srv__GetBool_Request__init(&mut msg as *mut _) {
        panic!("Call to orbbec_camera_msgs__srv__GetBool_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetBool_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetBool_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetBool_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetBool_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetBool_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetBool_Request where Self: Sized {
  const TYPE_NAME: &'static str = "orbbec_camera_msgs/srv/GetBool_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetBool_Request() }
  }
}


#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetBool_Response() -> *const std::ffi::c_void;
}

#[link(name = "orbbec_camera_msgs__rosidl_generator_c")]
extern "C" {
    fn orbbec_camera_msgs__srv__GetBool_Response__init(msg: *mut GetBool_Response) -> bool;
    fn orbbec_camera_msgs__srv__GetBool_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetBool_Response>, size: usize) -> bool;
    fn orbbec_camera_msgs__srv__GetBool_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetBool_Response>);
    fn orbbec_camera_msgs__srv__GetBool_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetBool_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetBool_Response>) -> bool;
}

// Corresponds to orbbec_camera_msgs__srv__GetBool_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
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
    pub message: rosidl_runtime_rs::String,

}



impl Default for GetBool_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !orbbec_camera_msgs__srv__GetBool_Response__init(&mut msg as *mut _) {
        panic!("Call to orbbec_camera_msgs__srv__GetBool_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetBool_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetBool_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetBool_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetBool_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetBool_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetBool_Response where Self: Sized {
  const TYPE_NAME: &'static str = "orbbec_camera_msgs/srv/GetBool_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetBool_Response() }
  }
}


#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetDeviceInfo_Request() -> *const std::ffi::c_void;
}

#[link(name = "orbbec_camera_msgs__rosidl_generator_c")]
extern "C" {
    fn orbbec_camera_msgs__srv__GetDeviceInfo_Request__init(msg: *mut GetDeviceInfo_Request) -> bool;
    fn orbbec_camera_msgs__srv__GetDeviceInfo_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetDeviceInfo_Request>, size: usize) -> bool;
    fn orbbec_camera_msgs__srv__GetDeviceInfo_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetDeviceInfo_Request>);
    fn orbbec_camera_msgs__srv__GetDeviceInfo_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetDeviceInfo_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetDeviceInfo_Request>) -> bool;
}

// Corresponds to orbbec_camera_msgs__srv__GetDeviceInfo_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetDeviceInfo_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetDeviceInfo_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !orbbec_camera_msgs__srv__GetDeviceInfo_Request__init(&mut msg as *mut _) {
        panic!("Call to orbbec_camera_msgs__srv__GetDeviceInfo_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetDeviceInfo_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetDeviceInfo_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetDeviceInfo_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetDeviceInfo_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetDeviceInfo_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetDeviceInfo_Request where Self: Sized {
  const TYPE_NAME: &'static str = "orbbec_camera_msgs/srv/GetDeviceInfo_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetDeviceInfo_Request() }
  }
}


#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetDeviceInfo_Response() -> *const std::ffi::c_void;
}

#[link(name = "orbbec_camera_msgs__rosidl_generator_c")]
extern "C" {
    fn orbbec_camera_msgs__srv__GetDeviceInfo_Response__init(msg: *mut GetDeviceInfo_Response) -> bool;
    fn orbbec_camera_msgs__srv__GetDeviceInfo_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetDeviceInfo_Response>, size: usize) -> bool;
    fn orbbec_camera_msgs__srv__GetDeviceInfo_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetDeviceInfo_Response>);
    fn orbbec_camera_msgs__srv__GetDeviceInfo_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetDeviceInfo_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetDeviceInfo_Response>) -> bool;
}

// Corresponds to orbbec_camera_msgs__srv__GetDeviceInfo_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetDeviceInfo_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub info: super::super::msg::rmw::DeviceInfo,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for GetDeviceInfo_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !orbbec_camera_msgs__srv__GetDeviceInfo_Response__init(&mut msg as *mut _) {
        panic!("Call to orbbec_camera_msgs__srv__GetDeviceInfo_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetDeviceInfo_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetDeviceInfo_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetDeviceInfo_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetDeviceInfo_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetDeviceInfo_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetDeviceInfo_Response where Self: Sized {
  const TYPE_NAME: &'static str = "orbbec_camera_msgs/srv/GetDeviceInfo_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetDeviceInfo_Response() }
  }
}


#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetCameraInfo_Request() -> *const std::ffi::c_void;
}

#[link(name = "orbbec_camera_msgs__rosidl_generator_c")]
extern "C" {
    fn orbbec_camera_msgs__srv__GetCameraInfo_Request__init(msg: *mut GetCameraInfo_Request) -> bool;
    fn orbbec_camera_msgs__srv__GetCameraInfo_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetCameraInfo_Request>, size: usize) -> bool;
    fn orbbec_camera_msgs__srv__GetCameraInfo_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetCameraInfo_Request>);
    fn orbbec_camera_msgs__srv__GetCameraInfo_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetCameraInfo_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetCameraInfo_Request>) -> bool;
}

// Corresponds to orbbec_camera_msgs__srv__GetCameraInfo_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCameraInfo_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetCameraInfo_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !orbbec_camera_msgs__srv__GetCameraInfo_Request__init(&mut msg as *mut _) {
        panic!("Call to orbbec_camera_msgs__srv__GetCameraInfo_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetCameraInfo_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetCameraInfo_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetCameraInfo_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetCameraInfo_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetCameraInfo_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetCameraInfo_Request where Self: Sized {
  const TYPE_NAME: &'static str = "orbbec_camera_msgs/srv/GetCameraInfo_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetCameraInfo_Request() }
  }
}


#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetCameraInfo_Response() -> *const std::ffi::c_void;
}

#[link(name = "orbbec_camera_msgs__rosidl_generator_c")]
extern "C" {
    fn orbbec_camera_msgs__srv__GetCameraInfo_Response__init(msg: *mut GetCameraInfo_Response) -> bool;
    fn orbbec_camera_msgs__srv__GetCameraInfo_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetCameraInfo_Response>, size: usize) -> bool;
    fn orbbec_camera_msgs__srv__GetCameraInfo_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetCameraInfo_Response>);
    fn orbbec_camera_msgs__srv__GetCameraInfo_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetCameraInfo_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetCameraInfo_Response>) -> bool;
}

// Corresponds to orbbec_camera_msgs__srv__GetCameraInfo_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetCameraInfo_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub info: sensor_msgs::msg::rmw::CameraInfo,

}



impl Default for GetCameraInfo_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !orbbec_camera_msgs__srv__GetCameraInfo_Response__init(&mut msg as *mut _) {
        panic!("Call to orbbec_camera_msgs__srv__GetCameraInfo_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetCameraInfo_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetCameraInfo_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetCameraInfo_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetCameraInfo_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetCameraInfo_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetCameraInfo_Response where Self: Sized {
  const TYPE_NAME: &'static str = "orbbec_camera_msgs/srv/GetCameraInfo_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetCameraInfo_Response() }
  }
}


#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetInt32_Request() -> *const std::ffi::c_void;
}

#[link(name = "orbbec_camera_msgs__rosidl_generator_c")]
extern "C" {
    fn orbbec_camera_msgs__srv__GetInt32_Request__init(msg: *mut GetInt32_Request) -> bool;
    fn orbbec_camera_msgs__srv__GetInt32_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetInt32_Request>, size: usize) -> bool;
    fn orbbec_camera_msgs__srv__GetInt32_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetInt32_Request>);
    fn orbbec_camera_msgs__srv__GetInt32_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetInt32_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetInt32_Request>) -> bool;
}

// Corresponds to orbbec_camera_msgs__srv__GetInt32_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetInt32_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetInt32_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !orbbec_camera_msgs__srv__GetInt32_Request__init(&mut msg as *mut _) {
        panic!("Call to orbbec_camera_msgs__srv__GetInt32_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetInt32_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetInt32_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetInt32_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetInt32_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetInt32_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetInt32_Request where Self: Sized {
  const TYPE_NAME: &'static str = "orbbec_camera_msgs/srv/GetInt32_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetInt32_Request() }
  }
}


#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetInt32_Response() -> *const std::ffi::c_void;
}

#[link(name = "orbbec_camera_msgs__rosidl_generator_c")]
extern "C" {
    fn orbbec_camera_msgs__srv__GetInt32_Response__init(msg: *mut GetInt32_Response) -> bool;
    fn orbbec_camera_msgs__srv__GetInt32_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetInt32_Response>, size: usize) -> bool;
    fn orbbec_camera_msgs__srv__GetInt32_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetInt32_Response>);
    fn orbbec_camera_msgs__srv__GetInt32_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetInt32_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetInt32_Response>) -> bool;
}

// Corresponds to orbbec_camera_msgs__srv__GetInt32_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
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
    pub message: rosidl_runtime_rs::String,

}



impl Default for GetInt32_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !orbbec_camera_msgs__srv__GetInt32_Response__init(&mut msg as *mut _) {
        panic!("Call to orbbec_camera_msgs__srv__GetInt32_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetInt32_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetInt32_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetInt32_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetInt32_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetInt32_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetInt32_Response where Self: Sized {
  const TYPE_NAME: &'static str = "orbbec_camera_msgs/srv/GetInt32_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetInt32_Response() }
  }
}


#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetString_Request() -> *const std::ffi::c_void;
}

#[link(name = "orbbec_camera_msgs__rosidl_generator_c")]
extern "C" {
    fn orbbec_camera_msgs__srv__GetString_Request__init(msg: *mut GetString_Request) -> bool;
    fn orbbec_camera_msgs__srv__GetString_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetString_Request>, size: usize) -> bool;
    fn orbbec_camera_msgs__srv__GetString_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetString_Request>);
    fn orbbec_camera_msgs__srv__GetString_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetString_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetString_Request>) -> bool;
}

// Corresponds to orbbec_camera_msgs__srv__GetString_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetString_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetString_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !orbbec_camera_msgs__srv__GetString_Request__init(&mut msg as *mut _) {
        panic!("Call to orbbec_camera_msgs__srv__GetString_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetString_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetString_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetString_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetString_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetString_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetString_Request where Self: Sized {
  const TYPE_NAME: &'static str = "orbbec_camera_msgs/srv/GetString_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetString_Request() }
  }
}


#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetString_Response() -> *const std::ffi::c_void;
}

#[link(name = "orbbec_camera_msgs__rosidl_generator_c")]
extern "C" {
    fn orbbec_camera_msgs__srv__GetString_Response__init(msg: *mut GetString_Response) -> bool;
    fn orbbec_camera_msgs__srv__GetString_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetString_Response>, size: usize) -> bool;
    fn orbbec_camera_msgs__srv__GetString_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetString_Response>);
    fn orbbec_camera_msgs__srv__GetString_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetString_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetString_Response>) -> bool;
}

// Corresponds to orbbec_camera_msgs__srv__GetString_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetString_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub data: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for GetString_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !orbbec_camera_msgs__srv__GetString_Response__init(&mut msg as *mut _) {
        panic!("Call to orbbec_camera_msgs__srv__GetString_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetString_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetString_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetString_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetString_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetString_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetString_Response where Self: Sized {
  const TYPE_NAME: &'static str = "orbbec_camera_msgs/srv/GetString_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetString_Response() }
  }
}


#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__SetFilter_Request() -> *const std::ffi::c_void;
}

#[link(name = "orbbec_camera_msgs__rosidl_generator_c")]
extern "C" {
    fn orbbec_camera_msgs__srv__SetFilter_Request__init(msg: *mut SetFilter_Request) -> bool;
    fn orbbec_camera_msgs__srv__SetFilter_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetFilter_Request>, size: usize) -> bool;
    fn orbbec_camera_msgs__srv__SetFilter_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetFilter_Request>);
    fn orbbec_camera_msgs__srv__SetFilter_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetFilter_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SetFilter_Request>) -> bool;
}

// Corresponds to orbbec_camera_msgs__srv__SetFilter_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetFilter_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub filter_name: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub filter_enable: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub filter_param: rosidl_runtime_rs::Sequence<f32>,

}



impl Default for SetFilter_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !orbbec_camera_msgs__srv__SetFilter_Request__init(&mut msg as *mut _) {
        panic!("Call to orbbec_camera_msgs__srv__SetFilter_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetFilter_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetFilter_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetFilter_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetFilter_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetFilter_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetFilter_Request where Self: Sized {
  const TYPE_NAME: &'static str = "orbbec_camera_msgs/srv/SetFilter_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__SetFilter_Request() }
  }
}


#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__SetFilter_Response() -> *const std::ffi::c_void;
}

#[link(name = "orbbec_camera_msgs__rosidl_generator_c")]
extern "C" {
    fn orbbec_camera_msgs__srv__SetFilter_Response__init(msg: *mut SetFilter_Response) -> bool;
    fn orbbec_camera_msgs__srv__SetFilter_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetFilter_Response>, size: usize) -> bool;
    fn orbbec_camera_msgs__srv__SetFilter_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetFilter_Response>);
    fn orbbec_camera_msgs__srv__SetFilter_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetFilter_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SetFilter_Response>) -> bool;
}

// Corresponds to orbbec_camera_msgs__srv__SetFilter_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetFilter_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for SetFilter_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !orbbec_camera_msgs__srv__SetFilter_Response__init(&mut msg as *mut _) {
        panic!("Call to orbbec_camera_msgs__srv__SetFilter_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetFilter_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetFilter_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetFilter_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetFilter_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetFilter_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetFilter_Response where Self: Sized {
  const TYPE_NAME: &'static str = "orbbec_camera_msgs/srv/SetFilter_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__SetFilter_Response() }
  }
}


#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__SetInt32_Request() -> *const std::ffi::c_void;
}

#[link(name = "orbbec_camera_msgs__rosidl_generator_c")]
extern "C" {
    fn orbbec_camera_msgs__srv__SetInt32_Request__init(msg: *mut SetInt32_Request) -> bool;
    fn orbbec_camera_msgs__srv__SetInt32_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetInt32_Request>, size: usize) -> bool;
    fn orbbec_camera_msgs__srv__SetInt32_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetInt32_Request>);
    fn orbbec_camera_msgs__srv__SetInt32_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetInt32_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SetInt32_Request>) -> bool;
}

// Corresponds to orbbec_camera_msgs__srv__SetInt32_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetInt32_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub data: i32,

}



impl Default for SetInt32_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !orbbec_camera_msgs__srv__SetInt32_Request__init(&mut msg as *mut _) {
        panic!("Call to orbbec_camera_msgs__srv__SetInt32_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetInt32_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetInt32_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetInt32_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetInt32_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetInt32_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetInt32_Request where Self: Sized {
  const TYPE_NAME: &'static str = "orbbec_camera_msgs/srv/SetInt32_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__SetInt32_Request() }
  }
}


#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__SetInt32_Response() -> *const std::ffi::c_void;
}

#[link(name = "orbbec_camera_msgs__rosidl_generator_c")]
extern "C" {
    fn orbbec_camera_msgs__srv__SetInt32_Response__init(msg: *mut SetInt32_Response) -> bool;
    fn orbbec_camera_msgs__srv__SetInt32_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetInt32_Response>, size: usize) -> bool;
    fn orbbec_camera_msgs__srv__SetInt32_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetInt32_Response>);
    fn orbbec_camera_msgs__srv__SetInt32_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetInt32_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SetInt32_Response>) -> bool;
}

// Corresponds to orbbec_camera_msgs__srv__SetInt32_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetInt32_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for SetInt32_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !orbbec_camera_msgs__srv__SetInt32_Response__init(&mut msg as *mut _) {
        panic!("Call to orbbec_camera_msgs__srv__SetInt32_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetInt32_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetInt32_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetInt32_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetInt32_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetInt32_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetInt32_Response where Self: Sized {
  const TYPE_NAME: &'static str = "orbbec_camera_msgs/srv/SetInt32_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__SetInt32_Response() }
  }
}


#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__SetString_Request() -> *const std::ffi::c_void;
}

#[link(name = "orbbec_camera_msgs__rosidl_generator_c")]
extern "C" {
    fn orbbec_camera_msgs__srv__SetString_Request__init(msg: *mut SetString_Request) -> bool;
    fn orbbec_camera_msgs__srv__SetString_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetString_Request>, size: usize) -> bool;
    fn orbbec_camera_msgs__srv__SetString_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetString_Request>);
    fn orbbec_camera_msgs__srv__SetString_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetString_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SetString_Request>) -> bool;
}

// Corresponds to orbbec_camera_msgs__srv__SetString_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetString_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub data: rosidl_runtime_rs::String,

}



impl Default for SetString_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !orbbec_camera_msgs__srv__SetString_Request__init(&mut msg as *mut _) {
        panic!("Call to orbbec_camera_msgs__srv__SetString_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetString_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetString_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetString_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetString_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetString_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetString_Request where Self: Sized {
  const TYPE_NAME: &'static str = "orbbec_camera_msgs/srv/SetString_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__SetString_Request() }
  }
}


#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__SetString_Response() -> *const std::ffi::c_void;
}

#[link(name = "orbbec_camera_msgs__rosidl_generator_c")]
extern "C" {
    fn orbbec_camera_msgs__srv__SetString_Response__init(msg: *mut SetString_Response) -> bool;
    fn orbbec_camera_msgs__srv__SetString_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetString_Response>, size: usize) -> bool;
    fn orbbec_camera_msgs__srv__SetString_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetString_Response>);
    fn orbbec_camera_msgs__srv__SetString_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetString_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SetString_Response>) -> bool;
}

// Corresponds to orbbec_camera_msgs__srv__SetString_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetString_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for SetString_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !orbbec_camera_msgs__srv__SetString_Response__init(&mut msg as *mut _) {
        panic!("Call to orbbec_camera_msgs__srv__SetString_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetString_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetString_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetString_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetString_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetString_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetString_Response where Self: Sized {
  const TYPE_NAME: &'static str = "orbbec_camera_msgs/srv/SetString_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__SetString_Response() }
  }
}


#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__SetArrays_Request() -> *const std::ffi::c_void;
}

#[link(name = "orbbec_camera_msgs__rosidl_generator_c")]
extern "C" {
    fn orbbec_camera_msgs__srv__SetArrays_Request__init(msg: *mut SetArrays_Request) -> bool;
    fn orbbec_camera_msgs__srv__SetArrays_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetArrays_Request>, size: usize) -> bool;
    fn orbbec_camera_msgs__srv__SetArrays_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetArrays_Request>);
    fn orbbec_camera_msgs__srv__SetArrays_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetArrays_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SetArrays_Request>) -> bool;
}

// Corresponds to orbbec_camera_msgs__srv__SetArrays_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetArrays_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub enable: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub data_param: rosidl_runtime_rs::Sequence<f32>,

}



impl Default for SetArrays_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !orbbec_camera_msgs__srv__SetArrays_Request__init(&mut msg as *mut _) {
        panic!("Call to orbbec_camera_msgs__srv__SetArrays_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetArrays_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetArrays_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetArrays_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetArrays_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetArrays_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetArrays_Request where Self: Sized {
  const TYPE_NAME: &'static str = "orbbec_camera_msgs/srv/SetArrays_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__SetArrays_Request() }
  }
}


#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__SetArrays_Response() -> *const std::ffi::c_void;
}

#[link(name = "orbbec_camera_msgs__rosidl_generator_c")]
extern "C" {
    fn orbbec_camera_msgs__srv__SetArrays_Response__init(msg: *mut SetArrays_Response) -> bool;
    fn orbbec_camera_msgs__srv__SetArrays_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetArrays_Response>, size: usize) -> bool;
    fn orbbec_camera_msgs__srv__SetArrays_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetArrays_Response>);
    fn orbbec_camera_msgs__srv__SetArrays_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetArrays_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SetArrays_Response>) -> bool;
}

// Corresponds to orbbec_camera_msgs__srv__SetArrays_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetArrays_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for SetArrays_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !orbbec_camera_msgs__srv__SetArrays_Response__init(&mut msg as *mut _) {
        panic!("Call to orbbec_camera_msgs__srv__SetArrays_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetArrays_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetArrays_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetArrays_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetArrays_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetArrays_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetArrays_Response where Self: Sized {
  const TYPE_NAME: &'static str = "orbbec_camera_msgs/srv/SetArrays_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__SetArrays_Response() }
  }
}


#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetUserCalibParams_Request() -> *const std::ffi::c_void;
}

#[link(name = "orbbec_camera_msgs__rosidl_generator_c")]
extern "C" {
    fn orbbec_camera_msgs__srv__GetUserCalibParams_Request__init(msg: *mut GetUserCalibParams_Request) -> bool;
    fn orbbec_camera_msgs__srv__GetUserCalibParams_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetUserCalibParams_Request>, size: usize) -> bool;
    fn orbbec_camera_msgs__srv__GetUserCalibParams_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetUserCalibParams_Request>);
    fn orbbec_camera_msgs__srv__GetUserCalibParams_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetUserCalibParams_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetUserCalibParams_Request>) -> bool;
}

// Corresponds to orbbec_camera_msgs__srv__GetUserCalibParams_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetUserCalibParams_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetUserCalibParams_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !orbbec_camera_msgs__srv__GetUserCalibParams_Request__init(&mut msg as *mut _) {
        panic!("Call to orbbec_camera_msgs__srv__GetUserCalibParams_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetUserCalibParams_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetUserCalibParams_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetUserCalibParams_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetUserCalibParams_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetUserCalibParams_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetUserCalibParams_Request where Self: Sized {
  const TYPE_NAME: &'static str = "orbbec_camera_msgs/srv/GetUserCalibParams_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetUserCalibParams_Request() }
  }
}


#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetUserCalibParams_Response() -> *const std::ffi::c_void;
}

#[link(name = "orbbec_camera_msgs__rosidl_generator_c")]
extern "C" {
    fn orbbec_camera_msgs__srv__GetUserCalibParams_Response__init(msg: *mut GetUserCalibParams_Response) -> bool;
    fn orbbec_camera_msgs__srv__GetUserCalibParams_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetUserCalibParams_Response>, size: usize) -> bool;
    fn orbbec_camera_msgs__srv__GetUserCalibParams_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetUserCalibParams_Response>);
    fn orbbec_camera_msgs__srv__GetUserCalibParams_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetUserCalibParams_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetUserCalibParams_Response>) -> bool;
}

// Corresponds to orbbec_camera_msgs__srv__GetUserCalibParams_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
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
    pub message: rosidl_runtime_rs::String,

}



impl Default for GetUserCalibParams_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !orbbec_camera_msgs__srv__GetUserCalibParams_Response__init(&mut msg as *mut _) {
        panic!("Call to orbbec_camera_msgs__srv__GetUserCalibParams_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetUserCalibParams_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetUserCalibParams_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetUserCalibParams_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__GetUserCalibParams_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetUserCalibParams_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetUserCalibParams_Response where Self: Sized {
  const TYPE_NAME: &'static str = "orbbec_camera_msgs/srv/GetUserCalibParams_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__GetUserCalibParams_Response() }
  }
}


#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__SetUserCalibParams_Request() -> *const std::ffi::c_void;
}

#[link(name = "orbbec_camera_msgs__rosidl_generator_c")]
extern "C" {
    fn orbbec_camera_msgs__srv__SetUserCalibParams_Request__init(msg: *mut SetUserCalibParams_Request) -> bool;
    fn orbbec_camera_msgs__srv__SetUserCalibParams_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetUserCalibParams_Request>, size: usize) -> bool;
    fn orbbec_camera_msgs__srv__SetUserCalibParams_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetUserCalibParams_Request>);
    fn orbbec_camera_msgs__srv__SetUserCalibParams_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetUserCalibParams_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SetUserCalibParams_Request>) -> bool;
}

// Corresponds to orbbec_camera_msgs__srv__SetUserCalibParams_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !orbbec_camera_msgs__srv__SetUserCalibParams_Request__init(&mut msg as *mut _) {
        panic!("Call to orbbec_camera_msgs__srv__SetUserCalibParams_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetUserCalibParams_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetUserCalibParams_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetUserCalibParams_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetUserCalibParams_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetUserCalibParams_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetUserCalibParams_Request where Self: Sized {
  const TYPE_NAME: &'static str = "orbbec_camera_msgs/srv/SetUserCalibParams_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__SetUserCalibParams_Request() }
  }
}


#[link(name = "orbbec_camera_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__SetUserCalibParams_Response() -> *const std::ffi::c_void;
}

#[link(name = "orbbec_camera_msgs__rosidl_generator_c")]
extern "C" {
    fn orbbec_camera_msgs__srv__SetUserCalibParams_Response__init(msg: *mut SetUserCalibParams_Response) -> bool;
    fn orbbec_camera_msgs__srv__SetUserCalibParams_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetUserCalibParams_Response>, size: usize) -> bool;
    fn orbbec_camera_msgs__srv__SetUserCalibParams_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetUserCalibParams_Response>);
    fn orbbec_camera_msgs__srv__SetUserCalibParams_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetUserCalibParams_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SetUserCalibParams_Response>) -> bool;
}

// Corresponds to orbbec_camera_msgs__srv__SetUserCalibParams_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetUserCalibParams_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for SetUserCalibParams_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !orbbec_camera_msgs__srv__SetUserCalibParams_Response__init(&mut msg as *mut _) {
        panic!("Call to orbbec_camera_msgs__srv__SetUserCalibParams_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetUserCalibParams_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetUserCalibParams_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetUserCalibParams_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { orbbec_camera_msgs__srv__SetUserCalibParams_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetUserCalibParams_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetUserCalibParams_Response where Self: Sized {
  const TYPE_NAME: &'static str = "orbbec_camera_msgs/srv/SetUserCalibParams_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__orbbec_camera_msgs__srv__SetUserCalibParams_Response() }
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


