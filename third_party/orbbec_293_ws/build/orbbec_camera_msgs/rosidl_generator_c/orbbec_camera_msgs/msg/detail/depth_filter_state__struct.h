// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from orbbec_camera_msgs:msg/DepthFilterState.idl
// generated code does not contain a copyright notice

#ifndef ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTER_STATE__STRUCT_H_
#define ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTER_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'filter_name'
#include "rosidl_runtime_c/string.h"
// Member 'params'
#include "orbbec_camera_msgs/msg/detail/depth_filter_param__struct.h"

/// Struct defined in msg/DepthFilterState in the package orbbec_camera_msgs.
typedef struct orbbec_camera_msgs__msg__DepthFilterState
{
  rosidl_runtime_c__String filter_name;
  bool enabled;
  orbbec_camera_msgs__msg__DepthFilterParam__Sequence params;
} orbbec_camera_msgs__msg__DepthFilterState;

// Struct for a sequence of orbbec_camera_msgs__msg__DepthFilterState.
typedef struct orbbec_camera_msgs__msg__DepthFilterState__Sequence
{
  orbbec_camera_msgs__msg__DepthFilterState * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} orbbec_camera_msgs__msg__DepthFilterState__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTER_STATE__STRUCT_H_
