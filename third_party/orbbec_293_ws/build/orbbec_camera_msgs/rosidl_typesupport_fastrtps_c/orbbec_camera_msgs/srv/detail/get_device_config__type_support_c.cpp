// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from orbbec_camera_msgs:srv/GetDeviceConfig.idl
// generated code does not contain a copyright notice
#include "orbbec_camera_msgs/srv/detail/get_device_config__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "orbbec_camera_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "orbbec_camera_msgs/srv/detail/get_device_config__struct.h"
#include "orbbec_camera_msgs/srv/detail/get_device_config__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif


// forward declare type support functions


using _GetDeviceConfig_Request__ros_msg_type = orbbec_camera_msgs__srv__GetDeviceConfig_Request;

static bool _GetDeviceConfig_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _GetDeviceConfig_Request__ros_msg_type * ros_message = static_cast<const _GetDeviceConfig_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: structure_needs_at_least_one_member
  {
    cdr << ros_message->structure_needs_at_least_one_member;
  }

  return true;
}

static bool _GetDeviceConfig_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _GetDeviceConfig_Request__ros_msg_type * ros_message = static_cast<_GetDeviceConfig_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: structure_needs_at_least_one_member
  {
    cdr >> ros_message->structure_needs_at_least_one_member;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_orbbec_camera_msgs
size_t get_serialized_size_orbbec_camera_msgs__srv__GetDeviceConfig_Request(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _GetDeviceConfig_Request__ros_msg_type * ros_message = static_cast<const _GetDeviceConfig_Request__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name structure_needs_at_least_one_member
  {
    size_t item_size = sizeof(ros_message->structure_needs_at_least_one_member);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _GetDeviceConfig_Request__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_orbbec_camera_msgs__srv__GetDeviceConfig_Request(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_orbbec_camera_msgs
size_t max_serialized_size_orbbec_camera_msgs__srv__GetDeviceConfig_Request(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: structure_needs_at_least_one_member
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = orbbec_camera_msgs__srv__GetDeviceConfig_Request;
    is_plain =
      (
      offsetof(DataType, structure_needs_at_least_one_member) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _GetDeviceConfig_Request__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_orbbec_camera_msgs__srv__GetDeviceConfig_Request(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_GetDeviceConfig_Request = {
  "orbbec_camera_msgs::srv",
  "GetDeviceConfig_Request",
  _GetDeviceConfig_Request__cdr_serialize,
  _GetDeviceConfig_Request__cdr_deserialize,
  _GetDeviceConfig_Request__get_serialized_size,
  _GetDeviceConfig_Request__max_serialized_size
};

static rosidl_message_type_support_t _GetDeviceConfig_Request__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_GetDeviceConfig_Request,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, orbbec_camera_msgs, srv, GetDeviceConfig_Request)() {
  return &_GetDeviceConfig_Request__type_support;
}

#if defined(__cplusplus)
}
#endif

// already included above
// #include <cassert>
// already included above
// #include <limits>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "orbbec_camera_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
// already included above
// #include "orbbec_camera_msgs/srv/detail/get_device_config__struct.h"
// already included above
// #include "orbbec_camera_msgs/srv/detail/get_device_config__functions.h"
// already included above
// #include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "rosidl_runtime_c/string.h"  // align_mode, align_target_stream, color_preset, data_json, depth_precision, device_preset, disparity_to_depth_mode, exposure_range_mode, frame_aggregate_mode, intra_camera_sync_reference, message, preset_version, schema_version, sync_mode, time_domain
#include "rosidl_runtime_c/string_functions.h"  // align_mode, align_target_stream, color_preset, data_json, depth_precision, device_preset, disparity_to_depth_mode, exposure_range_mode, frame_aggregate_mode, intra_camera_sync_reference, message, preset_version, schema_version, sync_mode, time_domain

// forward declare type support functions


using _GetDeviceConfig_Response__ros_msg_type = orbbec_camera_msgs__srv__GetDeviceConfig_Response;

static bool _GetDeviceConfig_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _GetDeviceConfig_Response__ros_msg_type * ros_message = static_cast<const _GetDeviceConfig_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: schema_version
  {
    const rosidl_runtime_c__String * str = &ros_message->schema_version;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: device_preset
  {
    const rosidl_runtime_c__String * str = &ros_message->device_preset;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: preset_version
  {
    const rosidl_runtime_c__String * str = &ros_message->preset_version;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: color_preset
  {
    const rosidl_runtime_c__String * str = &ros_message->color_preset;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: depth_precision
  {
    const rosidl_runtime_c__String * str = &ros_message->depth_precision;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: disparity_to_depth_mode
  {
    const rosidl_runtime_c__String * str = &ros_message->disparity_to_depth_mode;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: exposure_range_mode
  {
    const rosidl_runtime_c__String * str = &ros_message->exposure_range_mode;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: depth_registration
  {
    cdr << (ros_message->depth_registration ? true : false);
  }

  // Field name: align_mode
  {
    const rosidl_runtime_c__String * str = &ros_message->align_mode;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: align_target_stream
  {
    const rosidl_runtime_c__String * str = &ros_message->align_target_stream;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: frame_aggregate_mode
  {
    const rosidl_runtime_c__String * str = &ros_message->frame_aggregate_mode;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: enable_frame_sync
  {
    cdr << (ros_message->enable_frame_sync ? true : false);
  }

  // Field name: time_domain
  {
    const rosidl_runtime_c__String * str = &ros_message->time_domain;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: sync_mode
  {
    const rosidl_runtime_c__String * str = &ros_message->sync_mode;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: intra_camera_sync_reference
  {
    const rosidl_runtime_c__String * str = &ros_message->intra_camera_sync_reference;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: data_json
  {
    const rosidl_runtime_c__String * str = &ros_message->data_json;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: success
  {
    cdr << (ros_message->success ? true : false);
  }

  // Field name: message
  {
    const rosidl_runtime_c__String * str = &ros_message->message;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

static bool _GetDeviceConfig_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _GetDeviceConfig_Response__ros_msg_type * ros_message = static_cast<_GetDeviceConfig_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: schema_version
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->schema_version.data) {
      rosidl_runtime_c__String__init(&ros_message->schema_version);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->schema_version,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'schema_version'\n");
      return false;
    }
  }

  // Field name: device_preset
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->device_preset.data) {
      rosidl_runtime_c__String__init(&ros_message->device_preset);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->device_preset,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'device_preset'\n");
      return false;
    }
  }

  // Field name: preset_version
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->preset_version.data) {
      rosidl_runtime_c__String__init(&ros_message->preset_version);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->preset_version,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'preset_version'\n");
      return false;
    }
  }

  // Field name: color_preset
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->color_preset.data) {
      rosidl_runtime_c__String__init(&ros_message->color_preset);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->color_preset,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'color_preset'\n");
      return false;
    }
  }

  // Field name: depth_precision
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->depth_precision.data) {
      rosidl_runtime_c__String__init(&ros_message->depth_precision);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->depth_precision,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'depth_precision'\n");
      return false;
    }
  }

  // Field name: disparity_to_depth_mode
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->disparity_to_depth_mode.data) {
      rosidl_runtime_c__String__init(&ros_message->disparity_to_depth_mode);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->disparity_to_depth_mode,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'disparity_to_depth_mode'\n");
      return false;
    }
  }

  // Field name: exposure_range_mode
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->exposure_range_mode.data) {
      rosidl_runtime_c__String__init(&ros_message->exposure_range_mode);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->exposure_range_mode,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'exposure_range_mode'\n");
      return false;
    }
  }

  // Field name: depth_registration
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->depth_registration = tmp ? true : false;
  }

  // Field name: align_mode
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->align_mode.data) {
      rosidl_runtime_c__String__init(&ros_message->align_mode);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->align_mode,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'align_mode'\n");
      return false;
    }
  }

  // Field name: align_target_stream
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->align_target_stream.data) {
      rosidl_runtime_c__String__init(&ros_message->align_target_stream);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->align_target_stream,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'align_target_stream'\n");
      return false;
    }
  }

  // Field name: frame_aggregate_mode
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->frame_aggregate_mode.data) {
      rosidl_runtime_c__String__init(&ros_message->frame_aggregate_mode);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->frame_aggregate_mode,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'frame_aggregate_mode'\n");
      return false;
    }
  }

  // Field name: enable_frame_sync
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->enable_frame_sync = tmp ? true : false;
  }

  // Field name: time_domain
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->time_domain.data) {
      rosidl_runtime_c__String__init(&ros_message->time_domain);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->time_domain,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'time_domain'\n");
      return false;
    }
  }

  // Field name: sync_mode
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->sync_mode.data) {
      rosidl_runtime_c__String__init(&ros_message->sync_mode);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->sync_mode,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'sync_mode'\n");
      return false;
    }
  }

  // Field name: intra_camera_sync_reference
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->intra_camera_sync_reference.data) {
      rosidl_runtime_c__String__init(&ros_message->intra_camera_sync_reference);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->intra_camera_sync_reference,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'intra_camera_sync_reference'\n");
      return false;
    }
  }

  // Field name: data_json
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->data_json.data) {
      rosidl_runtime_c__String__init(&ros_message->data_json);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->data_json,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'data_json'\n");
      return false;
    }
  }

  // Field name: success
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->success = tmp ? true : false;
  }

  // Field name: message
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->message.data) {
      rosidl_runtime_c__String__init(&ros_message->message);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->message,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'message'\n");
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_orbbec_camera_msgs
size_t get_serialized_size_orbbec_camera_msgs__srv__GetDeviceConfig_Response(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _GetDeviceConfig_Response__ros_msg_type * ros_message = static_cast<const _GetDeviceConfig_Response__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name schema_version
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->schema_version.size + 1);
  // field.name device_preset
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->device_preset.size + 1);
  // field.name preset_version
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->preset_version.size + 1);
  // field.name color_preset
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->color_preset.size + 1);
  // field.name depth_precision
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->depth_precision.size + 1);
  // field.name disparity_to_depth_mode
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->disparity_to_depth_mode.size + 1);
  // field.name exposure_range_mode
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->exposure_range_mode.size + 1);
  // field.name depth_registration
  {
    size_t item_size = sizeof(ros_message->depth_registration);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name align_mode
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->align_mode.size + 1);
  // field.name align_target_stream
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->align_target_stream.size + 1);
  // field.name frame_aggregate_mode
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->frame_aggregate_mode.size + 1);
  // field.name enable_frame_sync
  {
    size_t item_size = sizeof(ros_message->enable_frame_sync);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name time_domain
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->time_domain.size + 1);
  // field.name sync_mode
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->sync_mode.size + 1);
  // field.name intra_camera_sync_reference
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->intra_camera_sync_reference.size + 1);
  // field.name data_json
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->data_json.size + 1);
  // field.name success
  {
    size_t item_size = sizeof(ros_message->success);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name message
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->message.size + 1);

  return current_alignment - initial_alignment;
}

