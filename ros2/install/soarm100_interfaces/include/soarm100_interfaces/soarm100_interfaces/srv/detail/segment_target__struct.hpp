// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from soarm100_interfaces:srv/SegmentTarget.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__SRV__DETAIL__SEGMENT_TARGET__STRUCT_HPP_
#define SOARM100_INTERFACES__SRV__DETAIL__SEGMENT_TARGET__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__srv__SegmentTarget_Request __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__srv__SegmentTarget_Request __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SegmentTarget_Request_
{
  using Type = SegmentTarget_Request_<ContainerAllocator>;

  explicit SegmentTarget_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->target_prompt = "";
      this->force_yolo = false;
    }
  }

  explicit SegmentTarget_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : target_prompt(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->target_prompt = "";
      this->force_yolo = false;
    }
  }

  // field types and members
  using _target_prompt_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _target_prompt_type target_prompt;
  using _force_yolo_type =
    bool;
  _force_yolo_type force_yolo;

  // setters for named parameter idiom
  Type & set__target_prompt(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->target_prompt = _arg;
    return *this;
  }
  Type & set__force_yolo(
    const bool & _arg)
  {
    this->force_yolo = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    soarm100_interfaces::srv::SegmentTarget_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::srv::SegmentTarget_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::srv::SegmentTarget_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::srv::SegmentTarget_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::srv::SegmentTarget_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::srv::SegmentTarget_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::srv::SegmentTarget_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::srv::SegmentTarget_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::srv::SegmentTarget_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::srv::SegmentTarget_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__srv__SegmentTarget_Request
    std::shared_ptr<soarm100_interfaces::srv::SegmentTarget_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__srv__SegmentTarget_Request
    std::shared_ptr<soarm100_interfaces::srv::SegmentTarget_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SegmentTarget_Request_ & other) const
  {
    if (this->target_prompt != other.target_prompt) {
      return false;
    }
    if (this->force_yolo != other.force_yolo) {
      return false;
    }
    return true;
  }
  bool operator!=(const SegmentTarget_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SegmentTarget_Request_

// alias to use template instance with default allocator
using SegmentTarget_Request =
  soarm100_interfaces::srv::SegmentTarget_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace soarm100_interfaces


// Include directives for member types
// Member 'target_center'
#include "geometry_msgs/msg/detail/pose_stamped__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__srv__SegmentTarget_Response __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__srv__SegmentTarget_Response __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SegmentTarget_Response_
{
  using Type = SegmentTarget_Response_<ContainerAllocator>;

  explicit SegmentTarget_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : target_center(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->reason = "";
      this->score = 0.0f;
      std::fill<typename std::array<float, 4>::iterator, float>(this->bbox_xyxy.begin(), this->bbox_xyxy.end(), 0.0f);
      this->mask_topic = "";
      this->debug_json = "";
    }
  }

  explicit SegmentTarget_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : reason(_alloc),
    target_center(_alloc, _init),
    bbox_xyxy(_alloc),
    mask_topic(_alloc),
    debug_json(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->reason = "";
      this->score = 0.0f;
      std::fill<typename std::array<float, 4>::iterator, float>(this->bbox_xyxy.begin(), this->bbox_xyxy.end(), 0.0f);
      this->mask_topic = "";
      this->debug_json = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _reason_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _reason_type reason;
  using _target_center_type =
    geometry_msgs::msg::PoseStamped_<ContainerAllocator>;
  _target_center_type target_center;
  using _score_type =
    float;
  _score_type score;
  using _bbox_xyxy_type =
    std::array<float, 4>;
  _bbox_xyxy_type bbox_xyxy;
  using _mask_topic_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _mask_topic_type mask_topic;
  using _debug_json_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _debug_json_type debug_json;

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
  Type & set__target_center(
    const geometry_msgs::msg::PoseStamped_<ContainerAllocator> & _arg)
  {
    this->target_center = _arg;
    return *this;
  }
  Type & set__score(
    const float & _arg)
  {
    this->score = _arg;
    return *this;
  }
  Type & set__bbox_xyxy(
    const std::array<float, 4> & _arg)
  {
    this->bbox_xyxy = _arg;
    return *this;
  }
  Type & set__mask_topic(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->mask_topic = _arg;
    return *this;
  }
  Type & set__debug_json(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->debug_json = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    soarm100_interfaces::srv::SegmentTarget_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::srv::SegmentTarget_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::srv::SegmentTarget_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::srv::SegmentTarget_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::srv::SegmentTarget_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::srv::SegmentTarget_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::srv::SegmentTarget_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::srv::SegmentTarget_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::srv::SegmentTarget_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::srv::SegmentTarget_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__srv__SegmentTarget_Response
    std::shared_ptr<soarm100_interfaces::srv::SegmentTarget_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__srv__SegmentTarget_Response
    std::shared_ptr<soarm100_interfaces::srv::SegmentTarget_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SegmentTarget_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->reason != other.reason) {
      return false;
    }
    if (this->target_center != other.target_center) {
      return false;
    }
    if (this->score != other.score) {
      return false;
    }
    if (this->bbox_xyxy != other.bbox_xyxy) {
      return false;
    }
    if (this->mask_topic != other.mask_topic) {
      return false;
    }
    if (this->debug_json != other.debug_json) {
      return false;
    }
    return true;
  }
  bool operator!=(const SegmentTarget_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SegmentTarget_Response_

// alias to use template instance with default allocator
using SegmentTarget_Response =
  soarm100_interfaces::srv::SegmentTarget_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace soarm100_interfaces

namespace soarm100_interfaces
{

namespace srv
{

struct SegmentTarget
{
  using Request = soarm100_interfaces::srv::SegmentTarget_Request;
  using Response = soarm100_interfaces::srv::SegmentTarget_Response;
};

}  // namespace srv

}  // namespace soarm100_interfaces

#endif  // SOARM100_INTERFACES__SRV__DETAIL__SEGMENT_TARGET__STRUCT_HPP_
