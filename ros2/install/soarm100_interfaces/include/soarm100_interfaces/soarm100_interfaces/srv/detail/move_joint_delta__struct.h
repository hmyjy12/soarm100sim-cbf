// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from soarm100_interfaces:srv/MoveJointDelta.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__SRV__DETAIL__MOVE_JOINT_DELTA__STRUCT_H_
#define SOARM100_INTERFACES__SRV__DETAIL__MOVE_JOINT_DELTA__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'confirmation'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/MoveJointDelta in the package soarm100_interfaces.
typedef struct soarm100_interfaces__srv__MoveJointDelta_Request
{
  double delta_rad[7];
  double duration;
  double hold;
  bool keep_target;
  rosidl_runtime_c__String confirmation;
} soarm100_interfaces__srv__MoveJointDelta_Request;

// Struct for a sequence of soarm100_interfaces__srv__MoveJointDelta_Request.
typedef struct soarm100_interfaces__srv__MoveJointDelta_Request__Sequence
{
  soarm100_interfaces__srv__MoveJointDelta_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__srv__MoveJointDelta_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'reason'
// Member 'log_path'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/MoveJointDelta in the package soarm100_interfaces.
typedef struct soarm100_interfaces__srv__MoveJointDelta_Response
{
  bool success;
  rosidl_runtime_c__String reason;
  rosidl_runtime_c__String log_path;
} soarm100_interfaces__srv__MoveJointDelta_Response;

// Struct for a sequence of soarm100_interfaces__srv__MoveJointDelta_Response.
typedef struct soarm100_interfaces__srv__MoveJointDelta_Response__Sequence
{
  soarm100_interfaces__srv__MoveJointDelta_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__srv__MoveJointDelta_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SOARM100_INTERFACES__SRV__DETAIL__MOVE_JOINT_DELTA__STRUCT_H_