static uint32_t _GetDeviceConfig_Response__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_orbbec_camera_msgs__srv__GetDeviceConfig_Response(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_orbbec_camera_msgs
size_t max_serialized_size_orbbec_camera_msgs__srv__GetDeviceConfig_Response(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: schema_version
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: device_preset
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: preset_version
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: color_preset
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: depth_precision
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: disparity_to_depth_mode
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: exposure_range_mode
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: depth_registration
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: align_mode
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: align_target_stream
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: frame_aggregate_mode
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: enable_frame_sync
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: time_domain
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: sync_mode
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: intra_camera_sync_reference
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: data_json
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: success
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: message
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = orbbec_camera_msgs__srv__GetDeviceConfig_Response;
    is_plain =
      (
      offsetof(DataType, message) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _GetDeviceConfig_Response__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_orbbec_camera_msgs__srv__GetDeviceConfig_Response(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_GetDeviceConfig_Response = {
  "orbbec_camera_msgs::srv",
  "GetDeviceConfig_Response",
  _GetDeviceConfig_Response__cdr_serialize,
  _GetDeviceConfig_Response__cdr_deserialize,
  _GetDeviceConfig_Response__get_serialized_size,
  _GetDeviceConfig_Response__max_serialized_size
};

static rosidl_message_type_support_t _GetDeviceConfig_Response__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_GetDeviceConfig_Response,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, orbbec_camera_msgs, srv, GetDeviceConfig_Response)() {
  return &_GetDeviceConfig_Response__type_support;
}

#if defined(__cplusplus)
}
#endif

#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "orbbec_camera_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "orbbec_camera_msgs/srv/get_device_config.h"

#if defined(__cplusplus)
extern "C"
{
#endif

static service_type_support_callbacks_t GetDeviceConfig__callbacks = {
  "orbbec_camera_msgs::srv",
  "GetDeviceConfig",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, orbbec_camera_msgs, srv, GetDeviceConfig_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, orbbec_camera_msgs, srv, GetDeviceConfig_Response)(),
};

static rosidl_service_type_support_t GetDeviceConfig__handle = {
  rosidl_typesupport_fastrtps_c__identifier,
  &GetDeviceConfig__callbacks,
  get_service_typesupport_handle_function,
};

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, orbbec_camera_msgs, srv, GetDeviceConfig)() {
  return &GetDeviceConfig__handle;
}

#if defined(__cplusplus)
}
#endif
