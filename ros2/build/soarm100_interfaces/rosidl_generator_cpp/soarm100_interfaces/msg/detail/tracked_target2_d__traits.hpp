// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from soarm100_interfaces:msg/TrackedTarget2D.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__MSG__DETAIL__TRACKED_TARGET2_D__TRAITS_HPP_
#define SOARM100_INTERFACES__MSG__DETAIL__TRACKED_TARGET2_D__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "soarm100_interfaces/msg/detail/tracked_target2_d__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace soarm100_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const TrackedTarget2D & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: valid
  {
    out << "valid: ";
    rosidl_generator_traits::value_to_yaml(msg.valid, out);
    out << ", ";
  }

  // member: u
  {
    out << "u: ";
    rosidl_generator_traits::value_to_yaml(msg.u, out);
    out << ", ";
  }

  // member: v
  {
    out << "v: ";
    rosidl_generator_traits::value_to_yaml(msg.v, out);
    out << ", ";
  }

  // member: reference_u
  {
    out << "reference_u: ";
    rosidl_generator_traits::value_to_yaml(msg.reference_u, out);
    out << ", ";
  }

  // member: reference_v
  {
    out << "reference_v: ";
    rosidl_generator_traits::value_to_yaml(msg.reference_v, out);
    out << ", ";
  }

  // member: delta_u
  {
    out << "delta_u: ";
    rosidl_generator_traits::value_to_yaml(msg.delta_u, out);
    out << ", ";
  }

  // member: delta_v
  {
    out << "delta_v: ";
    rosidl_generator_traits::value_to_yaml(msg.delta_v, out);
    out << ", ";
  }

  // member: width
  {
    out << "width: ";
    rosidl_generator_traits::value_to_yaml(msg.width, out);
    out << ", ";
  }

  // member: height
  {
    out << "height: ";
    rosidl_generator_traits::value_to_yaml(msg.height, out);
    out << ", ";
  }

  // member: image_width
  {
    out << "image_width: ";
    rosidl_generator_traits::value_to_yaml(msg.image_width, out);
    out << ", ";
  }

  // member: image_height
  {
    out << "image_height: ";
    rosidl_generator_traits::value_to_yaml(msg.image_height, out);
    out << ", ";
  }

  // member: confidence
  {
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
    out << ", ";
  }

  // member: lost_frames
  {
    out << "lost_frames: ";
    rosidl_generator_traits::value_to_yaml(msg.lost_frames, out);
    out << ", ";
  }

  // member: replan_required
  {
    out << "replan_required: ";
    rosidl_generator_traits::value_to_yaml(msg.replan_required, out);
    out << ", ";
  }

  // member: reason
  {
    out << "reason: ";
    rosidl_generator_traits::value_to_yaml(msg.reason, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TrackedTarget2D & msg,
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

  // member: valid
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "valid: ";
    rosidl_generator_traits::value_to_yaml(msg.valid, out);
    out << "\n";
  }

  // member: u
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "u: ";
    rosidl_generator_traits::value_to_yaml(msg.u, out);
    out << "\n";
  }

  // member: v
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "v: ";
    rosidl_generator_traits::value_to_yaml(msg.v, out);
    out << "\n";
  }

  // member: reference_u
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "reference_u: ";
    rosidl_generator_traits::value_to_yaml(msg.reference_u, out);
    out << "\n";
  }

  // member: reference_v
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "reference_v: ";
    rosidl_generator_traits::value_to_yaml(msg.reference_v, out);
    out << "\n";
  }

  // member: delta_u
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "delta_u: ";
    rosidl_generator_traits::value_to_yaml(msg.delta_u, out);
    out << "\n";
  }

  // member: delta_v
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "delta_v: ";
    rosidl_generator_traits::value_to_yaml(msg.delta_v, out);
    out << "\n";
  }

  // member: width
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "width: ";
    rosidl_generator_traits::value_to_yaml(msg.width, out);
    out << "\n";
  }

  // member: height
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "height: ";
    rosidl_generator_traits::value_to_yaml(msg.height, out);
    out << "\n";
  }

  // member: image_width
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "image_width: ";
    rosidl_generator_traits::value_to_yaml(msg.image_width, out);
    out << "\n";
  }

  // member: image_height
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "image_height: ";
    rosidl_generator_traits::value_to_yaml(msg.image_height, out);
    out << "\n";
  }

  // member: confidence
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
    out << "\n";
  }

  // member: lost_frames
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "lost_frames: ";
    rosidl_generator_traits::value_to_yaml(msg.lost_frames, out);
    out << "\n";
  }

  // member: replan_required
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "replan_required: ";
    rosidl_generator_traits::value_to_yaml(msg.replan_required, out);
    out << "\n";
  }

  // member: reason
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "reason: ";
    rosidl_generator_traits::value_to_yaml(msg.reason, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TrackedTarget2D & msg, bool use_flow_style = false)
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

}  // namespace soarm100_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use soarm100_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const soarm100_interfaces::msg::TrackedTarget2D & msg,
  std::ostream & out, size_t indentation = 0)
{
  soarm100_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use soarm100_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const soarm100_interfaces::msg::TrackedTarget2D & msg)
{
  return soarm100_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<soarm100_interfaces::msg::TrackedTarget2D>()
{
  return "soarm100_interfaces::msg::TrackedTarget2D";
}

template<>
inline const char * name<soarm100_interfaces::msg::TrackedTarget2D>()
{
  return "soarm100_interfaces/msg/TrackedTarget2D";
}

template<>
struct has_fixed_size<soarm100_interfaces::msg::TrackedTarget2D>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<soarm100_interfaces::msg::TrackedTarget2D>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<soarm100_interfaces::msg::TrackedTarget2D>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SOARM100_INTERFACES__MSG__DETAIL__TRACKED_TARGET2_D__TRAITS_HPP_
