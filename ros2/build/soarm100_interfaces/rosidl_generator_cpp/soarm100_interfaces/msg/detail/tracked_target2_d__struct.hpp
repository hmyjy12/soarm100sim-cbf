// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from soarm100_interfaces:msg/TrackedTarget2D.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__MSG__DETAIL__TRACKED_TARGET2_D__STRUCT_HPP_
#define SOARM100_INTERFACES__MSG__DETAIL__TRACKED_TARGET2_D__STRUCT_HPP_

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

#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__msg__TrackedTarget2D __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__msg__TrackedTarget2D __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct TrackedTarget2D_
{
  using Type = TrackedTarget2D_<ContainerAllocator>;

  explicit TrackedTarget2D_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->valid = false;
      this->u = 0.0f;
      this->v = 0.0f;
      this->reference_u = 0.0f;
      this->reference_v = 0.0f;
      this->delta_u = 0.0f;
      this->delta_v = 0.0f;
      this->width = 0.0f;
      this->height = 0.0f;
      this->image_width = 0ul;
      this->image_height = 0ul;
      this->confidence = 0.0f;
      this->lost_frames = 0ul;
      this->replan_required = false;
      this->reason = "";
    }
  }

  explicit TrackedTarget2D_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    reason(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->valid = false;
      this->u = 0.0f;
      this->v = 0.0f;
      this->reference_u = 0.0f;
      this->reference_v = 0.0f;
      this->delta_u = 0.0f;
      this->delta_v = 0.0f;
      this->width = 0.0f;
      this->height = 0.0f;
      this->image_width = 0ul;
      this->image_height = 0ul;
      this->confidence = 0.0f;
      this->lost_frames = 0ul;
      this->replan_required = false;
      this->reason = "";
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _valid_type =
    bool;
  _valid_type valid;
  using _u_type =
    float;
  _u_type u;
  using _v_type =
    float;
  _v_type v;
  using _reference_u_type =
    float;
  _reference_u_type reference_u;
  using _reference_v_type =
    float;
  _reference_v_type reference_v;
  using _delta_u_type =
    float;
  _delta_u_type delta_u;
  using _delta_v_type =
    float;
  _delta_v_type delta_v;
  using _width_type =
    float;
  _width_type width;
  using _height_type =
    float;
  _height_type height;
  using _image_width_type =
    uint32_t;
  _image_width_type image_width;
  using _image_height_type =
    uint32_t;
  _image_height_type image_height;
  using _confidence_type =
    float;
  _confidence_type confidence;
  using _lost_frames_type =
    uint32_t;
  _lost_frames_type lost_frames;
  using _replan_required_type =
    bool;
  _replan_required_type replan_required;
  using _reason_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _reason_type reason;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__valid(
    const bool & _arg)
  {
    this->valid = _arg;
    return *this;
  }
  Type & set__u(
    const float & _arg)
  {
    this->u = _arg;
    return *this;
  }
  Type & set__v(
    const float & _arg)
  {
    this->v = _arg;
    return *this;
  }
  Type & set__reference_u(
    const float & _arg)
  {
    this->reference_u = _arg;
    return *this;
  }
  Type & set__reference_v(
    const float & _arg)
  {
    this->reference_v = _arg;
    return *this;
  }
  Type & set__delta_u(
    const float & _arg)
  {
    this->delta_u = _arg;
    return *this;
  }
  Type & set__delta_v(
    const float & _arg)
  {
    this->delta_v = _arg;
    return *this;
  }
  Type & set__width(
    const float & _arg)
  {
    this->width = _arg;
    return *this;
  }
  Type & set__height(
    const float & _arg)
  {
    this->height = _arg;
    return *this;
  }
  Type & set__image_width(
    const uint32_t & _arg)
  {
    this->image_width = _arg;
    return *this;
  }
  Type & set__image_height(
    const uint32_t & _arg)
  {
    this->image_height = _arg;
    return *this;
  }
  Type & set__confidence(
    const float & _arg)
  {
    this->confidence = _arg;
    return *this;
  }
  Type & set__lost_frames(
    const uint32_t & _arg)
  {
    this->lost_frames = _arg;
    return *this;
  }
  Type & set__replan_required(
    const bool & _arg)
  {
    this->replan_required = _arg;
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
    soarm100_interfaces::msg::TrackedTarget2D_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::msg::TrackedTarget2D_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::msg::TrackedTarget2D_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::msg::TrackedTarget2D_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::msg::TrackedTarget2D_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::msg::TrackedTarget2D_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::msg::TrackedTarget2D_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::msg::TrackedTarget2D_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::msg::TrackedTarget2D_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::msg::TrackedTarget2D_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__msg__TrackedTarget2D
    std::shared_ptr<soarm100_interfaces::msg::TrackedTarget2D_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__msg__TrackedTarget2D
    std::shared_ptr<soarm100_interfaces::msg::TrackedTarget2D_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TrackedTarget2D_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->valid != other.valid) {
      return false;
    }
    if (this->u != other.u) {
      return false;
    }
    if (this->v != other.v) {
      return false;
    }
    if (this->reference_u != other.reference_u) {
      return false;
    }
    if (this->reference_v != other.reference_v) {
      return false;
    }
    if (this->delta_u != other.delta_u) {
      return false;
    }
    if (this->delta_v != other.delta_v) {
      return false;
    }
    if (this->width != other.width) {
      return false;
    }
    if (this->height != other.height) {
      return false;
    }
    if (this->image_width != other.image_width) {
      return false;
    }
    if (this->image_height != other.image_height) {
      return false;
    }
    if (this->confidence != other.confidence) {
      return false;
    }
    if (this->lost_frames != other.lost_frames) {
      return false;
    }
    if (this->replan_required != other.replan_required) {
      return false;
    }
    if (this->reason != other.reason) {
      return false;
    }
    return true;
  }
  bool operator!=(const TrackedTarget2D_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TrackedTarget2D_

// alias to use template instance with default allocator
using TrackedTarget2D =
  soarm100_interfaces::msg::TrackedTarget2D_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace soarm100_interfaces

#endif  // SOARM100_INTERFACES__MSG__DETAIL__TRACKED_TARGET2_D__STRUCT_HPP_
