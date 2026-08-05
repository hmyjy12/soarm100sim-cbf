// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from orbbec_camera_msgs:msg/DepthFilterParam.idl
// generated code does not contain a copyright notice

#ifndef ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTER_PARAM__BUILDER_HPP_
#define ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTER_PARAM__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "orbbec_camera_msgs/msg/detail/depth_filter_param__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace orbbec_camera_msgs
{

namespace msg
{

namespace builder
{

class Init_DepthFilterParam_value
{
public:
  explicit Init_DepthFilterParam_value(::orbbec_camera_msgs::msg::DepthFilterParam & msg)
  : msg_(msg)
  {}
  ::orbbec_camera_msgs::msg::DepthFilterParam value(::orbbec_camera_msgs::msg::DepthFilterParam::_value_type arg)
  {
    msg_.value = std::move(arg);
    return std::move(msg_);
  }

private:
  ::orbbec_camera_msgs::msg::DepthFilterParam msg_;
};

class Init_DepthFilterParam_name
{
public:
  Init_DepthFilterParam_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_DepthFilterParam_value name(::orbbec_camera_msgs::msg::DepthFilterParam::_name_type arg)
  {
    msg_.name = std::move(arg);
    return Init_DepthFilterParam_value(msg_);
  }

private:
  ::orbbec_camera_msgs::msg::DepthFilterParam msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::orbbec_camera_msgs::msg::DepthFilterParam>()
{
  return orbbec_camera_msgs::msg::builder::Init_DepthFilterParam_name();
}

}  // namespace orbbec_camera_msgs

#endif  // ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTER_PARAM__BUILDER_HPP_
