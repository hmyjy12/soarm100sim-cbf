// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from soarm100_interfaces:srv/MoveSingleJoint.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__SRV__DETAIL__MOVE_SINGLE_JOINT__TRAITS_HPP_
#define SOARM100_INTERFACES__SRV__DETAIL__MOVE_SINGLE_JOINT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "soarm100_interfaces/srv/detail/move_single_joint__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace soarm100_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const MoveSingleJoint_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: joint
  {
    out << "joint: ";
    rosidl_generator_traits::value_to_yaml(msg.joint, out);
    out << ", ";
  }

  // member: delta_deg
  {
    out << "delta_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.delta_deg, out);
    out << ", ";
  }

  // member: duration
  {
    out << "duration: ";
    rosidl_generator_traits::value_to_yaml(msg.duration, out);
    out << ", ";
  }

  // member: hold
  {
    out << "hold: ";
    rosidl_generator_traits::value_to_yaml(msg.hold, out);
    out << ", ";
  }

  // member: confirmation
  {
    out << "confirmation: ";
    rosidl_generator_traits::value_to_yaml(msg.confirmation, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MoveSingleJoint_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: joint
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "joint: ";
    rosidl_generator_traits::value_to_yaml(msg.joint, out);
    out << "\n";
  }

  // member: delta_deg
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "delta_deg: ";
    rosidl_generator_traits::value_to_yaml(msg.delta_deg, out);
    out << "\n";
  }

  // member: duration
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "duration: ";
    rosidl_generator_traits::value_to_yaml(msg.duration, out);
    out << "\n";
  }

  // member: hold
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "hold: ";
    rosidl_generator_traits::value_to_yaml(msg.hold, out);
    out << "\n";
  }

  // member: confirmation
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "confirmation: ";
    rosidl_generator_traits::value_to_yaml(msg.confirmation, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MoveSingleJoint_Request & msg, bool use_flow_style = false)
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

}  // namespace soarm100_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use soarm100_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const soarm100_interfaces::srv::MoveSingleJoint_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  soarm100_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use soarm100_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const soarm100_interfaces::srv::MoveSingleJoint_Request & msg)
{
  return soarm100_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<soarm100_interfaces::srv::MoveSingleJoint_Request>()
{
  return "soarm100_interfaces::srv::MoveSingleJoint_Request";
}

template<>
inline const char * name<soarm100_interfaces::srv::MoveSingleJoint_Request>()
{
  return "soarm100_interfaces/srv/MoveSingleJoint_Request";
}

template<>
struct has_fixed_size<soarm100_interfaces::srv::MoveSingleJoint_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<soarm100_interfaces::srv::MoveSingleJoint_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<soarm100_interfaces::srv::MoveSingleJoint_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace soarm100_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const MoveSingleJoint_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: reason
  {
    out << "reason: ";
    rosidl_generator_traits::value_to_yaml(msg.reason, out);
    out << ", ";
  }

  // member: log_path
  {
    out << "log_path: ";
    rosidl_generator_traits::value_to_yaml(msg.log_path, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const MoveSingleJoint_Response & msg,
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

  // member: reason
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "reason: ";
    rosidl_generator_traits::value_to_yaml(msg.reason, out);
    out << "\n";
  }

  // member: log_path
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "log_path: ";
    rosidl_generator_traits::value_to_yaml(msg.log_path, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MoveSingleJoint_Response & msg, bool use_flow_style = false)
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

}  // namespace soarm100_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use soarm100_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const soarm100_interfaces::srv::MoveSingleJoint_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  soarm100_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use soarm100_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const soarm100_interfaces::srv::MoveSingleJoint_Response & msg)
{
  return soarm100_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<soarm100_interfaces::srv::MoveSingleJoint_Response>()
{
  return "soarm100_interfaces::srv::MoveSingleJoint_Response";
}

template<>
inline const char * name<soarm100_interfaces::srv::MoveSingleJoint_Response>()
{
  return "soarm100_interfaces/srv/MoveSingleJoint_Response";
}

template<>
struct has_fixed_size<soarm100_interfaces::srv::MoveSingleJoint_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<soarm100_interfaces::srv::MoveSingleJoint_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<soarm100_interfaces::srv::MoveSingleJoint_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<soarm100_interfaces::srv::MoveSingleJoint>()
{
  return "soarm100_interfaces::srv::MoveSingleJoint";
}

template<>
inline const char * name<soarm100_interfaces::srv::MoveSingleJoint>()
{
  return "soarm100_interfaces/srv/MoveSingleJoint";
}

template<>
struct has_fixed_size<soarm100_interfaces::srv::MoveSingleJoint>
  : std::integral_constant<
    bool,
    has_fixed_size<soarm100_interfaces::srv::MoveSingleJoint_Request>::value &&
    has_fixed_size<soarm100_interfaces::srv::MoveSingleJoint_Response>::value
  >
{
};

template<>
struct has_bounded_size<soarm100_interfaces::srv::MoveSingleJoint>
  : std::integral_constant<
    bool,
    has_bounded_size<soarm100_interfaces::srv::MoveSingleJoint_Request>::value &&
    has_bounded_size<soarm100_interfaces::srv::MoveSingleJoint_Response>::value
  >
{
};

template<>
struct is_service<soarm100_interfaces::srv::MoveSingleJoint>
  : std::true_type
{
};

template<>
struct is_service_request<soarm100_interfaces::srv::MoveSingleJoint_Request>
  : std::true_type
{
};

template<>
struct is_service_response<soarm100_interfaces::srv::MoveSingleJoint_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // SOARM100_INTERFACES__SRV__DETAIL__MOVE_SINGLE_JOINT__TRAITS_HPP_
