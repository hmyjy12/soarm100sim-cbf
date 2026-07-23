
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecuteGrasp_Goal() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__ExecuteGrasp_Goal__init(msg: *mut ExecuteGrasp_Goal) -> bool;
    fn soarm100_interfaces__action__ExecuteGrasp_Goal__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_Goal>, size: usize) -> bool;
    fn soarm100_interfaces__action__ExecuteGrasp_Goal__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_Goal>);
    fn soarm100_interfaces__action__ExecuteGrasp_Goal__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteGrasp_Goal>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_Goal>) -> bool;
}

// Corresponds to soarm100_interfaces__action__ExecuteGrasp_Goal
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteGrasp_Goal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target_prompt: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub enable_avoidance: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub approximate_target_pose: geometry_msgs::msg::rmw::PoseStamped,

}



impl Default for ExecuteGrasp_Goal {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__ExecuteGrasp_Goal__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__ExecuteGrasp_Goal__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteGrasp_Goal {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_Goal__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_Goal__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_Goal__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteGrasp_Goal {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteGrasp_Goal where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/ExecuteGrasp_Goal";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecuteGrasp_Goal() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecuteGrasp_Result() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__ExecuteGrasp_Result__init(msg: *mut ExecuteGrasp_Result) -> bool;
    fn soarm100_interfaces__action__ExecuteGrasp_Result__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_Result>, size: usize) -> bool;
    fn soarm100_interfaces__action__ExecuteGrasp_Result__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_Result>);
    fn soarm100_interfaces__action__ExecuteGrasp_Result__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteGrasp_Result>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_Result>) -> bool;
}

// Corresponds to soarm100_interfaces__action__ExecuteGrasp_Result
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteGrasp_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub final_grasp_pose: geometry_msgs::msg::rmw::PoseStamped,


    // This member is not documented.
    #[allow(missing_docs)]
    pub lift_height: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub attempts: u8,

}



impl Default for ExecuteGrasp_Result {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__ExecuteGrasp_Result__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__ExecuteGrasp_Result__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteGrasp_Result {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_Result__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_Result__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_Result__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteGrasp_Result {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteGrasp_Result where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/ExecuteGrasp_Result";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecuteGrasp_Result() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecuteGrasp_Feedback() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__ExecuteGrasp_Feedback__init(msg: *mut ExecuteGrasp_Feedback) -> bool;
    fn soarm100_interfaces__action__ExecuteGrasp_Feedback__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_Feedback>, size: usize) -> bool;
    fn soarm100_interfaces__action__ExecuteGrasp_Feedback__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_Feedback>);
    fn soarm100_interfaces__action__ExecuteGrasp_Feedback__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteGrasp_Feedback>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_Feedback>) -> bool;
}

// Corresponds to soarm100_interfaces__action__ExecuteGrasp_Feedback
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteGrasp_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub stage: rosidl_runtime_rs::String,


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
    pub reason: rosidl_runtime_rs::String,

}



impl Default for ExecuteGrasp_Feedback {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__ExecuteGrasp_Feedback__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__ExecuteGrasp_Feedback__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteGrasp_Feedback {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_Feedback__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_Feedback__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_Feedback__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteGrasp_Feedback {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteGrasp_Feedback where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/ExecuteGrasp_Feedback";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecuteGrasp_Feedback() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecuteGrasp_FeedbackMessage() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__ExecuteGrasp_FeedbackMessage__init(msg: *mut ExecuteGrasp_FeedbackMessage) -> bool;
    fn soarm100_interfaces__action__ExecuteGrasp_FeedbackMessage__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_FeedbackMessage>, size: usize) -> bool;
    fn soarm100_interfaces__action__ExecuteGrasp_FeedbackMessage__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_FeedbackMessage>);
    fn soarm100_interfaces__action__ExecuteGrasp_FeedbackMessage__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteGrasp_FeedbackMessage>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_FeedbackMessage>) -> bool;
}

// Corresponds to soarm100_interfaces__action__ExecuteGrasp_FeedbackMessage
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteGrasp_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::super::action::rmw::ExecuteGrasp_Feedback,

}



