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
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__MoveSingleJoint_Request() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__srv__MoveSingleJoint_Request__init(msg: *mut MoveSingleJoint_Request) -> bool;
    fn soarm100_interfaces__srv__MoveSingleJoint_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveSingleJoint_Request>, size: usize) -> bool;
    fn soarm100_interfaces__srv__MoveSingleJoint_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveSingleJoint_Request>);
    fn soarm100_interfaces__srv__MoveSingleJoint_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveSingleJoint_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveSingleJoint_Request>) -> bool;
}

// Corresponds to soarm100_interfaces__srv__MoveSingleJoint_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveSingleJoint_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub joint: rosidl_runtime_rs::String,


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
    pub confirmation: rosidl_runtime_rs::String,

}



impl Default for MoveSingleJoint_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__srv__MoveSingleJoint_Request__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__srv__MoveSingleJoint_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveSingleJoint_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveSingleJoint_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveSingleJoint_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveSingleJoint_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveSingleJoint_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveSingleJoint_Request where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/srv/MoveSingleJoint_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__MoveSingleJoint_Request() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__MoveSingleJoint_Response() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__srv__MoveSingleJoint_Response__init(msg: *mut MoveSingleJoint_Response) -> bool;
    fn soarm100_interfaces__srv__MoveSingleJoint_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveSingleJoint_Response>, size: usize) -> bool;
    fn soarm100_interfaces__srv__MoveSingleJoint_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveSingleJoint_Response>);
    fn soarm100_interfaces__srv__MoveSingleJoint_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveSingleJoint_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveSingleJoint_Response>) -> bool;
}

// Corresponds to soarm100_interfaces__srv__MoveSingleJoint_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveSingleJoint_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub log_path: rosidl_runtime_rs::String,

}



impl Default for MoveSingleJoint_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__srv__MoveSingleJoint_Response__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__srv__MoveSingleJoint_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveSingleJoint_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveSingleJoint_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveSingleJoint_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveSingleJoint_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveSingleJoint_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveSingleJoint_Response where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/srv/MoveSingleJoint_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__MoveSingleJoint_Response() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__MoveJointDelta_Request() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__srv__MoveJointDelta_Request__init(msg: *mut MoveJointDelta_Request) -> bool;
    fn soarm100_interfaces__srv__MoveJointDelta_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveJointDelta_Request>, size: usize) -> bool;
    fn soarm100_interfaces__srv__MoveJointDelta_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveJointDelta_Request>);
    fn soarm100_interfaces__srv__MoveJointDelta_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveJointDelta_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveJointDelta_Request>) -> bool;
}

// Corresponds to soarm100_interfaces__srv__MoveJointDelta_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
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
    pub confirmation: rosidl_runtime_rs::String,

}



impl Default for MoveJointDelta_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__srv__MoveJointDelta_Request__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__srv__MoveJointDelta_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveJointDelta_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveJointDelta_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveJointDelta_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveJointDelta_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveJointDelta_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveJointDelta_Request where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/srv/MoveJointDelta_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__MoveJointDelta_Request() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__MoveJointDelta_Response() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__srv__MoveJointDelta_Response__init(msg: *mut MoveJointDelta_Response) -> bool;
    fn soarm100_interfaces__srv__MoveJointDelta_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveJointDelta_Response>, size: usize) -> bool;
    fn soarm100_interfaces__srv__MoveJointDelta_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveJointDelta_Response>);
    fn soarm100_interfaces__srv__MoveJointDelta_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveJointDelta_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveJointDelta_Response>) -> bool;
}

// Corresponds to soarm100_interfaces__srv__MoveJointDelta_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveJointDelta_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub log_path: rosidl_runtime_rs::String,

}



impl Default for MoveJointDelta_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__srv__MoveJointDelta_Response__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__srv__MoveJointDelta_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveJointDelta_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveJointDelta_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveJointDelta_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveJointDelta_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveJointDelta_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveJointDelta_Response where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/srv/MoveJointDelta_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__MoveJointDelta_Response() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__MoveNamedPose_Request() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__srv__MoveNamedPose_Request__init(msg: *mut MoveNamedPose_Request) -> bool;
    fn soarm100_interfaces__srv__MoveNamedPose_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveNamedPose_Request>, size: usize) -> bool;
    fn soarm100_interfaces__srv__MoveNamedPose_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveNamedPose_Request>);
    fn soarm100_interfaces__srv__MoveNamedPose_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveNamedPose_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveNamedPose_Request>) -> bool;
}

// Corresponds to soarm100_interfaces__srv__MoveNamedPose_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveNamedPose_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pose_name: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub duration: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub hold: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub confirmation: rosidl_runtime_rs::String,

}



