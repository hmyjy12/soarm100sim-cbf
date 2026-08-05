// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from soarm100_interfaces:srv/SetHardwareTorque.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__SRV__DETAIL__SET_HARDWARE_TORQUE__TRAITS_HPP_
#define SOARM100_INTERFACES__SRV__DETAIL__SET_HARDWARE_TORQUE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "soarm100_interfaces/srv/detail/set_hardware_torque__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace soarm100_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetHardwareTorque_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: enabled
  {
    out << "enabled: ";
    rosidl_generator_traits::value_to_yaml(msg.enabled, out);
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
  const SetHardwareTorque_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: enabled
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "enabled: ";
    rosidl_generator_traits::value_to_yaml(msg.enabled, out);
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

inline std::string to_yaml(const SetHardwareTorque_Request & msg, bool use_flow_style = false)
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
  const soarm100_interfaces::srv::SetHardwareTorque_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  soarm100_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use soarm100_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const soarm100_interfaces::srv::SetHardwareTorque_Request & msg)
{
  return soarm100_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<soarm100_interfaces::srv::SetHardwareTorque_Request>()
{
  return "soarm100_interfaces::srv::SetHardwareTorque_Request";
}

template<>
inline const char * name<soarm100_interfaces::srv::SetHardwareTorque_Request>()
{
  return "soarm100_interfaces/srv/SetHardwareTorque_Request";
}

template<>
struct has_fixed_size<soarm100_interfaces::srv::SetHardwareTorque_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<soarm100_interfaces::srv::SetHardwareTorque_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<soarm100_interfaces::srv::SetHardwareTorque_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace soarm100_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const SetHardwareTorque_Response & msg,
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
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SetHardwareTorque_Response & msg,
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
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SetHardwareTorque_Response & msg, bool use_flow_style = false)
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
  const soarm100_interfaces::srv::SetHardwareTorque_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  soarm100_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use soarm100_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const soarm100_interfaces::srv::SetHardwareTorque_Response & msg)
{
  return soarm100_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<soarm100_interfaces::srv::SetHardwareTorque_Response>()
{
  return "soarm100_interfaces::srv::SetHardwareTorque_Response";
}

template<>
inline const char * name<soarm100_interfaces::srv::SetHardwareTorque_Response>()
{
  return "soarm100_interfaces/srv/SetHardwareTorque_Response";
}

template<>
struct has_fixed_size<soarm100_interfaces::srv::SetHardwareTorque_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<soarm100_interfaces::srv::SetHardwareTorque_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<soarm100_interfaces::srv::SetHardwareTorque_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<soarm100_interfaces::srv::SetHardwareTorque>()
{
  return "soarm100_interfaces::srv::SetHardwareTorque";
}

template<>
inline const char * name<soarm100_interfaces::srv::SetHardwareTorque>()
{
  return "soarm100_interfaces/srv/SetHardwareTorque";
}

template<>
struct has_fixed_size<soarm100_interfaces::srv::SetHardwareTorque>
  : std::integral_constant<
    bool,
    has_fixed_size<soarm100_interfaces::srv::SetHardwareTorque_Request>::value &&
    has_fixed_size<soarm100_interfaces::srv::SetHardwareTorque_Response>::value
  >
{
};

template<>
struct has_bounded_size<soarm100_interfaces::srv::SetHardwareTorque>
  : std::integral_constant<
    bool,
    has_bounded_size<soarm100_interfaces::srv::SetHardwareTorque_Request>::value &&
    has_bounded_size<soarm100_interfaces::srv::SetHardwareTorque_Response>::value
  >
{
};

template<>
struct is_service<soarm100_interfaces::srv::SetHardwareTorque>
  : std::true_type
{
};

template<>
struct is_service_request<soarm100_interfaces::srv::SetHardwareTorque_Request>
  : std::true_type
{
};

template<>
struct is_service_response<soarm100_interfaces::srv::SetHardwareTorque_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // SOARM100_INTERFACES__SRV__DETAIL__SET_HARDWARE_TORQUE__TRAITS_HPP_