impl Default for ExecuteGrasp_FeedbackMessage {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__ExecuteGrasp_FeedbackMessage__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__ExecuteGrasp_FeedbackMessage__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteGrasp_FeedbackMessage {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_FeedbackMessage__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_FeedbackMessage__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_FeedbackMessage__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteGrasp_FeedbackMessage {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteGrasp_FeedbackMessage where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/ExecuteGrasp_FeedbackMessage";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecuteGrasp_FeedbackMessage() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecutePlannedGrasp_Goal() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__ExecutePlannedGrasp_Goal__init(msg: *mut ExecutePlannedGrasp_Goal) -> bool;
    fn soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_Goal>, size: usize) -> bool;
    fn soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_Goal>);
    fn soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_Goal>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_Goal>) -> bool;
}

// Corresponds to soarm100_interfaces__action__ExecutePlannedGrasp_Goal
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecutePlannedGrasp_Goal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pregrasp_pose: geometry_msgs::msg::rmw::PoseStamped,


    // This member is not documented.
    #[allow(missing_docs)]
    pub grasp_pose: geometry_msgs::msg::rmw::PoseStamped,


    // This member is not documented.
    #[allow(missing_docs)]
    pub gripper_width: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub enable_avoidance: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_object: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_pos: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub traj_log: rosidl_runtime_rs::String,

}



impl Default for ExecutePlannedGrasp_Goal {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__ExecutePlannedGrasp_Goal__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__ExecutePlannedGrasp_Goal__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecutePlannedGrasp_Goal {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecutePlannedGrasp_Goal {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecutePlannedGrasp_Goal where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/ExecutePlannedGrasp_Goal";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecutePlannedGrasp_Goal() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecutePlannedGrasp_Result() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__ExecutePlannedGrasp_Result__init(msg: *mut ExecutePlannedGrasp_Result) -> bool;
    fn soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_Result>, size: usize) -> bool;
    fn soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_Result>);
    fn soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_Result>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_Result>) -> bool;
}

// Corresponds to soarm100_interfaces__action__ExecutePlannedGrasp_Result
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecutePlannedGrasp_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub lift_height: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub return_code: u8,

}



impl Default for ExecutePlannedGrasp_Result {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__ExecutePlannedGrasp_Result__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__ExecutePlannedGrasp_Result__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecutePlannedGrasp_Result {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecutePlannedGrasp_Result {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecutePlannedGrasp_Result where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/ExecutePlannedGrasp_Result";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecutePlannedGrasp_Result() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecutePlannedGrasp_Feedback() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__init(msg: *mut ExecutePlannedGrasp_Feedback) -> bool;
    fn soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_Feedback>, size: usize) -> bool;
    fn soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_Feedback>);
    fn soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_Feedback>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_Feedback>) -> bool;
}

// Corresponds to soarm100_interfaces__action__ExecutePlannedGrasp_Feedback
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecutePlannedGrasp_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub stage: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub lift_height: f32,

}



impl Default for ExecutePlannedGrasp_Feedback {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecutePlannedGrasp_Feedback {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecutePlannedGrasp_Feedback {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecutePlannedGrasp_Feedback where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/ExecutePlannedGrasp_Feedback";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecutePlannedGrasp_Feedback() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__init(msg: *mut ExecutePlannedGrasp_FeedbackMessage) -> bool;
    fn soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_FeedbackMessage>, size: usize) -> bool;
    fn soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_FeedbackMessage>);
    fn soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_FeedbackMessage>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_FeedbackMessage>) -> bool;
}

// Corresponds to soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecutePlannedGrasp_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::super::action::rmw::ExecutePlannedGrasp_Feedback,

}



