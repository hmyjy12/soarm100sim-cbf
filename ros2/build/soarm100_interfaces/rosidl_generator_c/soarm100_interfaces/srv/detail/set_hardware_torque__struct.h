// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from soarm100_interfaces:srv/SetHardwareTorque.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__SRV__DETAIL__SET_HARDWARE_TORQUE__STRUCT_H_
#define SOARM100_INTERFACES__SRV__DETAIL__SET_HARDWARE_TORQUE__STRUCT_H_

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

/// Struct defined in srv/SetHardwareTorque in the package soarm100_interfaces.
typedef struct soarm100_interfaces__srv__SetHardwareTorque_Request
{
  bool enabled;
  rosidl_runtime_c__String confirmation;
} soarm100_interfaces__srv__SetHardwareTorque_Request;

// Struct for a sequence of soarm100_interfaces__srv__SetHardwareTorque_Request.
typedef struct soarm100_interfaces__srv__SetHardwareTorque_Request__Sequence
{
  soarm100_interfaces__srv__SetHardwareTorque_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__srv__SetHardwareTorque_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'reason'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/SetHardwareTorque in the package soarm100_interfaces.
typedef struct soarm100_interfaces__srv__SetHardwareTorque_Response
{
  bool success;
  rosidl_runtime_c__String reason;
} soarm100_interfaces__srv__SetHardwareTorque_Response;

// Struct for a sequence of soarm100_interfaces__srv__SetHardwareTorque_Response.
typedef struct soarm100_interfaces__srv__SetHardwareTorque_Response__Sequence
{
  soarm100_interfaces__srv__SetHardwareTorque_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} soarm100_interfaces__srv__SetHardwareTorque_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SOARM100_INTERFACES__SRV__DETAIL__SET_HARDWARE_TORQUE__STRUCT_H_
