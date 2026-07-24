// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from soarm100_interfaces:action/PlanGrasp.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__ACTION__DETAIL__PLAN_GRASP__STRUCT_H_
#define SOARM100_INTERFACES__ACTION__DETAIL__PLAN_GRASP__STRUCT_H_

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
// Member 'target_cloud'
#include "sensor_msgs/msg/detail/point_cloud2__struct.h"

/// Struct defined in action/PlanGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__PlanGrasp_Goal
{
  rosidl_runtime_c__String target_prompt;
  geometry_msgs__msg__PoseStamped approximate_target_pose;
  sensor_msgs__msg__PointCloud2 target_cloud;
  uint16_t top_k;
} soarm100_interfaces__action__PlanGrasp_Goal;

// Struct for a sequence of soarm100_interfaces__action__PlanGrasp_Goal.
typedef struct soarm100_interfaces__action__PlanGrasp_Goal__Sequence
{
  soarm100_interfaces__action__PlanGrasp_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__PlanGrasp_Goal__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'reason'
// already included above
// #include "rosidl_runtime_c/string.h"
// Member 'selected_grasp_pose'
// Member 'selected_pregrasp_pose'
// Member 'target_center_pose'
// already included above
// #include "geometry_msgs/msg/detail/pose_stamped__struct.h"

/// Struct defined in action/PlanGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__PlanGrasp_Result
{
  bool success;
  rosidl_runtime_c__String reason;
  geometry_msgs__msg__PoseStamped selected_grasp_pose;
  geometry_msgs__msg__PoseStamped selected_pregrasp_pose;
  geometry_msgs__msg__PoseStamped target_center_pose;
  float grasp_score;
  float gripper_width;
  uint16_t candidate_count;
} soarm100_interfaces__action__PlanGrasp_Result;

// Struct for a sequence of soarm100_interfaces__action__PlanGrasp_Result.
typedef struct soarm100_interfaces__action__PlanGrasp_Result__Sequence
{
  soarm100_interfaces__action__PlanGrasp_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__PlanGrasp_Result__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stage'
// Member 'reason'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/PlanGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__PlanGrasp_Feedback
{
  rosidl_runtime_c__String stage;
  uint16_t candidate_count;
  float best_score;
  rosidl_runtime_c__String reason;
} soarm100_interfaces__action__PlanGrasp_Feedback;

// Struct for a sequence of soarm100_interfaces__action__PlanGrasp_Feedback.
typedef struct soarm100_interfaces__action__PlanGrasp_Feedback__Sequence
{
  soarm100_interfaces__action__PlanGrasp_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__PlanGrasp_Feedback__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "soarm100_interfaces/action/detail/plan_grasp__struct.h"

/// Struct defined in action/PlanGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__PlanGrasp_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  soarm100_interfaces__action__PlanGrasp_Goal goal;
} soarm100_interfaces__action__PlanGrasp_SendGoal_Request;

// Struct for a sequence of soarm100_interfaces__action__PlanGrasp_SendGoal_Request.
typedef struct soarm100_interfaces__action__PlanGrasp_SendGoal_Request__Sequence
{
  soarm100_interfaces__action__PlanGrasp_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__PlanGrasp_SendGoal_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/PlanGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__PlanGrasp_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} soarm100_interfaces__action__PlanGrasp_SendGoal_Response;

// Struct for a sequence of soarm100_interfaces__action__PlanGrasp_SendGoal_Response.
typedef struct soarm100_interfaces__action__PlanGrasp_SendGoal_Response__Sequence
{
  soarm100_interfaces__action__PlanGrasp_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__PlanGrasp_SendGoal_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/PlanGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__PlanGrasp_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} soarm100_interfaces__action__PlanGrasp_GetResult_Request;

// Struct for a sequence of soarm100_interfaces__action__PlanGrasp_GetResult_Request.
typedef struct soarm100_interfaces__action__PlanGrasp_GetResult_Request__Sequence
{
  soarm100_interfaces__action__PlanGrasp_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__PlanGrasp_GetResult_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__struct.h"

/// Struct defined in action/PlanGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__PlanGrasp_GetResult_Response
{
  int8_t status;
  soarm100_interfaces__action__PlanGrasp_Result result;
} soarm100_interfaces__action__PlanGrasp_GetResult_Response;

// Struct for a sequence of soarm100_interfaces__action__PlanGrasp_GetResult_Response.
typedef struct soarm100_interfaces__action__PlanGrasp_GetResult_Response__Sequence
{
  soarm100_interfaces__action__PlanGrasp_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__PlanGrasp_GetResult_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "soarm100_interfaces/action/detail/plan_grasp__struct.h"

/// Struct defined in action/PlanGrasp in the package soarm100_interfaces.
typedef struct soarm100_interfaces__action__PlanGrasp_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  soarm100_interfaces__action__PlanGrasp_Feedback feedback;
} soarm100_interfaces__action__PlanGrasp_FeedbackMessage;

// Struct for a sequence of soarm100_interfaces__action__PlanGrasp_FeedbackMessage.
typedef struct soarm100_interfaces__action__PlanGrasp_FeedbackMessage__Sequence
{
  soarm100_interfaces__action__PlanGrasp_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__action__PlanGrasp_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SOARM100_INTERFACES__ACTION__DETAIL__PLAN_GRASP__STRUCT_H_