impl Default for ExecutePlannedGrasp_FeedbackMessage {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecutePlannedGrasp_FeedbackMessage {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecutePlannedGrasp_FeedbackMessage {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecutePlannedGrasp_FeedbackMessage where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/ExecutePlannedGrasp_FeedbackMessage";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__PlanGrasp_Goal() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__PlanGrasp_Goal__init(msg: *mut PlanGrasp_Goal) -> bool;
    fn soarm100_interfaces__action__PlanGrasp_Goal__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_Goal>, size: usize) -> bool;
    fn soarm100_interfaces__action__PlanGrasp_Goal__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_Goal>);
    fn soarm100_interfaces__action__PlanGrasp_Goal__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PlanGrasp_Goal>, out_seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_Goal>) -> bool;
}

// Corresponds to soarm100_interfaces__action__PlanGrasp_Goal
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlanGrasp_Goal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target_prompt: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub approximate_target_pose: geometry_msgs::msg::rmw::PoseStamped,


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_cloud: sensor_msgs::msg::rmw::PointCloud2,


    // This member is not documented.
    #[allow(missing_docs)]
    pub top_k: u16,

}



impl Default for PlanGrasp_Goal {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__PlanGrasp_Goal__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__PlanGrasp_Goal__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PlanGrasp_Goal {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_Goal__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_Goal__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_Goal__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PlanGrasp_Goal {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PlanGrasp_Goal where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/PlanGrasp_Goal";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__PlanGrasp_Goal() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__PlanGrasp_Result() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__PlanGrasp_Result__init(msg: *mut PlanGrasp_Result) -> bool;
    fn soarm100_interfaces__action__PlanGrasp_Result__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_Result>, size: usize) -> bool;
    fn soarm100_interfaces__action__PlanGrasp_Result__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_Result>);
    fn soarm100_interfaces__action__PlanGrasp_Result__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PlanGrasp_Result>, out_seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_Result>) -> bool;
}

// Corresponds to soarm100_interfaces__action__PlanGrasp_Result
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlanGrasp_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub selected_grasp_pose: geometry_msgs::msg::rmw::PoseStamped,


    // This member is not documented.
    #[allow(missing_docs)]
    pub selected_pregrasp_pose: geometry_msgs::msg::rmw::PoseStamped,


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
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__PlanGrasp_Result__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__PlanGrasp_Result__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PlanGrasp_Result {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_Result__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_Result__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_Result__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PlanGrasp_Result {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PlanGrasp_Result where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/PlanGrasp_Result";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__PlanGrasp_Result() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__PlanGrasp_Feedback() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__PlanGrasp_Feedback__init(msg: *mut PlanGrasp_Feedback) -> bool;
    fn soarm100_interfaces__action__PlanGrasp_Feedback__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_Feedback>, size: usize) -> bool;
    fn soarm100_interfaces__action__PlanGrasp_Feedback__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_Feedback>);
    fn soarm100_interfaces__action__PlanGrasp_Feedback__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PlanGrasp_Feedback>, out_seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_Feedback>) -> bool;
}

// Corresponds to soarm100_interfaces__action__PlanGrasp_Feedback
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlanGrasp_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub stage: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub candidate_count: u16,


    // This member is not documented.
    #[allow(missing_docs)]
    pub best_score: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: rosidl_runtime_rs::String,

}



impl Default for PlanGrasp_Feedback {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__PlanGrasp_Feedback__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__PlanGrasp_Feedback__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PlanGrasp_Feedback {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_Feedback__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_Feedback__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_Feedback__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PlanGrasp_Feedback {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PlanGrasp_Feedback where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/PlanGrasp_Feedback";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__PlanGrasp_Feedback() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__PlanGrasp_FeedbackMessage() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__PlanGrasp_FeedbackMessage__init(msg: *mut PlanGrasp_FeedbackMessage) -> bool;
    fn soarm100_interfaces__action__PlanGrasp_FeedbackMessage__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_FeedbackMessage>, size: usize) -> bool;
    fn soarm100_interfaces__action__PlanGrasp_FeedbackMessage__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_FeedbackMessage>);
    fn soarm100_interfaces__action__PlanGrasp_FeedbackMessage__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PlanGrasp_FeedbackMessage>, out_seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_FeedbackMessage>) -> bool;
}

