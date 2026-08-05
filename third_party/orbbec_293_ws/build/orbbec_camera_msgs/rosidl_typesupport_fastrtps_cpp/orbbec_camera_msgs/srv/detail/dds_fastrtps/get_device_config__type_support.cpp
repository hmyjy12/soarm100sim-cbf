// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from orbbec_camera_msgs:srv/GetDeviceConfig.idl
// generated code does not contain a copyright notice
#include "orbbec_camera_msgs/srv/detail/get_device_config__rosidl_typesupport_fastrtps_cpp.hpp"
#include "orbbec_camera_msgs/srv/detail/get_device_config__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace orbbec_camera_msgs
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_orbbec_camera_msgs
cdr_serialize(
  const orbbec_camera_msgs::srv::GetDeviceConfig_Request & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: structure_needs_at_least_one_member
  cdr << ros_message.structure_needs_at_least_one_member;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_orbbec_camera_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  orbbec_camera_msgs::srv::GetDeviceConfig_Request & ros_message)
{
  // Member: structure_needs_at_least_one_member
  cdr >> ros_message.structure_needs_at_least_one_member;

  return true;
}  // NOLINT(readability/fn_size)

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_orbbec_camera_msgs
get_serialized_size(
  const orbbec_camera_msgs::srv::GetDeviceConfig_Request & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: structure_needs_at_least_one_member
  {
    size_t item_size = sizeof(ros_message.structure_needs_at_least_one_member);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_orbbec_camera_msgs
max_serialized_size_GetDeviceConfig_Request(
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


  // Member: structure_needs_at_least_one_member
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
    using DataType = orbbec_camera_msgs::srv::GetDeviceConfig_Request;
    is_plain =
      (
      offsetof(DataType, structure_needs_at_least_one_member) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _GetDeviceConfig_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const orbbec_camera_msgs::srv::GetDeviceConfig_Request *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _GetDeviceConfig_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<orbbec_camera_msgs::srv::GetDeviceConfig_Request *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _GetDeviceConfig_Request__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const orbbec_camera_msgs::srv::GetDeviceConfig_Request *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _GetDeviceConfig_Request__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_GetDeviceConfig_Request(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _GetDeviceConfig_Request__callbacks = {
  "orbbec_camera_msgs::srv",
  "GetDeviceConfig_Request",
  _GetDeviceConfig_Request__cdr_serialize,
  _GetDeviceConfig_Request__cdr_deserialize,
  _GetDeviceConfig_Request__get_serialized_size,
  _GetDeviceConfig_Request__max_serialized_size
};

static rosidl_message_type_support_t _GetDeviceConfig_Request__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_GetDeviceConfig_Request__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace orbbec_camera_msgs

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_orbbec_camera_msgs
const rosidl_message_type_support_t *
get_message_type_support_handle<orbbec_camera_msgs::srv::GetDeviceConfig_Request>()
{
  return &orbbec_camera_msgs::srv::typesupport_fastrtps_cpp::_GetDeviceConfig_Request__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, orbbec_camera_msgs, srv, GetDeviceConfig_Request)() {
  return &orbbec_camera_msgs::srv::typesupport_fastrtps_cpp::_GetDeviceConfig_Request__handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include <limits>
// already included above
// #include <stdexcept>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
// already included above
// #include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace orbbec_camera_msgs
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_orbbec_camera_msgs
cdr_serialize(
  const orbbec_camera_msgs::srv::GetDeviceConfig_Response & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: schema_version
  cdr << ros_message.schema_version;
  // Member: device_preset
  cdr << ros_message.device_preset;
  // Member: preset_version
  cdr << ros_message.preset_version;
  // Member: color_preset
  cdr << ros_message.color_preset;
  // Member: depth_precision
  cdr << ros_message.depth_precision;
  // Member: disparity_to_depth_mode
  cdr << ros_message.disparity_to_depth_mode;
  // Member: exposure_range_mode
  cdr << ros_message.exposure_range_mode;
  // Member: depth_registration
  cdr << (ros_message.depth_registration ? true : false);
  // Member: align_mode
  cdr << ros_message.align_mode;
  // Member: align_target_stream
  cdr << ros_message.align_target_stream;
  // Member: frame_aggregate_mode
  cdr << ros_message.frame_aggregate_mode;
  // Member: enable_frame_sync
  cdr << (ros_message.enable_frame_sync ? true : false);
  // Member: time_domain
  cdr << ros_message.time_domain;
  // Member: sync_mode
  cdr << ros_message.sync_mode;
  // Member: intra_camera_sync_reference
  cdr << ros_message.intra_camera_sync_reference;
  // Member: data_json
  cdr << ros_message.data_json;
  // Member: success
  cdr << (ros_message.success ? true : false);
  // Member: message
  cdr << ros_message.message;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_orbbec_camera_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  orbbec_camera_msgs::srv::GetDeviceConfig_Response & ros_message)
{
  // Member: schema_version
  cdr >> ros_message.schema_version;

  // Member: device_preset
  cdr >> ros_message.device_preset;

  // Member: preset_version
  cdr >> ros_message.preset_version;

  // Member: color_preset
  cdr >> ros_message.color_preset;

  // Member: depth_precision
  cdr >> ros_message.depth_precision;

  // Member: disparity_to_depth_mode
  cdr >> ros_message.disparity_to_depth_mode;

  // Member: exposure_range_mode
  cdr >> ros_message.exposure_range_mode;

  // Member: depth_registration
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.depth_registration = tmp ? true : false;
  }

  // Member: align_mode
  cdr >> ros_message.align_mode;

  // Member: align_target_stream
  cdr >> ros_message.align_target_stream;

  // Member: frame_aggregate_mode
  cdr >> ros_message.frame_aggregate_mode;

  // Member: enable_frame_sync
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.enable_frame_sync = tmp ? true : false;
  }

  // Member: time_domain
  cdr >> ros_message.time_domain;

  // Member: sync_mode
  cdr >> ros_message.sync_mode;

  // Member: intra_camera_sync_reference
  cdr >> ros_message.intra_camera_sync_reference;

  // Member: data_json
  cdr >> ros_message.data_json;

  // Member: success
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.success = tmp ? true : false;
  }

  // Member: message
  cdr >> ros_message.message;

  return true;
}  // NOLINT(readability/fn_size)

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_orbbec_camera_msgs
get_serialized_size(
  const orbbec_camera_msgs::srv::GetDeviceConfig_Response & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: schema_version
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.schema_version.size() + 1);
  // Member: device_preset
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.device_preset.size() + 1);
  // Member: preset_version
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.preset_version.size() + 1);
  // Member: color_preset
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.color_preset.size() + 1);
  // Member: depth_precision
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.depth_precision.size() + 1);
  // Member: disparity_to_depth_mode
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.disparity_to_depth_mode.size() + 1);
  // Member: exposure_range_mode
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.exposure_range_mode.size() + 1);
  // Member: depth_registration
  {
    size_t item_size = sizeof(ros_message.depth_registration);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: align_mode
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.align_mode.size() + 1);
  // Member: align_target_stream
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.align_target_stream.size() + 1);
  // Member: frame_aggregate_mode
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.frame_aggregate_mode.size() + 1);
  // Member: enable_frame_sync
  {
    size_t item_size = sizeof(ros_message.enable_frame_sync);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: time_domain
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.time_domain.size() + 1);
  // Member: sync_mode
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.sync_mode.size() + 1);
  // Member: intra_camera_sync_reference
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.intra_camera_sync_reference.size() + 1);
  // Member: data_json
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.data_json.size() + 1);
  // Member: success
  {
    size_t item_size = sizeof(ros_message.success);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: message
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.message.size() + 1);

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_orbbec_camera_msgs
max_serialized_size_GetDeviceConfig_Response(
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


  // Member: schema_version
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

  // Member: device_preset
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

  // Member: preset_version
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

  // Member: color_preset
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

  // Member: depth_precision
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

  // Member: disparity_to_depth_mode
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

  // Member: exposure_range_mode
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

  // Member: depth_registration
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: align_mode
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

  // Member: align_target_stream
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

  // Member: frame_aggregate_mode
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

  // Member: enable_frame_sync
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: time_domain
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

  // Member: sync_mode
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

  // Member: intra_camera_sync_reference
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

  // Member: data_json
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

  // Member: success
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: message
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
    using DataType = orbbec_camera_msgs::srv::GetDeviceConfig_Response;
    is_plain =
      (
      offsetof(DataType, message) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _GetDeviceConfig_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const orbbec_camera_msgs::srv::GetDeviceConfig_Response *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _GetDeviceConfig_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<orbbec_camera_msgs::srv::GetDeviceConfig_Response *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _GetDeviceConfig_Response__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const orbbec_camera_msgs::srv::GetDeviceConfig_Response *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _GetDeviceConfig_Response__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_GetDeviceConfig_Response(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _GetDeviceConfig_Response__callbacks = {
  "orbbec_camera_msgs::srv",
  "GetDeviceConfig_Response",
  _GetDeviceConfig_Response__cdr_serialize,
  _GetDeviceConfig_Response__cdr_deserialize,
  _GetDeviceConfig_Response__get_serialized_size,
  _GetDeviceConfig_Response__max_serialized_size
};

static rosidl_message_type_support_t _GetDeviceConfig_Response__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_GetDeviceConfig_Response__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace orbbec_camera_msgs

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_orbbec_camera_msgs
const rosidl_message_type_support_t *
get_message_type_support_handle<orbbec_camera_msgs::srv::GetDeviceConfig_Response>()
{
  return &orbbec_camera_msgs::srv::typesupport_fastrtps_cpp::_GetDeviceConfig_Response__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, orbbec_camera_msgs, srv, GetDeviceConfig_Response)() {
  return &orbbec_camera_msgs::srv::typesupport_fastrtps_cpp::_GetDeviceConfig_Response__handle;
}

#ifdef __cplusplus
}
#endif

#include "rmw/error_handling.h"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/service_type_support_decl.hpp"

namespace orbbec_camera_msgs
{

namespace srv
{

namespace typesupport_fastrtps_cpp
{

static service_type_support_callbacks_t _GetDeviceConfig__callbacks = {
  "orbbec_camera_msgs::srv",
  "GetDeviceConfig",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, orbbec_camera_msgs, srv, GetDeviceConfig_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, orbbec_camera_msgs, srv, GetDeviceConfig_Response)(),
};

static rosidl_service_type_support_t _GetDeviceConfig__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_GetDeviceConfig__callbacks,
  get_service_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace srv

}  // namespace orbbec_camera_msgs

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_orbbec_camera_msgs
const rosidl_service_type_support_t *
get_service_type_support_handle<orbbec_camera_msgs::srv::GetDeviceConfig>()
{
  return &orbbec_camera_msgs::srv::typesupport_fastrtps_cpp::_GetDeviceConfig__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, orbbec_camera_msgs, srv, GetDeviceConfig)() {
  return &orbbec_camera_msgs::srv::typesupport_fastrtps_cpp::_GetDeviceConfig__handle;
}

#ifdef __cplusplus
}
#endif
