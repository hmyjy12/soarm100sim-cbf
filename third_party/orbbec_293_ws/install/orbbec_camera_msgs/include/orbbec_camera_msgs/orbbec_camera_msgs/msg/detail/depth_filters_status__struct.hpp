// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from orbbec_camera_msgs:msg/DepthFiltersStatus.idl
// generated code does not contain a copyright notice

#ifndef ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTERS_STATUS__STRUCT_HPP_
#define ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTERS_STATUS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"
// Member 'filters'
#include "orbbec_camera_msgs/msg/detail/depth_filter_state__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__orbbec_camera_msgs__msg__DepthFiltersStatus __attribute__((deprecated))
#else
# define DEPRECATED__orbbec_camera_msgs__msg__DepthFiltersStatus __declspec(deprecated)
#endif

namespace orbbec_camera_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct DepthFiltersStatus_
{
  using Type = DepthFiltersStatus_<ContainerAllocator>;

  explicit DepthFiltersStatus_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    (void)_init;
  }

  explicit DepthFiltersStatus_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _filters_type =
    std::vector<orbbec_camera_msgs::msg::DepthFilterState_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<orbbec_camera_msgs::msg::DepthFilterState_<ContainerAllocator>>>;
  _filters_type filters;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__filters(
    const std::vector<orbbec_camera_msgs::msg::DepthFilterState_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<orbbec_camera_msgs::msg::DepthFilterState_<ContainerAllocator>>> & _arg)
  {
    this->filters = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    orbbec_camera_msgs::msg::DepthFiltersStatus_<ContainerAllocator> *;
  using ConstRawPtr =
    const orbbec_camera_msgs::msg::DepthFiltersStatus_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<orbbec_camera_msgs::msg::DepthFiltersStatus_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<orbbec_camera_msgs::msg::DepthFiltersStatus_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      orbbec_camera_msgs::msg::DepthFiltersStatus_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<orbbec_camera_msgs::msg::DepthFiltersStatus_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      orbbec_camera_msgs::msg::DepthFiltersStatus_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<orbbec_camera_msgs::msg::DepthFiltersStatus_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<orbbec_camera_msgs::msg::DepthFiltersStatus_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<orbbec_camera_msgs::msg::DepthFiltersStatus_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__orbbec_camera_msgs__msg__DepthFiltersStatus
    std::shared_ptr<orbbec_camera_msgs::msg::DepthFiltersStatus_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__orbbec_camera_msgs__msg__DepthFiltersStatus
    std::shared_ptr<orbbec_camera_msgs::msg::DepthFiltersStatus_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DepthFiltersStatus_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->filters != other.filters) {
      return false;
    }
    return true;
  }
  bool operator!=(const DepthFiltersStatus_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DepthFiltersStatus_

// alias to use template instance with default allocator
using DepthFiltersStatus =
  orbbec_camera_msgs::msg::DepthFiltersStatus_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace orbbec_camera_msgs

#endif  // ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTERS_STATUS__STRUCT_HPP_
