// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from soarm100_interfaces:msg/TrackedTarget2D.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__MSG__DETAIL__TRACKED_TARGET2_D__BUILDER_HPP_
#define SOARM100_INTERFACES__MSG__DETAIL__TRACKED_TARGET2_D__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "soarm100_interfaces/msg/detail/tracked_target2_d__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace soarm100_interfaces
{

namespace msg
{

namespace builder
{

class Init_TrackedTarget2D_reason
{
public:
  explicit Init_TrackedTarget2D_reason(::soarm100_interfaces::msg::TrackedTarget2D & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::msg::TrackedTarget2D reason(::soarm100_interfaces::msg::TrackedTarget2D::_reason_type arg)
  {
    msg_.reason = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::msg::TrackedTarget2D msg_;
};

class Init_TrackedTarget2D_replan_required
{
public:
  explicit Init_TrackedTarget2D_replan_required(::soarm100_interfaces::msg::TrackedTarget2D & msg)
  : msg_(msg)
  {}
  Init_TrackedTarget2D_reason replan_required(::soarm100_interfaces::msg::TrackedTarget2D::_replan_required_type arg)
  {
    msg_.replan_required = std::move(arg);
    return Init_TrackedTarget2D_reason(msg_);
  }

private:
  ::soarm100_interfaces::msg::TrackedTarget2D msg_;
};

class Init_TrackedTarget2D_lost_frames
{
public:
  explicit Init_TrackedTarget2D_lost_frames(::soarm100_interfaces::msg::TrackedTarget2D & msg)
  : msg_(msg)
  {}
  Init_TrackedTarget2D_replan_required lost_frames(::soarm100_interfaces::msg::TrackedTarget2D::_lost_frames_type arg)
  {
    msg_.lost_frames = std::move(arg);
    return Init_TrackedTarget2D_replan_required(msg_);
  }

private:
  ::soarm100_interfaces::msg::TrackedTarget2D msg_;
};

class Init_TrackedTarget2D_confidence
{
public:
  explicit Init_TrackedTarget2D_confidence(::soarm100_interfaces::msg::TrackedTarget2D & msg)
  : msg_(msg)
  {}
  Init_TrackedTarget2D_lost_frames confidence(::soarm100_interfaces::msg::TrackedTarget2D::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return Init_TrackedTarget2D_lost_frames(msg_);
  }

private:
  ::soarm100_interfaces::msg::TrackedTarget2D msg_;
};

class Init_TrackedTarget2D_image_height
{
public:
  explicit Init_TrackedTarget2D_image_height(::soarm100_interfaces::msg::TrackedTarget2D & msg)
  : msg_(msg)
  {}
  Init_TrackedTarget2D_confidence image_height(::soarm100_interfaces::msg::TrackedTarget2D::_image_height_type arg)
  {
    msg_.image_height = std::move(arg);
    return Init_TrackedTarget2D_confidence(msg_);
  }

private:
  ::soarm100_interfaces::msg::TrackedTarget2D msg_;
};

class Init_TrackedTarget2D_image_width
{
public:
  explicit Init_TrackedTarget2D_image_width(::soarm100_interfaces::msg::TrackedTarget2D & msg)
  : msg_(msg)
  {}
  Init_TrackedTarget2D_image_height image_width(::soarm100_interfaces::msg::TrackedTarget2D::_image_width_type arg)
  {
    msg_.image_width = std::move(arg);
    return Init_TrackedTarget2D_image_height(msg_);
  }

private:
  ::soarm100_interfaces::msg::TrackedTarget2D msg_;
};

class Init_TrackedTarget2D_height
{
public:
  explicit Init_TrackedTarget2D_height(::soarm100_interfaces::msg::TrackedTarget2D & msg)
  : msg_(msg)
  {}
  Init_TrackedTarget2D_image_width height(::soarm100_interfaces::msg::TrackedTarget2D::_height_type arg)
  {
    msg_.height = std::move(arg);
    return Init_TrackedTarget2D_image_width(msg_);
  }

private:
  ::soarm100_interfaces::msg::TrackedTarget2D msg_;
};

class Init_TrackedTarget2D_width
{
public:
  explicit Init_TrackedTarget2D_width(::soarm100_interfaces::msg::TrackedTarget2D & msg)
  : msg_(msg)
  {}
  Init_TrackedTarget2D_height width(::soarm100_interfaces::msg::TrackedTarget2D::_width_type arg)
  {
    msg_.width = std::move(arg);
    return Init_TrackedTarget2D_height(msg_);
  }

private:
  ::soarm100_interfaces::msg::TrackedTarget2D msg_;
};

class Init_TrackedTarget2D_delta_v
{
public:
  explicit Init_TrackedTarget2D_delta_v(::soarm100_interfaces::msg::TrackedTarget2D & msg)
  : msg_(msg)
  {}
  Init_TrackedTarget2D_width delta_v(::soarm100_interfaces::msg::TrackedTarget2D::_delta_v_type arg)
  {
    msg_.delta_v = std::move(arg);
    return Init_TrackedTarget2D_width(msg_);
  }

private:
  ::soarm100_interfaces::msg::TrackedTarget2D msg_;
};

class Init_TrackedTarget2D_delta_u
{
public:
  explicit Init_TrackedTarget2D_delta_u(::soarm100_interfaces::msg::TrackedTarget2D & msg)
  : msg_(msg)
  {}
  Init_TrackedTarget2D_delta_v delta_u(::soarm100_interfaces::msg::TrackedTarget2D::_delta_u_type arg)
  {
    msg_.delta_u = std::move(arg);
    return Init_TrackedTarget2D_delta_v(msg_);
  }

private:
  ::soarm100_interfaces::msg::TrackedTarget2D msg_;
};

class Init_TrackedTarget2D_reference_v
{
public:
  explicit Init_TrackedTarget2D_reference_v(::soarm100_interfaces::msg::TrackedTarget2D & msg)
  : msg_(msg)
  {}
  Init_TrackedTarget2D_delta_u reference_v(::soarm100_interfaces::msg::TrackedTarget2D::_reference_v_type arg)
  {
    msg_.reference_v = std::move(arg);
    return Init_TrackedTarget2D_delta_u(msg_);
  }

private:
  ::soarm100_interfaces::msg::TrackedTarget2D msg_;
};

class Init_TrackedTarget2D_reference_u
{
public:
  explicit Init_TrackedTarget2D_reference_u(::soarm100_interfaces::msg::TrackedTarget2D & msg)
  : msg_(msg)
  {}
  Init_TrackedTarget2D_reference_v reference_u(::soarm100_interfaces::msg::TrackedTarget2D::_reference_u_type arg)
  {
    msg_.reference_u = std::move(arg);
    return Init_TrackedTarget2D_reference_v(msg_);
  }

private:
  ::soarm100_interfaces::msg::TrackedTarget2D msg_;
};

class Init_TrackedTarget2D_v
{
public:
  explicit Init_TrackedTarget2D_v(::soarm100_interfaces::msg::TrackedTarget2D & msg)
  : msg_(msg)
  {}
  Init_TrackedTarget2D_reference_u v(::soarm100_interfaces::msg::TrackedTarget2D::_v_type arg)
  {
    msg_.v = std::move(arg);
    return Init_TrackedTarget2D_reference_u(msg_);
  }

private:
  ::soarm100_interfaces::msg::TrackedTarget2D msg_;
};

class Init_TrackedTarget2D_u
{
public:
  explicit Init_TrackedTarget2D_u(::soarm100_interfaces::msg::TrackedTarget2D & msg)
  : msg_(msg)
  {}
  Init_TrackedTarget2D_v u(::soarm100_interfaces::msg::TrackedTarget2D::_u_type arg)
  {
    msg_.u = std::move(arg);
    return Init_TrackedTarget2D_v(msg_);
  }

private:
  ::soarm100_interfaces::msg::TrackedTarget2D msg_;
};

class Init_TrackedTarget2D_valid
{
public:
  explicit Init_TrackedTarget2D_valid(::soarm100_interfaces::msg::TrackedTarget2D & msg)
  : msg_(msg)
  {}
  Init_TrackedTarget2D_u valid(::soarm100_interfaces::msg::TrackedTarget2D::_valid_type arg)
  {
    msg_.valid = std::move(arg);
    return Init_TrackedTarget2D_u(msg_);
  }

private:
  ::soarm100_interfaces::msg::TrackedTarget2D msg_;
};

class Init_TrackedTarget2D_header
{
public:
  Init_TrackedTarget2D_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TrackedTarget2D_valid header(::soarm100_interfaces::msg::TrackedTarget2D::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_TrackedTarget2D_valid(msg_);
  }

private:
  ::soarm100_interfaces::msg::TrackedTarget2D msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::msg::TrackedTarget2D>()
{
  return soarm100_interfaces::msg::builder::Init_TrackedTarget2D_header();
}

}  // namespace soarm100_interfaces

#endif  // SOARM100_INTERFACES__MSG__DETAIL__TRACKED_TARGET2_D__BUILDER_HPP_
