#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__SegmentTarget_Request() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__srv__SegmentTarget_Request__init(msg: *mut SegmentTarget_Request) -> bool;
    fn soarm100_interfaces__srv__SegmentTarget_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SegmentTarget_Request>, size: usize) -> bool;
    fn soarm100_interfaces__srv__SegmentTarget_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SegmentTarget_Request>);
    fn soarm100_interfaces__srv__SegmentTarget_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SegmentTarget_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SegmentTarget_Request>) -> bool;
}

// Corresponds to soarm100_interfaces__srv__SegmentTarget_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SegmentTarget_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target_prompt: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub force_yolo: bool,

}



impl Default for SegmentTarget_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__srv__SegmentTarget_Request__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__srv__SegmentTarget_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SegmentTarget_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__SegmentTarget_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__SegmentTarget_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__SegmentTarget_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SegmentTarget_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SegmentTarget_Request where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/srv/SegmentTarget_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__SegmentTarget_Request() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__SegmentTarget_Response() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__srv__SegmentTarget_Response__init(msg: *mut SegmentTarget_Response) -> bool;
    fn soarm100_interfaces__srv__SegmentTarget_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SegmentTarget_Response>, size: usize) -> bool;
    fn soarm100_interfaces__srv__SegmentTarget_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SegmentTarget_Response>);
    fn soarm100_interfaces__srv__SegmentTarget_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SegmentTarget_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SegmentTarget_Response>) -> bool;
}

// Corresponds to soarm100_interfaces__srv__SegmentTarget_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SegmentTarget_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_center: geometry_msgs::msg::rmw::PoseStamped,


    // This member is not documented.
    #[allow(missing_docs)]
    pub score: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub bbox_xyxy: [f32; 4],


    // This member is not documented.
    #[allow(missing_docs)]
    pub mask_topic: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub debug_json: rosidl_runtime_rs::String,

}



impl Default for SegmentTarget_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__srv__SegmentTarget_Response__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__srv__SegmentTarget_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SegmentTarget_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__SegmentTarget_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__SegmentTarget_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__SegmentTarget_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SegmentTarget_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SegmentTarget_Response where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/srv/SegmentTarget_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__SegmentTarget_Response() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__SetAvoidance_Request() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__srv__SetAvoidance_Request__init(msg: *mut SetAvoidance_Request) -> bool;
    fn soarm100_interfaces__srv__SetAvoidance_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetAvoidance_Request>, size: usize) -> bool;
    fn soarm100_interfaces__srv__SetAvoidance_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetAvoidance_Request>);
    fn soarm100_interfaces__srv__SetAvoidance_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetAvoidance_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SetAvoidance_Request>) -> bool;
}

// Corresponds to soarm100_interfaces__srv__SetAvoidance_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetAvoidance_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub enabled: bool,

}



impl Default for SetAvoidance_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__srv__SetAvoidance_Request__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__srv__SetAvoidance_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetAvoidance_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__SetAvoidance_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__SetAvoidance_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__SetAvoidance_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetAvoidance_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetAvoidance_Request where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/srv/SetAvoidance_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__SetAvoidance_Request() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__SetAvoidance_Response() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__srv__SetAvoidance_Response__init(msg: *mut SetAvoidance_Response) -> bool;
    fn soarm100_interfaces__srv__SetAvoidance_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetAvoidance_Response>, size: usize) -> bool;
    fn soarm100_interfaces__srv__SetAvoidance_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetAvoidance_Response>);
    fn soarm100_interfaces__srv__SetAvoidance_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetAvoidance_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SetAvoidance_Response>) -> bool;
}

// Corresponds to soarm100_interfaces__srv__SetAvoidance_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetAvoidance_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: rosidl_runtime_rs::String,

}



impl Default for SetAvoidance_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__srv__SetAvoidance_Response__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__srv__SetAvoidance_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetAvoidance_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__SetAvoidance_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__SetAvoidance_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__SetAvoidance_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetAvoidance_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetAvoidance_Response where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/srv/SetAvoidance_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__SetAvoidance_Response() }
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


