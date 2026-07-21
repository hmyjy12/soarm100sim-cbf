// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from soarm100_interfaces:srv/SegmentTarget.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__SRV__DETAIL__SEGMENT_TARGET__BUILDER_HPP_
#define SOARM100_INTERFACES__SRV__DETAIL__SEGMENT_TARGET__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "soarm100_interfaces/srv/detail/segment_target__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace soarm100_interfaces
{

namespace srv
{

namespace builder
{

class Init_SegmentTarget_Request_force_yolo
{
public:
  explicit Init_SegmentTarget_Request_force_yolo(::soarm100_interfaces::srv::SegmentTarget_Request & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::srv::SegmentTarget_Request force_yolo(::soarm100_interfaces::srv::SegmentTarget_Request::_force_yolo_type arg)
  {
    msg_.force_yolo = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::srv::SegmentTarget_Request msg_;
};

class Init_SegmentTarget_Request_target_prompt
{
public:
  Init_SegmentTarget_Request_target_prompt()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SegmentTarget_Request_force_yolo target_prompt(::soarm100_interfaces::srv::SegmentTarget_Request::_target_prompt_type arg)
  {
    msg_.target_prompt = std::move(arg);
    return Init_SegmentTarget_Request_force_yolo(msg_);
  }

private:
  ::soarm100_interfaces::srv::SegmentTarget_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::srv::SegmentTarget_Request>()
{
  return soarm100_interfaces::srv::builder::Init_SegmentTarget_Request_target_prompt();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace srv
{

namespace builder
{

class Init_SegmentTarget_Response_debug_json
{
public:
  explicit Init_SegmentTarget_Response_debug_json(::soarm100_interfaces::srv::SegmentTarget_Response & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::srv::SegmentTarget_Response debug_json(::soarm100_interfaces::srv::SegmentTarget_Response::_debug_json_type arg)
  {
    msg_.debug_json = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::srv::SegmentTarget_Response msg_;
};

class Init_SegmentTarget_Response_mask_topic
{
public:
  explicit Init_SegmentTarget_Response_mask_topic(::soarm100_interfaces::srv::SegmentTarget_Response & msg)
  : msg_(msg)
  {}
  Init_SegmentTarget_Response_debug_json mask_topic(::soarm100_interfaces::srv::SegmentTarget_Response::_mask_topic_type arg)
  {
    msg_.mask_topic = std::move(arg);
    return Init_SegmentTarget_Response_debug_json(msg_);
  }

private:
  ::soarm100_interfaces::srv::SegmentTarget_Response msg_;
};

class Init_SegmentTarget_Response_bbox_xyxy
{
public:
  explicit Init_SegmentTarget_Response_bbox_xyxy(::soarm100_interfaces::srv::SegmentTarget_Response & msg)
  : msg_(msg)
  {}
  Init_SegmentTarget_Response_mask_topic bbox_xyxy(::soarm100_interfaces::srv::SegmentTarget_Response::_bbox_xyxy_type arg)
  {
    msg_.bbox_xyxy = std::move(arg);
    return Init_SegmentTarget_Response_mask_topic(msg_);
  }

private:
  ::soarm100_interfaces::srv::SegmentTarget_Response msg_;
};

class Init_SegmentTarget_Response_score
{
public:
  explicit Init_SegmentTarget_Response_score(::soarm100_interfaces::srv::SegmentTarget_Response & msg)
  : msg_(msg)
  {}
  Init_SegmentTarget_Response_bbox_xyxy score(::soarm100_interfaces::srv::SegmentTarget_Response::_score_type arg)
  {
    msg_.score = std::move(arg);
    return Init_SegmentTarget_Response_bbox_xyxy(msg_);
  }

private:
  ::soarm100_interfaces::srv::SegmentTarget_Response msg_;
};

class Init_SegmentTarget_Response_target_center
{
public:
  explicit Init_SegmentTarget_Response_target_center(::soarm100_interfaces::srv::SegmentTarget_Response & msg)
  : msg_(msg)
  {}
  Init_SegmentTarget_Response_score target_center(::soarm100_interfaces::srv::SegmentTarget_Response::_target_center_type arg)
  {
    msg_.target_center = std::move(arg);
    return Init_SegmentTarget_Response_score(msg_);
  }

private:
  ::soarm100_interfaces::srv::SegmentTarget_Response msg_;
};

class Init_SegmentTarget_Response_reason
{
public:
  explicit Init_SegmentTarget_Response_reason(::soarm100_interfaces::srv::SegmentTarget_Response & msg)
  : msg_(msg)
  {}
  Init_SegmentTarget_Response_target_center reason(::soarm100_interfaces::srv::SegmentTarget_Response::_reason_type arg)
  {
    msg_.reason = std::move(arg);
    return Init_SegmentTarget_Response_target_center(msg_);
  }

private:
  ::soarm100_interfaces::srv::SegmentTarget_Response msg_;
};

class Init_SegmentTarget_Response_success
{
public:
  Init_SegmentTarget_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SegmentTarget_Response_reason success(::soarm100_interfaces::srv::SegmentTarget_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_SegmentTarget_Response_reason(msg_);
  }

private:
  ::soarm100_interfaces::srv::SegmentTarget_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::srv::SegmentTarget_Response>()
{
  return soarm100_interfaces::srv::builder::Init_SegmentTarget_Response_success();
}

}  // namespace soarm100_interfaces

#endif  // SOARM100_INTERFACES__SRV__DETAIL__SEGMENT_TARGET__BUILDER_HPP_
