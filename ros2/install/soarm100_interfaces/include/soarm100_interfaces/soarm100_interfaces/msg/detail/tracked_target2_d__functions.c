// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from soarm100_interfaces:msg/TrackedTarget2D.idl
// generated code does not contain a copyright notice
#include "soarm100_interfaces/msg/detail/tracked_target2_d__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `reason`
#include "rosidl_runtime_c/string_functions.h"

bool
soarm100_interfaces__msg__TrackedTarget2D__init(soarm100_interfaces__msg__TrackedTarget2D * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    soarm100_interfaces__msg__TrackedTarget2D__fini(msg);
    return false;
  }
  // valid
  // u
  // v
  // reference_u
  // reference_v
  // delta_u
  // delta_v
  // width
  // height
  // image_width
  // image_height
  // confidence
  // lost_frames
  // replan_required
  // reason
  if (!rosidl_runtime_c__String__init(&msg->reason)) {
    soarm100_interfaces__msg__TrackedTarget2D__fini(msg);
    return false;
  }
  return true;
}

void
soarm100_interfaces__msg__TrackedTarget2D__fini(soarm100_interfaces__msg__TrackedTarget2D * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // valid
  // u
  // v
  // reference_u
  // reference_v
  // delta_u
  // delta_v
  // width
  // height
  // image_width
  // image_height
  // confidence
  // lost_frames
  // replan_required
  // reason
  rosidl_runtime_c__String__fini(&msg->reason);
}

bool
soarm100_interfaces__msg__TrackedTarget2D__are_equal(const soarm100_interfaces__msg__TrackedTarget2D * lhs, const soarm100_interfaces__msg__TrackedTarget2D * rhs)
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
  // valid
  if (lhs->valid != rhs->valid) {
    return false;
  }
  // u
  if (lhs->u != rhs->u) {
    return false;
  }
  // v
  if (lhs->v != rhs->v) {
    return false;
  }
  // reference_u
  if (lhs->reference_u != rhs->reference_u) {
    return false;
  }
  // reference_v
  if (lhs->reference_v != rhs->reference_v) {
    return false;
  }
  // delta_u
  if (lhs->delta_u != rhs->delta_u) {
    return false;
  }
  // delta_v
  if (lhs->delta_v != rhs->delta_v) {
    return false;
  }
  // width
  if (lhs->width != rhs->width) {
    return false;
  }
  // height
  if (lhs->height != rhs->height) {
    return false;
  }
  // image_width
  if (lhs->image_width != rhs->image_width) {
    return false;
  }
  // image_height
  if (lhs->image_height != rhs->image_height) {
    return false;
  }
  // confidence
  if (lhs->confidence != rhs->confidence) {
    return false;
  }
  // lost_frames
  if (lhs->lost_frames != rhs->lost_frames) {
    return false;
  }
  // replan_required
  if (lhs->replan_required != rhs->replan_required) {
    return false;
  }
  // reason
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->reason), &(rhs->reason)))
  {
    return false;
  }
  return true;
}

bool
soarm100_interfaces__msg__TrackedTarget2D__copy(
  const soarm100_interfaces__msg__TrackedTarget2D * input,
  soarm100_interfaces__msg__TrackedTarget2D * output)
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
  // valid
  output->valid = input->valid;
  // u
  output->u = input->u;
  // v
  output->v = input->v;
  // reference_u
  output->reference_u = input->reference_u;
  // reference_v
  output->reference_v = input->reference_v;
  // delta_u
  output->delta_u = input->delta_u;
  // delta_v
  output->delta_v = input->delta_v;
  // width
  output->width = input->width;
  // height
  output->height = input->height;
  // image_width
  output->image_width = input->image_width;
  // image_height
  output->image_height = input->image_height;
  // confidence
  output->confidence = input->confidence;
  // lost_frames
  output->lost_frames = input->lost_frames;
  // replan_required
  output->replan_required = input->replan_required;
  // reason
  if (!rosidl_runtime_c__String__copy(
      &(input->reason), &(output->reason)))
  {
    return false;
  }
  return true;
}

soarm100_interfaces__msg__TrackedTarget2D *
soarm100_interfaces__msg__TrackedTarget2D__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  soarm100_interfaces__msg__TrackedTarget2D * msg = (soarm100_interfaces__msg__TrackedTarget2D *)allocator.allocate(sizeof(soarm100_interfaces__msg__TrackedTarget2D), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(soarm100_interfaces__msg__TrackedTarget2D));
  bool success = soarm100_interfaces__msg__TrackedTarget2D__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
soarm100_interfaces__msg__TrackedTarget2D__destroy(soarm100_interfaces__msg__TrackedTarget2D * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    soarm100_interfaces__msg__TrackedTarget2D__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
soarm100_interfaces__msg__TrackedTarget2D__Sequence__init(soarm100_interfaces__msg__TrackedTarget2D__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  soarm100_interfaces__msg__TrackedTarget2D * data = NULL;

  if (size) {
    data = (soarm100_interfaces__msg__TrackedTarget2D *)allocator.zero_allocate(size, sizeof(soarm100_interfaces__msg__TrackedTarget2D), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = soarm100_interfaces__msg__TrackedTarget2D__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        soarm100_interfaces__msg__TrackedTarget2D__fini(&data[i - 1]);
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
soarm100_interfaces__msg__TrackedTarget2D__Sequence__fini(soarm100_interfaces__msg__TrackedTarget2D__Sequence * array)
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
      soarm100_interfaces__msg__TrackedTarget2D__fini(&array->data[i]);
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

soarm100_interfaces__msg__TrackedTarget2D__Sequence *
soarm100_interfaces__msg__TrackedTarget2D__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  soarm100_interfaces__msg__TrackedTarget2D__Sequence * array = (soarm100_interfaces__msg__TrackedTarget2D__Sequence *)allocator.allocate(sizeof(soarm100_interfaces__msg__TrackedTarget2D__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = soarm100_interfaces__msg__TrackedTarget2D__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
soarm100_interfaces__msg__TrackedTarget2D__Sequence__destroy(soarm100_interfaces__msg__TrackedTarget2D__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    soarm100_interfaces__msg__TrackedTarget2D__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
soarm100_interfaces__msg__TrackedTarget2D__Sequence__are_equal(const soarm100_interfaces__msg__TrackedTarget2D__Sequence * lhs, const soarm100_interfaces__msg__TrackedTarget2D__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!soarm100_interfaces__msg__TrackedTarget2D__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
soarm100_interfaces__msg__TrackedTarget2D__Sequence__copy(
  const soarm100_interfaces__msg__TrackedTarget2D__Sequence * input,
  soarm100_interfaces__msg__TrackedTarget2D__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(soarm100_interfaces__msg__TrackedTarget2D);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    soarm100_interfaces__msg__TrackedTarget2D * data =
      (soarm100_interfaces__msg__TrackedTarget2D *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!soarm100_interfaces__msg__TrackedTarget2D__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          soarm100_interfaces__msg__TrackedTarget2D__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!soarm100_interfaces__msg__TrackedTarget2D__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
