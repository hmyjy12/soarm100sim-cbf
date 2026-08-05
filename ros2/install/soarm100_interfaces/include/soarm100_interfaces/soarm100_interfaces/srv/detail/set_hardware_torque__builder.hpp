// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from soarm100_interfaces:srv/SetHardwareTorque.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__SRV__DETAIL__SET_HARDWARE_TORQUE__BUILDER_HPP_
#define SOARM100_INTERFACES__SRV__DETAIL__SET_HARDWARE_TORQUE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "soarm100_interfaces/srv/detail/set_hardware_torque__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace soarm100_interfaces
{

namespace srv
{

namespace builder
{

class Init_SetHardwareTorque_Request_confirmation
{
public:
  explicit Init_SetHardwareTorque_Request_confirmation(::soarm100_interfaces::srv::SetHardwareTorque_Request & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::srv::SetHardwareTorque_Request confirmation(::soarm100_interfaces::srv::SetHardwareTorque_Request::_confirmation_type arg)
  {
    msg_.confirmation = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::srv::SetHardwareTorque_Request msg_;
};

class Init_SetHardwareTorque_Request_enabled
{
public:
  Init_SetHardwareTorque_Request_enabled()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetHardwareTorque_Request_confirmation enabled(::soarm100_interfaces::srv::SetHardwareTorque_Request::_enabled_type arg)
  {
    msg_.enabled = std::move(arg);
    return Init_SetHardwareTorque_Request_confirmation(msg_);
  }

private:
  ::soarm100_interfaces::srv::SetHardwareTorque_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::srv::SetHardwareTorque_Request>()
{
  return soarm100_interfaces::srv::builder::Init_SetHardwareTorque_Request_enabled();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace srv
{

namespace builder
{

class Init_SetHardwareTorque_Response_reason
{
public:
  explicit Init_SetHardwareTorque_Response_reason(::soarm100_interfaces::srv::SetHardwareTorque_Response & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::srv::SetHardwareTorque_Response reason(::soarm100_interfaces::srv::SetHardwareTorque_Response::_reason_type arg)
  {
    msg_.reason = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::srv::SetHardwareTorque_Response msg_;
};

class Init_SetHardwareTorque_Response_success
{
public:
  Init_SetHardwareTorque_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SetHardwareTorque_Response_reason success(::soarm100_interfaces::srv::SetHardwareTorque_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_SetHardwareTorque_Response_reason(msg_);
  }

private:
  ::soarm100_interfaces::srv::SetHardwareTorque_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::srv::SetHardwareTorque_Response>()
{
  return soarm100_interfaces::srv::builder::Init_SetHardwareTorque_Response_success();
}

}  // namespace soarm100_interfaces

#endif  // SOARM100_INTERFACES__SRV__DETAIL__SET_HARDWARE_TORQUE__BUILDER_HPP_
