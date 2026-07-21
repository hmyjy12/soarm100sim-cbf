// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from soarm100_interfaces:srv/SetAvoidance.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__SRV__DETAIL__SET_AVOIDANCE__STRUCT_H_
#define SOARM100_INTERFACES__SRV__DETAIL__SET_AVOIDANCE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/SetAvoidance in the package soarm100_interfaces.
typedef struct soarm100_interfaces__srv__SetAvoidance_Request
{
  bool enabled;
} soarm100_interfaces__srv__SetAvoidance_Request;

// Struct for a sequence of soarm100_interfaces__srv__SetAvoidance_Request.
typedef struct soarm100_interfaces__srv__SetAvoidance_Request__Sequence
{
  soarm100_interfaces__srv__SetAvoidance_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__srv__SetAvoidance_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'reason'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/SetAvoidance in the package soarm100_interfaces.
typedef struct soarm100_interfaces__srv__SetAvoidance_Response
{
  bool success;
  rosidl_runtime_c__String reason;
} soarm100_interfaces__srv__SetAvoidance_Response;

// Struct for a sequence of soarm100_interfaces__srv__SetAvoidance_Response.
typedef struct soarm100_interfaces__srv__SetAvoidance_Response__Sequence
{
  soarm100_interfaces__srv__SetAvoidance_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__srv__SetAvoidance_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SOARM100_INTERFACES__SRV__DETAIL__SET_AVOIDANCE__STRUCT_H_
