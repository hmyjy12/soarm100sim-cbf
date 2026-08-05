// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from orbbec_camera_msgs:msg/DepthFiltersStatus.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "orbbec_camera_msgs/msg/detail/depth_filters_status__rosidl_typesupport_introspection_c.h"
#include "orbbec_camera_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "orbbec_camera_msgs/msg/detail/depth_filters_status__functions.h"
#include "orbbec_camera_msgs/msg/detail/depth_filters_status__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `filters`
#include "orbbec_camera_msgs/msg/depth_filter_state.h"
// Member `filters`
#include "orbbec_camera_msgs/msg/detail/depth_filter_state__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__DepthFiltersStatus_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  orbbec_camera_msgs__msg__DepthFiltersStatus__init(message_memory);
}

void orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__DepthFiltersStatus_fini_function(void * message_memory)
{
  orbbec_camera_msgs__msg__DepthFiltersStatus__fini(message_memory);
}

size_t orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__size_function__DepthFiltersStatus__filters(
  const void * untyped_member)
{
  const orbbec_camera_msgs__msg__DepthFilterState__Sequence * member =
    (const orbbec_camera_msgs__msg__DepthFilterState__Sequence *)(untyped_member);
  return member->size;
}

const void * orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__get_const_function__DepthFiltersStatus__filters(
  const void * untyped_member, size_t index)
{
  const orbbec_camera_msgs__msg__DepthFilterState__Sequence * member =
    (const orbbec_camera_msgs__msg__DepthFilterState__Sequence *)(untyped_member);
  return &member->data[index];
}

void * orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__get_function__DepthFiltersStatus__filters(
  void * untyped_member, size_t index)
{
  orbbec_camera_msgs__msg__DepthFilterState__Sequence * member =
    (orbbec_camera_msgs__msg__DepthFilterState__Sequence *)(untyped_member);
  return &member->data[index];
}

void orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__fetch_function__DepthFiltersStatus__filters(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const orbbec_camera_msgs__msg__DepthFilterState * item =
    ((const orbbec_camera_msgs__msg__DepthFilterState *)
    orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__get_const_function__DepthFiltersStatus__filters(untyped_member, index));
  orbbec_camera_msgs__msg__DepthFilterState * value =
    (orbbec_camera_msgs__msg__DepthFilterState *)(untyped_value);
  *value = *item;
}

void orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__assign_function__DepthFiltersStatus__filters(
  void * untyped_member, size_t index, const void * untyped_value)
{
  orbbec_camera_msgs__msg__DepthFilterState * item =
    ((orbbec_camera_msgs__msg__DepthFilterState *)
    orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__get_function__DepthFiltersStatus__filters(untyped_member, index));
  const orbbec_camera_msgs__msg__DepthFilterState * value =
    (const orbbec_camera_msgs__msg__DepthFilterState *)(untyped_value);
  *item = *value;
}

bool orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__resize_function__DepthFiltersStatus__filters(
  void * untyped_member, size_t size)
{
  orbbec_camera_msgs__msg__DepthFilterState__Sequence * member =
    (orbbec_camera_msgs__msg__DepthFilterState__Sequence *)(untyped_member);
  orbbec_camera_msgs__msg__DepthFilterState__Sequence__fini(member);
  return orbbec_camera_msgs__msg__DepthFilterState__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__DepthFiltersStatus_message_member_array[2] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(orbbec_camera_msgs__msg__DepthFiltersStatus, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "filters",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(orbbec_camera_msgs__msg__DepthFiltersStatus, filters),  // bytes offset in struct
    NULL,  // default value
    orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__size_function__DepthFiltersStatus__filters,  // size() function pointer
    orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__get_const_function__DepthFiltersStatus__filters,  // get_const(index) function pointer
    orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__get_function__DepthFiltersStatus__filters,  // get(index) function pointer
    orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__fetch_function__DepthFiltersStatus__filters,  // fetch(index, &value) function pointer
    orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__assign_function__DepthFiltersStatus__filters,  // assign(index, value) function pointer
    orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__resize_function__DepthFiltersStatus__filters  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__DepthFiltersStatus_message_members = {
  "orbbec_camera_msgs__msg",  // message namespace
  "DepthFiltersStatus",  // message name
  2,  // number of fields
  sizeof(orbbec_camera_msgs__msg__DepthFiltersStatus),
  orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__DepthFiltersStatus_message_member_array,  // message members
  orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__DepthFiltersStatus_init_function,  // function to initialize message memory (memory has to be allocated)
  orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__DepthFiltersStatus_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__DepthFiltersStatus_message_type_support_handle = {
  0,
  &orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__DepthFiltersStatus_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_orbbec_camera_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, orbbec_camera_msgs, msg, DepthFiltersStatus)() {
  orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__DepthFiltersStatus_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__DepthFiltersStatus_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, orbbec_camera_msgs, msg, DepthFilterState)();
  if (!orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__DepthFiltersStatus_message_type_support_handle.typesupport_identifier) {
    orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__DepthFiltersStatus_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &orbbec_camera_msgs__msg__DepthFiltersStatus__rosidl_typesupport_introspection_c__DepthFiltersStatus_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
