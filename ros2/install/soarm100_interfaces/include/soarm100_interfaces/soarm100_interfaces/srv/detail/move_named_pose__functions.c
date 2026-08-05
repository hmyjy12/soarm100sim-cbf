// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from soarm100_interfaces:srv/MoveNamedPose.idl
// generated code does not contain a copyright notice
#include "soarm100_interfaces/srv/detail/move_named_pose__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `pose_name`
// Member `confirmation`
#include "rosidl_runtime_c/string_functions.h"

bool
soarm100_interfaces__srv__MoveNamedPose_Request__init(soarm100_interfaces__srv__MoveNamedPose_Request * msg)
{
  if (!msg) {
    return false;
  }
  // pose_name
  if (!rosidl_runtime_c__String__init(&msg->pose_name)) {
    soarm100_interfaces__srv__MoveNamedPose_Request__fini(msg);
    return false;
  }
  // duration
  // hold
  // confirmation
  if (!rosidl_runtime_c__String__init(&msg->confirmation)) {
    soarm100_interfaces__srv__MoveNamedPose_Request__fini(msg);
    return false;
  }
  return true;
}

void
soarm100_interfaces__srv__MoveNamedPose_Request__fini(soarm100_interfaces__srv__MoveNamedPose_Request * msg)
{
  if (!msg) {
    return;
  }
  // pose_name
  rosidl_runtime_c__String__fini(&msg->pose_name);
  // duration
  // hold
  // confirmation
  rosidl_runtime_c__String__fini(&msg->confirmation);
}

bool
soarm100_interfaces__srv__MoveNamedPose_Request__are_equal(const soarm100_interfaces__srv__MoveNamedPose_Request * lhs, const soarm100_interfaces__srv__MoveNamedPose_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // pose_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->pose_name), &(rhs->pose_name)))
  {
    return false;
  }
  // duration
  if (lhs->duration != rhs->duration) {
    return false;
  }
  // hold
  if (lhs->hold != rhs->hold) {
    return false;
  }
  // confirmation
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->confirmation), &(rhs->confirmation)))
  {
    return false;
  }
  return true;
}

bool
soarm100_interfaces__srv__MoveNamedPose_Request__copy(
  const soarm100_interfaces__srv__MoveNamedPose_Request * input,
  soarm100_interfaces__srv__MoveNamedPose_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // pose_name
  if (!rosidl_runtime_c__String__copy(
      &(input->pose_name), &(output->pose_name)))
  {
    return false;
  }
  // duration
  output->duration = input->duration;
  // hold
  output->hold = input->hold;
  // confirmation
  if (!rosidl_runtime_c__String__copy(
      &(input->confirmation), &(output->confirmation)))
  {
    return false;
  }
  return true;
}

