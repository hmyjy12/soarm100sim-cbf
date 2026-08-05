// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from orbbec_camera_msgs:srv/GetDeviceConfig.idl
// generated code does not contain a copyright notice

#ifndef ORBBEC_CAMERA_MSGS__SRV__DETAIL__GET_DEVICE_CONFIG__TRAITS_HPP_
#define ORBBEC_CAMERA_MSGS__SRV__DETAIL__GET_DEVICE_CONFIG__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "orbbec_camera_msgs/srv/detail/get_device_config__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace orbbec_camera_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetDeviceConfig_Request & msg,
  std::ostream & out)
{
  (void)msg;
  out << "null";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetDeviceConfig_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  (void)msg;
  (void)indentation;
  out << "null\n";
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetDeviceConfig_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace orbbec_camera_msgs

namespace rosidl_generator_traits
{

[[deprecated("use orbbec_camera_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const orbbec_camera_msgs::srv::GetDeviceConfig_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  orbbec_camera_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use orbbec_camera_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const orbbec_camera_msgs::srv::GetDeviceConfig_Request & msg)
{
  return orbbec_camera_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<orbbec_camera_msgs::srv::GetDeviceConfig_Request>()
{
  return "orbbec_camera_msgs::srv::GetDeviceConfig_Request";
}

template<>
inline const char * name<orbbec_camera_msgs::srv::GetDeviceConfig_Request>()
{
  return "orbbec_camera_msgs/srv/GetDeviceConfig_Request";
}

template<>
struct has_fixed_size<orbbec_camera_msgs::srv::GetDeviceConfig_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<orbbec_camera_msgs::srv::GetDeviceConfig_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<orbbec_camera_msgs::srv::GetDeviceConfig_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace orbbec_camera_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetDeviceConfig_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: schema_version
  {
    out << "schema_version: ";
    rosidl_generator_traits::value_to_yaml(msg.schema_version, out);
    out << ", ";
  }

  // member: device_preset
  {
    out << "device_preset: ";
    rosidl_generator_traits::value_to_yaml(msg.device_preset, out);
    out << ", ";
  }

  // member: preset_version
  {
    out << "preset_version: ";
    rosidl_generator_traits::value_to_yaml(msg.preset_version, out);
    out << ", ";
  }

  // member: color_preset
  {
    out << "color_preset: ";
    rosidl_generator_traits::value_to_yaml(msg.color_preset, out);
    out << ", ";
  }

  // member: depth_precision
  {
    out << "depth_precision: ";
    rosidl_generator_traits::value_to_yaml(msg.depth_precision, out);
    out << ", ";
  }

  // member: disparity_to_depth_mode
  {
    out << "disparity_to_depth_mode: ";
    rosidl_generator_traits::value_to_yaml(msg.disparity_to_depth_mode, out);
    out << ", ";
  }

  // member: exposure_range_mode
  {
    out << "exposure_range_mode: ";
    rosidl_generator_traits::value_to_yaml(msg.exposure_range_mode, out);
    out << ", ";
  }

  // member: depth_registration
  {
    out << "depth_registration: ";
    rosidl_generator_traits::value_to_yaml(msg.depth_registration, out);
    out << ", ";
  }

  // member: align_mode
  {
    out << "align_mode: ";
    rosidl_generator_traits::value_to_yaml(msg.align_mode, out);
    out << ", ";
  }

  // member: align_target_stream
  {
    out << "align_target_stream: ";
    rosidl_generator_traits::value_to_yaml(msg.align_target_stream, out);
    out << ", ";
  }

  // member: frame_aggregate_mode
  {
    out << "frame_aggregate_mode: ";
    rosidl_generator_traits::value_to_yaml(msg.frame_aggregate_mode, out);
    out << ", ";
  }

  // member: enable_frame_sync
  {
    out << "enable_frame_sync: ";
    rosidl_generator_traits::value_to_yaml(msg.enable_frame_sync, out);
    out << ", ";
  }

  // member: time_domain
  {
    out << "time_domain: ";
    rosidl_generator_traits::value_to_yaml(msg.time_domain, out);
    out << ", ";
  }

  // member: sync_mode
  {
    out << "sync_mode: ";
    rosidl_generator_traits::value_to_yaml(msg.sync_mode, out);
    out << ", ";
  }

  // member: intra_camera_sync_reference
  {
    out << "intra_camera_sync_reference: ";
    rosidl_generator_traits::value_to_yaml(msg.intra_camera_sync_reference, out);
    out << ", ";
  }

  // member: data_json
  {
    out << "data_json: ";
    rosidl_generator_traits::value_to_yaml(msg.data_json, out);
    out << ", ";
  }

  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetDeviceConfig_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: schema_version
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "schema_version: ";
    rosidl_generator_traits::value_to_yaml(msg.schema_version, out);
    out << "\n";
  }

  // member: device_preset
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "device_preset: ";
    rosidl_generator_traits::value_to_yaml(msg.device_preset, out);
    out << "\n";
  }

  // member: preset_version
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "preset_version: ";
    rosidl_generator_traits::value_to_yaml(msg.preset_version, out);
    out << "\n";
  }

  // member: color_preset
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "color_preset: ";
    rosidl_generator_traits::value_to_yaml(msg.color_preset, out);
    out << "\n";
  }

  // member: depth_precision
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "depth_precision: ";
    rosidl_generator_traits::value_to_yaml(msg.depth_precision, out);
    out << "\n";
  }

  // member: disparity_to_depth_mode
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "disparity_to_depth_mode: ";
    rosidl_generator_traits::value_to_yaml(msg.disparity_to_depth_mode, out);
    out << "\n";
  }

  // member: exposure_range_mode
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "exposure_range_mode: ";
    rosidl_generator_traits::value_to_yaml(msg.exposure_range_mode, out);
    out << "\n";
  }

  // member: depth_registration
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "depth_registration: ";
    rosidl_generator_traits::value_to_yaml(msg.depth_registration, out);
    out << "\n";
  }

  // member: align_mode
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "align_mode: ";
    rosidl_generator_traits::value_to_yaml(msg.align_mode, out);
    out << "\n";
  }

  // member: align_target_stream
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "align_target_stream: ";
    rosidl_generator_traits::value_to_yaml(msg.align_target_stream, out);
    out << "\n";
  }

  // member: frame_aggregate_mode
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "frame_aggregate_mode: ";
    rosidl_generator_traits::value_to_yaml(msg.frame_aggregate_mode, out);
    out << "\n";
  }

  // member: enable_frame_sync
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "enable_frame_sync: ";
    rosidl_generator_traits::value_to_yaml(msg.enable_frame_sync, out);
    out << "\n";
  }

  // member: time_domain
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "time_domain: ";
    rosidl_generator_traits::value_to_yaml(msg.time_domain, out);
    out << "\n";
  }

  // member: sync_mode
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sync_mode: ";
    rosidl_generator_traits::value_to_yaml(msg.sync_mode, out);
    out << "\n";
  }

  // member: intra_camera_sync_reference
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "intra_camera_sync_reference: ";
    rosidl_generator_traits::value_to_yaml(msg.intra_camera_sync_reference, out);
    out << "\n";
  }

  // member: data_json
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "data_json: ";
    rosidl_generator_traits::value_to_yaml(msg.data_json, out);
    out << "\n";
  }

  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetDeviceConfig_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace orbbec_camera_msgs

