// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from soarm100_interfaces:srv/MoveNamedPose.idl
// generated code does not contain a copyright notice
#include "soarm100_interfaces/srv/detail/move_named_pose__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "soarm100_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "soarm100_interfaces/srv/detail/move_named_pose__struct.h"
#include "soarm100_interfaces/srv/detail/move_named_pose__functions.h"
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

#include "rosidl_runtime_c/string.h"  // confirmation, pose_name
#include "rosidl_runtime_c/string_functions.h"  // confirmation, pose_name

// forward declare type support functions


using _MoveNamedPose_Request__ros_msg_type = soarm100_interfaces__srv__MoveNamedPose_Request;

static bool _MoveNamedPose_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _MoveNamedPose_Request__ros_msg_type * ros_message = static_cast<const _MoveNamedPose_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: pose_name
  {
    const rosidl_runtime_c__String * str = &ros_message->pose_name;
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

  // Field name: duration
  {
    cdr << ros_message->duration;
  }

  // Field name: hold
  {
    cdr << ros_message->hold;
  }

  // Field name: confirmation
  {
    const rosidl_runtime_c__String * str = &ros_message->confirmation;
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

static bool _MoveNamedPose_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _MoveNamedPose_Request__ros_msg_type * ros_message = static_cast<_MoveNamedPose_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: pose_name
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->pose_name.data) {
      rosidl_runtime_c__String__init(&ros_message->pose_name);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->pose_name,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'pose_name'\n");
      return false;
    }
  }

  // Field name: duration
  {
    cdr >> ros_message->duration;
  }

  // Field name: hold
  {
    cdr >> ros_message->hold;
  }

  // Field name: confirmation
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->confirmation.data) {
      rosidl_runtime_c__String__init(&ros_message->confirmation);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->confirmation,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'confirmation'\n");
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_soarm100_interfaces
size_t get_serialized_size_soarm100_interfaces__srv__MoveNamedPose_Request(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _MoveNamedPose_Request__ros_msg_type * ros_message = static_cast<const _MoveNamedPose_Request__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name pose_name
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->pose_name.size + 1);
  // field.name duration
  {
    size_t item_size = sizeof(ros_message->duration);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name hold
  {
    size_t item_size = sizeof(ros_message->hold);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name confirmation
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->confirmation.size + 1);

  return current_alignment - initial_alignment;
}

static uint32_t _MoveNamedPose_Request__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_soarm100_interfaces__srv__MoveNamedPose_Request(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_soarm100_interfaces
size_t max_serialized_size_soarm100_interfaces__srv__MoveNamedPose_Request(
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

  // member: pose_name
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
  // member: duration
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: hold
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: confirmation
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
    using DataType = soarm100_interfaces__srv__MoveNamedPose_Request;
    is_plain =
      (
      offsetof(DataType, confirmation) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _MoveNamedPose_Request__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_soarm100_interfaces__srv__MoveNamedPose_Request(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_MoveNamedPose_Request = {
  "soarm100_interfaces::srv",
  "MoveNamedPose_Request",
  _MoveNamedPose_Request__cdr_serialize,
  _MoveNamedPose_Request__cdr_deserialize,
  _MoveNamedPose_Request__get_serialized_size,
  _MoveNamedPose_Request__max_serialized_size
};

static rosidl_message_type_support_t _MoveNamedPose_Request__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_MoveNamedPose_Request,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, soarm100_interfaces, srv, MoveNamedPose_Request)() {
  return &_MoveNamedPose_Request__type_support;
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
// #include "soarm100_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
// already included above
// #include "soarm100_interfaces/srv/detail/move_named_pose__struct.h"
// already included above
// #include "soarm100_interfaces/srv/detail/move_named_pose__functions.h"
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

// already included above
// #include "rosidl_runtime_c/string.h"  // log_path, reason
// already included above
// #include "rosidl_runtime_c/string_functions.h"  // log_path, reason

// forward declare type support functions


using _MoveNamedPose_Response__ros_msg_type = soarm100_interfaces__srv__MoveNamedPose_Response;

static bool _MoveNamedPose_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _MoveNamedPose_Response__ros_msg_type * ros_message = static_cast<const _MoveNamedPose_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: success
  {
    cdr << (ros_message->success ? true : false);
  }

  // Field name: reason
  {
    const rosidl_runtime_c__String * str = &ros_message->reason;
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

  // Field name: log_path
  {
    const rosidl_runtime_c__String * str = &ros_message->log_path;
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

static bool _MoveNamedPose_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _MoveNamedPose_Response__ros_msg_type * ros_message = static_cast<_MoveNamedPose_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: success
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->success = tmp ? true : false;
  }

  // Field name: reason
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->reason.data) {
      rosidl_runtime_c__String__init(&ros_message->reason);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->reason,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'reason'\n");
      return false;
    }
  }

  // Field name: log_path
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->log_path.data) {
      rosidl_runtime_c__String__init(&ros_message->log_path);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->log_path,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'log_path'\n");
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_soarm100_interfaces
size_t get_serialized_size_soarm100_interfaces__srv__MoveNamedPose_Response(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _MoveNamedPose_Response__ros_msg_type * ros_message = static_cast<const _MoveNamedPose_Response__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name success
  {
    size_t item_size = sizeof(ros_message->success);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name reason
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->reason.size + 1);
  // field.name log_path
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->log_path.size + 1);

  return current_alignment - initial_alignment;
}

static uint32_t _MoveNamedPose_Response__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_soarm100_interfaces__srv__MoveNamedPose_Response(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_soarm100_interfaces
size_t max_serialized_size_soarm100_interfaces__srv__MoveNamedPose_Response(
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

  // member: success
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: reason
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
  // member: log_path
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
    using DataType = soarm100_interfaces__srv__MoveNamedPose_Response;
    is_plain =
      (
      offsetof(DataType, log_path) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _MoveNamedPose_Response__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_soarm100_interfaces__srv__MoveNamedPose_Response(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_MoveNamedPose_Response = {
  "soarm100_interfaces::srv",
  "MoveNamedPose_Response",
  _MoveNamedPose_Response__cdr_serialize,
  _MoveNamedPose_Response__cdr_deserialize,
  _MoveNamedPose_Response__get_serialized_size,
  _MoveNamedPose_Response__max_serialized_size
};

static rosidl_message_type_support_t _MoveNamedPose_Response__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_MoveNamedPose_Response,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, soarm100_interfaces, srv, MoveNamedPose_Response)() {
  return &_MoveNamedPose_Response__type_support;
}

#if defined(__cplusplus)
}
#endif

#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "soarm100_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "soarm100_interfaces/srv/move_named_pose.h"

#if defined(__cplusplus)
extern "C"
{
#endif

static service_type_support_callbacks_t MoveNamedPose__callbacks = {
  "soarm100_interfaces::srv",
  "MoveNamedPose",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, soarm100_interfaces, srv, MoveNamedPose_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, soarm100_interfaces, srv, MoveNamedPose_Response)(),
};

static rosidl_service_type_support_t MoveNamedPose__handle = {
  rosidl_typesupport_fastrtps_c__identifier,
  &MoveNamedPose__callbacks,
  get_service_typesupport_handle_function,
};

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, soarm100_interfaces, srv, MoveNamedPose)() {
  return &MoveNamedPose__handle;
}

#if defined(__cplusplus)
}
#endif
