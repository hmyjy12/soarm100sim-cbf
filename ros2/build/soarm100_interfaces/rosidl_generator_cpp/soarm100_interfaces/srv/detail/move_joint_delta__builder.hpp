// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from soarm100_interfaces:srv/MoveJointDelta.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__SRV__DETAIL__MOVE_JOINT_DELTA__BUILDER_HPP_
#define SOARM100_INTERFACES__SRV__DETAIL__MOVE_JOINT_DELTA__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "soarm100_interfaces/srv/detail/move_joint_delta__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace soarm100_interfaces
{

namespace srv
{

namespace builder
{

class Init_MoveJointDelta_Request_confirmation
{
public:
  explicit Init_MoveJointDelta_Request_confirmation(::soarm100_interfaces::srv::MoveJointDelta_Request & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::srv::MoveJointDelta_Request confirmation(::soarm100_interfaces::srv::MoveJointDelta_Request::_confirmation_type arg)
  {
    msg_.confirmation = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::srv::MoveJointDelta_Request msg_;
};

class Init_MoveJointDelta_Request_keep_target
{
public:
  explicit Init_MoveJointDelta_Request_keep_target(::soarm100_interfaces::srv::MoveJointDelta_Request & msg)
  : msg_(msg)
  {}
  Init_MoveJointDelta_Request_confirmation keep_target(::soarm100_interfaces::srv::MoveJointDelta_Request::_keep_target_type arg)
  {
    msg_.keep_target = std::move(arg);
    return Init_MoveJointDelta_Request_confirmation(msg_);
  }

private:
  ::soarm100_interfaces::srv::MoveJointDelta_Request msg_;
};

class Init_MoveJointDelta_Request_hold
{
public:
  explicit Init_MoveJointDelta_Request_hold(::soarm100_interfaces::srv::MoveJointDelta_Request & msg)
  : msg_(msg)
  {}
  Init_MoveJointDelta_Request_keep_target hold(::soarm100_interfaces::srv::MoveJointDelta_Request::_hold_type arg)
  {
    msg_.hold = std::move(arg);
    return Init_MoveJointDelta_Request_keep_target(msg_);
  }

private:
  ::soarm100_interfaces::srv::MoveJointDelta_Request msg_;
};

class Init_MoveJointDelta_Request_duration
{
public:
  explicit Init_MoveJointDelta_Request_duration(::soarm100_interfaces::srv::MoveJointDelta_Request & msg)
  : msg_(msg)
  {}
  Init_MoveJointDelta_Request_hold duration(::soarm100_interfaces::srv::MoveJointDelta_Request::_duration_type arg)
  {
    msg_.duration = std::move(arg);
    return Init_MoveJointDelta_Request_hold(msg_);
  }

private:
  ::soarm100_interfaces::srv::MoveJointDelta_Request msg_;
};

class Init_MoveJointDelta_Request_delta_rad
{
public:
  Init_MoveJointDelta_Request_delta_rad()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveJointDelta_Request_duration delta_rad(::soarm100_interfaces::srv::MoveJointDelta_Request::_delta_rad_type arg)
  {
    msg_.delta_rad = std::move(arg);
    return Init_MoveJointDelta_Request_duration(msg_);
  }

private:
  ::soarm100_interfaces::srv::MoveJointDelta_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::srv::MoveJointDelta_Request>()
{
  return soarm100_interfaces::srv::builder::Init_MoveJointDelta_Request_delta_rad();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace srv
{

namespace builder
{

class Init_MoveJointDelta_Response_log_path
{
public:
  explicit Init_MoveJointDelta_Response_log_path(::soarm100_interfaces::srv::MoveJointDelta_Response & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::srv::MoveJointDelta_Response log_path(::soarm100_interfaces::srv::MoveJointDelta_Response::_log_path_type arg)
  {
    msg_.log_path = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::srv::MoveJointDelta_Response msg_;
};

class Init_MoveJointDelta_Response_reason
{
public:
  explicit Init_MoveJointDelta_Response_reason(::soarm100_interfaces::srv::MoveJointDelta_Response & msg)
  : msg_(msg)
  {}
  Init_MoveJointDelta_Response_log_path reason(::soarm100_interfaces::srv::MoveJointDelta_Response::_reason_type arg)
  {
    msg_.reason = std::move(arg);
    return Init_MoveJointDelta_Response_log_path(msg_);
  }

private:
  ::soarm100_interfaces::srv::MoveJointDelta_Response msg_;
};

class Init_MoveJointDelta_Response_success
{
public:
  Init_MoveJointDelta_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MoveJointDelta_Response_reason success(::soarm100_interfaces::srv::MoveJointDelta_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_MoveJointDelta_Response_reason(msg_);
  }

private:
  ::soarm100_interfaces::srv::MoveJointDelta_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::srv::MoveJointDelta_Response>()
{
  return soarm100_interfaces::srv::builder::Init_MoveJointDelta_Response_success();
}

}  // namespace soarm100_interfaces

#endif  // SOARM100_INTERFACES__SRV__DETAIL__MOVE_JOINT_DELTA__BUILDER_HPP_
