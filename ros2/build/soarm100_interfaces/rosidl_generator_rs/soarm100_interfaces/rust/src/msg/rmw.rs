#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "soarm100_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__msg__TrackedTarget2D() -> *const std::ffi::c_void;
}

#[link(name = "soarm100_interfaces__rosidl_generator_c")]
extern "C" {
    fn soarm100_interfaces__msg__TrackedTarget2D__init(msg: *mut TrackedTarget2D) -> bool;
    fn soarm100_interfaces__msg__TrackedTarget2D__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<TrackedTarget2D>, size: usize) -> bool;
    fn soarm100_interfaces__msg__TrackedTarget2D__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<TrackedTarget2D>);
    fn soarm100_interfaces__msg__TrackedTarget2D__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<TrackedTarget2D>, out_seq: *mut rosidl_runtime_rs::Sequence<TrackedTarget2D>) -> bool;
}

// Corresponds to soarm100_interfaces__msg__TrackedTarget2D
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct TrackedTarget2D {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub valid: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub u: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub v: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reference_u: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reference_v: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub delta_u: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub delta_v: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub width: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub height: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub image_width: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub image_height: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub confidence: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub lost_frames: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub replan_required: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub reason: rosidl_runtime_rs::String,

}



impl Default for TrackedTarget2D {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !soarm100_interfaces__msg__TrackedTarget2D__init(&mut msg as *mut _) {
        panic!("Call to soarm100_interfaces__msg__TrackedTarget2D__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for TrackedTarget2D {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__msg__TrackedTarget2D__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__msg__TrackedTarget2D__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { soarm100_interfaces__msg__TrackedTarget2D__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for TrackedTarget2D {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for TrackedTarget2D where Self: Sized {
  const TYPE_NAME: &'static str = "soarm100_interfaces/msg/TrackedTarget2D";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__soarm100_interfaces__msg__TrackedTarget2D() }
  }
}


