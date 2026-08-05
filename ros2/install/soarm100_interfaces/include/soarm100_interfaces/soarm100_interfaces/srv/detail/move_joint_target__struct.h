// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from soarm100_interfaces:srv/MoveJointTarget.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__SRV__DETAIL__MOVE_JOINT_TARGET__STRUCT_H_
#define SOARM100_INTERFACES__SRV__DETAIL__MOVE_JOINT_TARGET__STRUCT_H_

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

/// Struct defined in srv/MoveJointTarget in the package soarm100_interfaces.
typedef struct soarm100_interfaces__srv__MoveJointTarget_Request
{
  double position_rad[7];
  double duration;
  rosidl_runtime_c__String confirmation;
} soarm100_interfaces__srv__MoveJointTarget_Request;

// Struct for a sequence of soarm100_interfaces__srv__MoveJointTarget_Request.
typedef struct soarm100_interfaces__srv__MoveJointTarget_Request__Sequence
{
  soarm100_interfaces__srv__MoveJointTarget_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__srv__MoveJointTarget_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'reason'
// Member 'log_path'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/MoveJointTarget in the package soarm100_interfaces.
typedef struct soarm100_interfaces__srv__MoveJointTarget_Response
{
  bool success;
  rosidl_runtime_c__String reason;
  rosidl_runtime_c__String log_path;
} soarm100_interfaces__srv__MoveJointTarget_Response;

// Struct for a sequence of soarm100_interfaces__srv__MoveJointTarget_Response.
typedef struct soarm100_interfaces__srv__MoveJointTarget_Response__Sequence
{
  soarm100_interfaces__srv__MoveJointTarget_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__srv__MoveJointTarget_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SOARM100_INTERFACES__SRV__DETAIL__MOVE_JOINT_TARGET__STRUCT_H_
