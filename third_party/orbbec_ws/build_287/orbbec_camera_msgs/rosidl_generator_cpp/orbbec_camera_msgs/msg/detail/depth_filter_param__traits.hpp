// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from orbbec_camera_msgs:msg/DepthFilterParam.idl
// generated code does not contain a copyright notice

#ifndef ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTER_PARAM__TRAITS_HPP_
#define ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTER_PARAM__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "orbbec_camera_msgs/msg/detail/depth_filter_param__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace orbbec_camera_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const DepthFilterParam & msg,
  std::ostream & out)
{
  out << "{";
  // member: name
  {
    out << "name: ";
    rosidl_generator_traits::value_to_yaml(msg.name, out);
    out << ", ";
  }

  // member: value
  {
    out << "value: ";
    rosidl_generator_traits::value_to_yaml(msg.value, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const DepthFilterParam & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "name: ";
    rosidl_generator_traits::value_to_yaml(msg.name, out);
    out << "\n";
  }

  // member: value
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "value: ";
    rosidl_generator_traits::value_to_yaml(msg.value, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const DepthFilterParam & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace orbbec_camera_msgs

namespace rosidl_generator_traits
{

[[deprecated("use orbbec_camera_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const orbbec_camera_msgs::msg::DepthFilterParam & msg,
  std::ostream & out, size_t indentation = 0)
{
  orbbec_camera_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use orbbec_camera_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const orbbec_camera_msgs::msg::DepthFilterParam & msg)
{
  return orbbec_camera_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<orbbec_camera_msgs::msg::DepthFilterParam>()
{
  return "orbbec_camera_msgs::msg::DepthFilterParam";
}

template<>
inline const char * name<orbbec_camera_msgs::msg::DepthFilterParam>()
{
  return "orbbec_camera_msgs/msg/DepthFilterParam";
}

template<>
struct has_fixed_size<orbbec_camera_msgs::msg::DepthFilterParam>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<orbbec_camera_msgs::msg::DepthFilterParam>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<orbbec_camera_msgs::msg::DepthFilterParam>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTER_PARAM__TRAITS_HPP_
