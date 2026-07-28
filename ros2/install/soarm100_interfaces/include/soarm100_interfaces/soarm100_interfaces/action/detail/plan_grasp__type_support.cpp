// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from soarm100_interfaces:action/PlanGrasp.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "soarm100_interfaces/action/detail/plan_grasp__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace soarm100_interfaces
{

namespace action
{

namespace rosidl_typesupport_introspection_cpp
{

void PlanGrasp_Goal_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) soarm100_interfaces::action::PlanGrasp_Goal(_init);
}

void PlanGrasp_Goal_fini_function(void * message_memory)
{
  auto typed_message = static_cast<soarm100_interfaces::action::PlanGrasp_Goal *>(message_memory);
  typed_message->~PlanGrasp_Goal();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember PlanGrasp_Goal_message_member_array[4] = {
  {
    "target_prompt",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_Goal, target_prompt),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "approximate_target_pose",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::PoseStamped>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_Goal, approximate_target_pose),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "target_cloud",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<sensor_msgs::msg::PointCloud2>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_Goal, target_cloud),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "top_k",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT16,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_Goal, top_k),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers PlanGrasp_Goal_message_members = {
  "soarm100_interfaces::action",  // message namespace
  "PlanGrasp_Goal",  // message name
  4,  // number of fields
  sizeof(soarm100_interfaces::action::PlanGrasp_Goal),
  PlanGrasp_Goal_message_member_array,  // message members
  PlanGrasp_Goal_init_function,  // function to initialize message memory (memory has to be allocated)
  PlanGrasp_Goal_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t PlanGrasp_Goal_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &PlanGrasp_Goal_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace action

}  // namespace soarm100_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<soarm100_interfaces::action::PlanGrasp_Goal>()
{
  return &::soarm100_interfaces::action::rosidl_typesupport_introspection_cpp::PlanGrasp_Goal_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, soarm100_interfaces, action, PlanGrasp_Goal)() {
  return &::soarm100_interfaces::action::rosidl_typesupport_introspection_cpp::PlanGrasp_Goal_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "array"
// already included above
// #include "cstddef"
// already included above
// #include "string"
// already included above
// #include "vector"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__struct.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/field_types.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace soarm100_interfaces
{

namespace action
{

namespace rosidl_typesupport_introspection_cpp
{

void PlanGrasp_Result_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) soarm100_interfaces::action::PlanGrasp_Result(_init);
}

void PlanGrasp_Result_fini_function(void * message_memory)
{
  auto typed_message = static_cast<soarm100_interfaces::action::PlanGrasp_Result *>(message_memory);
  typed_message->~PlanGrasp_Result();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember PlanGrasp_Result_message_member_array[8] = {
  {
    "success",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_Result, success),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "reason",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_Result, reason),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "selected_grasp_pose",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::PoseStamped>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_Result, selected_grasp_pose),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "selected_pregrasp_pose",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::PoseStamped>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_Result, selected_pregrasp_pose),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "target_center_pose",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<geometry_msgs::msg::PoseStamped>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_Result, target_center_pose),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "grasp_score",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_Result, grasp_score),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "gripper_width",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_Result, gripper_width),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "candidate_count",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT16,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_Result, candidate_count),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers PlanGrasp_Result_message_members = {
  "soarm100_interfaces::action",  // message namespace
  "PlanGrasp_Result",  // message name
  8,  // number of fields
  sizeof(soarm100_interfaces::action::PlanGrasp_Result),
  PlanGrasp_Result_message_member_array,  // message members
  PlanGrasp_Result_init_function,  // function to initialize message memory (memory has to be allocated)
  PlanGrasp_Result_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t PlanGrasp_Result_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &PlanGrasp_Result_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace action

}  // namespace soarm100_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<soarm100_interfaces::action::PlanGrasp_Result>()
{
  return &::soarm100_interfaces::action::rosidl_typesupport_introspection_cpp::PlanGrasp_Result_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, soarm100_interfaces, action, PlanGrasp_Result)() {
  return &::soarm100_interfaces::action::rosidl_typesupport_introspection_cpp::PlanGrasp_Result_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "array"
// already included above
// #include "cstddef"
// already included above
// #include "string"
// already included above
// #include "vector"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__struct.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/field_types.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace soarm100_interfaces
{

namespace action
{

namespace rosidl_typesupport_introspection_cpp
{

void PlanGrasp_Feedback_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) soarm100_interfaces::action::PlanGrasp_Feedback(_init);
}

void PlanGrasp_Feedback_fini_function(void * message_memory)
{
  auto typed_message = static_cast<soarm100_interfaces::action::PlanGrasp_Feedback *>(message_memory);
  typed_message->~PlanGrasp_Feedback();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember PlanGrasp_Feedback_message_member_array[4] = {
  {
    "stage",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_Feedback, stage),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "candidate_count",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_UINT16,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_Feedback, candidate_count),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "best_score",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_Feedback, best_score),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "reason",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_Feedback, reason),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers PlanGrasp_Feedback_message_members = {
  "soarm100_interfaces::action",  // message namespace
  "PlanGrasp_Feedback",  // message name
  4,  // number of fields
  sizeof(soarm100_interfaces::action::PlanGrasp_Feedback),
  PlanGrasp_Feedback_message_member_array,  // message members
  PlanGrasp_Feedback_init_function,  // function to initialize message memory (memory has to be allocated)
  PlanGrasp_Feedback_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t PlanGrasp_Feedback_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &PlanGrasp_Feedback_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace action

}  // namespace soarm100_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<soarm100_interfaces::action::PlanGrasp_Feedback>()
{
  return &::soarm100_interfaces::action::rosidl_typesupport_introspection_cpp::PlanGrasp_Feedback_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, soarm100_interfaces, action, PlanGrasp_Feedback)() {
  return &::soarm100_interfaces::action::rosidl_typesupport_introspection_cpp::PlanGrasp_Feedback_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "array"
// already included above
// #include "cstddef"
// already included above
// #include "string"
// already included above
// #include "vector"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__struct.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/field_types.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace soarm100_interfaces
{

namespace action
{

namespace rosidl_typesupport_introspection_cpp
{

void PlanGrasp_SendGoal_Request_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) soarm100_interfaces::action::PlanGrasp_SendGoal_Request(_init);
}

void PlanGrasp_SendGoal_Request_fini_function(void * message_memory)
{
  auto typed_message = static_cast<soarm100_interfaces::action::PlanGrasp_SendGoal_Request *>(message_memory);
  typed_message->~PlanGrasp_SendGoal_Request();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember PlanGrasp_SendGoal_Request_message_member_array[2] = {
  {
    "goal_id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<unique_identifier_msgs::msg::UUID>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_SendGoal_Request, goal_id),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "goal",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<soarm100_interfaces::action::PlanGrasp_Goal>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_SendGoal_Request, goal),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers PlanGrasp_SendGoal_Request_message_members = {
  "soarm100_interfaces::action",  // message namespace
  "PlanGrasp_SendGoal_Request",  // message name
  2,  // number of fields
  sizeof(soarm100_interfaces::action::PlanGrasp_SendGoal_Request),
  PlanGrasp_SendGoal_Request_message_member_array,  // message members
  PlanGrasp_SendGoal_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  PlanGrasp_SendGoal_Request_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t PlanGrasp_SendGoal_Request_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &PlanGrasp_SendGoal_Request_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace action

}  // namespace soarm100_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<soarm100_interfaces::action::PlanGrasp_SendGoal_Request>()
{
  return &::soarm100_interfaces::action::rosidl_typesupport_introspection_cpp::PlanGrasp_SendGoal_Request_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, soarm100_interfaces, action, PlanGrasp_SendGoal_Request)() {
  return &::soarm100_interfaces::action::rosidl_typesupport_introspection_cpp::PlanGrasp_SendGoal_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "array"
// already included above
// #include "cstddef"
// already included above
// #include "string"
// already included above
// #include "vector"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__struct.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/field_types.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace soarm100_interfaces
{

namespace action
{

namespace rosidl_typesupport_introspection_cpp
{

void PlanGrasp_SendGoal_Response_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) soarm100_interfaces::action::PlanGrasp_SendGoal_Response(_init);
}

void PlanGrasp_SendGoal_Response_fini_function(void * message_memory)
{
  auto typed_message = static_cast<soarm100_interfaces::action::PlanGrasp_SendGoal_Response *>(message_memory);
  typed_message->~PlanGrasp_SendGoal_Response();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember PlanGrasp_SendGoal_Response_message_member_array[2] = {
  {
    "accepted",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_SendGoal_Response, accepted),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "stamp",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<builtin_interfaces::msg::Time>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_SendGoal_Response, stamp),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers PlanGrasp_SendGoal_Response_message_members = {
  "soarm100_interfaces::action",  // message namespace
  "PlanGrasp_SendGoal_Response",  // message name
  2,  // number of fields
  sizeof(soarm100_interfaces::action::PlanGrasp_SendGoal_Response),
  PlanGrasp_SendGoal_Response_message_member_array,  // message members
  PlanGrasp_SendGoal_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  PlanGrasp_SendGoal_Response_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t PlanGrasp_SendGoal_Response_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &PlanGrasp_SendGoal_Response_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace action

}  // namespace soarm100_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<soarm100_interfaces::action::PlanGrasp_SendGoal_Response>()
{
  return &::soarm100_interfaces::action::rosidl_typesupport_introspection_cpp::PlanGrasp_SendGoal_Response_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, soarm100_interfaces, action, PlanGrasp_SendGoal_Response)() {
  return &::soarm100_interfaces::action::rosidl_typesupport_introspection_cpp::PlanGrasp_SendGoal_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "rosidl_typesupport_introspection_cpp/visibility_control.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__struct.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/service_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/service_type_support_decl.hpp"

namespace soarm100_interfaces
{

namespace action
{

namespace rosidl_typesupport_introspection_cpp
{

// this is intentionally not const to allow initialization later to prevent an initialization race
static ::rosidl_typesupport_introspection_cpp::ServiceMembers PlanGrasp_SendGoal_service_members = {
  "soarm100_interfaces::action",  // service namespace
  "PlanGrasp_SendGoal",  // service name
  // these two fields are initialized below on the first access
  // see get_service_type_support_handle<soarm100_interfaces::action::PlanGrasp_SendGoal>()
  nullptr,  // request message
  nullptr  // response message
};

static const rosidl_service_type_support_t PlanGrasp_SendGoal_service_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &PlanGrasp_SendGoal_service_members,
  get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace action

}  // namespace soarm100_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<soarm100_interfaces::action::PlanGrasp_SendGoal>()
{
  // get a handle to the value to be returned
  auto service_type_support =
    &::soarm100_interfaces::action::rosidl_typesupport_introspection_cpp::PlanGrasp_SendGoal_service_type_support_handle;
  // get a non-const and properly typed version of the data void *
  auto service_members = const_cast<::rosidl_typesupport_introspection_cpp::ServiceMembers *>(
    static_cast<const ::rosidl_typesupport_introspection_cpp::ServiceMembers *>(
      service_type_support->data));
  // make sure that both the request_members_ and the response_members_ are initialized
  // if they are not, initialize them
  if (
    service_members->request_members_ == nullptr ||
    service_members->response_members_ == nullptr)
  {
    // initialize the request_members_ with the static function from the external library
    service_members->request_members_ = static_cast<
      const ::rosidl_typesupport_introspection_cpp::MessageMembers *
      >(
      ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<
        ::soarm100_interfaces::action::PlanGrasp_SendGoal_Request
      >()->data
      );
    // initialize the response_members_ with the static function from the external library
    service_members->response_members_ = static_cast<
      const ::rosidl_typesupport_introspection_cpp::MessageMembers *
      >(
      ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<
        ::soarm100_interfaces::action::PlanGrasp_SendGoal_Response
      >()->data
      );
  }
  // finally return the properly initialized service_type_support handle
  return service_type_support;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, soarm100_interfaces, action, PlanGrasp_SendGoal)() {
  return ::rosidl_typesupport_introspection_cpp::get_service_type_support_handle<soarm100_interfaces::action::PlanGrasp_SendGoal>();
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "array"
// already included above
// #include "cstddef"
// already included above
// #include "string"
// already included above
// #include "vector"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__struct.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/field_types.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace soarm100_interfaces
{

namespace action
{

namespace rosidl_typesupport_introspection_cpp
{

void PlanGrasp_GetResult_Request_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) soarm100_interfaces::action::PlanGrasp_GetResult_Request(_init);
}

void PlanGrasp_GetResult_Request_fini_function(void * message_memory)
{
  auto typed_message = static_cast<soarm100_interfaces::action::PlanGrasp_GetResult_Request *>(message_memory);
  typed_message->~PlanGrasp_GetResult_Request();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember PlanGrasp_GetResult_Request_message_member_array[1] = {
  {
    "goal_id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<unique_identifier_msgs::msg::UUID>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_GetResult_Request, goal_id),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers PlanGrasp_GetResult_Request_message_members = {
  "soarm100_interfaces::action",  // message namespace
  "PlanGrasp_GetResult_Request",  // message name
  1,  // number of fields
  sizeof(soarm100_interfaces::action::PlanGrasp_GetResult_Request),
  PlanGrasp_GetResult_Request_message_member_array,  // message members
  PlanGrasp_GetResult_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  PlanGrasp_GetResult_Request_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t PlanGrasp_GetResult_Request_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &PlanGrasp_GetResult_Request_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace action

}  // namespace soarm100_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<soarm100_interfaces::action::PlanGrasp_GetResult_Request>()
{
  return &::soarm100_interfaces::action::rosidl_typesupport_introspection_cpp::PlanGrasp_GetResult_Request_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, soarm100_interfaces, action, PlanGrasp_GetResult_Request)() {
  return &::soarm100_interfaces::action::rosidl_typesupport_introspection_cpp::PlanGrasp_GetResult_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "array"
// already included above
// #include "cstddef"
// already included above
// #include "string"
// already included above
// #include "vector"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__struct.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/field_types.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace soarm100_interfaces
{

namespace action
{

namespace rosidl_typesupport_introspection_cpp
{

void PlanGrasp_GetResult_Response_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) soarm100_interfaces::action::PlanGrasp_GetResult_Response(_init);
}

void PlanGrasp_GetResult_Response_fini_function(void * message_memory)
{
  auto typed_message = static_cast<soarm100_interfaces::action::PlanGrasp_GetResult_Response *>(message_memory);
  typed_message->~PlanGrasp_GetResult_Response();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember PlanGrasp_GetResult_Response_message_member_array[2] = {
  {
    "status",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_GetResult_Response, status),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "result",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<soarm100_interfaces::action::PlanGrasp_Result>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_GetResult_Response, result),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers PlanGrasp_GetResult_Response_message_members = {
  "soarm100_interfaces::action",  // message namespace
  "PlanGrasp_GetResult_Response",  // message name
  2,  // number of fields
  sizeof(soarm100_interfaces::action::PlanGrasp_GetResult_Response),
  PlanGrasp_GetResult_Response_message_member_array,  // message members
  PlanGrasp_GetResult_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  PlanGrasp_GetResult_Response_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t PlanGrasp_GetResult_Response_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &PlanGrasp_GetResult_Response_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace action

}  // namespace soarm100_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<soarm100_interfaces::action::PlanGrasp_GetResult_Response>()
{
  return &::soarm100_interfaces::action::rosidl_typesupport_introspection_cpp::PlanGrasp_GetResult_Response_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, soarm100_interfaces, action, PlanGrasp_GetResult_Response)() {
  return &::soarm100_interfaces::action::rosidl_typesupport_introspection_cpp::PlanGrasp_GetResult_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "rosidl_typesupport_introspection_cpp/visibility_control.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__struct.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/service_introspection.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/service_type_support_decl.hpp"

namespace soarm100_interfaces
{

namespace action
{

namespace rosidl_typesupport_introspection_cpp
{

// this is intentionally not const to allow initialization later to prevent an initialization race
static ::rosidl_typesupport_introspection_cpp::ServiceMembers PlanGrasp_GetResult_service_members = {
  "soarm100_interfaces::action",  // service namespace
  "PlanGrasp_GetResult",  // service name
  // these two fields are initialized below on the first access
  // see get_service_type_support_handle<soarm100_interfaces::action::PlanGrasp_GetResult>()
  nullptr,  // request message
  nullptr  // response message
};

static const rosidl_service_type_support_t PlanGrasp_GetResult_service_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &PlanGrasp_GetResult_service_members,
  get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace action

}  // namespace soarm100_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<soarm100_interfaces::action::PlanGrasp_GetResult>()
{
  // get a handle to the value to be returned
  auto service_type_support =
    &::soarm100_interfaces::action::rosidl_typesupport_introspection_cpp::PlanGrasp_GetResult_service_type_support_handle;
  // get a non-const and properly typed version of the data void *
  auto service_members = const_cast<::rosidl_typesupport_introspection_cpp::ServiceMembers *>(
    static_cast<const ::rosidl_typesupport_introspection_cpp::ServiceMembers *>(
      service_type_support->data));
  // make sure that both the request_members_ and the response_members_ are initialized
  // if they are not, initialize them
  if (
    service_members->request_members_ == nullptr ||
    service_members->response_members_ == nullptr)
  {
    // initialize the request_members_ with the static function from the external library
    service_members->request_members_ = static_cast<
      const ::rosidl_typesupport_introspection_cpp::MessageMembers *
      >(
      ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<
        ::soarm100_interfaces::action::PlanGrasp_GetResult_Request
      >()->data
      );
    // initialize the response_members_ with the static function from the external library
    service_members->response_members_ = static_cast<
      const ::rosidl_typesupport_introspection_cpp::MessageMembers *
      >(
      ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<
        ::soarm100_interfaces::action::PlanGrasp_GetResult_Response
      >()->data
      );
  }
  // finally return the properly initialized service_type_support handle
  return service_type_support;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, soarm100_interfaces, action, PlanGrasp_GetResult)() {
  return ::rosidl_typesupport_introspection_cpp::get_service_type_support_handle<soarm100_interfaces::action::PlanGrasp_GetResult>();
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "array"
// already included above
// #include "cstddef"
// already included above
// #include "string"
// already included above
// #include "vector"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__struct.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/field_types.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace soarm100_interfaces
{

namespace action
{

namespace rosidl_typesupport_introspection_cpp
{

void PlanGrasp_FeedbackMessage_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) soarm100_interfaces::action::PlanGrasp_FeedbackMessage(_init);
}

void PlanGrasp_FeedbackMessage_fini_function(void * message_memory)
{
  auto typed_message = static_cast<soarm100_interfaces::action::PlanGrasp_FeedbackMessage *>(message_memory);
  typed_message->~PlanGrasp_FeedbackMessage();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember PlanGrasp_FeedbackMessage_message_member_array[2] = {
  {
    "goal_id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<unique_identifier_msgs::msg::UUID>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_FeedbackMessage, goal_id),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "feedback",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<soarm100_interfaces::action::PlanGrasp_Feedback>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces::action::PlanGrasp_FeedbackMessage, feedback),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers PlanGrasp_FeedbackMessage_message_members = {
  "soarm100_interfaces::action",  // message namespace
  "PlanGrasp_FeedbackMessage",  // message name
  2,  // number of fields
  sizeof(soarm100_interfaces::action::PlanGrasp_FeedbackMessage),
  PlanGrasp_FeedbackMessage_message_member_array,  // message members
  PlanGrasp_FeedbackMessage_init_function,  // function to initialize message memory (memory has to be allocated)
  PlanGrasp_FeedbackMessage_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t PlanGrasp_FeedbackMessage_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &PlanGrasp_FeedbackMessage_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace action

}  // namespace soarm100_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<soarm100_interfaces::action::PlanGrasp_FeedbackMessage>()
{
  return &::soarm100_interfaces::action::rosidl_typesupport_introspection_cpp::PlanGrasp_FeedbackMessage_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, soarm100_interfaces, action, PlanGrasp_FeedbackMessage)() {
  return &::soarm100_interfaces::action::rosidl_typesupport_introspection_cpp::PlanGrasp_FeedbackMessage_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
