// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from orbbec_camera_msgs:msg/DepthFilterParam.idl
// generated code does not contain a copyright notice
#include "orbbec_camera_msgs/msg/detail/depth_filter_param__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `name`
// Member `value`
#include "rosidl_runtime_c/string_functions.h"

bool
orbbec_camera_msgs__msg__DepthFilterParam__init(orbbec_camera_msgs__msg__DepthFilterParam * msg)
{
  if (!msg) {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__init(&msg->name)) {
    orbbec_camera_msgs__msg__DepthFilterParam__fini(msg);
    return false;
  }
  // value
  if (!rosidl_runtime_c__String__init(&msg->value)) {
    orbbec_camera_msgs__msg__DepthFilterParam__fini(msg);
    return false;
  }
  return true;
}

void
orbbec_camera_msgs__msg__DepthFilterParam__fini(orbbec_camera_msgs__msg__DepthFilterParam * msg)
{
  if (!msg) {
    return;
  }
  // name
  rosidl_runtime_c__String__fini(&msg->name);
  // value
  rosidl_runtime_c__String__fini(&msg->value);
}

bool
orbbec_camera_msgs__msg__DepthFilterParam__are_equal(const orbbec_camera_msgs__msg__DepthFilterParam * lhs, const orbbec_camera_msgs__msg__DepthFilterParam * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->name), &(rhs->name)))
  {
    return false;
  }
  // value
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->value), &(rhs->value)))
  {
    return false;
  }
  return true;
}

bool
orbbec_camera_msgs__msg__DepthFilterParam__copy(
  const orbbec_camera_msgs__msg__DepthFilterParam * input,
  orbbec_camera_msgs__msg__DepthFilterParam * output)
{
  if (!input || !output) {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__copy(
      &(input->name), &(output->name)))
  {
    return false;
  }
  // value
  if (!rosidl_runtime_c__String__copy(
      &(input->value), &(output->value)))
  {
    return false;
  }
  return true;
}

orbbec_camera_msgs__msg__DepthFilterParam *
orbbec_camera_msgs__msg__DepthFilterParam__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  orbbec_camera_msgs__msg__DepthFilterParam * msg = (orbbec_camera_msgs__msg__DepthFilterParam *)allocator.allocate(sizeof(orbbec_camera_msgs__msg__DepthFilterParam), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(orbbec_camera_msgs__msg__DepthFilterParam));
  bool success = orbbec_camera_msgs__msg__DepthFilterParam__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
orbbec_camera_msgs__msg__DepthFilterParam__destroy(orbbec_camera_msgs__msg__DepthFilterParam * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    orbbec_camera_msgs__msg__DepthFilterParam__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
orbbec_camera_msgs__msg__DepthFilterParam__Sequence__init(orbbec_camera_msgs__msg__DepthFilterParam__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  orbbec_camera_msgs__msg__DepthFilterParam * data = NULL;

  if (size) {
    data = (orbbec_camera_msgs__msg__DepthFilterParam *)allocator.zero_allocate(size, sizeof(orbbec_camera_msgs__msg__DepthFilterParam), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = orbbec_camera_msgs__msg__DepthFilterParam__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        orbbec_camera_msgs__msg__DepthFilterParam__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
orbbec_camera_msgs__msg__DepthFilterParam__Sequence__fini(orbbec_camera_msgs__msg__DepthFilterParam__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      orbbec_camera_msgs__msg__DepthFilterParam__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

orbbec_camera_msgs__msg__DepthFilterParam__Sequence *
orbbec_camera_msgs__msg__DepthFilterParam__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  orbbec_camera_msgs__msg__DepthFilterParam__Sequence * array = (orbbec_camera_msgs__msg__DepthFilterParam__Sequence *)allocator.allocate(sizeof(orbbec_camera_msgs__msg__DepthFilterParam__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = orbbec_camera_msgs__msg__DepthFilterParam__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
orbbec_camera_msgs__msg__DepthFilterParam__Sequence__destroy(orbbec_camera_msgs__msg__DepthFilterParam__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    orbbec_camera_msgs__msg__DepthFilterParam__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
orbbec_camera_msgs__msg__DepthFilterParam__Sequence__are_equal(const orbbec_camera_msgs__msg__DepthFilterParam__Sequence * lhs, const orbbec_camera_msgs__msg__DepthFilterParam__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!orbbec_camera_msgs__msg__DepthFilterParam__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
orbbec_camera_msgs__msg__DepthFilterParam__Sequence__copy(
  const orbbec_camera_msgs__msg__DepthFilterParam__Sequence * input,
  orbbec_camera_msgs__msg__DepthFilterParam__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(orbbec_camera_msgs__msg__DepthFilterParam);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    orbbec_camera_msgs__msg__DepthFilterParam * data =
      (orbbec_camera_msgs__msg__DepthFilterParam *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!orbbec_camera_msgs__msg__DepthFilterParam__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          orbbec_camera_msgs__msg__DepthFilterParam__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!orbbec_camera_msgs__msg__DepthFilterParam__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
