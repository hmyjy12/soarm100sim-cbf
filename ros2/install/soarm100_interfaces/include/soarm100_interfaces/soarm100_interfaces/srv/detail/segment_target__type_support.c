// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from soarm100_interfaces:srv/SegmentTarget.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "soarm100_interfaces/srv/detail/segment_target__rosidl_typesupport_introspection_c.h"
#include "soarm100_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "soarm100_interfaces/srv/detail/segment_target__functions.h"
#include "soarm100_interfaces/srv/detail/segment_target__struct.h"


// Include directives for member types
// Member `target_prompt`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void soarm100_interfaces__srv__SegmentTarget_Request__rosidl_typesupport_introspection_c__SegmentTarget_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  soarm100_interfaces__srv__SegmentTarget_Request__init(message_memory);
}

void soarm100_interfaces__srv__SegmentTarget_Request__rosidl_typesupport_introspection_c__SegmentTarget_Request_fini_function(void * message_memory)
{
  soarm100_interfaces__srv__SegmentTarget_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember soarm100_interfaces__srv__SegmentTarget_Request__rosidl_typesupport_introspection_c__SegmentTarget_Request_message_member_array[2] = {
  {
    "target_prompt",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__srv__SegmentTarget_Request, target_prompt),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "force_yolo",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__srv__SegmentTarget_Request, force_yolo),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers soarm100_interfaces__srv__SegmentTarget_Request__rosidl_typesupport_introspection_c__SegmentTarget_Request_message_members = {
  "soarm100_interfaces__srv",  // message namespace
  "SegmentTarget_Request",  // message name
  2,  // number of fields
  sizeof(soarm100_interfaces__srv__SegmentTarget_Request),
  soarm100_interfaces__srv__SegmentTarget_Request__rosidl_typesupport_introspection_c__SegmentTarget_Request_message_member_array,  // message members
  soarm100_interfaces__srv__SegmentTarget_Request__rosidl_typesupport_introspection_c__SegmentTarget_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  soarm100_interfaces__srv__SegmentTarget_Request__rosidl_typesupport_introspection_c__SegmentTarget_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t soarm100_interfaces__srv__SegmentTarget_Request__rosidl_typesupport_introspection_c__SegmentTarget_Request_message_type_support_handle = {
  0,
  &soarm100_interfaces__srv__SegmentTarget_Request__rosidl_typesupport_introspection_c__SegmentTarget_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_soarm100_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, srv, SegmentTarget_Request)() {
  if (!soarm100_interfaces__srv__SegmentTarget_Request__rosidl_typesupport_introspection_c__SegmentTarget_Request_message_type_support_handle.typesupport_identifier) {
    soarm100_interfaces__srv__SegmentTarget_Request__rosidl_typesupport_introspection_c__SegmentTarget_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &soarm100_interfaces__srv__SegmentTarget_Request__rosidl_typesupport_introspection_c__SegmentTarget_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "soarm100_interfaces/srv/detail/segment_target__rosidl_typesupport_introspection_c.h"
// already included above
// #include "soarm100_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "soarm100_interfaces/srv/detail/segment_target__functions.h"
// already included above
// #include "soarm100_interfaces/srv/detail/segment_target__struct.h"


// Include directives for member types
// Member `reason`
// Member `mask_topic`
// Member `debug_json`
// already included above
// #include "rosidl_runtime_c/string_functions.h"
// Member `target_center`
#include "geometry_msgs/msg/pose_stamped.h"
// Member `target_center`
#include "geometry_msgs/msg/detail/pose_stamped__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__SegmentTarget_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  soarm100_interfaces__srv__SegmentTarget_Response__init(message_memory);
}

void soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__SegmentTarget_Response_fini_function(void * message_memory)
{
  soarm100_interfaces__srv__SegmentTarget_Response__fini(message_memory);
}

size_t soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__size_function__SegmentTarget_Response__bbox_xyxy(
  const void * untyped_member)
{
  (void)untyped_member;
  return 4;
}

const void * soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__get_const_function__SegmentTarget_Response__bbox_xyxy(
  const void * untyped_member, size_t index)
{
  const float * member =
    (const float *)(untyped_member);
  return &member[index];
}

void * soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__get_function__SegmentTarget_Response__bbox_xyxy(
  void * untyped_member, size_t index)
{
  float * member =
    (float *)(untyped_member);
  return &member[index];
}

void soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__fetch_function__SegmentTarget_Response__bbox_xyxy(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const float * item =
    ((const float *)
    soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__get_const_function__SegmentTarget_Response__bbox_xyxy(untyped_member, index));
  float * value =
    (float *)(untyped_value);
  *value = *item;
}

void soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__assign_function__SegmentTarget_Response__bbox_xyxy(
  void * untyped_member, size_t index, const void * untyped_value)
{
  float * item =
    ((float *)
    soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__get_function__SegmentTarget_Response__bbox_xyxy(untyped_member, index));
  const float * value =
    (const float *)(untyped_value);
  *item = *value;
}

static rosidl_typesupport_introspection_c__MessageMember soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__SegmentTarget_Response_message_member_array[7] = {
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__srv__SegmentTarget_Response, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "reason",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__srv__SegmentTarget_Response, reason),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "target_center",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__srv__SegmentTarget_Response, target_center),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "score",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__srv__SegmentTarget_Response, score),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "bbox_xyxy",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    4,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__srv__SegmentTarget_Response, bbox_xyxy),  // bytes offset in struct
    NULL,  // default value
    soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__size_function__SegmentTarget_Response__bbox_xyxy,  // size() function pointer
    soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__get_const_function__SegmentTarget_Response__bbox_xyxy,  // get_const(index) function pointer
    soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__get_function__SegmentTarget_Response__bbox_xyxy,  // get(index) function pointer
    soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__fetch_function__SegmentTarget_Response__bbox_xyxy,  // fetch(index, &value) function pointer
    soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__assign_function__SegmentTarget_Response__bbox_xyxy,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "mask_topic",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__srv__SegmentTarget_Response, mask_topic),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "debug_json",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(soarm100_interfaces__srv__SegmentTarget_Response, debug_json),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__SegmentTarget_Response_message_members = {
  "soarm100_interfaces__srv",  // message namespace
  "SegmentTarget_Response",  // message name
  7,  // number of fields
  sizeof(soarm100_interfaces__srv__SegmentTarget_Response),
  soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__SegmentTarget_Response_message_member_array,  // message members
  soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__SegmentTarget_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__SegmentTarget_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__SegmentTarget_Response_message_type_support_handle = {
  0,
  &soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__SegmentTarget_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_soarm100_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, srv, SegmentTarget_Response)() {
  soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__SegmentTarget_Response_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, PoseStamped)();
  if (!soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__SegmentTarget_Response_message_type_support_handle.typesupport_identifier) {
    soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__SegmentTarget_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &soarm100_interfaces__srv__SegmentTarget_Response__rosidl_typesupport_introspection_c__SegmentTarget_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "soarm100_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "soarm100_interfaces/srv/detail/segment_target__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers soarm100_interfaces__srv__detail__segment_target__rosidl_typesupport_introspection_c__SegmentTarget_service_members = {
  "soarm100_interfaces__srv",  // service namespace
  "SegmentTarget",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // soarm100_interfaces__srv__detail__segment_target__rosidl_typesupport_introspection_c__SegmentTarget_Request_message_type_support_handle,
  NULL  // response message
  // soarm100_interfaces__srv__detail__segment_target__rosidl_typesupport_introspection_c__SegmentTarget_Response_message_type_support_handle
};

static rosidl_service_type_support_t soarm100_interfaces__srv__detail__segment_target__rosidl_typesupport_introspection_c__SegmentTarget_service_type_support_handle = {
  0,
  &soarm100_interfaces__srv__detail__segment_target__rosidl_typesupport_introspection_c__SegmentTarget_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, srv, SegmentTarget_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, srv, SegmentTarget_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_soarm100_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, srv, SegmentTarget)() {
  if (!soarm100_interfaces__srv__detail__segment_target__rosidl_typesupport_introspection_c__SegmentTarget_service_type_support_handle.typesupport_identifier) {
    soarm100_interfaces__srv__detail__segment_target__rosidl_typesupport_introspection_c__SegmentTarget_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)soarm100_interfaces__srv__detail__segment_target__rosidl_typesupport_introspection_c__SegmentTarget_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, srv, SegmentTarget_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, srv, SegmentTarget_Response)()->data;
  }

  return &soarm100_interfaces__srv__detail__segment_target__rosidl_typesupport_introspection_c__SegmentTarget_service_type_support_handle;
}
