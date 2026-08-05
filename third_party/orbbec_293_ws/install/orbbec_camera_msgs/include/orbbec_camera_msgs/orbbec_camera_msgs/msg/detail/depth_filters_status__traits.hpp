// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from orbbec_camera_msgs:msg/DepthFiltersStatus.idl
// generated code does not contain a copyright notice

#ifndef ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTERS_STATUS__TRAITS_HPP_
#define ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTERS_STATUS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "orbbec_camera_msgs/msg/detail/depth_filters_status__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'filters'
#include "orbbec_camera_msgs/msg/detail/depth_filter_state__traits.hpp"

namespace orbbec_camera_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const DepthFiltersStatus & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: filters
  {
    if (msg.filters.size() == 0) {
      out << "filters: []";
    } else {
      out << "filters: [";
      size_t pending_items = msg.filters.size();
      for (auto item : msg.filters) {
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
  const DepthFiltersStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: filters
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.filters.size() == 0) {
      out << "filters: []\n";
    } else {
      out << "filters:\n";
      for (auto item : msg.filters) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const DepthFiltersStatus & msg, bool use_flow_style = false)
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
  const orbbec_camera_msgs::msg::DepthFiltersStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  orbbec_camera_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use orbbec_camera_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const orbbec_camera_msgs::msg::DepthFiltersStatus & msg)
{
  return orbbec_camera_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<orbbec_camera_msgs::msg::DepthFiltersStatus>()
{
  return "orbbec_camera_msgs::msg::DepthFiltersStatus";
}

template<>
inline const char * name<orbbec_camera_msgs::msg::DepthFiltersStatus>()
{
  return "orbbec_camera_msgs/msg/DepthFiltersStatus";
}

template<>
struct has_fixed_size<orbbec_camera_msgs::msg::DepthFiltersStatus>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<orbbec_camera_msgs::msg::DepthFiltersStatus>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<orbbec_camera_msgs::msg::DepthFiltersStatus>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTERS_STATUS__TRAITS_HPP_