soarm100_interfaces__srv__MoveNamedPose_Request *
soarm100_interfaces__srv__MoveNamedPose_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  soarm100_interfaces__srv__MoveNamedPose_Request * msg = (soarm100_interfaces__srv__MoveNamedPose_Request *)allocator.allocate(sizeof(soarm100_interfaces__srv__MoveNamedPose_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(soarm100_interfaces__srv__MoveNamedPose_Request));
  bool success = soarm100_interfaces__srv__MoveNamedPose_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
soarm100_interfaces__srv__MoveNamedPose_Request__destroy(soarm100_interfaces__srv__MoveNamedPose_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    soarm100_interfaces__srv__MoveNamedPose_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
soarm100_interfaces__srv__MoveNamedPose_Request__Sequence__init(soarm100_interfaces__srv__MoveNamedPose_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  soarm100_interfaces__srv__MoveNamedPose_Request * data = NULL;

  if (size) {
    data = (soarm100_interfaces__srv__MoveNamedPose_Request *)allocator.zero_allocate(size, sizeof(soarm100_interfaces__srv__MoveNamedPose_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = soarm100_interfaces__srv__MoveNamedPose_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        soarm100_interfaces__srv__MoveNamedPose_Request__fini(&data[i - 1]);
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
soarm100_interfaces__srv__MoveNamedPose_Request__Sequence__fini(soarm100_interfaces__srv__MoveNamedPose_Request__Sequence * array)
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
      soarm100_interfaces__srv__MoveNamedPose_Request__fini(&array->data[i]);
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

soarm100_interfaces__srv__MoveNamedPose_Request__Sequence *
soarm100_interfaces__srv__MoveNamedPose_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  soarm100_interfaces__srv__MoveNamedPose_Request__Sequence * array = (soarm100_interfaces__srv__MoveNamedPose_Request__Sequence *)allocator.allocate(sizeof(soarm100_interfaces__srv__MoveNamedPose_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = soarm100_interfaces__srv__MoveNamedPose_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
soarm100_interfaces__srv__MoveNamedPose_Request__Sequence__destroy(soarm100_interfaces__srv__MoveNamedPose_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    soarm100_interfaces__srv__MoveNamedPose_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
soarm100_interfaces__srv__MoveNamedPose_Request__Sequence__are_equal(const soarm100_interfaces__srv__MoveNamedPose_Request__Sequence * lhs, const soarm100_interfaces__srv__MoveNamedPose_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!soarm100_interfaces__srv__MoveNamedPose_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
soarm100_interfaces__srv__MoveNamedPose_Request__Sequence__copy(
  const soarm100_interfaces__srv__MoveNamedPose_Request__Sequence * input,
  soarm100_interfaces__srv__MoveNamedPose_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(soarm100_interfaces__srv__MoveNamedPose_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    soarm100_interfaces__srv__MoveNamedPose_Request * data =
      (soarm100_interfaces__srv__MoveNamedPose_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!soarm100_interfaces__srv__MoveNamedPose_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          soarm100_interfaces__srv__MoveNamedPose_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!soarm100_interfaces__srv__MoveNamedPose_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `reason`
// Member `log_path`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
soarm100_interfaces__srv__MoveNamedPose_Response__init(soarm100_interfaces__srv__MoveNamedPose_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // reason
  if (!rosidl_runtime_c__String__init(&msg->reason)) {
    soarm100_interfaces__srv__MoveNamedPose_Response__fini(msg);
    return false;
  }
  // log_path
  if (!rosidl_runtime_c__String__init(&msg->log_path)) {
    soarm100_interfaces__srv__MoveNamedPose_Response__fini(msg);
    return false;
  }
  return true;
}

void
soarm100_interfaces__srv__MoveNamedPose_Response__fini(soarm100_interfaces__srv__MoveNamedPose_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
  // reason
  rosidl_runtime_c__String__fini(&msg->reason);
  // log_path
  rosidl_runtime_c__String__fini(&msg->log_path);
}

bool
soarm100_interfaces__srv__MoveNamedPose_Response__are_equal(const soarm100_interfaces__srv__MoveNamedPose_Response * lhs, const soarm100_interfaces__srv__MoveNamedPose_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // reason
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->reason), &(rhs->reason)))
  {
    return false;
  }
  // log_path
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->log_path), &(rhs->log_path)))
  {
    return false;
  }
  return true;
}

bool
soarm100_interfaces__srv__MoveNamedPose_Response__copy(
  const soarm100_interfaces__srv__MoveNamedPose_Response * input,
  soarm100_interfaces__srv__MoveNamedPose_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  // reason
  if (!rosidl_runtime_c__String__copy(
      &(input->reason), &(output->reason)))
  {
    return false;
  }
  // log_path
  if (!rosidl_runtime_c__String__copy(
      &(input->log_path), &(output->log_path)))
  {
    return false;
  }
  return true;
}

soarm100_interfaces__srv__MoveNamedPose_Response *
soarm100_interfaces__srv__MoveNamedPose_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  soarm100_interfaces__srv__MoveNamedPose_Response * msg = (soarm100_interfaces__srv__MoveNamedPose_Response *)allocator.allocate(sizeof(soarm100_interfaces__srv__MoveNamedPose_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(soarm100_interfaces__srv__MoveNamedPose_Response));
  bool success = soarm100_interfaces__srv__MoveNamedPose_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
soarm100_interfaces__srv__MoveNamedPose_Response__destroy(soarm100_interfaces__srv__MoveNamedPose_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    soarm100_interfaces__srv__MoveNamedPose_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
soarm100_interfaces__srv__MoveNamedPose_Response__Sequence__init(soarm100_interfaces__srv__MoveNamedPose_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  soarm100_interfaces__srv__MoveNamedPose_Response * data = NULL;

  if (size) {
    data = (soarm100_interfaces__srv__MoveNamedPose_Response *)allocator.zero_allocate(size, sizeof(soarm100_interfaces__srv__MoveNamedPose_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = soarm100_interfaces__srv__MoveNamedPose_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        soarm100_interfaces__srv__MoveNamedPose_Response__fini(&data[i - 1]);
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
soarm100_interfaces__srv__MoveNamedPose_Response__Sequence__fini(soarm100_interfaces__srv__MoveNamedPose_Response__Sequence * array)
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
      soarm100_interfaces__srv__MoveNamedPose_Response__fini(&array->data[i]);
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

soarm100_interfaces__srv__MoveNamedPose_Response__Sequence *
soarm100_interfaces__srv__MoveNamedPose_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  soarm100_interfaces__srv__MoveNamedPose_Response__Sequence * array = (soarm100_interfaces__srv__MoveNamedPose_Response__Sequence *)allocator.allocate(sizeof(soarm100_interfaces__srv__MoveNamedPose_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = soarm100_interfaces__srv__MoveNamedPose_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
soarm100_interfaces__srv__MoveNamedPose_Response__Sequence__destroy(soarm100_interfaces__srv__MoveNamedPose_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    soarm100_interfaces__srv__MoveNamedPose_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
soarm100_interfaces__srv__MoveNamedPose_Response__Sequence__are_equal(const soarm100_interfaces__srv__MoveNamedPose_Response__Sequence * lhs, const soarm100_interfaces__srv__MoveNamedPose_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!soarm100_interfaces__srv__MoveNamedPose_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
soarm100_interfaces__srv__MoveNamedPose_Response__Sequence__copy(
  const soarm100_interfaces__srv__MoveNamedPose_Response__Sequence * input,
  soarm100_interfaces__srv__MoveNamedPose_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(soarm100_interfaces__srv__MoveNamedPose_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    soarm100_interfaces__srv__MoveNamedPose_Response * data =
      (soarm100_interfaces__srv__MoveNamedPose_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!soarm100_interfaces__srv__MoveNamedPose_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          soarm100_interfaces__srv__MoveNamedPose_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!soarm100_interfaces__srv__MoveNamedPose_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
