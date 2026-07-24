// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from soarm100_interfaces:msg/TrackedTarget2D.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__MSG__DETAIL__TRACKED_TARGET2_D__STRUCT_H_
#define SOARM100_INTERFACES__MSG__DETAIL__TRACKED_TARGET2_D__STRUCT_H_

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
// Member 'reason'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/TrackedTarget2D in the package soarm100_interfaces.
typedef struct soarm100_interfaces__msg__TrackedTarget2D
{
  std_msgs__msg__Header header;
  bool valid;
  float u;
  float v;
  float reference_u;
  float reference_v;
  float delta_u;
  float delta_v;
  float width;
  float height;
  uint32_t image_width;
  uint32_t image_height;
  float confidence;
  uint32_t lost_frames;
  bool replan_required;
  rosidl_runtime_c__String reason;
} soarm100_interfaces__msg__TrackedTarget2D;

// Struct for a sequence of soarm100_interfaces__msg__TrackedTarget2D.
typedef struct soarm100_interfaces__msg__TrackedTarget2D__Sequence
{
  soarm100_interfaces__msg__TrackedTarget2D * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__msg__TrackedTarget2D__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SOARM100_INTERFACES__MSG__DETAIL__TRACKED_TARGET2_D__STRUCT_H_
