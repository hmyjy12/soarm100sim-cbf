#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to soarm100_interfaces__msg__TrackedTarget2D

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct TrackedTarget2D {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


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
    pub reason: std::string::String,

}



impl Default for TrackedTarget2D {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::TrackedTarget2D::default())
  }
}

impl rosidl_runtime_rs::Message for TrackedTarget2D {
  type RmwMsg = super::msg::rmw::TrackedTarget2D;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        valid: msg.valid,
        u: msg.u,
        v: msg.v,
        reference_u: msg.reference_u,
        reference_v: msg.reference_v,
        delta_u: msg.delta_u,
        delta_v: msg.delta_v,
        width: msg.width,
        height: msg.height,
        image_width: msg.image_width,
        image_height: msg.image_height,
        confidence: msg.confidence,
        lost_frames: msg.lost_frames,
        replan_required: msg.replan_required,
        reason: msg.reason.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
      valid: msg.valid,
      u: msg.u,
      v: msg.v,
      reference_u: msg.reference_u,
      reference_v: msg.reference_v,
      delta_u: msg.delta_u,
      delta_v: msg.delta_v,
      width: msg.width,
      height: msg.height,
      image_width: msg.image_width,
      image_height: msg.image_height,
      confidence: msg.confidence,
      lost_frames: msg.lost_frames,
      replan_required: msg.replan_required,
        reason: msg.reason.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      valid: msg.valid,
      u: msg.u,
      v: msg.v,
      reference_u: msg.reference_u,
      reference_v: msg.reference_v,
      delta_u: msg.delta_u,
      delta_v: msg.delta_v,
      width: msg.width,
      height: msg.height,
      image_width: msg.image_width,
      image_height: msg.image_height,
      confidence: msg.confidence,
      lost_frames: msg.lost_frames,
      replan_required: msg.replan_required,
      reason: msg.reason.to_string(),
    }
  }
}


