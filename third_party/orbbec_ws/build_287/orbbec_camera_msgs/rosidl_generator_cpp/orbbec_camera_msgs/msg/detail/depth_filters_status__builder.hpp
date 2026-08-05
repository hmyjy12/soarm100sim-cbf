// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from orbbec_camera_msgs:msg/DepthFiltersStatus.idl
// generated code does not contain a copyright notice

#ifndef ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTERS_STATUS__BUILDER_HPP_
#define ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTERS_STATUS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "orbbec_camera_msgs/msg/detail/depth_filters_status__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace orbbec_camera_msgs
{

namespace msg
{

namespace builder
{

class Init_DepthFiltersStatus_filters
{
public:
  explicit Init_DepthFiltersStatus_filters(::orbbec_camera_msgs::msg::DepthFiltersStatus & msg)
  : msg_(msg)
  {}
  ::orbbec_camera_msgs::msg::DepthFiltersStatus filters(::orbbec_camera_msgs::msg::DepthFiltersStatus::_filters_type arg)
  {
    msg_.filters = std::move(arg);
    return std::move(msg_);
  }

private:
  ::orbbec_camera_msgs::msg::DepthFiltersStatus msg_;
};

class Init_DepthFiltersStatus_header
{
public:
  Init_DepthFiltersStatus_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_DepthFiltersStatus_filters header(::orbbec_camera_msgs::msg::DepthFiltersStatus::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_DepthFiltersStatus_filters(msg_);
  }

private:
  ::orbbec_camera_msgs::msg::DepthFiltersStatus msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::orbbec_camera_msgs::msg::DepthFiltersStatus>()
{
  return orbbec_camera_msgs::msg::builder::Init_DepthFiltersStatus_header();
}

}  // namespace orbbec_camera_msgs

#endif  // ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTERS_STATUS__BUILDER_HPP_
