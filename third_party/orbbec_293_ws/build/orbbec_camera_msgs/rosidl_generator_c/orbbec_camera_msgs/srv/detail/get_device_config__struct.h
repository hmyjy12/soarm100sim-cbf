// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from orbbec_camera_msgs:srv/GetDeviceConfig.idl
// generated code does not contain a copyright notice

#ifndef ORBBEC_CAMERA_MSGS__SRV__DETAIL__GET_DEVICE_CONFIG__STRUCT_H_
#define ORBBEC_CAMERA_MSGS__SRV__DETAIL__GET_DEVICE_CONFIG__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/GetDeviceConfig in the package orbbec_camera_msgs.
typedef struct orbbec_camera_msgs__srv__GetDeviceConfig_Request
{
  uint8_t structure_needs_at_least_one_member;
} orbbec_camera_msgs__srv__GetDeviceConfig_Request;

// Struct for a sequence of orbbec_camera_msgs__srv__GetDeviceConfig_Request.
typedef struct orbbec_camera_msgs__srv__GetDeviceConfig_Request__Sequence
{
  orbbec_camera_msgs__srv__GetDeviceConfig_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} orbbec_camera_msgs__srv__GetDeviceConfig_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'schema_version'
// Member 'device_preset'
// Member 'preset_version'
// Member 'color_preset'
// Member 'depth_precision'
// Member 'disparity_to_depth_mode'
// Member 'exposure_range_mode'
// Member 'align_mode'
// Member 'align_target_stream'
// Member 'frame_aggregate_mode'
// Member 'time_domain'
// Member 'sync_mode'
// Member 'intra_camera_sync_reference'
// Member 'data_json'
// Member 'message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/GetDeviceConfig in the package orbbec_camera_msgs.
typedef struct orbbec_camera_msgs__srv__GetDeviceConfig_Response
{
  rosidl_runtime_c__String schema_version;
  /// Effective device configuration state that is not provided by existing device/version services.
  rosidl_runtime_c__String device_preset;
  rosidl_runtime_c__String preset_version;
  rosidl_runtime_c__String color_preset;
  rosidl_runtime_c__String depth_precision;
  rosidl_runtime_c__String disparity_to_depth_mode;
  rosidl_runtime_c__String exposure_range_mode;
  bool depth_registration;
  rosidl_runtime_c__String align_mode;
  rosidl_runtime_c__String align_target_stream;
  rosidl_runtime_c__String frame_aggregate_mode;
  bool enable_frame_sync;
  rosidl_runtime_c__String time_domain;
  rosidl_runtime_c__String sync_mode;
  rosidl_runtime_c__String intra_camera_sync_reference;
  /// Reserved for future non-breaking, device-specific extensions.
  rosidl_runtime_c__String data_json;
  bool success;
  rosidl_runtime_c__String message;
} orbbec_camera_msgs__srv__GetDeviceConfig_Response;

// Struct for a sequence of orbbec_camera_msgs__srv__GetDeviceConfig_Response.
typedef struct orbbec_camera_msgs__srv__GetDeviceConfig_Response__Sequence
{
  orbbec_camera_msgs__srv__GetDeviceConfig_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} orbbec_camera_msgs__srv__GetDeviceConfig_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ORBBEC_CAMERA_MSGS__SRV__DETAIL__GET_DEVICE_CONFIG__STRUCT_H_
