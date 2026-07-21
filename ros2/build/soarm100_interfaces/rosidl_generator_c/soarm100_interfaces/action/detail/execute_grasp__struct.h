// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from soarm100_interfaces:action/ExecuteGrasp.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_GRASP__STRUCT_H_
#define SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_GRASP__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'target_prompt'
#include "rosidl_runtime_c/string.h"
// Member 'approximate_target_pose'
#include "geometry_msgs/msg/detail/pose_stamped__struct.h"

/// Struct defined in action/ExecuteGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__ExecuteGrasp_Goal
{
  rosidl_runtime_c__String target_prompt;
  bool enable_avoidance;
  geometry_msgs__msg__PoseStamped approximate_target_pose;
} soarm100_interfaces__action__ExecuteGrasp_Goal;

// Struct for a sequence of soarm100_interfaces__action__ExecuteGrasp_Goal.
typedef struct soarm100_interfaces__action__ExecuteGrasp_Goal__Sequence
{
  soarm100_interfaces__action__ExecuteGrasp_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__ExecuteGrasp_Goal__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'reason'
// already included above
// #include "rosidl_runtime_c/string.h"
// Member 'final_grasp_pose'
// already included above
// #include "geometry_msgs/msg/detail/pose_stamped__struct.h"

/// Struct defined in action/ExecuteGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__ExecuteGrasp_Result
{
  bool success;
  rosidl_runtime_c__String reason;
  geometry_msgs__msg__PoseStamped final_grasp_pose;
  float lift_height;
  uint8_t attempts;
} soarm100_interfaces__action__ExecuteGrasp_Result;

// Struct for a sequence of soarm100_interfaces__action__ExecuteGrasp_Result.
typedef struct soarm100_interfaces__action__ExecuteGrasp_Result__Sequence
{
  soarm100_interfaces__action__ExecuteGrasp_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__ExecuteGrasp_Result__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stage'
// Member 'reason'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/ExecuteGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__ExecuteGrasp_Feedback
{
  rosidl_runtime_c__String stage;
  float target_visible_score;
  float grasp_score;
  float tcp_pos_err;
  float tcp_ori_err;
  float sdf_min_dist;
  bool cbf_active;
  bool tracking_valid;
  bool replan_running;
  rosidl_runtime_c__String reason;
} soarm100_interfaces__action__ExecuteGrasp_Feedback;

// Struct for a sequence of soarm100_interfaces__action__ExecuteGrasp_Feedback.
typedef struct soarm100_interfaces__action__ExecuteGrasp_Feedback__Sequence
{
  soarm100_interfaces__action__ExecuteGrasp_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__ExecuteGrasp_Feedback__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "soarm100_interfaces/action/detail/execute_grasp__struct.h"

/// Struct defined in action/ExecuteGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__ExecuteGrasp_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  soarm100_interfaces__action__ExecuteGrasp_Goal goal;
} soarm100_interfaces__action__ExecuteGrasp_SendGoal_Request;

// Struct for a sequence of soarm100_interfaces__action__ExecuteGrasp_SendGoal_Request.
typedef struct soarm100_interfaces__action__ExecuteGrasp_SendGoal_Request__Sequence
{
  soarm100_interfaces__action__ExecuteGrasp_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__ExecuteGrasp_SendGoal_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/ExecuteGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__ExecuteGrasp_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} soarm100_interfaces__action__ExecuteGrasp_SendGoal_Response;

// Struct for a sequence of soarm100_interfaces__action__ExecuteGrasp_SendGoal_Response.
typedef struct soarm100_interfaces__action__ExecuteGrasp_SendGoal_Response__Sequence
{
  soarm100_interfaces__action__ExecuteGrasp_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__ExecuteGrasp_SendGoal_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/ExecuteGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__ExecuteGrasp_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} soarm100_interfaces__action__ExecuteGrasp_GetResult_Request;

// Struct for a sequence of soarm100_interfaces__action__ExecuteGrasp_GetResult_Request.
typedef struct soarm100_interfaces__action__ExecuteGrasp_GetResult_Request__Sequence
{
  soarm100_interfaces__action__ExecuteGrasp_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__ExecuteGrasp_GetResult_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "soarm100_interfaces/action/detail/execute_grasp__struct.h"

/// Struct defined in action/ExecuteGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__ExecuteGrasp_GetResult_Response
{
  int8_t status;
  soarm100_interfaces__action__ExecuteGrasp_Result result;
} soarm100_interfaces__action__ExecuteGrasp_GetResult_Response;

// Struct for a sequence of soarm100_interfaces__action__ExecuteGrasp_GetResult_Response.
typedef struct soarm100_interfaces__action__ExecuteGrasp_GetResult_Response__Sequence
{
  soarm100_interfaces__action__ExecuteGrasp_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__ExecuteGrasp_GetResult_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "soarm100_interfaces/action/detail/execute_grasp__struct.h"

/// Struct defined in action/ExecuteGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__ExecuteGrasp_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  soarm100_interfaces__action__ExecuteGrasp_Feedback feedback;
} soarm100_interfaces__action__ExecuteGrasp_FeedbackMessage;

// Struct for a sequence of soarm100_interfaces__action__ExecuteGrasp_FeedbackMessage.
typedef struct soarm100_interfaces__action__ExecuteGrasp_FeedbackMessage__Sequence
{
  soarm100_interfaces__action__ExecuteGrasp_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__ExecuteGrasp_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_GRASP__STRUCT_H_
