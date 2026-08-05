// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from orbbec_camera_msgs:srv/GetDeviceConfig.idl
// generated code does not contain a copyright notice

#ifndef ORBBEC_CAMERA_MSGS__SRV__DETAIL__GET_DEVICE_CONFIG__STRUCT_HPP_
#define ORBBEC_CAMERA_MSGS__SRV__DETAIL__GET_DEVICE_CONFIG__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__orbbec_camera_msgs__srv__GetDeviceConfig_Request __attribute__((deprecated))
#else
# define DEPRECATED__orbbec_camera_msgs__srv__GetDeviceConfig_Request __declspec(deprecated)
#endif

namespace orbbec_camera_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetDeviceConfig_Request_
{
  using Type = GetDeviceConfig_Request_<ContainerAllocator>;

  explicit GetDeviceConfig_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  explicit GetDeviceConfig_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  // field types and members
  using _structure_needs_at_least_one_member_type =
    uint8_t;
  _structure_needs_at_least_one_member_type structure_needs_at_least_one_member;


  // constant declarations

  // pointer types
  using RawPtr =
    orbbec_camera_msgs::srv::GetDeviceConfig_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const orbbec_camera_msgs::srv::GetDeviceConfig_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<orbbec_camera_msgs::srv::GetDeviceConfig_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<orbbec_camera_msgs::srv::GetDeviceConfig_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      orbbec_camera_msgs::srv::GetDeviceConfig_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<orbbec_camera_msgs::srv::GetDeviceConfig_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      orbbec_camera_msgs::srv::GetDeviceConfig_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<orbbec_camera_msgs::srv::GetDeviceConfig_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<orbbec_camera_msgs::srv::GetDeviceConfig_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<orbbec_camera_msgs::srv::GetDeviceConfig_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__orbbec_camera_msgs__srv__GetDeviceConfig_Request
    std::shared_ptr<orbbec_camera_msgs::srv::GetDeviceConfig_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__orbbec_camera_msgs__srv__GetDeviceConfig_Request
    std::shared_ptr<orbbec_camera_msgs::srv::GetDeviceConfig_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetDeviceConfig_Request_ & other) const
  {
    if (this->structure_needs_at_least_one_member != other.structure_needs_at_least_one_member) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetDeviceConfig_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetDeviceConfig_Request_

// alias to use template instance with default allocator
using GetDeviceConfig_Request =
  orbbec_camera_msgs::srv::GetDeviceConfig_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace orbbec_camera_msgs


#ifndef _WIN32
# define DEPRECATED__orbbec_camera_msgs__srv__GetDeviceConfig_Response __attribute__((deprecated))
#else
# define DEPRECATED__orbbec_camera_msgs__srv__GetDeviceConfig_Response __declspec(deprecated)
#endif

namespace orbbec_camera_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetDeviceConfig_Response_
{
  using Type = GetDeviceConfig_Response_<ContainerAllocator>;

  explicit GetDeviceConfig_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->schema_version = "";
      this->device_preset = "";
      this->preset_version = "";
      this->color_preset = "";
      this->depth_precision = "";
      this->disparity_to_depth_mode = "";
      this->exposure_range_mode = "";
      this->depth_registration = false;
      this->align_mode = "";
      this->align_target_stream = "";
      this->frame_aggregate_mode = "";
      this->enable_frame_sync = false;
      this->time_domain = "";
      this->sync_mode = "";
      this->intra_camera_sync_reference = "";
      this->data_json = "";
      this->success = false;
      this->message = "";
    }
  }

  explicit GetDeviceConfig_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : schema_version(_alloc),
    device_preset(_alloc),
    preset_version(_alloc),
    color_preset(_alloc),
    depth_precision(_alloc),
    disparity_to_depth_mode(_alloc),
    exposure_range_mode(_alloc),
    align_mode(_alloc),
    align_target_stream(_alloc),
    frame_aggregate_mode(_alloc),
    time_domain(_alloc),
    sync_mode(_alloc),
    intra_camera_sync_reference(_alloc),
    data_json(_alloc),
    message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->schema_version = "";
      this->device_preset = "";
      this->preset_version = "";
      this->color_preset = "";
      this->depth_precision = "";
      this->disparity_to_depth_mode = "";
      this->exposure_range_mode = "";
      this->depth_registration = false;
      this->align_mode = "";
      this->align_target_stream = "";
      this->frame_aggregate_mode = "";
      this->enable_frame_sync = false;
      this->time_domain = "";
      this->sync_mode = "";
      this->intra_camera_sync_reference = "";
      this->data_json = "";
      this->success = false;
      this->message = "";
    }
  }

  // field types and members
  using _schema_version_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _schema_version_type schema_version;
  using _device_preset_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _device_preset_type device_preset;
  using _preset_version_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _preset_version_type preset_version;
  using _color_preset_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _color_preset_type color_preset;
  using _depth_precision_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _depth_precision_type depth_precision;
  using _disparity_to_depth_mode_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _disparity_to_depth_mode_type disparity_to_depth_mode;
  using _exposure_range_mode_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _exposure_range_mode_type exposure_range_mode;
  using _depth_registration_type =
    bool;
  _depth_registration_type depth_registration;
  using _align_mode_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _align_mode_type align_mode;
  using _align_target_stream_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _align_target_stream_type align_target_stream;
  using _frame_aggregate_mode_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _frame_aggregate_mode_type frame_aggregate_mode;
  using _enable_frame_sync_type =
    bool;
  _enable_frame_sync_type enable_frame_sync;
  using _time_domain_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _time_domain_type time_domain;
  using _sync_mode_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _sync_mode_type sync_mode;
  using _intra_camera_sync_reference_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _intra_camera_sync_reference_type intra_camera_sync_reference;
  using _data_json_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _data_json_type data_json;
  using _success_type =
    bool;
  _success_type success;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__schema_version(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->schema_version = _arg;
    return *this;
  }
  Type & set__device_preset(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->device_preset = _arg;
    return *this;
  }
  Type & set__preset_version(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->preset_version = _arg;
    return *this;
  }
  Type & set__color_preset(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->color_preset = _arg;
    return *this;
  }
  Type & set__depth_precision(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->depth_precision = _arg;
    return *this;
  }
  Type & set__disparity_to_depth_mode(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->disparity_to_depth_mode = _arg;
    return *this;
  }
  Type & set__exposure_range_mode(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->exposure_range_mode = _arg;
    return *this;
  }
  Type & set__depth_registration(
    const bool & _arg)
  {
    this->depth_registration = _arg;
    return *this;
  }
  Type & set__align_mode(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->align_mode = _arg;
    return *this;
  }
  Type & set__align_target_stream(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->align_target_stream = _arg;
    return *this;
  }
  Type & set__frame_aggregate_mode(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->frame_aggregate_mode = _arg;
    return *this;
  }
  Type & set__enable_frame_sync(
    const bool & _arg)
  {
    this->enable_frame_sync = _arg;
    return *this;
  }
  Type & set__time_domain(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->time_domain = _arg;
    return *this;
  }
  Type & set__sync_mode(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->sync_mode = _arg;
    return *this;
  }
  Type & set__intra_camera_sync_reference(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->intra_camera_sync_reference = _arg;
    return *this;
  }
  Type & set__data_json(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->data_json = _arg;
    return *this;
  }
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    orbbec_camera_msgs::srv::GetDeviceConfig_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const orbbec_camera_msgs::srv::GetDeviceConfig_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<orbbec_camera_msgs::srv::GetDeviceConfig_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<orbbec_camera_msgs::srv::GetDeviceConfig_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      orbbec_camera_msgs::srv::GetDeviceConfig_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<orbbec_camera_msgs::srv::GetDeviceConfig_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      orbbec_camera_msgs::srv::GetDeviceConfig_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<orbbec_camera_msgs::srv::GetDeviceConfig_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<orbbec_camera_msgs::srv::GetDeviceConfig_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<orbbec_camera_msgs::srv::GetDeviceConfig_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__orbbec_camera_msgs__srv__GetDeviceConfig_Response
    std::shared_ptr<orbbec_camera_msgs::srv::GetDeviceConfig_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__orbbec_camera_msgs__srv__GetDeviceConfig_Response
    std::shared_ptr<orbbec_camera_msgs::srv::GetDeviceConfig_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetDeviceConfig_Response_ & other) const
  {
    if (this->schema_version != other.schema_version) {
      return false;
    }
    if (this->device_preset != other.device_preset) {
      return false;
    }
    if (this->preset_version != other.preset_version) {
      return false;
    }
    if (this->color_preset != other.color_preset) {
      return false;
    }
    if (this->depth_precision != other.depth_precision) {
      return false;
    }
    if (this->disparity_to_depth_mode != other.disparity_to_depth_mode) {
      return false;
    }
    if (this->exposure_range_mode != other.exposure_range_mode) {
      return false;
    }
    if (this->depth_registration != other.depth_registration) {
      return false;
    }
    if (this->align_mode != other.align_mode) {
      return false;
    }
    if (this->align_target_stream != other.align_target_stream) {
      return false;
    }
    if (this->frame_aggregate_mode != other.frame_aggregate_mode) {
      return false;
    }
    if (this->enable_frame_sync != other.enable_frame_sync) {
      return false;
    }
    if (this->time_domain != other.time_domain) {
      return false;
    }
    if (this->sync_mode != other.sync_mode) {
      return false;
    }
    if (this->intra_camera_sync_reference != other.intra_camera_sync_reference) {
      return false;
    }
    if (this->data_json != other.data_json) {
      return false;
    }
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetDeviceConfig_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetDeviceConfig_Response_

// alias to use template instance with default allocator
using GetDeviceConfig_Response =
  orbbec_camera_msgs::srv::GetDeviceConfig_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace orbbec_camera_msgs

namespace orbbec_camera_msgs
{

namespace srv
{

struct GetDeviceConfig
{
  using Request = orbbec_camera_msgs::srv::GetDeviceConfig_Request;
  using Response = orbbec_camera_msgs::srv::GetDeviceConfig_Response;
};

}  // namespace srv

}  // namespace orbbec_camera_msgs

#endif  // ORBBEC_CAMERA_MSGS__SRV__DETAIL__GET_DEVICE_CONFIG__STRUCT_HPP_