namespace rosidl_generator_traits
{

[[deprecated("use orbbec_camera_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const orbbec_camera_msgs::srv::GetDeviceConfig_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  orbbec_camera_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use orbbec_camera_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const orbbec_camera_msgs::srv::GetDeviceConfig_Response & msg)
{
  return orbbec_camera_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<orbbec_camera_msgs::srv::GetDeviceConfig_Response>()
{
  return "orbbec_camera_msgs::srv::GetDeviceConfig_Response";
}

template<>
inline const char * name<orbbec_camera_msgs::srv::GetDeviceConfig_Response>()
{
  return "orbbec_camera_msgs/srv/GetDeviceConfig_Response";
}

template<>
struct has_fixed_size<orbbec_camera_msgs::srv::GetDeviceConfig_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<orbbec_camera_msgs::srv::GetDeviceConfig_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<orbbec_camera_msgs::srv::GetDeviceConfig_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<orbbec_camera_msgs::srv::GetDeviceConfig>()
{
  return "orbbec_camera_msgs::srv::GetDeviceConfig";
}

template<>
inline const char * name<orbbec_camera_msgs::srv::GetDeviceConfig>()
{
  return "orbbec_camera_msgs/srv/GetDeviceConfig";
}

template<>
struct has_fixed_size<orbbec_camera_msgs::srv::GetDeviceConfig>
  : std::integral_constant<
    bool,
    has_fixed_size<orbbec_camera_msgs::srv::GetDeviceConfig_Request>::value &&
    has_fixed_size<orbbec_camera_msgs::srv::GetDeviceConfig_Response>::value
  >
{
};

template<>
struct has_bounded_size<orbbec_camera_msgs::srv::GetDeviceConfig>
  : std::integral_constant<
    bool,
    has_bounded_size<orbbec_camera_msgs::srv::GetDeviceConfig_Request>::value &&
    has_bounded_size<orbbec_camera_msgs::srv::GetDeviceConfig_Response>::value
  >
{
};

template<>
struct is_service<orbbec_camera_msgs::srv::GetDeviceConfig>
  : std::true_type
{
};

template<>
struct is_service_request<orbbec_camera_msgs::srv::GetDeviceConfig_Request>
  : std::true_type
{
};

template<>
struct is_service_response<orbbec_camera_msgs::srv::GetDeviceConfig_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // ORBBEC_CAMERA_MSGS__SRV__DETAIL__GET_DEVICE_CONFIG__TRAITS_HPP_
