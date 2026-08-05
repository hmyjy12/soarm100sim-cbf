// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from orbbec_camera_msgs:msg/DepthFilterParam.idl
// generated code does not contain a copyright notice

#ifndef ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTER_PARAM__STRUCT_H_
#define ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTER_PARAM__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'name'
// Member 'value'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/DepthFilterParam in the package orbbec_camera_msgs.
typedef struct orbbec_camera_msgs__msg__DepthFilterParam
{
  rosidl_runtime_c__String name;
  rosidl_runtime_c__String value;
} orbbec_camera_msgs__msg__DepthFilterParam;

// Struct for a sequence of orbbec_camera_msgs__msg__DepthFilterParam.
typedef struct orbbec_camera_msgs__msg__DepthFilterParam__Sequence
{
  orbbec_camera_msgs__msg__DepthFilterParam * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} orbbec_camera_msgs__msg__DepthFilterParam__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTER_PARAM__STRUCT_H_
