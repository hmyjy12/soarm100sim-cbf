// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from soarm100_interfaces:srv/MoveJointTarget.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__SRV__DETAIL__MOVE_JOINT_TARGET__STRUCT_HPP_
#define SOARM100_INTERFACES__SRV__DETAIL__MOVE_JOINT_TARGET__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__srv__MoveJointTarget_Request __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__srv__MoveJointTarget_Request __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct MoveJointTarget_Request_
{
  using Type = MoveJointTarget_Request_<ContainerAllocator>;

  explicit MoveJointTarget_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 7>::iterator, double>(this->position_rad.begin(), this->position_rad.end(), 0.0);
      this->duration = 0.0;
      this->confirmation = "";
    }
  }

  explicit MoveJointTarget_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : position_rad(_alloc),
    confirmation(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 7>::iterator, double>(this->position_rad.begin(), this->position_rad.end(), 0.0);
      this->duration = 0.0;
      this->confirmation = "";
    }
  }

  // field types and members
  using _position_rad_type =
    std::array<double, 7>;
  _position_rad_type position_rad;
  using _duration_type =
    double;
  _duration_type duration;
  using _confirmation_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _confirmation_type confirmation;

  // setters for named parameter idiom
  Type & set__position_rad(
    const std::array<double, 7> & _arg)
  {
    this->position_rad = _arg;
    return *this;
  }
  Type & set__duration(
    const double & _arg)
  {
    this->duration = _arg;
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
    soarm100_interfaces::srv::MoveJointTarget_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::srv::MoveJointTarget_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::srv::MoveJointTarget_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::srv::MoveJointTarget_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::srv::MoveJointTarget_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::srv::MoveJointTarget_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::srv::MoveJointTarget_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::srv::MoveJointTarget_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::srv::MoveJointTarget_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::srv::MoveJointTarget_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__srv__MoveJointTarget_Request
    std::shared_ptr<soarm100_interfaces::srv::MoveJointTarget_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__srv__MoveJointTarget_Request
    std::shared_ptr<soarm100_interfaces::srv::MoveJointTarget_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MoveJointTarget_Request_ & other) const
  {
    if (this->position_rad != other.position_rad) {
      return false;
    }
    if (this->duration != other.duration) {
      return false;
    }
    if (this->confirmation != other.confirmation) {
      return false;
    }
    return true;
  }
  bool operator!=(const MoveJointTarget_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MoveJointTarget_Request_

// alias to use template instance with default allocator
using MoveJointTarget_Request =
  soarm100_interfaces::srv::MoveJointTarget_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace soarm100_interfaces


#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__srv__MoveJointTarget_Response __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__srv__MoveJointTarget_Response __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct MoveJointTarget_Response_
{
  using Type = MoveJointTarget_Response_<ContainerAllocator>;

  explicit MoveJointTarget_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->reason = "";
      this->log_path = "";
    }
  }

  explicit MoveJointTarget_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : reason(_alloc),
    log_path(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->reason = "";
      this->log_path = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _reason_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _reason_type reason;
  using _log_path_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _log_path_type log_path;

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
  Type & set__log_path(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->log_path = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    soarm100_interfaces::srv::MoveJointTarget_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::srv::MoveJointTarget_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::srv::MoveJointTarget_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::srv::MoveJointTarget_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::srv::MoveJointTarget_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::srv::MoveJointTarget_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::srv::MoveJointTarget_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::srv::MoveJointTarget_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::srv::MoveJointTarget_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::srv::MoveJointTarget_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__srv__MoveJointTarget_Response
    std::shared_ptr<soarm100_interfaces::srv::MoveJointTarget_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__srv__MoveJointTarget_Response
    std::shared_ptr<soarm100_interfaces::srv::MoveJointTarget_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MoveJointTarget_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->reason != other.reason) {
      return false;
    }
    if (this->log_path != other.log_path) {
      return false;
    }
    return true;
  }
  bool operator!=(const MoveJointTarget_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MoveJointTarget_Response_

// alias to use template instance with default allocator
using MoveJointTarget_Response =
  soarm100_interfaces::srv::MoveJointTarget_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace soarm100_interfaces

namespace soarm100_interfaces
{

namespace srv
{

struct MoveJointTarget
{
  using Request = soarm100_interfaces::srv::MoveJointTarget_Request;
  using Response = soarm100_interfaces::srv::MoveJointTarget_Response;
};

}  // namespace srv

}  // namespace soarm100_interfaces

#endif  // SOARM100_INTERFACES__SRV__DETAIL__MOVE_JOINT_TARGET__STRUCT_HPP_
