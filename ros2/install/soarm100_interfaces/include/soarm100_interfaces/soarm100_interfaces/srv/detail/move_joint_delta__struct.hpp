// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from soarm100_interfaces:srv/MoveJointDelta.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__SRV__DETAIL__MOVE_JOINT_DELTA__STRUCT_HPP_
#define SOARM100_INTERFACES__SRV__DETAIL__MOVE_JOINT_DELTA__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__srv__MoveJointDelta_Request __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__srv__MoveJointDelta_Request __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct MoveJointDelta_Request_
{
  using Type = MoveJointDelta_Request_<ContainerAllocator>;

  explicit MoveJointDelta_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 7>::iterator, double>(this->delta_rad.begin(), this->delta_rad.end(), 0.0);
      this->duration = 0.0;
      this->hold = 0.0;
      this->keep_target = false;
      this->confirmation = "";
    }
  }

  explicit MoveJointDelta_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : delta_rad(_alloc),
    confirmation(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 7>::iterator, double>(this->delta_rad.begin(), this->delta_rad.end(), 0.0);
      this->duration = 0.0;
      this->hold = 0.0;
      this->keep_target = false;
      this->confirmation = "";
    }
  }

  // field types and members
  using _delta_rad_type =
    std::array<double, 7>;
  _delta_rad_type delta_rad;
  using _duration_type =
    double;
  _duration_type duration;
  using _hold_type =
    double;
  _hold_type hold;
  using _keep_target_type =
    bool;
  _keep_target_type keep_target;
  using _confirmation_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _confirmation_type confirmation;

  // setters for named parameter idiom
  Type & set__delta_rad(
    const std::array<double, 7> & _arg)
  {
    this->delta_rad = _arg;
    return *this;
  }
  Type & set__duration(
    const double & _arg)
  {
    this->duration = _arg;
    return *this;
  }
  Type & set__hold(
    const double & _arg)
  {
    this->hold = _arg;
    return *this;
  }
  Type & set__keep_target(
    const bool & _arg)
  {
    this->keep_target = _arg;
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
    soarm100_interfaces::srv::MoveJointDelta_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::srv::MoveJointDelta_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::srv::MoveJointDelta_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::srv::MoveJointDelta_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::srv::MoveJointDelta_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::srv::MoveJointDelta_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::srv::MoveJointDelta_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::srv::MoveJointDelta_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::srv::MoveJointDelta_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::srv::MoveJointDelta_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__srv__MoveJointDelta_Request
    std::shared_ptr<soarm100_interfaces::srv::MoveJointDelta_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__srv__MoveJointDelta_Request
    std::shared_ptr<soarm100_interfaces::srv::MoveJointDelta_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MoveJointDelta_Request_ & other) const
  {
    if (this->delta_rad != other.delta_rad) {
      return false;
    }
    if (this->duration != other.duration) {
      return false;
    }
    if (this->hold != other.hold) {
      return false;
    }
    if (this->keep_target != other.keep_target) {
      return false;
    }
    if (this->confirmation != other.confirmation) {
      return false;
    }
    return true;
  }
  bool operator!=(const MoveJointDelta_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MoveJointDelta_Request_

// alias to use template instance with default allocator
using MoveJointDelta_Request =
  soarm100_interfaces::srv::MoveJointDelta_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace soarm100_interfaces


#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__srv__MoveJointDelta_Response __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__srv__MoveJointDelta_Response __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct MoveJointDelta_Response_
{
  using Type = MoveJointDelta_Response_<ContainerAllocator>;

  explicit MoveJointDelta_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->reason = "";
      this->log_path = "";
    }
  }

  explicit MoveJointDelta_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    soarm100_interfaces::srv::MoveJointDelta_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::srv::MoveJointDelta_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::srv::MoveJointDelta_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::srv::MoveJointDelta_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::srv::MoveJointDelta_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::srv::MoveJointDelta_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::srv::MoveJointDelta_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::srv::MoveJointDelta_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::srv::MoveJointDelta_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::srv::MoveJointDelta_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__srv__MoveJointDelta_Response
    std::shared_ptr<soarm100_interfaces::srv::MoveJointDelta_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__srv__MoveJointDelta_Response
    std::shared_ptr<soarm100_interfaces::srv::MoveJointDelta_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MoveJointDelta_Response_ & other) const
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
  bool operator!=(const MoveJointDelta_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MoveJointDelta_Response_

// alias to use template instance with default allocator
using MoveJointDelta_Response =
  soarm100_interfaces::srv::MoveJointDelta_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace soarm100_interfaces

namespace soarm100_interfaces
{

namespace srv
{

struct MoveJointDelta
{
  using Request = soarm100_interfaces::srv::MoveJointDelta_Request;
  using Response = soarm100_interfaces::srv::MoveJointDelta_Response;
};

}  // namespace srv

}  // namespace soarm100_interfaces

#endif  // SOARM100_INTERFACES__SRV__DETAIL__MOVE_JOINT_DELTA__STRUCT_HPP_
