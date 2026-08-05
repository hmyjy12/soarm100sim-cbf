// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from orbbec_camera_msgs:msg/DepthFilterState.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "orbbec_camera_msgs/msg/detail/depth_filter_state__rosidl_typesupport_introspection_c.h"
#include "orbbec_camera_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "orbbec_camera_msgs/msg/detail/depth_filter_state__functions.h"
#include "orbbec_camera_msgs/msg/detail/depth_filter_state__struct.h"


// Include directives for member types
// Member `filter_name`
#include "rosidl_runtime_c/string_functions.h"
// Member `params`
#include "orbbec_camera_msgs/msg/depth_filter_param.h"
// Member `params`
#include "orbbec_camera_msgs/msg/detail/depth_filter_param__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__DepthFilterState_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  orbbec_camera_msgs__msg__DepthFilterState__init(message_memory);
}

void orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__DepthFilterState_fini_function(void * message_memory)
{
  orbbec_camera_msgs__msg__DepthFilterState__fini(message_memory);
}

size_t orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__size_function__DepthFilterState__params(
  const void * untyped_member)
{
  const orbbec_camera_msgs__msg__DepthFilterParam__Sequence * member =
    (const orbbec_camera_msgs__msg__DepthFilterParam__Sequence *)(untyped_member);
  return member->size;
}

const void * orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__get_const_function__DepthFilterState__params(
  const void * untyped_member, size_t index)
{
  const orbbec_camera_msgs__msg__DepthFilterParam__Sequence * member =
    (const orbbec_camera_msgs__msg__DepthFilterParam__Sequence *)(untyped_member);
  return &member->data[index];
}

void * orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__get_function__DepthFilterState__params(
  void * untyped_member, size_t index)
{
  orbbec_camera_msgs__msg__DepthFilterParam__Sequence * member =
    (orbbec_camera_msgs__msg__DepthFilterParam__Sequence *)(untyped_member);
  return &member->data[index];
}

void orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__fetch_function__DepthFilterState__params(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const orbbec_camera_msgs__msg__DepthFilterParam * item =
    ((const orbbec_camera_msgs__msg__DepthFilterParam *)
    orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__get_const_function__DepthFilterState__params(untyped_member, index));
  orbbec_camera_msgs__msg__DepthFilterParam * value =
    (orbbec_camera_msgs__msg__DepthFilterParam *)(untyped_value);
  *value = *item;
}

void orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__assign_function__DepthFilterState__params(
  void * untyped_member, size_t index, const void * untyped_value)
{
  orbbec_camera_msgs__msg__DepthFilterParam * item =
    ((orbbec_camera_msgs__msg__DepthFilterParam *)
    orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__get_function__DepthFilterState__params(untyped_member, index));
  const orbbec_camera_msgs__msg__DepthFilterParam * value =
    (const orbbec_camera_msgs__msg__DepthFilterParam *)(untyped_value);
  *item = *value;
}

bool orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__resize_function__DepthFilterState__params(
  void * untyped_member, size_t size)
{
  orbbec_camera_msgs__msg__DepthFilterParam__Sequence * member =
    (orbbec_camera_msgs__msg__DepthFilterParam__Sequence *)(untyped_member);
  orbbec_camera_msgs__msg__DepthFilterParam__Sequence__fini(member);
  return orbbec_camera_msgs__msg__DepthFilterParam__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__DepthFilterState_message_member_array[3] = {
  {
    "filter_name",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(orbbec_camera_msgs__msg__DepthFilterState, filter_name),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "enabled",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(orbbec_camera_msgs__msg__DepthFilterState, enabled),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "params",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(orbbec_camera_msgs__msg__DepthFilterState, params),  // bytes offset in struct
    NULL,  // default value
    orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__size_function__DepthFilterState__params,  // size() function pointer
    orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__get_const_function__DepthFilterState__params,  // get_const(index) function pointer
    orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__get_function__DepthFilterState__params,  // get(index) function pointer
    orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__fetch_function__DepthFilterState__params,  // fetch(index, &value) function pointer
    orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__assign_function__DepthFilterState__params,  // assign(index, value) function pointer
    orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__resize_function__DepthFilterState__params  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__DepthFilterState_message_members = {
  "orbbec_camera_msgs__msg",  // message namespace
  "DepthFilterState",  // message name
  3,  // number of fields
  sizeof(orbbec_camera_msgs__msg__DepthFilterState),
  orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__DepthFilterState_message_member_array,  // message members
  orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__DepthFilterState_init_function,  // function to initialize message memory (memory has to be allocated)
  orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__DepthFilterState_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__DepthFilterState_message_type_support_handle = {
  0,
  &orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__DepthFilterState_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_orbbec_camera_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, orbbec_camera_msgs, msg, DepthFilterState)() {
  orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__DepthFilterState_message_member_array[2].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, orbbec_camera_msgs, msg, DepthFilterParam)();
  if (!orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__DepthFilterState_message_type_support_handle.typesupport_identifier) {
    orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__DepthFilterState_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &orbbec_camera_msgs__msg__DepthFilterState__rosidl_typesupport_introspection_c__DepthFilterState_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