// Corresponds to soarm100_interfaces__action__PlanGrasp_FeedbackMessage
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlanGrasp_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::super::action::rmw::PlanGrasp_Feedback,

}



impl Default for PlanGrasp_FeedbackMessage {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__PlanGrasp_FeedbackMessage__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__PlanGrasp_FeedbackMessage__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PlanGrasp_FeedbackMessage {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_FeedbackMessage__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_FeedbackMessage__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_FeedbackMessage__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PlanGrasp_FeedbackMessage {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PlanGrasp_FeedbackMessage where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/PlanGrasp_FeedbackMessage";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__PlanGrasp_FeedbackMessage() }
  }
}




#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecuteGrasp_SendGoal_Request() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__ExecuteGrasp_SendGoal_Request__init(msg: *mut ExecuteGrasp_SendGoal_Request) -> bool;
    fn soarm100_interfaces__action__ExecuteGrasp_SendGoal_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_SendGoal_Request>, size: usize) -> bool;
    fn soarm100_interfaces__action__ExecuteGrasp_SendGoal_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_SendGoal_Request>);
    fn soarm100_interfaces__action__ExecuteGrasp_SendGoal_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteGrasp_SendGoal_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_SendGoal_Request>) -> bool;
}

// Corresponds to soarm100_interfaces__action__ExecuteGrasp_SendGoal_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteGrasp_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::super::action::rmw::ExecuteGrasp_Goal,

}



impl Default for ExecuteGrasp_SendGoal_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__ExecuteGrasp_SendGoal_Request__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__ExecuteGrasp_SendGoal_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteGrasp_SendGoal_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_SendGoal_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_SendGoal_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_SendGoal_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteGrasp_SendGoal_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteGrasp_SendGoal_Request where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/ExecuteGrasp_SendGoal_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecuteGrasp_SendGoal_Request() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecuteGrasp_SendGoal_Response() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__ExecuteGrasp_SendGoal_Response__init(msg: *mut ExecuteGrasp_SendGoal_Response) -> bool;
    fn soarm100_interfaces__action__ExecuteGrasp_SendGoal_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_SendGoal_Response>, size: usize) -> bool;
    fn soarm100_interfaces__action__ExecuteGrasp_SendGoal_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_SendGoal_Response>);
    fn soarm100_interfaces__action__ExecuteGrasp_SendGoal_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteGrasp_SendGoal_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_SendGoal_Response>) -> bool;
}

// Corresponds to soarm100_interfaces__action__ExecuteGrasp_SendGoal_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteGrasp_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,

}



impl Default for ExecuteGrasp_SendGoal_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__ExecuteGrasp_SendGoal_Response__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__ExecuteGrasp_SendGoal_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteGrasp_SendGoal_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_SendGoal_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_SendGoal_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_SendGoal_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteGrasp_SendGoal_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteGrasp_SendGoal_Response where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/ExecuteGrasp_SendGoal_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecuteGrasp_SendGoal_Response() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecuteGrasp_GetResult_Request() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__ExecuteGrasp_GetResult_Request__init(msg: *mut ExecuteGrasp_GetResult_Request) -> bool;
    fn soarm100_interfaces__action__ExecuteGrasp_GetResult_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_GetResult_Request>, size: usize) -> bool;
    fn soarm100_interfaces__action__ExecuteGrasp_GetResult_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_GetResult_Request>);
    fn soarm100_interfaces__action__ExecuteGrasp_GetResult_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteGrasp_GetResult_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_GetResult_Request>) -> bool;
}

// Corresponds to soarm100_interfaces__action__ExecuteGrasp_GetResult_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteGrasp_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,

}



