// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from soarm100_interfaces:action/ExecuteGrasp.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_GRASP__TRAITS_HPP_
#define SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_GRASP__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "soarm100_interfaces/action/detail/execute_grasp__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'approximate_target_pose'
#include "geometry_msgs/msg/detail/pose_stamped__traits.hpp"

namespace soarm100_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const ExecuteGrasp_Goal & msg,
  std::ostream & out)
{
  out << "{";
  // member: target_prompt
  {
    out << "target_prompt: ";
    rosidl_generator_traits::value_to_yaml(msg.target_prompt, out);
    out << ", ";
  }

  // member: enable_avoidance
  {
    out << "enable_avoidance: ";
    rosidl_generator_traits::value_to_yaml(msg.enable_avoidance, out);
    out << ", ";
  }

  // member: approximate_target_pose
  {
    out << "approximate_target_pose: ";
    to_flow_style_yaml(msg.approximate_target_pose, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ExecuteGrasp_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: target_prompt
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "target_prompt: ";
    rosidl_generator_traits::value_to_yaml(msg.target_prompt, out);
    out << "\n";
  }

  // member: enable_avoidance
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "enable_avoidance: ";
    rosidl_generator_traits::value_to_yaml(msg.enable_avoidance, out);
    out << "\n";
  }

  // member: approximate_target_pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "approximate_target_pose:\n";
    to_block_style_yaml(msg.approximate_target_pose, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ExecuteGrasp_Goal & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace soarm100_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use soarm100_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const soarm100_interfaces::action::ExecuteGrasp_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  soarm100_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use soarm100_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const soarm100_interfaces::action::ExecuteGrasp_Goal & msg)
{
  return soarm100_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<soarm100_interfaces::action::ExecuteGrasp_Goal>()
{
  return "soarm100_interfaces::action::ExecuteGrasp_Goal";
}

template<>
inline const char * name<soarm100_interfaces::action::ExecuteGrasp_Goal>()
{
  return "soarm100_interfaces/action/ExecuteGrasp_Goal";
}

template<>
struct has_fixed_size<soarm100_interfaces::action::ExecuteGrasp_Goal>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<soarm100_interfaces::action::ExecuteGrasp_Goal>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<soarm100_interfaces::action::ExecuteGrasp_Goal>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'final_grasp_pose'
// already included above
// #include "geometry_msgs/msg/detail/pose_stamped__traits.hpp"

namespace soarm100_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const ExecuteGrasp_Result & msg,
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

  // member: final_grasp_pose
  {
    out << "final_grasp_pose: ";
    to_flow_style_yaml(msg.final_grasp_pose, out);
    out << ", ";
  }

  // member: lift_height
  {
    out << "lift_height: ";
    rosidl_generator_traits::value_to_yaml(msg.lift_height, out);
    out << ", ";
  }

  // member: attempts
  {
    out << "attempts: ";
    rosidl_generator_traits::value_to_yaml(msg.attempts, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ExecuteGrasp_Result & msg,
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

  // member: final_grasp_pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "final_grasp_pose:\n";
    to_block_style_yaml(msg.final_grasp_pose, out, indentation + 2);
  }

  // member: lift_height
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "lift_height: ";
    rosidl_generator_traits::value_to_yaml(msg.lift_height, out);
    out << "\n";
  }

  // member: attempts
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "attempts: ";
    rosidl_generator_traits::value_to_yaml(msg.attempts, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ExecuteGrasp_Result & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace soarm100_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use soarm100_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const soarm100_interfaces::action::ExecuteGrasp_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  soarm100_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use soarm100_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const soarm100_interfaces::action::ExecuteGrasp_Result & msg)
{
  return soarm100_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<soarm100_interfaces::action::ExecuteGrasp_Result>()
{
  return "soarm100_interfaces::action::ExecuteGrasp_Result";
}

template<>
inline const char * name<soarm100_interfaces::action::ExecuteGrasp_Result>()
{
  return "soarm100_interfaces/action/ExecuteGrasp_Result";
}

template<>
struct has_fixed_size<soarm100_interfaces::action::ExecuteGrasp_Result>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<soarm100_interfaces::action::ExecuteGrasp_Result>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<soarm100_interfaces::action::ExecuteGrasp_Result>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace soarm100_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const ExecuteGrasp_Feedback & msg,
  std::ostream & out)
{
  out << "{";
  // member: stage
  {
    out << "stage: ";
    rosidl_generator_traits::value_to_yaml(msg.stage, out);
    out << ", ";
  }

  // member: target_visible_score
  {
    out << "target_visible_score: ";
    rosidl_generator_traits::value_to_yaml(msg.target_visible_score, out);
    out << ", ";
  }

  // member: grasp_score
  {
    out << "grasp_score: ";
    rosidl_generator_traits::value_to_yaml(msg.grasp_score, out);
    out << ", ";
  }

  // member: tcp_pos_err
  {
    out << "tcp_pos_err: ";
    rosidl_generator_traits::value_to_yaml(msg.tcp_pos_err, out);
    out << ", ";
  }

  // member: tcp_ori_err
  {
    out << "tcp_ori_err: ";
    rosidl_generator_traits::value_to_yaml(msg.tcp_ori_err, out);
    out << ", ";
  }

  // member: sdf_min_dist
  {
    out << "sdf_min_dist: ";
    rosidl_generator_traits::value_to_yaml(msg.sdf_min_dist, out);
    out << ", ";
  }

  // member: cbf_active
  {
    out << "cbf_active: ";
    rosidl_generator_traits::value_to_yaml(msg.cbf_active, out);
    out << ", ";
  }

  // member: tracking_valid
  {
    out << "tracking_valid: ";
    rosidl_generator_traits::value_to_yaml(msg.tracking_valid, out);
    out << ", ";
  }

  // member: replan_running
  {
    out << "replan_running: ";
    rosidl_generator_traits::value_to_yaml(msg.replan_running, out);
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
  const ExecuteGrasp_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: stage
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stage: ";
    rosidl_generator_traits::value_to_yaml(msg.stage, out);
    out << "\n";
  }

  // member: target_visible_score
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "target_visible_score: ";
    rosidl_generator_traits::value_to_yaml(msg.target_visible_score, out);
    out << "\n";
  }

  // member: grasp_score
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "grasp_score: ";
    rosidl_generator_traits::value_to_yaml(msg.grasp_score, out);
    out << "\n";
  }

  // member: tcp_pos_err
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "tcp_pos_err: ";
    rosidl_generator_traits::value_to_yaml(msg.tcp_pos_err, out);
    out << "\n";
  }

  // member: tcp_ori_err
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "tcp_ori_err: ";
    rosidl_generator_traits::value_to_yaml(msg.tcp_ori_err, out);
    out << "\n";
  }

  // member: sdf_min_dist
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sdf_min_dist: ";
    rosidl_generator_traits::value_to_yaml(msg.sdf_min_dist, out);
    out << "\n";
  }

  // member: cbf_active
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "cbf_active: ";
    rosidl_generator_traits::value_to_yaml(msg.cbf_active, out);
    out << "\n";
  }

  // member: tracking_valid
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "tracking_valid: ";
    rosidl_generator_traits::value_to_yaml(msg.tracking_valid, out);
    out << "\n";
  }

  // member: replan_running
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "replan_running: ";
    rosidl_generator_traits::value_to_yaml(msg.replan_running, out);
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

