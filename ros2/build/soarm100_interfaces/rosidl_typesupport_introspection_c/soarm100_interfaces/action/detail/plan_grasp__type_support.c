// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from soarm100_interfaces:action/PlanGrasp.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "soarm100_interfaces/action/detail/plan_grasp__rosidl_typesupport_introspection_c.h"
#include "soarm100_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "soarm100_interfaces/action/detail/plan_grasp__functions.h"
#include "soarm100_interfaces/action/detail/plan_grasp__struct.h"


// Include directives for member types
// Member `target_prompt`
#include "rosidl_runtime_c/string_functions.h"
// Member `approximate_target_pose`
#include "geometry_msgs/msg/pose_stamped.h"
// Member `approximate_target_pose`
#include "geometry_msgs/msg/detail/pose_stamped__rosidl_typesupport_introspection_c.h"
// Member `target_cloud`
#include "sensor_msgs/msg/point_cloud2.h"
// Member `target_cloud`
#include "sensor_msgs/msg/detail/point_cloud2__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void soarm100_interfaces__action__PlanGrasp_Goal__rosidl_typesupport_introspection_c__PlanGrasp_Goal_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  soarm100_interfaces__action__PlanGrasp_Goal__init(message_memory);
}

void soarm100_interfaces__action__PlanGrasp_Goal__rosidl_typesupport_introspection_c__PlanGrasp_Goal_fini_function(void * message_memory)
{
  soarm100_interfaces__action__PlanGrasp_Goal__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember soarm100_interfaces__action__PlanGrasp_Goal__rosidl_typesupport_introspection_c__PlanGrasp_Goal_message_member_array[4] = {
  {
    "target_prompt",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_Goal, target_prompt),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "approximate_target_pose",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_Goal, approximate_target_pose),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "target_cloud",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_Goal, target_cloud),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "top_k",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT16,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_Goal, top_k),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers soarm100_interfaces__action__PlanGrasp_Goal__rosidl_typesupport_introspection_c__PlanGrasp_Goal_message_members = {
  "soarm100_interfaces__action",  // message namespace
  "PlanGrasp_Goal",  // message name
  4,  // number of fields
  sizeof(soarm100_interfaces__action__PlanGrasp_Goal),
  soarm100_interfaces__action__PlanGrasp_Goal__rosidl_typesupport_introspection_c__PlanGrasp_Goal_message_member_array,  // message members
  soarm100_interfaces__action__PlanGrasp_Goal__rosidl_typesupport_introspection_c__PlanGrasp_Goal_init_function,  // function to initialize message memory (memory has to be allocated)
  soarm100_interfaces__action__PlanGrasp_Goal__rosidl_typesupport_introspection_c__PlanGrasp_Goal_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t soarm100_interfaces__action__PlanGrasp_Goal__rosidl_typesupport_introspection_c__PlanGrasp_Goal_message_type_support_handle = {
  0,
  &soarm100_interfaces__action__PlanGrasp_Goal__rosidl_typesupport_introspection_c__PlanGrasp_Goal_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_soarm100_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, PlanGrasp_Goal)() {
  soarm100_interfaces__action__PlanGrasp_Goal__rosidl_typesupport_introspection_c__PlanGrasp_Goal_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, PoseStamped)();
  soarm100_interfaces__action__PlanGrasp_Goal__rosidl_typesupport_introspection_c__PlanGrasp_Goal_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, sensor_msgs, msg, PointCloud2)();
  if (!soarm100_interfaces__action__PlanGrasp_Goal__rosidl_typesupport_introspection_c__PlanGrasp_Goal_message_type_support_handle.typesupport_identifier) {
    soarm100_interfaces__action__PlanGrasp_Goal__rosidl_typesupport_introspection_c__PlanGrasp_Goal_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &soarm100_interfaces__action__PlanGrasp_Goal__rosidl_typesupport_introspection_c__PlanGrasp_Goal_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__rosidl_typesupport_introspection_c.h"
// already included above
// #include "soarm100_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__functions.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__struct.h"


// Include directives for member types
// Member `reason`
// already included above
// #include "rosidl_runtime_c/string_functions.h"
// Member `selected_grasp_pose`
// Member `selected_pregrasp_pose`
// already included above
// #include "geometry_msgs/msg/pose_stamped.h"
// Member `selected_grasp_pose`
// Member `selected_pregrasp_pose`
// already included above
// #include "geometry_msgs/msg/detail/pose_stamped__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void soarm100_interfaces__action__PlanGrasp_Result__rosidl_typesupport_introspection_c__PlanGrasp_Result_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  soarm100_interfaces__action__PlanGrasp_Result__init(message_memory);
}