impl Default for ExecuteGrasp_GetResult_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__ExecuteGrasp_GetResult_Request__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__ExecuteGrasp_GetResult_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteGrasp_GetResult_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_GetResult_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_GetResult_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_GetResult_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteGrasp_GetResult_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteGrasp_GetResult_Request where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/ExecuteGrasp_GetResult_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecuteGrasp_GetResult_Request() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecuteGrasp_GetResult_Response() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__ExecuteGrasp_GetResult_Response__init(msg: *mut ExecuteGrasp_GetResult_Response) -> bool;
    fn soarm100_interfaces__action__ExecuteGrasp_GetResult_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_GetResult_Response>, size: usize) -> bool;
    fn soarm100_interfaces__action__ExecuteGrasp_GetResult_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_GetResult_Response>);
    fn soarm100_interfaces__action__ExecuteGrasp_GetResult_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecuteGrasp_GetResult_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecuteGrasp_GetResult_Response>) -> bool;
}

// Corresponds to soarm100_interfaces__action__ExecuteGrasp_GetResult_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecuteGrasp_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::super::action::rmw::ExecuteGrasp_Result,

}



impl Default for ExecuteGrasp_GetResult_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__ExecuteGrasp_GetResult_Response__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__ExecuteGrasp_GetResult_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecuteGrasp_GetResult_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_GetResult_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_GetResult_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecuteGrasp_GetResult_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecuteGrasp_GetResult_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecuteGrasp_GetResult_Response where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/ExecuteGrasp_GetResult_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecuteGrasp_GetResult_Response() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__init(msg: *mut ExecutePlannedGrasp_SendGoal_Request) -> bool;
    fn soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_SendGoal_Request>, size: usize) -> bool;
    fn soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_SendGoal_Request>);
    fn soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_SendGoal_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_SendGoal_Request>) -> bool;
}

// Corresponds to soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecutePlannedGrasp_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::super::action::rmw::ExecutePlannedGrasp_Goal,

}



impl Default for ExecutePlannedGrasp_SendGoal_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecutePlannedGrasp_SendGoal_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecutePlannedGrasp_SendGoal_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecutePlannedGrasp_SendGoal_Request where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/ExecutePlannedGrasp_SendGoal_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__init(msg: *mut ExecutePlannedGrasp_SendGoal_Response) -> bool;
    fn soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_SendGoal_Response>, size: usize) -> bool;
    fn soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_SendGoal_Response>);
    fn soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_SendGoal_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_SendGoal_Response>) -> bool;
}

// Corresponds to soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecutePlannedGrasp_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,

}



impl Default for ExecutePlannedGrasp_SendGoal_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecutePlannedGrasp_SendGoal_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecutePlannedGrasp_SendGoal_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecutePlannedGrasp_SendGoal_Response where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/ExecutePlannedGrasp_SendGoal_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__init(msg: *mut ExecutePlannedGrasp_GetResult_Request) -> bool;
    fn soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_GetResult_Request>, size: usize) -> bool;
    fn soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_GetResult_Request>);
    fn soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_GetResult_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_GetResult_Request>) -> bool;
}

// Corresponds to soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecutePlannedGrasp_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,

}



impl Default for ExecutePlannedGrasp_GetResult_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecutePlannedGrasp_GetResult_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecutePlannedGrasp_GetResult_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecutePlannedGrasp_GetResult_Request where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/ExecutePlannedGrasp_GetResult_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__init(msg: *mut ExecutePlannedGrasp_GetResult_Response) -> bool;
    fn soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_GetResult_Response>, size: usize) -> bool;
    fn soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_GetResult_Response>);
    fn soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_GetResult_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<ExecutePlannedGrasp_GetResult_Response>) -> bool;
}

// Corresponds to soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ExecutePlannedGrasp_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::super::action::rmw::ExecutePlannedGrasp_Result,

}



impl Default for ExecutePlannedGrasp_GetResult_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ExecutePlannedGrasp_GetResult_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ExecutePlannedGrasp_GetResult_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ExecutePlannedGrasp_GetResult_Response where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/ExecutePlannedGrasp_GetResult_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__PlanGrasp_SendGoal_Request() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__PlanGrasp_SendGoal_Request__init(msg: *mut PlanGrasp_SendGoal_Request) -> bool;
    fn soarm100_interfaces__action__PlanGrasp_SendGoal_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_SendGoal_Request>, size: usize) -> bool;
    fn soarm100_interfaces__action__PlanGrasp_SendGoal_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_SendGoal_Request>);
    fn soarm100_interfaces__action__PlanGrasp_SendGoal_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PlanGrasp_SendGoal_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_SendGoal_Request>) -> bool;
}

