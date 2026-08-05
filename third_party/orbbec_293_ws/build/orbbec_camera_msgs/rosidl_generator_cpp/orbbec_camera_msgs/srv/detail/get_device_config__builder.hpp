// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from orbbec_camera_msgs:srv/GetDeviceConfig.idl
// generated code does not contain a copyright notice

#ifndef ORBBEC_CAMERA_MSGS__SRV__DETAIL__GET_DEVICE_CONFIG__BUILDER_HPP_
#define ORBBEC_CAMERA_MSGS__SRV__DETAIL__GET_DEVICE_CONFIG__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "orbbec_camera_msgs/srv/detail/get_device_config__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace orbbec_camera_msgs
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::orbbec_camera_msgs::srv::GetDeviceConfig_Request>()
{
  return ::orbbec_camera_msgs::srv::GetDeviceConfig_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace orbbec_camera_msgs


namespace orbbec_camera_msgs
{

namespace srv
{

namespace builder
{

class Init_GetDeviceConfig_Response_message
{
public:
  explicit Init_GetDeviceConfig_Response_message(::orbbec_camera_msgs::srv::GetDeviceConfig_Response & msg)
  : msg_(msg)
  {}
  ::orbbec_camera_msgs::srv::GetDeviceConfig_Response message(::orbbec_camera_msgs::srv::GetDeviceConfig_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::orbbec_camera_msgs::srv::GetDeviceConfig_Response msg_;
};

class Init_GetDeviceConfig_Response_success
{
public:
  explicit Init_GetDeviceConfig_Response_success(::orbbec_camera_msgs::srv::GetDeviceConfig_Response & msg)
  : msg_(msg)
  {}
  Init_GetDeviceConfig_Response_message success(::orbbec_camera_msgs::srv::GetDeviceConfig_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_GetDeviceConfig_Response_message(msg_);
  }

private:
  ::orbbec_camera_msgs::srv::GetDeviceConfig_Response msg_;
};

class Init_GetDeviceConfig_Response_data_json
{
public:
  explicit Init_GetDeviceConfig_Response_data_json(::orbbec_camera_msgs::srv::GetDeviceConfig_Response & msg)
  : msg_(msg)
  {}
  Init_GetDeviceConfig_Response_success data_json(::orbbec_camera_msgs::srv::GetDeviceConfig_Response::_data_json_type arg)
  {
    msg_.data_json = std::move(arg);
    return Init_GetDeviceConfig_Response_success(msg_);
  }

private:
  ::orbbec_camera_msgs::srv::GetDeviceConfig_Response msg_;
};

class Init_GetDeviceConfig_Response_intra_camera_sync_reference
{
public:
  explicit Init_GetDeviceConfig_Response_intra_camera_sync_reference(::orbbec_camera_msgs::srv::GetDeviceConfig_Response & msg)
  : msg_(msg)
  {}
  Init_GetDeviceConfig_Response_data_json intra_camera_sync_reference(::orbbec_camera_msgs::srv::GetDeviceConfig_Response::_intra_camera_sync_reference_type arg)
  {
    msg_.intra_camera_sync_reference = std::move(arg);
    return Init_GetDeviceConfig_Response_data_json(msg_);
  }

private:
  ::orbbec_camera_msgs::srv::GetDeviceConfig_Response msg_;
};

class Init_GetDeviceConfig_Response_sync_mode
{
public:
  explicit Init_GetDeviceConfig_Response_sync_mode(::orbbec_camera_msgs::srv::GetDeviceConfig_Response & msg)
  : msg_(msg)
  {}
  Init_GetDeviceConfig_Response_intra_camera_sync_reference sync_mode(::orbbec_camera_msgs::srv::GetDeviceConfig_Response::_sync_mode_type arg)
  {
    msg_.sync_mode = std::move(arg);
    return Init_GetDeviceConfig_Response_intra_camera_sync_reference(msg_);
  }

private:
  ::orbbec_camera_msgs::srv::GetDeviceConfig_Response msg_;
};

class Init_GetDeviceConfig_Response_time_domain
{
public:
  explicit Init_GetDeviceConfig_Response_time_domain(::orbbec_camera_msgs::srv::GetDeviceConfig_Response & msg)
  : msg_(msg)
  {}
  Init_GetDeviceConfig_Response_sync_mode time_domain(::orbbec_camera_msgs::srv::GetDeviceConfig_Response::_time_domain_type arg)
  {
    msg_.time_domain = std::move(arg);
    return Init_GetDeviceConfig_Response_sync_mode(msg_);
  }

private:
  ::orbbec_camera_msgs::srv::GetDeviceConfig_Response msg_;
};

class Init_GetDeviceConfig_Response_enable_frame_sync
{
public:
  explicit Init_GetDeviceConfig_Response_enable_frame_sync(::orbbec_camera_msgs::srv::GetDeviceConfig_Response & msg)
  : msg_(msg)
  {}
  Init_GetDeviceConfig_Response_time_domain enable_frame_sync(::orbbec_camera_msgs::srv::GetDeviceConfig_Response::_enable_frame_sync_type arg)
  {
    msg_.enable_frame_sync = std::move(arg);
    return Init_GetDeviceConfig_Response_time_domain(msg_);
  }

private:
  ::orbbec_camera_msgs::srv::GetDeviceConfig_Response msg_;
};

class Init_GetDeviceConfig_Response_frame_aggregate_mode
{
public:
  explicit Init_GetDeviceConfig_Response_frame_aggregate_mode(::orbbec_camera_msgs::srv::GetDeviceConfig_Response & msg)
  : msg_(msg)
  {}
  Init_GetDeviceConfig_Response_enable_frame_sync frame_aggregate_mode(::orbbec_camera_msgs::srv::GetDeviceConfig_Response::_frame_aggregate_mode_type arg)
  {
    msg_.frame_aggregate_mode = std::move(arg);
    return Init_GetDeviceConfig_Response_enable_frame_sync(msg_);
  }

private:
  ::orbbec_camera_msgs::srv::GetDeviceConfig_Response msg_;
};

class Init_GetDeviceConfig_Response_align_target_stream
{
public:
  explicit Init_GetDeviceConfig_Response_align_target_stream(::orbbec_camera_msgs::srv::GetDeviceConfig_Response & msg)
  : msg_(msg)
  {}
  Init_GetDeviceConfig_Response_frame_aggregate_mode align_target_stream(::orbbec_camera_msgs::srv::GetDeviceConfig_Response::_align_target_stream_type arg)
  {
    msg_.align_target_stream = std::move(arg);
    return Init_GetDeviceConfig_Response_frame_aggregate_mode(msg_);
  }

private:
  ::orbbec_camera_msgs::srv::GetDeviceConfig_Response msg_;
};

class Init_GetDeviceConfig_Response_align_mode
{
public:
  explicit Init_GetDeviceConfig_Response_align_mode(::orbbec_camera_msgs::srv::GetDeviceConfig_Response & msg)
  : msg_(msg)
  {}
  Init_GetDeviceConfig_Response_align_target_stream align_mode(::orbbec_camera_msgs::srv::GetDeviceConfig_Response::_align_mode_type arg)
  {
    msg_.align_mode = std::move(arg);
    return Init_GetDeviceConfig_Response_align_target_stream(msg_);
  }

private:
  ::orbbec_camera_msgs::srv::GetDeviceConfig_Response msg_;
};

class Init_GetDeviceConfig_Response_depth_registration
{
public:
  explicit Init_GetDeviceConfig_Response_depth_registration(::orbbec_camera_msgs::srv::GetDeviceConfig_Response & msg)
  : msg_(msg)
  {}
  Init_GetDeviceConfig_Response_align_mode depth_registration(::orbbec_camera_msgs::srv::GetDeviceConfig_Response::_depth_registration_type arg)
  {
    msg_.depth_registration = std::move(arg);
    return Init_GetDeviceConfig_Response_align_mode(msg_);
  }

private:
  ::orbbec_camera_msgs::srv::GetDeviceConfig_Response msg_;
};

class Init_GetDeviceConfig_Response_exposure_range_mode
{
public:
  explicit Init_GetDeviceConfig_Response_exposure_range_mode(::orbbec_camera_msgs::srv::GetDeviceConfig_Response & msg)
  : msg_(msg)
  {}
  Init_GetDeviceConfig_Response_depth_registration exposure_range_mode(::orbbec_camera_msgs::srv::GetDeviceConfig_Response::_exposure_range_mode_type arg)
  {
    msg_.exposure_range_mode = std::move(arg);
    return Init_GetDeviceConfig_Response_depth_registration(msg_);
  }

private:
  ::orbbec_camera_msgs::srv::GetDeviceConfig_Response msg_;
};

class Init_GetDeviceConfig_Response_disparity_to_depth_mode
{
public:
  explicit Init_GetDeviceConfig_Response_disparity_to_depth_mode(::orbbec_camera_msgs::srv::GetDeviceConfig_Response & msg)
  : msg_(msg)
  {}
  Init_GetDeviceConfig_Response_exposure_range_mode disparity_to_depth_mode(::orbbec_camera_msgs::srv::GetDeviceConfig_Response::_disparity_to_depth_mode_type arg)
  {
    msg_.disparity_to_depth_mode = std::move(arg);
    return Init_GetDeviceConfig_Response_exposure_range_mode(msg_);
  }

private:
  ::orbbec_camera_msgs::srv::GetDeviceConfig_Response msg_;
};

class Init_GetDeviceConfig_Response_depth_precision
{
public:
  explicit Init_GetDeviceConfig_Response_depth_precision(::orbbec_camera_msgs::srv::GetDeviceConfig_Response & msg)
  : msg_(msg)
  {}
  Init_GetDeviceConfig_Response_disparity_to_depth_mode depth_precision(::orbbec_camera_msgs::srv::GetDeviceConfig_Response::_depth_precision_type arg)
  {
    msg_.depth_precision = std::move(arg);
    return Init_GetDeviceConfig_Response_disparity_to_depth_mode(msg_);
  }

private:
  ::orbbec_camera_msgs::srv::GetDeviceConfig_Response msg_;
};

class Init_GetDeviceConfig_Response_color_preset
{
public:
  explicit Init_GetDeviceConfig_Response_color_preset(::orbbec_camera_msgs::srv::GetDeviceConfig_Response & msg)
  : msg_(msg)
  {}
  Init_GetDeviceConfig_Response_depth_precision color_preset(::orbbec_camera_msgs::srv::GetDeviceConfig_Response::_color_preset_type arg)
  {
    msg_.color_preset = std::move(arg);
    return Init_GetDeviceConfig_Response_depth_precision(msg_);
  }

private:
  ::orbbec_camera_msgs::srv::GetDeviceConfig_Response msg_;
};

class Init_GetDeviceConfig_Response_preset_version
{
public:
  explicit Init_GetDeviceConfig_Response_preset_version(::orbbec_camera_msgs::srv::GetDeviceConfig_Response & msg)
  : msg_(msg)
  {}
  Init_GetDeviceConfig_Response_color_preset preset_version(::orbbec_camera_msgs::srv::GetDeviceConfig_Response::_preset_version_type arg)
  {
    msg_.preset_version = std::move(arg);
    return Init_GetDeviceConfig_Response_color_preset(msg_);
  }

private:
  ::orbbec_camera_msgs::srv::GetDeviceConfig_Response msg_;
};

class Init_GetDeviceConfig_Response_device_preset
{
public:
  explicit Init_GetDeviceConfig_Response_device_preset(::orbbec_camera_msgs::srv::GetDeviceConfig_Response & msg)
  : msg_(msg)
  {}
  Init_GetDeviceConfig_Response_preset_version device_preset(::orbbec_camera_msgs::srv::GetDeviceConfig_Response::_device_preset_type arg)
  {
    msg_.device_preset = std::move(arg);
    return Init_GetDeviceConfig_Response_preset_version(msg_);
  }

private:
  ::orbbec_camera_msgs::srv::GetDeviceConfig_Response msg_;
};

class Init_GetDeviceConfig_Response_schema_version
{
public:
  Init_GetDeviceConfig_Response_schema_version()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetDeviceConfig_Response_device_preset schema_version(::orbbec_camera_msgs::srv::GetDeviceConfig_Response::_schema_version_type arg)
  {
    msg_.schema_version = std::move(arg);
    return Init_GetDeviceConfig_Response_device_preset(msg_);
  }

private:
  ::orbbec_camera_msgs::srv::GetDeviceConfig_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::orbbec_camera_msgs::srv::GetDeviceConfig_Response>()
{
  return orbbec_camera_msgs::srv::builder::Init_GetDeviceConfig_Response_schema_version();
}

}  // namespace orbbec_camera_msgs

#endif  // ORBBEC_CAMERA_MSGS__SRV__DETAIL__GET_DEVICE_CONFIG__BUILDER_HPP_