void soarm100_interfaces__action__PlanGrasp_Result__rosidl_typesupport_introspection_c__PlanGrasp_Result_fini_function(void * message_memory)
{
  soarm100_interfaces__action__PlanGrasp_Result__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember soarm100_interfaces__action__PlanGrasp_Result__rosidl_typesupport_introspection_c__PlanGrasp_Result_message_member_array[7] = {
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_Result, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "reason",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_Result, reason),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "selected_grasp_pose",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_Result, selected_grasp_pose),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "selected_pregrasp_pose",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_Result, selected_pregrasp_pose),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "grasp_score",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_Result, grasp_score),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "gripper_width",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_Result, gripper_width),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "candidate_count",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT16,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_Result, candidate_count),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers soarm100_interfaces__action__PlanGrasp_Result__rosidl_typesupport_introspection_c__PlanGrasp_Result_message_members = {
  "soarm100_interfaces__action",  // message namespace
  "PlanGrasp_Result",  // message name
  7,  // number of fields
  sizeof(soarm100_interfaces__action__PlanGrasp_Result),
  soarm100_interfaces__action__PlanGrasp_Result__rosidl_typesupport_introspection_c__PlanGrasp_Result_message_member_array,  // message members
  soarm100_interfaces__action__PlanGrasp_Result__rosidl_typesupport_introspection_c__PlanGrasp_Result_init_function,  // function to initialize message memory (memory has to be allocated)
  soarm100_interfaces__action__PlanGrasp_Result__rosidl_typesupport_introspection_c__PlanGrasp_Result_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t soarm100_interfaces__action__PlanGrasp_Result__rosidl_typesupport_introspection_c__PlanGrasp_Result_message_type_support_handle = {
  0,
  &soarm100_interfaces__action__PlanGrasp_Result__rosidl_typesupport_introspection_c__PlanGrasp_Result_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_soarm100_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, PlanGrasp_Result)() {
  soarm100_interfaces__action__PlanGrasp_Result__rosidl_typesupport_introspection_c__PlanGrasp_Result_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, PoseStamped)();
  soarm100_interfaces__action__PlanGrasp_Result__rosidl_typesupport_introspection_c__PlanGrasp_Result_message_member_array[3].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, PoseStamped)();
  if (!soarm100_interfaces__action__PlanGrasp_Result__rosidl_typesupport_introspection_c__PlanGrasp_Result_message_type_support_handle.typesupport_identifier) {
    soarm100_interfaces__action__PlanGrasp_Result__rosidl_typesupport_introspection_c__PlanGrasp_Result_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &soarm100_interfaces__action__PlanGrasp_Result__rosidl_typesupport_introspection_c__PlanGrasp_Result_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__rosidl_typesupport_introspection_c.h"
// already included above
// #include "soarm100_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__functions.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__struct.h"


// Include directives for member types
// Member `stage`
// Member `reason`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void soarm100_interfaces__action__PlanGrasp_Feedback__rosidl_typesupport_introspection_c__PlanGrasp_Feedback_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  soarm100_interfaces__action__PlanGrasp_Feedback__init(message_memory);
}

