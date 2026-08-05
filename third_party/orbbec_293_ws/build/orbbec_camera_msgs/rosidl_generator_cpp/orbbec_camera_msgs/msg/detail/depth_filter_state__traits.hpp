// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from orbbec_camera_msgs:msg/DepthFilterState.idl
// generated code does not contain a copyright notice

#ifndef ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTER_STATE__TRAITS_HPP_
#define ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTER_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "orbbec_camera_msgs/msg/detail/depth_filter_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'params'
#include "orbbec_camera_msgs/msg/detail/depth_filter_param__traits.hpp"

namespace orbbec_camera_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const DepthFilterState & msg,
  std::ostream & out)
{
  out << "{";
  // member: filter_name
  {
    out << "filter_name: ";
    rosidl_generator_traits::value_to_yaml(msg.filter_name, out);
    out << ", ";
  }

  // member: enabled
  {
    out << "enabled: ";
    rosidl_generator_traits::value_to_yaml(msg.enabled, out);
    out << ", ";
  }

  // member: params
  {
    if (msg.params.size() == 0) {
      out << "params: []";
    } else {
      out << "params: [";
      size_t pending_items = msg.params.size();
      for (auto item : msg.params) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const DepthFilterState & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: filter_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "filter_name: ";
    rosidl_generator_traits::value_to_yaml(msg.filter_name, out);
    out << "\n";
  }

  // member: enabled
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "enabled: ";
    rosidl_generator_traits::value_to_yaml(msg.enabled, out);
    out << "\n";
  }

  // member: params
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.params.size() == 0) {
      out << "params: []\n";
    } else {
      out << "params:\n";
      for (auto item : msg.params) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const DepthFilterState & msg, bool use_flow_style = false)
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
  const orbbec_camera_msgs::msg::DepthFilterState & msg,
  std::ostream & out, size_t indentation = 0)
{
  orbbec_camera_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use orbbec_camera_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const orbbec_camera_msgs::msg::DepthFilterState & msg)
{
  return orbbec_camera_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<orbbec_camera_msgs::msg::DepthFilterState>()
{
  return "orbbec_camera_msgs::msg::DepthFilterState";
}

template<>
inline const char * name<orbbec_camera_msgs::msg::DepthFilterState>()
{
  return "orbbec_camera_msgs/msg/DepthFilterState";
}

template<>
struct has_fixed_size<orbbec_camera_msgs::msg::DepthFilterState>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<orbbec_camera_msgs::msg::DepthFilterState>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<orbbec_camera_msgs::msg::DepthFilterState>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTER_STATE__TRAITS_HPP_
