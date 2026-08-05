// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from orbbec_camera_msgs:msg/DepthFiltersStatus.idl
// generated code does not contain a copyright notice
#include "orbbec_camera_msgs/msg/detail/depth_filters_status__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `filters`
#include "orbbec_camera_msgs/msg/detail/depth_filter_state__functions.h"

bool
orbbec_camera_msgs__msg__DepthFiltersStatus__init(orbbec_camera_msgs__msg__DepthFiltersStatus * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    orbbec_camera_msgs__msg__DepthFiltersStatus__fini(msg);
    return false;
  }
  // filters
  if (!orbbec_camera_msgs__msg__DepthFilterState__Sequence__init(&msg->filters, 0)) {
    orbbec_camera_msgs__msg__DepthFiltersStatus__fini(msg);
    return false;
  }
  return true;
}

void
orbbec_camera_msgs__msg__DepthFiltersStatus__fini(orbbec_camera_msgs__msg__DepthFiltersStatus * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // filters
  orbbec_camera_msgs__msg__DepthFilterState__Sequence__fini(&msg->filters);
}

bool
orbbec_camera_msgs__msg__DepthFiltersStatus__are_equal(const orbbec_camera_msgs__msg__DepthFiltersStatus * lhs, const orbbec_camera_msgs__msg__DepthFiltersStatus * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // filters
  if (!orbbec_camera_msgs__msg__DepthFilterState__Sequence__are_equal(
      &(lhs->filters), &(rhs->filters)))
  {
    return false;
  }
  return true;
}

bool
orbbec_camera_msgs__msg__DepthFiltersStatus__copy(
  const orbbec_camera_msgs__msg__DepthFiltersStatus * input,
  orbbec_camera_msgs__msg__DepthFiltersStatus * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // filters
  if (!orbbec_camera_msgs__msg__DepthFilterState__Sequence__copy(
      &(input->filters), &(output->filters)))
  {
    return false;
  }
  return true;
}

orbbec_camera_msgs__msg__DepthFiltersStatus *
orbbec_camera_msgs__msg__DepthFiltersStatus__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  orbbec_camera_msgs__msg__DepthFiltersStatus * msg = (orbbec_camera_msgs__msg__DepthFiltersStatus *)allocator.allocate(sizeof(orbbec_camera_msgs__msg__DepthFiltersStatus), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(orbbec_camera_msgs__msg__DepthFiltersStatus));
  bool success = orbbec_camera_msgs__msg__DepthFiltersStatus__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
orbbec_camera_msgs__msg__DepthFiltersStatus__destroy(orbbec_camera_msgs__msg__DepthFiltersStatus * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    orbbec_camera_msgs__msg__DepthFiltersStatus__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
orbbec_camera_msgs__msg__DepthFiltersStatus__Sequence__init(orbbec_camera_msgs__msg__DepthFiltersStatus__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  orbbec_camera_msgs__msg__DepthFiltersStatus * data = NULL;

  if (size) {
    data = (orbbec_camera_msgs__msg__DepthFiltersStatus *)allocator.zero_allocate(size, sizeof(orbbec_camera_msgs__msg__DepthFiltersStatus), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = orbbec_camera_msgs__msg__DepthFiltersStatus__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        orbbec_camera_msgs__msg__DepthFiltersStatus__fini(&data[i - 1]);
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
orbbec_camera_msgs__msg__DepthFiltersStatus__Sequence__fini(orbbec_camera_msgs__msg__DepthFiltersStatus__Sequence * array)
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
      orbbec_camera_msgs__msg__DepthFiltersStatus__fini(&array->data[i]);
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

orbbec_camera_msgs__msg__DepthFiltersStatus__Sequence *
orbbec_camera_msgs__msg__DepthFiltersStatus__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  orbbec_camera_msgs__msg__DepthFiltersStatus__Sequence * array = (orbbec_camera_msgs__msg__DepthFiltersStatus__Sequence *)allocator.allocate(sizeof(orbbec_camera_msgs__msg__DepthFiltersStatus__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = orbbec_camera_msgs__msg__DepthFiltersStatus__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
orbbec_camera_msgs__msg__DepthFiltersStatus__Sequence__destroy(orbbec_camera_msgs__msg__DepthFiltersStatus__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    orbbec_camera_msgs__msg__DepthFiltersStatus__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
orbbec_camera_msgs__msg__DepthFiltersStatus__Sequence__are_equal(const orbbec_camera_msgs__msg__DepthFiltersStatus__Sequence * lhs, const orbbec_camera_msgs__msg__DepthFiltersStatus__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!orbbec_camera_msgs__msg__DepthFiltersStatus__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
orbbec_camera_msgs__msg__DepthFiltersStatus__Sequence__copy(
  const orbbec_camera_msgs__msg__DepthFiltersStatus__Sequence * input,
  orbbec_camera_msgs__msg__DepthFiltersStatus__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(orbbec_camera_msgs__msg__DepthFiltersStatus);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    orbbec_camera_msgs__msg__DepthFiltersStatus * data =
      (orbbec_camera_msgs__msg__DepthFiltersStatus *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!orbbec_camera_msgs__msg__DepthFiltersStatus__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          orbbec_camera_msgs__msg__DepthFiltersStatus__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!orbbec_camera_msgs__msg__DepthFiltersStatus__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
