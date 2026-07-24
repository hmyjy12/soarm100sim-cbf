// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from soarm100_interfaces:action/ExecutePlannedGrasp.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_PLANNED_GRASP__STRUCT_H_
#define SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_PLANNED_GRASP__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'pregrasp_pose'
// Member 'grasp_pose'
// Member 'tracking_reference_pose'
#include "geometry_msgs/msg/detail/pose_stamped__struct.h"
// Member 'target_prompt'
// Member 'target_object'
// Member 'target_pos'
// Member 'traj_log'
#include "rosidl_runtime_c/string.h"

/// Struct defined in action/ExecutePlannedGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__ExecutePlannedGrasp_Goal
{
  geometry_msgs__msg__PoseStamped pregrasp_pose;
  geometry_msgs__msg__PoseStamped grasp_pose;
  geometry_msgs__msg__PoseStamped tracking_reference_pose;
  float gripper_width;
  bool enable_avoidance;
  rosidl_runtime_c__String target_prompt;
  rosidl_runtime_c__String target_object;
  rosidl_runtime_c__String target_pos;
  rosidl_runtime_c__String traj_log;
} soarm100_interfaces__action__ExecutePlannedGrasp_Goal;

// Struct for a sequence of soarm100_interfaces__action__ExecutePlannedGrasp_Goal.
typedef struct soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence
{
  soarm100_interfaces__action__ExecutePlannedGrasp_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'reason'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/ExecutePlannedGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__ExecutePlannedGrasp_Result
{
  bool success;
  rosidl_runtime_c__String reason;
  float lift_height;
  uint8_t return_code;
} soarm100_interfaces__action__ExecutePlannedGrasp_Result;

// Struct for a sequence of soarm100_interfaces__action__ExecutePlannedGrasp_Result.
typedef struct soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence
{
  soarm100_interfaces__action__ExecutePlannedGrasp_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stage'
// Member 'reason'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/ExecutePlannedGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__ExecutePlannedGrasp_Feedback
{
  rosidl_runtime_c__String stage;
  rosidl_runtime_c__String reason;
  float lift_height;
} soarm100_interfaces__action__ExecutePlannedGrasp_Feedback;

// Struct for a sequence of soarm100_interfaces__action__ExecutePlannedGrasp_Feedback.
typedef struct soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence
{
  soarm100_interfaces__action__ExecutePlannedGrasp_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "soarm100_interfaces/action/detail/execute_planned_grasp__struct.h"

/// Struct defined in action/ExecutePlannedGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  soarm100_interfaces__action__ExecutePlannedGrasp_Goal goal;
} soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request;

// Struct for a sequence of soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request.
typedef struct soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence
{
  soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/ExecutePlannedGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response;

// Struct for a sequence of soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response.
typedef struct soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence
{
  soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/ExecutePlannedGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request;

// Struct for a sequence of soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request.
typedef struct soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence
{
  soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "soarm100_interfaces/action/detail/execute_planned_grasp__struct.h"

/// Struct defined in action/ExecutePlannedGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response
{
  int8_t status;
  soarm100_interfaces__action__ExecutePlannedGrasp_Result result;
} soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response;

// Struct for a sequence of soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response.
typedef struct soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence
{
  soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "soarm100_interfaces/action/detail/execute_planned_grasp__struct.h"

/// Struct defined in action/ExecutePlannedGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  soarm100_interfaces__action__ExecutePlannedGrasp_Feedback feedback;
} soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage;

// Struct for a sequence of soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage.
typedef struct soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence
{
  soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_PLANNED_GRASP__STRUCT_H_
