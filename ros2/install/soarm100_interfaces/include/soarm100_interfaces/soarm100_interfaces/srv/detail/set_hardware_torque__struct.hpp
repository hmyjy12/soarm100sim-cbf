// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from soarm100_interfaces:srv/SetHardwareTorque.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__SRV__DETAIL__SET_HARDWARE_TORQUE__STRUCT_HPP_
#define SOARM100_INTERFACES__SRV__DETAIL__SET_HARDWARE_TORQUE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__srv__SetHardwareTorque_Request __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__srv__SetHardwareTorque_Request __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SetHardwareTorque_Request_
{
  using Type = SetHardwareTorque_Request_<ContainerAllocator>;

  explicit SetHardwareTorque_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->enabled = false;
      this->confirmation = "";
    }
  }

  explicit SetHardwareTorque_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : confirmation(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->enabled = false;
      this->confirmation = "";
    }
  }

  // field types and members
  using _enabled_type =
    bool;
  _enabled_type enabled;
  using _confirmation_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _confirmation_type confirmation;

  // setters for named parameter idiom
  Type & set__enabled(
    const bool & _arg)
  {
    this->enabled = _arg;
    return *this;
  }
  Type & set__confirmation(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->confirmation = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    soarm100_interfaces::srv::SetHardwareTorque_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::srv::SetHardwareTorque_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::srv::SetHardwareTorque_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::srv::SetHardwareTorque_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::srv::SetHardwareTorque_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::srv::SetHardwareTorque_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::srv::SetHardwareTorque_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::srv::SetHardwareTorque_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::srv::SetHardwareTorque_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::srv::SetHardwareTorque_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__srv__SetHardwareTorque_Request
    std::shared_ptr<soarm100_interfaces::srv::SetHardwareTorque_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__srv__SetHardwareTorque_Request
    std::shared_ptr<soarm100_interfaces::srv::SetHardwareTorque_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SetHardwareTorque_Request_ & other) const
  {
    if (this->enabled != other.enabled) {
      return false;
    }
    if (this->confirmation != other.confirmation) {
      return false;
    }
    return true;
  }
  bool operator!=(const SetHardwareTorque_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SetHardwareTorque_Request_

// alias to use template instance with default allocator
using SetHardwareTorque_Request =
  soarm100_interfaces::srv::SetHardwareTorque_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace soarm100_interfaces


#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__srv__SetHardwareTorque_Response __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__srv__SetHardwareTorque_Response __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SetHardwareTorque_Response_
{
  using Type = SetHardwareTorque_Response_<ContainerAllocator>;

  explicit SetHardwareTorque_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->reason = "";
    }
  }

  explicit SetHardwareTorque_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : reason(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->reason = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _reason_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _reason_type reason;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__reason(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->reason = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    soarm100_interfaces::srv::SetHardwareTorque_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::srv::SetHardwareTorque_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::srv::SetHardwareTorque_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::srv::SetHardwareTorque_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::srv::SetHardwareTorque_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::srv::SetHardwareTorque_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::srv::SetHardwareTorque_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::srv::SetHardwareTorque_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::srv::SetHardwareTorque_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::srv::SetHardwareTorque_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__srv__SetHardwareTorque_Response
    std::shared_ptr<soarm100_interfaces::srv::SetHardwareTorque_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__srv__SetHardwareTorque_Response
    std::shared_ptr<soarm100_interfaces::srv::SetHardwareTorque_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SetHardwareTorque_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->reason != other.reason) {
      return false;
    }
    return true;
  }
  bool operator!=(const SetHardwareTorque_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SetHardwareTorque_Response_

// alias to use template instance with default allocator
using SetHardwareTorque_Response =
  soarm100_interfaces::srv::SetHardwareTorque_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace soarm100_interfaces

namespace soarm100_interfaces
{

namespace srv
{

struct SetHardwareTorque
{
  using Request = soarm100_interfaces::srv::SetHardwareTorque_Request;
  using Response = soarm100_interfaces::srv::SetHardwareTorque_Response;
};

}  // namespace srv

}  // namespace soarm100_interfaces

#endif  // SOARM100_INTERFACES__SRV__DETAIL__SET_HARDWARE_TORQUE__STRUCT_HPP_