// Corresponds to soarm100_interfaces__action__PlanGrasp_SendGoal_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlanGrasp_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::super::action::rmw::PlanGrasp_Goal,

}



impl Default for PlanGrasp_SendGoal_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__PlanGrasp_SendGoal_Request__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__PlanGrasp_SendGoal_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PlanGrasp_SendGoal_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_SendGoal_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_SendGoal_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_SendGoal_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PlanGrasp_SendGoal_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PlanGrasp_SendGoal_Request where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/PlanGrasp_SendGoal_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__PlanGrasp_SendGoal_Request() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__PlanGrasp_SendGoal_Response() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__PlanGrasp_SendGoal_Response__init(msg: *mut PlanGrasp_SendGoal_Response) -> bool;
    fn soarm100_interfaces__action__PlanGrasp_SendGoal_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_SendGoal_Response>, size: usize) -> bool;
    fn soarm100_interfaces__action__PlanGrasp_SendGoal_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_SendGoal_Response>);
    fn soarm100_interfaces__action__PlanGrasp_SendGoal_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PlanGrasp_SendGoal_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_SendGoal_Response>) -> bool;
}

// Corresponds to soarm100_interfaces__action__PlanGrasp_SendGoal_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlanGrasp_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,

}



impl Default for PlanGrasp_SendGoal_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__PlanGrasp_SendGoal_Response__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__PlanGrasp_SendGoal_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PlanGrasp_SendGoal_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_SendGoal_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_SendGoal_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_SendGoal_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PlanGrasp_SendGoal_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PlanGrasp_SendGoal_Response where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/PlanGrasp_SendGoal_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__PlanGrasp_SendGoal_Response() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__PlanGrasp_GetResult_Request() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__PlanGrasp_GetResult_Request__init(msg: *mut PlanGrasp_GetResult_Request) -> bool;
    fn soarm100_interfaces__action__PlanGrasp_GetResult_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_GetResult_Request>, size: usize) -> bool;
    fn soarm100_interfaces__action__PlanGrasp_GetResult_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_GetResult_Request>);
    fn soarm100_interfaces__action__PlanGrasp_GetResult_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PlanGrasp_GetResult_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_GetResult_Request>) -> bool;
}

// Corresponds to soarm100_interfaces__action__PlanGrasp_GetResult_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlanGrasp_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,

}



impl Default for PlanGrasp_GetResult_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__PlanGrasp_GetResult_Request__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__PlanGrasp_GetResult_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PlanGrasp_GetResult_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_GetResult_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_GetResult_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_GetResult_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PlanGrasp_GetResult_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PlanGrasp_GetResult_Request where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/PlanGrasp_GetResult_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__PlanGrasp_GetResult_Request() }
  }
}


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__PlanGrasp_GetResult_Response() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__action__PlanGrasp_GetResult_Response__init(msg: *mut PlanGrasp_GetResult_Response) -> bool;
    fn soarm100_interfaces__action__PlanGrasp_GetResult_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_GetResult_Response>, size: usize) -> bool;
    fn soarm100_interfaces__action__PlanGrasp_GetResult_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_GetResult_Response>);
    fn soarm100_interfaces__action__PlanGrasp_GetResult_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PlanGrasp_GetResult_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<PlanGrasp_GetResult_Response>) -> bool;
}

// Corresponds to soarm100_interfaces__action__PlanGrasp_GetResult_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PlanGrasp_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::super::action::rmw::PlanGrasp_Result,

}



impl Default for PlanGrasp_GetResult_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__action__PlanGrasp_GetResult_Response__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__action__PlanGrasp_GetResult_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PlanGrasp_GetResult_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_GetResult_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_GetResult_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__action__PlanGrasp_GetResult_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PlanGrasp_GetResult_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PlanGrasp_GetResult_Response where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/action/PlanGrasp_GetResult_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__action__PlanGrasp_GetResult_Response() }
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


