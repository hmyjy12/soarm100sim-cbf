// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from soarm100_interfaces:srv/SegmentTarget.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__SRV__DETAIL__SEGMENT_TARGET__STRUCT_H_
#define SOARM100_INTERFACES__SRV__DETAIL__SEGMENT_TARGET__STRUCT_H_

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

/// Struct defined in srv/SegmentTarget in the package soarm100_interfaces.
typedef struct soarm100_interfaces__srv__SegmentTarget_Request
{
  rosidl_runtime_c__String target_prompt;
  bool force_yolo;
} soarm100_interfaces__srv__SegmentTarget_Request;

// Struct for a sequence of soarm100_interfaces__srv__SegmentTarget_Request.
typedef struct soarm100_interfaces__srv__SegmentTarget_Request__Sequence
{
  soarm100_interfaces__srv__SegmentTarget_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__srv__SegmentTarget_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'reason'
// Member 'mask_topic'
// Member 'debug_json'
// already included above
// #include "rosidl_runtime_c/string.h"
// Member 'target_center'
#include "geometry_msgs/msg/detail/pose_stamped__struct.h"

/// Struct defined in srv/SegmentTarget in the package soarm100_interfaces.
typedef struct soarm100_interfaces__srv__SegmentTarget_Response
{
  bool success;
  rosidl_runtime_c__String reason;
  geometry_msgs__msg__PoseStamped target_center;
  float score;
  float bbox_xyxy[4];
  rosidl_runtime_c__String mask_topic;
  rosidl_runtime_c__String debug_json;
} soarm100_interfaces__srv__SegmentTarget_Response;

// Struct for a sequence of soarm100_interfaces__srv__SegmentTarget_Response.
typedef struct soarm100_interfaces__srv__SegmentTarget_Response__Sequence
{
  soarm100_interfaces__srv__SegmentTarget_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__srv__SegmentTarget_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SOARM100_INTERFACES__SRV__DETAIL__SEGMENT_TARGET__STRUCT_H_
