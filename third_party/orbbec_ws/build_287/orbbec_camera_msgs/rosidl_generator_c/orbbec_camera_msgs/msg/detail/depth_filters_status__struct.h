// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from orbbec_camera_msgs:msg/DepthFiltersStatus.idl
// generated code does not contain a copyright notice

#ifndef ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTERS_STATUS__STRUCT_H_
#define ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTERS_STATUS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'filters'
#include "orbbec_camera_msgs/msg/detail/depth_filter_state__struct.h"

/// Struct defined in msg/DepthFiltersStatus in the package orbbec_camera_msgs.
typedef struct orbbec_camera_msgs__msg__DepthFiltersStatus
{
  std_msgs__msg__Header header;
  orbbec_camera_msgs__msg__DepthFilterState__Sequence filters;
} orbbec_camera_msgs__msg__DepthFiltersStatus;

// Struct for a sequence of orbbec_camera_msgs__msg__DepthFiltersStatus.
typedef struct orbbec_camera_msgs__msg__DepthFiltersStatus__Sequence
{
  orbbec_camera_msgs__msg__DepthFiltersStatus * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} orbbec_camera_msgs__msg__DepthFiltersStatus__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ORBBEC_CAMERA_MSGS__MSG__DETAIL__DEPTH_FILTERS_STATUS__STRUCT_H_
