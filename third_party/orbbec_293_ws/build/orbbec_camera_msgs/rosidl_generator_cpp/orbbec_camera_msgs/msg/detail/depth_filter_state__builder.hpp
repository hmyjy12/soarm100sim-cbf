// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from orbbec_camera_msgs:msg/DepthFilterState.idl
// generated code does not contain a copyright notice

#ifndef ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTER_STATE__BUILDER_HPP_
#define ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTER_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "orbbec_camera_msgs/msg/detail/depth_filter_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace orbbec_camera_msgs
{

namespace msg
{

namespace builder
{

class Init_DepthFilterState_params
{
public:
  explicit Init_DepthFilterState_params(::orbbec_camera_msgs::msg::DepthFilterState & msg)
  : msg_(msg)
  {}
  ::orbbec_camera_msgs::msg::DepthFilterState params(::orbbec_camera_msgs::msg::DepthFilterState::_params_type arg)
  {
    msg_.params = std::move(arg);
    return std::move(msg_);
  }

private:
  ::orbbec_camera_msgs::msg::DepthFilterState msg_;
};

class Init_DepthFilterState_enabled
{
public:
  explicit Init_DepthFilterState_enabled(::orbbec_camera_msgs::msg::DepthFilterState & msg)
  : msg_(msg)
  {}
  Init_DepthFilterState_params enabled(::orbbec_camera_msgs::msg::DepthFilterState::_enabled_type arg)
  {
    msg_.enabled = std::move(arg);
    return Init_DepthFilterState_params(msg_);
  }

private:
  ::orbbec_camera_msgs::msg::DepthFilterState msg_;
};

class Init_DepthFilterState_filter_name
{
public:
  Init_DepthFilterState_filter_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_DepthFilterState_enabled filter_name(::orbbec_camera_msgs::msg::DepthFilterState::_filter_name_type arg)
  {
    msg_.filter_name = std::move(arg);
    return Init_DepthFilterState_enabled(msg_);
  }

private:
  ::orbbec_camera_msgs::msg::DepthFilterState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::orbbec_camera_msgs::msg::DepthFilterState>()
{
  return orbbec_camera_msgs::msg::builder::Init_DepthFilterState_filter_name();
}

}  // namespace orbbec_camera_msgs

#endif  // ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTER_STATE__BUILDER_HPP_