inline std::string to_yaml(const ExecuteGrasp_Feedback & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace soarm100_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use soarm100_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const soarm100_interfaces::action::ExecuteGrasp_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  soarm100_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use soarm100_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const soarm100_interfaces::action::ExecuteGrasp_Feedback & msg)
{
  return soarm100_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<soarm100_interfaces::action::ExecuteGrasp_Feedback>()
{
  return "soarm100_interfaces::action::ExecuteGrasp_Feedback";
}

template<>
inline const char * name<soarm100_interfaces::action::ExecuteGrasp_Feedback>()
{
  return "soarm100_interfaces/action/ExecuteGrasp_Feedback";
}

template<>
struct has_fixed_size<soarm100_interfaces::action::ExecuteGrasp_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<soarm100_interfaces::action::ExecuteGrasp_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<soarm100_interfaces::action::ExecuteGrasp_Feedback>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'goal'
#include "soarm100_interfaces/action/detail/execute_grasp__traits.hpp"

namespace soarm100_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const ExecuteGrasp_SendGoal_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: goal
  {
    out << "goal: ";
    to_flow_style_yaml(msg.goal, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ExecuteGrasp_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: goal
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal:\n";
    to_block_style_yaml(msg.goal, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ExecuteGrasp_SendGoal_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace soarm100_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use soarm100_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  soarm100_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use soarm100_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request & msg)
{
  return soarm100_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request>()
{
  return "soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request";
}

template<>
inline const char * name<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request>()
{
  return "soarm100_interfaces/action/ExecuteGrasp_SendGoal_Request";
}

template<>
struct has_fixed_size<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request>
  : std::integral_constant<bool, has_fixed_size<soarm100_interfaces::action::ExecuteGrasp_Goal>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request>
  : std::integral_constant<bool, has_bounded_size<soarm100_interfaces::action::ExecuteGrasp_Goal>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace soarm100_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const ExecuteGrasp_SendGoal_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: accepted
  {
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << ", ";
  }

  // member: stamp
  {
    out << "stamp: ";
    to_flow_style_yaml(msg.stamp, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ExecuteGrasp_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: accepted
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << "\n";
  }

  // member: stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp:\n";
    to_block_style_yaml(msg.stamp, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ExecuteGrasp_SendGoal_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace soarm100_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use soarm100_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  soarm100_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use soarm100_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response & msg)
{
  return soarm100_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response>()
{
  return "soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response";
}

template<>
inline const char * name<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response>()
{
  return "soarm100_interfaces/action/ExecuteGrasp_SendGoal_Response";
}

template<>
struct has_fixed_size<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response>
  : std::integral_constant<bool, has_fixed_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct has_bounded_size<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response>
  : std::integral_constant<bool, has_bounded_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct is_message<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<soarm100_interfaces::action::ExecuteGrasp_SendGoal>()
{
  return "soarm100_interfaces::action::ExecuteGrasp_SendGoal";
}

template<>
inline const char * name<soarm100_interfaces::action::ExecuteGrasp_SendGoal>()
{
  return "soarm100_interfaces/action/ExecuteGrasp_SendGoal";
}

template<>
struct has_fixed_size<soarm100_interfaces::action::ExecuteGrasp_SendGoal>
  : std::integral_constant<
    bool,
    has_fixed_size<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request>::value &&
    has_fixed_size<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response>::value
  >
{
};

template<>
struct has_bounded_size<soarm100_interfaces::action::ExecuteGrasp_SendGoal>
  : std::integral_constant<
    bool,
    has_bounded_size<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request>::value &&
    has_bounded_size<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response>::value
  >
{
};

template<>
struct is_service<soarm100_interfaces::action::ExecuteGrasp_SendGoal>
  : std::true_type
{
};

template<>
struct is_service_request<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request>
  : std::true_type
{
};

template<>
struct is_service_response<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"

namespace soarm100_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const ExecuteGrasp_GetResult_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ExecuteGrasp_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ExecuteGrasp_GetResult_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace soarm100_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use soarm100_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const soarm100_interfaces::action::ExecuteGrasp_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  soarm100_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use soarm100_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const soarm100_interfaces::action::ExecuteGrasp_GetResult_Request & msg)
{
  return soarm100_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<soarm100_interfaces::action::ExecuteGrasp_GetResult_Request>()
{
  return "soarm100_interfaces::action::ExecuteGrasp_GetResult_Request";
}

template<>
inline const char * name<soarm100_interfaces::action::ExecuteGrasp_GetResult_Request>()
{
  return "soarm100_interfaces/action/ExecuteGrasp_GetResult_Request";
}

template<>
struct has_fixed_size<soarm100_interfaces::action::ExecuteGrasp_GetResult_Request>
  : std::integral_constant<bool, has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<soarm100_interfaces::action::ExecuteGrasp_GetResult_Request>
  : std::integral_constant<bool, has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<soarm100_interfaces::action::ExecuteGrasp_GetResult_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'result'
// already included above
// #include "soarm100_interfaces/action/detail/execute_grasp__traits.hpp"

namespace soarm100_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const ExecuteGrasp_GetResult_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << ", ";
  }

  // member: result
  {
    out << "result: ";
    to_flow_style_yaml(msg.result, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ExecuteGrasp_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << "\n";
  }

  // member: result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result:\n";
    to_block_style_yaml(msg.result, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ExecuteGrasp_GetResult_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace soarm100_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use soarm100_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const soarm100_interfaces::action::ExecuteGrasp_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  soarm100_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use soarm100_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const soarm100_interfaces::action::ExecuteGrasp_GetResult_Response & msg)
{
  return soarm100_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<soarm100_interfaces::action::ExecuteGrasp_GetResult_Response>()
{
  return "soarm100_interfaces::action::ExecuteGrasp_GetResult_Response";
}

template<>
inline const char * name<soarm100_interfaces::action::ExecuteGrasp_GetResult_Response>()
{
  return "soarm100_interfaces/action/ExecuteGrasp_GetResult_Response";
}

template<>
struct has_fixed_size<soarm100_interfaces::action::ExecuteGrasp_GetResult_Response>
  : std::integral_constant<bool, has_fixed_size<soarm100_interfaces::action::ExecuteGrasp_Result>::value> {};

template<>
struct has_bounded_size<soarm100_interfaces::action::ExecuteGrasp_GetResult_Response>
  : std::integral_constant<bool, has_bounded_size<soarm100_interfaces::action::ExecuteGrasp_Result>::value> {};

template<>
struct is_message<soarm100_interfaces::action::ExecuteGrasp_GetResult_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<soarm100_interfaces::action::ExecuteGrasp_GetResult>()
{
  return "soarm100_interfaces::action::ExecuteGrasp_GetResult";
}

template<>
inline const char * name<soarm100_interfaces::action::ExecuteGrasp_GetResult>()
{
  return "soarm100_interfaces/action/ExecuteGrasp_GetResult";
}

template<>
struct has_fixed_size<soarm100_interfaces::action::ExecuteGrasp_GetResult>
  : std::integral_constant<
    bool,
    has_fixed_size<soarm100_interfaces::action::ExecuteGrasp_GetResult_Request>::value &&
    has_fixed_size<soarm100_interfaces::action::ExecuteGrasp_GetResult_Response>::value
  >
{
};

template<>
struct has_bounded_size<soarm100_interfaces::action::ExecuteGrasp_GetResult>
  : std::integral_constant<
    bool,
    has_bounded_size<soarm100_interfaces::action::ExecuteGrasp_GetResult_Request>::value &&
    has_bounded_size<soarm100_interfaces::action::ExecuteGrasp_GetResult_Response>::value
  >
{
};

template<>
struct is_service<soarm100_interfaces::action::ExecuteGrasp_GetResult>
  : std::true_type
{
};

template<>
struct is_service_request<soarm100_interfaces::action::ExecuteGrasp_GetResult_Request>
  : std::true_type
{
};

template<>
struct is_service_response<soarm100_interfaces::action::ExecuteGrasp_GetResult_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'feedback'
// already included above
// #include "soarm100_interfaces/action/detail/execute_grasp__traits.hpp"

namespace soarm100_interfaces
{

namespace action
{

inline void to_flow_style_yaml(
  const ExecuteGrasp_FeedbackMessage & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: feedback
  {
    out << "feedback: ";
    to_flow_style_yaml(msg.feedback, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ExecuteGrasp_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: feedback
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "feedback:\n";
    to_block_style_yaml(msg.feedback, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ExecuteGrasp_FeedbackMessage & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace soarm100_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use soarm100_interfaces::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  soarm100_interfaces::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use soarm100_interfaces::action::to_yaml() instead")]]
inline std::string to_yaml(const soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage & msg)
{
  return soarm100_interfaces::action::to_yaml(msg);
}

template<>
inline const char * data_type<soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage>()
{
  return "soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage";
}

template<>
inline const char * name<soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage>()
{
  return "soarm100_interfaces/action/ExecuteGrasp_FeedbackMessage";
}

template<>
struct has_fixed_size<soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage>
  : std::integral_constant<bool, has_fixed_size<soarm100_interfaces::action::ExecuteGrasp_Feedback>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage>
  : std::integral_constant<bool, has_bounded_size<soarm100_interfaces::action::ExecuteGrasp_Feedback>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage>
  : std::true_type {};

}  // namespace rosidl_generator_traits


namespace rosidl_generator_traits
{

template<>
struct is_action<soarm100_interfaces::action::ExecuteGrasp>
  : std::true_type
{
};

template<>
struct is_action_goal<soarm100_interfaces::action::ExecuteGrasp_Goal>
  : std::true_type
{
};

template<>
struct is_action_result<soarm100_interfaces::action::ExecuteGrasp_Result>
  : std::true_type
{
};

template<>
struct is_action_feedback<soarm100_interfaces::action::ExecuteGrasp_Feedback>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits


#endif  // SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_GRASP__TRAITS_HPP_