void soarm100_interfaces__action__PlanGrasp_Feedback__rosidl_typesupport_introspection_c__PlanGrasp_Feedback_fini_function(void * message_memory)
{
  soarm100_interfaces__action__PlanGrasp_Feedback__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember soarm100_interfaces__action__PlanGrasp_Feedback__rosidl_typesupport_introspection_c__PlanGrasp_Feedback_message_member_array[4] = {
  {
    "stage",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_Feedback, stage),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "candidate_count",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT16,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_Feedback, candidate_count),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "best_score",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_Feedback, best_score),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "reason",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_Feedback, reason),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers soarm100_interfaces__action__PlanGrasp_Feedback__rosidl_typesupport_introspection_c__PlanGrasp_Feedback_message_members = {
  "soarm100_interfaces__action",  // message namespace
  "PlanGrasp_Feedback",  // message name
  4,  // number of fields
  sizeof(soarm100_interfaces__action__PlanGrasp_Feedback),
  soarm100_interfaces__action__PlanGrasp_Feedback__rosidl_typesupport_introspection_c__PlanGrasp_Feedback_message_member_array,  // message members
  soarm100_interfaces__action__PlanGrasp_Feedback__rosidl_typesupport_introspection_c__PlanGrasp_Feedback_init_function,  // function to initialize message memory (memory has to be allocated)
  soarm100_interfaces__action__PlanGrasp_Feedback__rosidl_typesupport_introspection_c__PlanGrasp_Feedback_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t soarm100_interfaces__action__PlanGrasp_Feedback__rosidl_typesupport_introspection_c__PlanGrasp_Feedback_message_type_support_handle = {
  0,
  &soarm100_interfaces__action__PlanGrasp_Feedback__rosidl_typesupport_introspection_c__PlanGrasp_Feedback_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_soarm100_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, PlanGrasp_Feedback)() {
  if (!soarm100_interfaces__action__PlanGrasp_Feedback__rosidl_typesupport_introspection_c__PlanGrasp_Feedback_message_type_support_handle.typesupport_identifier) {
    soarm100_interfaces__action__PlanGrasp_Feedback__rosidl_typesupport_introspection_c__PlanGrasp_Feedback_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &soarm100_interfaces__action__PlanGrasp_Feedback__rosidl_typesupport_introspection_c__PlanGrasp_Feedback_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__rosidl_typesupport_introspection_c.h"
// already included above
// #include "soarm100_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__functions.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__struct.h"


// Include directives for member types
// Member `goal_id`
#include "unique_identifier_msgs/msg/uuid.h"
// Member `goal_id`
#include "unique_identifier_msgs/msg/detail/uuid__rosidl_typesupport_introspection_c.h"
// Member `goal`
#include "soarm100_interfaces/action/plan_grasp.h"
// Member `goal`
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void soarm100_interfaces__action__PlanGrasp_SendGoal_Request__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  soarm100_interfaces__action__PlanGrasp_SendGoal_Request__init(message_memory);
}

void soarm100_interfaces__action__PlanGrasp_SendGoal_Request__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Request_fini_function(void * message_memory)
{
  soarm100_interfaces__action__PlanGrasp_SendGoal_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember soarm100_interfaces__action__PlanGrasp_SendGoal_Request__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Request_message_member_array[2] = {
  {
    "goal_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_SendGoal_Request, goal_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "goal",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_SendGoal_Request, goal),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers soarm100_interfaces__action__PlanGrasp_SendGoal_Request__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Request_message_members = {
  "soarm100_interfaces__action",  // message namespace
  "PlanGrasp_SendGoal_Request",  // message name
  2,  // number of fields
  sizeof(soarm100_interfaces__action__PlanGrasp_SendGoal_Request),
  soarm100_interfaces__action__PlanGrasp_SendGoal_Request__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Request_message_member_array,  // message members
  soarm100_interfaces__action__PlanGrasp_SendGoal_Request__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  soarm100_interfaces__action__PlanGrasp_SendGoal_Request__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t soarm100_interfaces__action__PlanGrasp_SendGoal_Request__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Request_message_type_support_handle = {
  0,
  &soarm100_interfaces__action__PlanGrasp_SendGoal_Request__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_soarm100_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, PlanGrasp_SendGoal_Request)() {
  soarm100_interfaces__action__PlanGrasp_SendGoal_Request__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Request_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unique_identifier_msgs, msg, UUID)();
  soarm100_interfaces__action__PlanGrasp_SendGoal_Request__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Request_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, PlanGrasp_Goal)();
  if (!soarm100_interfaces__action__PlanGrasp_SendGoal_Request__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Request_message_type_support_handle.typesupport_identifier) {
    soarm100_interfaces__action__PlanGrasp_SendGoal_Request__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &soarm100_interfaces__action__PlanGrasp_SendGoal_Request__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__rosidl_typesupport_introspection_c.h"
// already included above
// #include "soarm100_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__functions.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__struct.h"


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/time.h"
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void soarm100_interfaces__action__PlanGrasp_SendGoal_Response__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  soarm100_interfaces__action__PlanGrasp_SendGoal_Response__init(message_memory);
}

void soarm100_interfaces__action__PlanGrasp_SendGoal_Response__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Response_fini_function(void * message_memory)
{
  soarm100_interfaces__action__PlanGrasp_SendGoal_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember soarm100_interfaces__action__PlanGrasp_SendGoal_Response__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Response_message_member_array[2] = {
  {
    "accepted",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_SendGoal_Response, accepted),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "stamp",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_SendGoal_Response, stamp),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers soarm100_interfaces__action__PlanGrasp_SendGoal_Response__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Response_message_members = {
  "soarm100_interfaces__action",  // message namespace
  "PlanGrasp_SendGoal_Response",  // message name
  2,  // number of fields
  sizeof(soarm100_interfaces__action__PlanGrasp_SendGoal_Response),
  soarm100_interfaces__action__PlanGrasp_SendGoal_Response__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Response_message_member_array,  // message members
  soarm100_interfaces__action__PlanGrasp_SendGoal_Response__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  soarm100_interfaces__action__PlanGrasp_SendGoal_Response__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t soarm100_interfaces__action__PlanGrasp_SendGoal_Response__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Response_message_type_support_handle = {
  0,
  &soarm100_interfaces__action__PlanGrasp_SendGoal_Response__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_soarm100_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, PlanGrasp_SendGoal_Response)() {
  soarm100_interfaces__action__PlanGrasp_SendGoal_Response__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Response_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, builtin_interfaces, msg, Time)();
  if (!soarm100_interfaces__action__PlanGrasp_SendGoal_Response__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Response_message_type_support_handle.typesupport_identifier) {
    soarm100_interfaces__action__PlanGrasp_SendGoal_Response__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &soarm100_interfaces__action__PlanGrasp_SendGoal_Response__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "soarm100_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers soarm100_interfaces__action__detail__plan_grasp__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_service_members = {
  "soarm100_interfaces__action",  // service namespace
  "PlanGrasp_SendGoal",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // soarm100_interfaces__action__detail__plan_grasp__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Request_message_type_support_handle,
  NULL  // response message
  // soarm100_interfaces__action__detail__plan_grasp__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_Response_message_type_support_handle
};

static rosidl_service_type_support_t soarm100_interfaces__action__detail__plan_grasp__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_service_type_support_handle = {
  0,
  &soarm100_interfaces__action__detail__plan_grasp__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, PlanGrasp_SendGoal_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, PlanGrasp_SendGoal_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_soarm100_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, PlanGrasp_SendGoal)() {
  if (!soarm100_interfaces__action__detail__plan_grasp__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_service_type_support_handle.typesupport_identifier) {
    soarm100_interfaces__action__detail__plan_grasp__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)soarm100_interfaces__action__detail__plan_grasp__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, PlanGrasp_SendGoal_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, PlanGrasp_SendGoal_Response)()->data;
  }

  return &soarm100_interfaces__action__detail__plan_grasp__rosidl_typesupport_introspection_c__PlanGrasp_SendGoal_service_type_support_handle;
}

// already included above
// #include <stddef.h>
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__rosidl_typesupport_introspection_c.h"
// already included above
// #include "soarm100_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__functions.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__struct.h"


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/uuid.h"
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void soarm100_interfaces__action__PlanGrasp_GetResult_Request__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  soarm100_interfaces__action__PlanGrasp_GetResult_Request__init(message_memory);
}

void soarm100_interfaces__action__PlanGrasp_GetResult_Request__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Request_fini_function(void * message_memory)
{
  soarm100_interfaces__action__PlanGrasp_GetResult_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember soarm100_interfaces__action__PlanGrasp_GetResult_Request__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Request_message_member_array[1] = {
  {
    "goal_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_GetResult_Request, goal_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers soarm100_interfaces__action__PlanGrasp_GetResult_Request__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Request_message_members = {
  "soarm100_interfaces__action",  // message namespace
  "PlanGrasp_GetResult_Request",  // message name
  1,  // number of fields
  sizeof(soarm100_interfaces__action__PlanGrasp_GetResult_Request),
  soarm100_interfaces__action__PlanGrasp_GetResult_Request__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Request_message_member_array,  // message members
  soarm100_interfaces__action__PlanGrasp_GetResult_Request__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  soarm100_interfaces__action__PlanGrasp_GetResult_Request__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t soarm100_interfaces__action__PlanGrasp_GetResult_Request__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Request_message_type_support_handle = {
  0,
  &soarm100_interfaces__action__PlanGrasp_GetResult_Request__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_soarm100_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, PlanGrasp_GetResult_Request)() {
  soarm100_interfaces__action__PlanGrasp_GetResult_Request__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Request_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unique_identifier_msgs, msg, UUID)();
  if (!soarm100_interfaces__action__PlanGrasp_GetResult_Request__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Request_message_type_support_handle.typesupport_identifier) {
    soarm100_interfaces__action__PlanGrasp_GetResult_Request__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &soarm100_interfaces__action__PlanGrasp_GetResult_Request__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__rosidl_typesupport_introspection_c.h"
// already included above
// #include "soarm100_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__functions.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__struct.h"


// Include directives for member types
// Member `result`
// already included above
// #include "soarm100_interfaces/action/plan_grasp.h"
// Member `result`
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void soarm100_interfaces__action__PlanGrasp_GetResult_Response__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  soarm100_interfaces__action__PlanGrasp_GetResult_Response__init(message_memory);
}

void soarm100_interfaces__action__PlanGrasp_GetResult_Response__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Response_fini_function(void * message_memory)
{
  soarm100_interfaces__action__PlanGrasp_GetResult_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember soarm100_interfaces__action__PlanGrasp_GetResult_Response__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Response_message_member_array[2] = {
  {
    "status",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_GetResult_Response, status),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "result",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_GetResult_Response, result),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers soarm100_interfaces__action__PlanGrasp_GetResult_Response__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Response_message_members = {
  "soarm100_interfaces__action",  // message namespace
  "PlanGrasp_GetResult_Response",  // message name
  2,  // number of fields
  sizeof(soarm100_interfaces__action__PlanGrasp_GetResult_Response),
  soarm100_interfaces__action__PlanGrasp_GetResult_Response__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Response_message_member_array,  // message members
  soarm100_interfaces__action__PlanGrasp_GetResult_Response__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  soarm100_interfaces__action__PlanGrasp_GetResult_Response__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t soarm100_interfaces__action__PlanGrasp_GetResult_Response__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Response_message_type_support_handle = {
  0,
  &soarm100_interfaces__action__PlanGrasp_GetResult_Response__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_soarm100_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, PlanGrasp_GetResult_Response)() {
  soarm100_interfaces__action__PlanGrasp_GetResult_Response__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Response_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, PlanGrasp_Result)();
  if (!soarm100_interfaces__action__PlanGrasp_GetResult_Response__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Response_message_type_support_handle.typesupport_identifier) {
    soarm100_interfaces__action__PlanGrasp_GetResult_Response__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &soarm100_interfaces__action__PlanGrasp_GetResult_Response__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "soarm100_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers soarm100_interfaces__action__detail__plan_grasp__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_service_members = {
  "soarm100_interfaces__action",  // service namespace
  "PlanGrasp_GetResult",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // soarm100_interfaces__action__detail__plan_grasp__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Request_message_type_support_handle,
  NULL  // response message
  // soarm100_interfaces__action__detail__plan_grasp__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_Response_message_type_support_handle
};

static rosidl_service_type_support_t soarm100_interfaces__action__detail__plan_grasp__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_service_type_support_handle = {
  0,
  &soarm100_interfaces__action__detail__plan_grasp__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, PlanGrasp_GetResult_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, PlanGrasp_GetResult_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_soarm100_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, PlanGrasp_GetResult)() {
  if (!soarm100_interfaces__action__detail__plan_grasp__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_service_type_support_handle.typesupport_identifier) {
    soarm100_interfaces__action__detail__plan_grasp__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)soarm100_interfaces__action__detail__plan_grasp__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, PlanGrasp_GetResult_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, PlanGrasp_GetResult_Response)()->data;
  }

  return &soarm100_interfaces__action__detail__plan_grasp__rosidl_typesupport_introspection_c__PlanGrasp_GetResult_service_type_support_handle;
}

// already included above
// #include <stddef.h>
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__rosidl_typesupport_introspection_c.h"
// already included above
// #include "soarm100_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__functions.h"
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__struct.h"


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/uuid.h"
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__rosidl_typesupport_introspection_c.h"
// Member `feedback`
// already included above
// #include "soarm100_interfaces/action/plan_grasp.h"
// Member `feedback`
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void soarm100_interfaces__action__PlanGrasp_FeedbackMessage__rosidl_typesupport_introspection_c__PlanGrasp_FeedbackMessage_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  soarm100_interfaces__action__PlanGrasp_FeedbackMessage__init(message_memory);
}

void soarm100_interfaces__action__PlanGrasp_FeedbackMessage__rosidl_typesupport_introspection_c__PlanGrasp_FeedbackMessage_fini_function(void * message_memory)
{
  soarm100_interfaces__action__PlanGrasp_FeedbackMessage__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember soarm100_interfaces__action__PlanGrasp_FeedbackMessage__rosidl_typesupport_introspection_c__PlanGrasp_FeedbackMessage_message_member_array[2] = {
  {
    "goal_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_FeedbackMessage, goal_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "feedback",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__action__PlanGrasp_FeedbackMessage, feedback),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers soarm100_interfaces__action__PlanGrasp_FeedbackMessage__rosidl_typesupport_introspection_c__PlanGrasp_FeedbackMessage_message_members = {
  "soarm100_interfaces__action",  // message namespace
  "PlanGrasp_FeedbackMessage",  // message name
  2,  // number of fields
  sizeof(soarm100_interfaces__action__PlanGrasp_FeedbackMessage),
  soarm100_interfaces__action__PlanGrasp_FeedbackMessage__rosidl_typesupport_introspection_c__PlanGrasp_FeedbackMessage_message_member_array,  // message members
  soarm100_interfaces__action__PlanGrasp_FeedbackMessage__rosidl_typesupport_introspection_c__PlanGrasp_FeedbackMessage_init_function,  // function to initialize message memory (memory has to be allocated)
  soarm100_interfaces__action__PlanGrasp_FeedbackMessage__rosidl_typesupport_introspection_c__PlanGrasp_FeedbackMessage_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t soarm100_interfaces__action__PlanGrasp_FeedbackMessage__rosidl_typesupport_introspection_c__PlanGrasp_FeedbackMessage_message_type_support_handle = {
  0,
  &soarm100_interfaces__action__PlanGrasp_FeedbackMessage__rosidl_typesupport_introspection_c__PlanGrasp_FeedbackMessage_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_soarm100_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, PlanGrasp_FeedbackMessage)() {
  soarm100_interfaces__action__PlanGrasp_FeedbackMessage__rosidl_typesupport_introspection_c__PlanGrasp_FeedbackMessage_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, unique_identifier_msgs, msg, UUID)();
  soarm100_interfaces__action__PlanGrasp_FeedbackMessage__rosidl_typesupport_introspection_c__PlanGrasp_FeedbackMessage_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, PlanGrasp_Feedback)();
  if (!soarm100_interfaces__action__PlanGrasp_FeedbackMessage__rosidl_typesupport_introspection_c__PlanGrasp_FeedbackMessage_message_type_support_handle.typesupport_identifier) {
    soarm100_interfaces__action__PlanGrasp_FeedbackMessage__rosidl_typesupport_introspection_c__PlanGrasp_FeedbackMessage_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &soarm100_interfaces__action__PlanGrasp_FeedbackMessage__rosidl_typesupport_introspection_c__PlanGrasp_FeedbackMessage_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