impl Default for MoveNamedPose_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__srv__MoveNamedPose_Request__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__srv__MoveNamedPose_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveNamedPose_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveNamedPose_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveNamedPose_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveNamedPose_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveNamedPose_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveNamedPose_Request where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/srv/MoveNamedPose_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__MoveNamedPose_Request() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__MoveNamedPose_Response() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__srv__MoveNamedPose_Response__init(msg: *mut MoveNamedPose_Response) -> bool;
    fn soarm100_interfaces__srv__MoveNamedPose_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveNamedPose_Response>, size: usize) -> bool;
    fn soarm100_interfaces__srv__MoveNamedPose_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveNamedPose_Response>);
    fn soarm100_interfaces__srv__MoveNamedPose_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveNamedPose_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveNamedPose_Response>) -> bool;
}

// Corresponds to soarm100_interfaces__srv__MoveNamedPose_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveNamedPose_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub log_path: rosidl_runtime_rs::String,

}



impl Default for MoveNamedPose_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__srv__MoveNamedPose_Response__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__srv__MoveNamedPose_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveNamedPose_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveNamedPose_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveNamedPose_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveNamedPose_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveNamedPose_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveNamedPose_Response where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/srv/MoveNamedPose_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__MoveNamedPose_Response() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__MoveJointTarget_Request() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__srv__MoveJointTarget_Request__init(msg: *mut MoveJointTarget_Request) -> bool;
    fn soarm100_interfaces__srv__MoveJointTarget_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveJointTarget_Request>, size: usize) -> bool;
    fn soarm100_interfaces__srv__MoveJointTarget_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveJointTarget_Request>);
    fn soarm100_interfaces__srv__MoveJointTarget_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveJointTarget_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveJointTarget_Request>) -> bool;
}

// Corresponds to soarm100_interfaces__srv__MoveJointTarget_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
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
    pub confirmation: rosidl_runtime_rs::String,

}



impl Default for MoveJointTarget_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__srv__MoveJointTarget_Request__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__srv__MoveJointTarget_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveJointTarget_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveJointTarget_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveJointTarget_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveJointTarget_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveJointTarget_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveJointTarget_Request where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/srv/MoveJointTarget_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__MoveJointTarget_Request() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__MoveJointTarget_Response() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__srv__MoveJointTarget_Response__init(msg: *mut MoveJointTarget_Response) -> bool;
    fn soarm100_interfaces__srv__MoveJointTarget_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MoveJointTarget_Response>, size: usize) -> bool;
    fn soarm100_interfaces__srv__MoveJointTarget_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MoveJointTarget_Response>);
    fn soarm100_interfaces__srv__MoveJointTarget_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MoveJointTarget_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<MoveJointTarget_Response>) -> bool;
}

// Corresponds to soarm100_interfaces__srv__MoveJointTarget_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MoveJointTarget_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub log_path: rosidl_runtime_rs::String,

}



impl Default for MoveJointTarget_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__srv__MoveJointTarget_Response__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__srv__MoveJointTarget_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MoveJointTarget_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveJointTarget_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveJointTarget_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__MoveJointTarget_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MoveJointTarget_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MoveJointTarget_Response where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/srv/MoveJointTarget_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__MoveJointTarget_Response() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__SetHardwareTorque_Request() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__srv__SetHardwareTorque_Request__init(msg: *mut SetHardwareTorque_Request) -> bool;
    fn soarm100_interfaces__srv__SetHardwareTorque_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetHardwareTorque_Request>, size: usize) -> bool;
    fn soarm100_interfaces__srv__SetHardwareTorque_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetHardwareTorque_Request>);
    fn soarm100_interfaces__srv__SetHardwareTorque_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetHardwareTorque_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SetHardwareTorque_Request>) -> bool;
}

// Corresponds to soarm100_interfaces__srv__SetHardwareTorque_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetHardwareTorque_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub enabled: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub confirmation: rosidl_runtime_rs::String,

}



impl Default for SetHardwareTorque_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__srv__SetHardwareTorque_Request__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__srv__SetHardwareTorque_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetHardwareTorque_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__SetHardwareTorque_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__SetHardwareTorque_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__SetHardwareTorque_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetHardwareTorque_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetHardwareTorque_Request where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/srv/SetHardwareTorque_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__SetHardwareTorque_Request() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__SetHardwareTorque_Response() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__srv__SetHardwareTorque_Response__init(msg: *mut SetHardwareTorque_Response) -> bool;
    fn soarm100_interfaces__srv__SetHardwareTorque_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetHardwareTorque_Response>, size: usize) -> bool;
    fn soarm100_interfaces__srv__SetHardwareTorque_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetHardwareTorque_Response>);
    fn soarm100_interfaces__srv__SetHardwareTorque_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetHardwareTorque_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SetHardwareTorque_Response>) -> bool;
}

// Corresponds to soarm100_interfaces__srv__SetHardwareTorque_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetHardwareTorque_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: rosidl_runtime_rs::String,

}



impl Default for SetHardwareTorque_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__srv__SetHardwareTorque_Response__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__srv__SetHardwareTorque_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetHardwareTorque_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__SetHardwareTorque_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__SetHardwareTorque_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__srv__SetHardwareTorque_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetHardwareTorque_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetHardwareTorque_Response where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/srv/SetHardwareTorque_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__srv__SetHardwareTorque_Response() }
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


