// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from orbbec_camera_msgs:msg/DepthFilterState.idl
// generated code does not contain a copyright notice

#ifndef ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTER_STATE__STRUCT_HPP_
#define ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTER_STATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'params'
#include "orbbec_camera_msgs/msg/detail/depth_filter_param__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__orbbec_camera_msgs__msg__DepthFilterState __attribute__((deprecated))
#else
# define DEPRECATED__orbbec_camera_msgs__msg__DepthFilterState __declspec(deprecated)
#endif

namespace orbbec_camera_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct DepthFilterState_
{
  using Type = DepthFilterState_<ContainerAllocator>;

  explicit DepthFilterState_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->filter_name = "";
      this->enabled = false;
    }
  }

  explicit DepthFilterState_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : filter_name(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->filter_name = "";
      this->enabled = false;
    }
  }

  // field types and members
  using _filter_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _filter_name_type filter_name;
  using _enabled_type =
    bool;
  _enabled_type enabled;
  using _params_type =
    std::vector<orbbec_camera_msgs::msg::DepthFilterParam_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<orbbec_camera_msgs::msg::DepthFilterParam_<ContainerAllocator>>>;
  _params_type params;

  // setters for named parameter idiom
  Type & set__filter_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->filter_name = _arg;
    return *this;
  }
  Type & set__enabled(
    const bool & _arg)
  {
    this->enabled = _arg;
    return *this;
  }
  Type & set__params(
    const std::vector<orbbec_camera_msgs::msg::DepthFilterParam_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<orbbec_camera_msgs::msg::DepthFilterParam_<ContainerAllocator>>> & _arg)
  {
    this->params = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    orbbec_camera_msgs::msg::DepthFilterState_<ContainerAllocator> *;
  using ConstRawPtr =
    const orbbec_camera_msgs::msg::DepthFilterState_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<orbbec_camera_msgs::msg::DepthFilterState_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<orbbec_camera_msgs::msg::DepthFilterState_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      orbbec_camera_msgs::msg::DepthFilterState_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<orbbec_camera_msgs::msg::DepthFilterState_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      orbbec_camera_msgs::msg::DepthFilterState_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<orbbec_camera_msgs::msg::DepthFilterState_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<orbbec_camera_msgs::msg::DepthFilterState_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<orbbec_camera_msgs::msg::DepthFilterState_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__orbbec_camera_msgs__msg__DepthFilterState
    std::shared_ptr<orbbec_camera_msgs::msg::DepthFilterState_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__orbbec_camera_msgs__msg__DepthFilterState
    std::shared_ptr<orbbec_camera_msgs::msg::DepthFilterState_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DepthFilterState_ & other) const
  {
    if (this->filter_name != other.filter_name) {
      return false;
    }
    if (this->enabled != other.enabled) {
      return false;
    }
    if (this->params != other.params) {
      return false;
    }
    return true;
  }
  bool operator!=(const DepthFilterState_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DepthFilterState_

// alias to use template instance with default allocator
using DepthFilterState =
  orbbec_camera_msgs::msg::DepthFilterState_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace orbbec_camera_msgs

#endif  // ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTER_STATE__STRUCT_HPP_
