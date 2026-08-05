// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from orbbec_camera_msgs:srv/SetBagRecording.idl
// generated code does not contain a copyright notice

#ifndef ORBBEC_CAMERA_MSGS__SRV__DETAIL__SET_BAG_RECORDING__TRAITS_HPP_
#define ORBBEC_CAMERA_MSGS__SRV__DETAIL__SET_BAG_RECORDING__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "orbbec_camera_msgs/srv/detail/set_bag_recording__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace orbbec_camera_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetBagRecording_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: enable
  {
    out << "enable: ";
    rosidl_generator_traits::value_to_yaml(msg.enable, out);
    out << ", ";
  }

  // member: file_path
  {
    out << "file_path: ";
    rosidl_generator_traits::value_to_yaml(msg.file_path, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SetBagRecording_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: enable
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "enable: ";
    rosidl_generator_traits::value_to_yaml(msg.enable, out);
    out << "\n";
  }

  // member: file_path
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "file_path: ";
    rosidl_generator_traits::value_to_yaml(msg.file_path, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SetBagRecording_Request & msg, bool use_flow_style = false)
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
  const orbbec_camera_msgs::srv::SetBagRecording_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  orbbec_camera_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use orbbec_camera_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const orbbec_camera_msgs::srv::SetBagRecording_Request & msg)
{
  return orbbec_camera_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<orbbec_camera_msgs::srv::SetBagRecording_Request>()
{
  return "orbbec_camera_msgs::srv::SetBagRecording_Request";
}

template<>
inline const char * name<orbbec_camera_msgs::srv::SetBagRecording_Request>()
{
  return "orbbec_camera_msgs/srv/SetBagRecording_Request";
}

template<>
struct has_fixed_size<orbbec_camera_msgs::srv::SetBagRecording_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<orbbec_camera_msgs::srv::SetBagRecording_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<orbbec_camera_msgs::srv::SetBagRecording_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace orbbec_camera_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetBagRecording_Response & msg,
  std::ostream & out)
{
  out << "{";
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
  const SetBagRecording_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
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

inline std::string to_yaml(const SetBagRecording_Response & msg, bool use_flow_style = false)
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
  const orbbec_camera_msgs::srv::SetBagRecording_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  orbbec_camera_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use orbbec_camera_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const orbbec_camera_msgs::srv::SetBagRecording_Response & msg)
{
  return orbbec_camera_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<orbbec_camera_msgs::srv::SetBagRecording_Response>()
{
  return "orbbec_camera_msgs::srv::SetBagRecording_Response";
}

template<>
inline const char * name<orbbec_camera_msgs::srv::SetBagRecording_Response>()
{
  return "orbbec_camera_msgs/srv/SetBagRecording_Response";
}

template<>
struct has_fixed_size<orbbec_camera_msgs::srv::SetBagRecording_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<orbbec_camera_msgs::srv::SetBagRecording_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<orbbec_camera_msgs::srv::SetBagRecording_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<orbbec_camera_msgs::srv::SetBagRecording>()
{
  return "orbbec_camera_msgs::srv::SetBagRecording";
}

template<>
inline const char * name<orbbec_camera_msgs::srv::SetBagRecording>()
{
  return "orbbec_camera_msgs/srv/SetBagRecording";
}

template<>
struct has_fixed_size<orbbec_camera_msgs::srv::SetBagRecording>
  : std::integral_constant<
    bool,
    has_fixed_size<orbbec_camera_msgs::srv::SetBagRecording_Request>::value &&
    has_fixed_size<orbbec_camera_msgs::srv::SetBagRecording_Response>::value
  >
{
};

template<>
struct has_bounded_size<orbbec_camera_msgs::srv::SetBagRecording>
  : std::integral_constant<
    bool,
    has_bounded_size<orbbec_camera_msgs::srv::SetBagRecording_Request>::value &&
    has_bounded_size<orbbec_camera_msgs::srv::SetBagRecording_Response>::value
  >
{
};

template<>
struct is_service<orbbec_camera_msgs::srv::SetBagRecording>
  : std::true_type
{
};

template<>
struct is_service_request<orbbec_camera_msgs::srv::SetBagRecording_Request>
  : std::true_type
{
};

template<>
struct is_service_response<orbbec_camera_msgs::srv::SetBagRecording_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // ORBBEC_CAMERA_MSGS__SRV__DETAIL__SET_BAG_RECORDING__TRAITS_HPP_
