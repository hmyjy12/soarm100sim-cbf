// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from orbbec_camera_msgs:srv/GetDeviceConfig.idl
// generated code does not contain a copyright notice
#include "orbbec_camera_msgs/srv/detail/get_device_config__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

bool
orbbec_camera_msgs__srv__GetDeviceConfig_Request__init(orbbec_camera_msgs__srv__GetDeviceConfig_Request * msg)
{
  if (!msg) {
    return false;
  }
  // structure_needs_at_least_one_member
  return true;
}

void
orbbec_camera_msgs__srv__GetDeviceConfig_Request__fini(orbbec_camera_msgs__srv__GetDeviceConfig_Request * msg)
{
  if (!msg) {
    return;
  }
  // structure_needs_at_least_one_member
}

bool
orbbec_camera_msgs__srv__GetDeviceConfig_Request__are_equal(const orbbec_camera_msgs__srv__GetDeviceConfig_Request * lhs, const orbbec_camera_msgs__srv__GetDeviceConfig_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // structure_needs_at_least_one_member
  if (lhs->structure_needs_at_least_one_member != rhs->structure_needs_at_least_one_member) {
    return false;
  }
  return true;
}

bool
orbbec_camera_msgs__srv__GetDeviceConfig_Request__copy(
  const orbbec_camera_msgs__srv__GetDeviceConfig_Request * input,
  orbbec_camera_msgs__srv__GetDeviceConfig_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // structure_needs_at_least_one_member
  output->structure_needs_at_least_one_member = input->structure_needs_at_least_one_member;
  return true;
}

orbbec_camera_msgs__srv__GetDeviceConfig_Request *
orbbec_camera_msgs__srv__GetDeviceConfig_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  orbbec_camera_msgs__srv__GetDeviceConfig_Request * msg = (orbbec_camera_msgs__srv__GetDeviceConfig_Request *)allocator.allocate(sizeof(orbbec_camera_msgs__srv__GetDeviceConfig_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(orbbec_camera_msgs__srv__GetDeviceConfig_Request));
  bool success = orbbec_camera_msgs__srv__GetDeviceConfig_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
orbbec_camera_msgs__srv__GetDeviceConfig_Request__destroy(orbbec_camera_msgs__srv__GetDeviceConfig_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    orbbec_camera_msgs__srv__GetDeviceConfig_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
orbbec_camera_msgs__srv__GetDeviceConfig_Request__Sequence__init(orbbec_camera_msgs__srv__GetDeviceConfig_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  orbbec_camera_msgs__srv__GetDeviceConfig_Request * data = NULL;

  if (size) {
    data = (orbbec_camera_msgs__srv__GetDeviceConfig_Request *)allocator.zero_allocate(size, sizeof(orbbec_camera_msgs__srv__GetDeviceConfig_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = orbbec_camera_msgs__srv__GetDeviceConfig_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        orbbec_camera_msgs__srv__GetDeviceConfig_Request__fini(&data[i - 1]);
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
orbbec_camera_msgs__srv__GetDeviceConfig_Request__Sequence__fini(orbbec_camera_msgs__srv__GetDeviceConfig_Request__Sequence * array)
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
      orbbec_camera_msgs__srv__GetDeviceConfig_Request__fini(&array->data[i]);
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

orbbec_camera_msgs__srv__GetDeviceConfig_Request__Sequence *
orbbec_camera_msgs__srv__GetDeviceConfig_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  orbbec_camera_msgs__srv__GetDeviceConfig_Request__Sequence * array = (orbbec_camera_msgs__srv__GetDeviceConfig_Request__Sequence *)allocator.allocate(sizeof(orbbec_camera_msgs__srv__GetDeviceConfig_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = orbbec_camera_msgs__srv__GetDeviceConfig_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
orbbec_camera_msgs__srv__GetDeviceConfig_Request__Sequence__destroy(orbbec_camera_msgs__srv__GetDeviceConfig_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    orbbec_camera_msgs__srv__GetDeviceConfig_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
orbbec_camera_msgs__srv__GetDeviceConfig_Request__Sequence__are_equal(const orbbec_camera_msgs__srv__GetDeviceConfig_Request__Sequence * lhs, const orbbec_camera_msgs__srv__GetDeviceConfig_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!orbbec_camera_msgs__srv__GetDeviceConfig_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
orbbec_camera_msgs__srv__GetDeviceConfig_Request__Sequence__copy(
  const orbbec_camera_msgs__srv__GetDeviceConfig_Request__Sequence * input,
  orbbec_camera_msgs__srv__GetDeviceConfig_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(orbbec_camera_msgs__srv__GetDeviceConfig_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    orbbec_camera_msgs__srv__GetDeviceConfig_Request * data =
      (orbbec_camera_msgs__srv__GetDeviceConfig_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!orbbec_camera_msgs__srv__GetDeviceConfig_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          orbbec_camera_msgs__srv__GetDeviceConfig_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!orbbec_camera_msgs__srv__GetDeviceConfig_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `schema_version`
// Member `device_preset`
// Member `preset_version`
// Member `color_preset`
// Member `depth_precision`
// Member `disparity_to_depth_mode`
// Member `exposure_range_mode`
// Member `align_mode`
// Member `align_target_stream`
// Member `frame_aggregate_mode`
// Member `time_domain`
// Member `sync_mode`
// Member `intra_camera_sync_reference`
// Member `data_json`
// Member `message`
#include "rosidl_runtime_c/string_functions.h"

bool
orbbec_camera_msgs__srv__GetDeviceConfig_Response__init(orbbec_camera_msgs__srv__GetDeviceConfig_Response * msg)
{
  if (!msg) {
    return false;
  }
  // schema_version
  if (!rosidl_runtime_c__String__init(&msg->schema_version)) {
    orbbec_camera_msgs__srv__GetDeviceConfig_Response__fini(msg);
    return false;
  }
  // device_preset
  if (!rosidl_runtime_c__String__init(&msg->device_preset)) {
    orbbec_camera_msgs__srv__GetDeviceConfig_Response__fini(msg);
    return false;
  }
  // preset_version
  if (!rosidl_runtime_c__String__init(&msg->preset_version)) {
    orbbec_camera_msgs__srv__GetDeviceConfig_Response__fini(msg);
    return false;
  }
  // color_preset
  if (!rosidl_runtime_c__String__init(&msg->color_preset)) {
    orbbec_camera_msgs__srv__GetDeviceConfig_Response__fini(msg);
    return false;
  }
  // depth_precision
  if (!rosidl_runtime_c__String__init(&msg->depth_precision)) {
    orbbec_camera_msgs__srv__GetDeviceConfig_Response__fini(msg);
    return false;
  }
  // disparity_to_depth_mode
  if (!rosidl_runtime_c__String__init(&msg->disparity_to_depth_mode)) {
    orbbec_camera_msgs__srv__GetDeviceConfig_Response__fini(msg);
    return false;
  }
  // exposure_range_mode
  if (!rosidl_runtime_c__String__init(&msg->exposure_range_mode)) {
    orbbec_camera_msgs__srv__GetDeviceConfig_Response__fini(msg);
    return false;
  }
  // depth_registration
  // align_mode
  if (!rosidl_runtime_c__String__init(&msg->align_mode)) {
    orbbec_camera_msgs__srv__GetDeviceConfig_Response__fini(msg);
    return false;
  }
  // align_target_stream
  if (!rosidl_runtime_c__String__init(&msg->align_target_stream)) {
    orbbec_camera_msgs__srv__GetDeviceConfig_Response__fini(msg);
    return false;
  }
  // frame_aggregate_mode
  if (!rosidl_runtime_c__String__init(&msg->frame_aggregate_mode)) {
    orbbec_camera_msgs__srv__GetDeviceConfig_Response__fini(msg);
    return false;
  }
  // enable_frame_sync
  // time_domain
  if (!rosidl_runtime_c__String__init(&msg->time_domain)) {
    orbbec_camera_msgs__srv__GetDeviceConfig_Response__fini(msg);
    return false;
  }
  // sync_mode
  if (!rosidl_runtime_c__String__init(&msg->sync_mode)) {
    orbbec_camera_msgs__srv__GetDeviceConfig_Response__fini(msg);
    return false;
  }
  // intra_camera_sync_reference
  if (!rosidl_runtime_c__String__init(&msg->intra_camera_sync_reference)) {
    orbbec_camera_msgs__srv__GetDeviceConfig_Response__fini(msg);
    return false;
  }
  // data_json
  if (!rosidl_runtime_c__String__init(&msg->data_json)) {
    orbbec_camera_msgs__srv__GetDeviceConfig_Response__fini(msg);
    return false;
  }
  // success
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    orbbec_camera_msgs__srv__GetDeviceConfig_Response__fini(msg);
    return false;
  }
  return true;
}

void
orbbec_camera_msgs__srv__GetDeviceConfig_Response__fini(orbbec_camera_msgs__srv__GetDeviceConfig_Response * msg)
{
  if (!msg) {
    return;
  }
  // schema_version
  rosidl_runtime_c__String__fini(&msg->schema_version);
  // device_preset
  rosidl_runtime_c__String__fini(&msg->device_preset);
  // preset_version
  rosidl_runtime_c__String__fini(&msg->preset_version);
  // color_preset
  rosidl_runtime_c__String__fini(&msg->color_preset);
  // depth_precision
  rosidl_runtime_c__String__fini(&msg->depth_precision);
  // disparity_to_depth_mode
  rosidl_runtime_c__String__fini(&msg->disparity_to_depth_mode);
  // exposure_range_mode
  rosidl_runtime_c__String__fini(&msg->exposure_range_mode);
  // depth_registration
  // align_mode
  rosidl_runtime_c__String__fini(&msg->align_mode);
  // align_target_stream
  rosidl_runtime_c__String__fini(&msg->align_target_stream);
  // frame_aggregate_mode
  rosidl_runtime_c__String__fini(&msg->frame_aggregate_mode);
  // enable_frame_sync
  // time_domain
  rosidl_runtime_c__String__fini(&msg->time_domain);
  // sync_mode
  rosidl_runtime_c__String__fini(&msg->sync_mode);
  // intra_camera_sync_reference
  rosidl_runtime_c__String__fini(&msg->intra_camera_sync_reference);
  // data_json
  rosidl_runtime_c__String__fini(&msg->data_json);
  // success
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
orbbec_camera_msgs__srv__GetDeviceConfig_Response__are_equal(const orbbec_camera_msgs__srv__GetDeviceConfig_Response * lhs, const orbbec_camera_msgs__srv__GetDeviceConfig_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // schema_version
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->schema_version), &(rhs->schema_version)))
  {
    return false;
  }
  // device_preset
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->device_preset), &(rhs->device_preset)))
  {
    return false;
  }
  // preset_version
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->preset_version), &(rhs->preset_version)))
  {
    return false;
  }
  // color_preset
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->color_preset), &(rhs->color_preset)))
  {
    return false;
  }
  // depth_precision
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->depth_precision), &(rhs->depth_precision)))
  {
    return false;
  }
  // disparity_to_depth_mode
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->disparity_to_depth_mode), &(rhs->disparity_to_depth_mode)))
  {
    return false;
  }
  // exposure_range_mode
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->exposure_range_mode), &(rhs->exposure_range_mode)))
  {
    return false;
  }
  // depth_registration
  if (lhs->depth_registration != rhs->depth_registration) {
    return false;
  }
  // align_mode
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->align_mode), &(rhs->align_mode)))
  {
    return false;
  }
  // align_target_stream
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->align_target_stream), &(rhs->align_target_stream)))
  {
    return false;
  }
  // frame_aggregate_mode
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->frame_aggregate_mode), &(rhs->frame_aggregate_mode)))
  {
    return false;
  }
  // enable_frame_sync
  if (lhs->enable_frame_sync != rhs->enable_frame_sync) {
    return false;
  }
  // time_domain
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->time_domain), &(rhs->time_domain)))
  {
    return false;
  }
  // sync_mode
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->sync_mode), &(rhs->sync_mode)))
  {
    return false;
  }
  // intra_camera_sync_reference
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->intra_camera_sync_reference), &(rhs->intra_camera_sync_reference)))
  {
    return false;
  }
  // data_json
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->data_json), &(rhs->data_json)))
  {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  return true;
}

bool
orbbec_camera_msgs__srv__GetDeviceConfig_Response__copy(
  const orbbec_camera_msgs__srv__GetDeviceConfig_Response * input,
  orbbec_camera_msgs__srv__GetDeviceConfig_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // schema_version
  if (!rosidl_runtime_c__String__copy(
      &(input->schema_version), &(output->schema_version)))
  {
    return false;
  }
  // device_preset
  if (!rosidl_runtime_c__String__copy(
      &(input->device_preset), &(output->device_preset)))
  {
    return false;
  }
  // preset_version
  if (!rosidl_runtime_c__String__copy(
      &(input->preset_version), &(output->preset_version)))
  {
    return false;
  }
  // color_preset
  if (!rosidl_runtime_c__String__copy(
      &(input->color_preset), &(output->color_preset)))
  {
    return false;
  }
  // depth_precision
  if (!rosidl_runtime_c__String__copy(
      &(input->depth_precision), &(output->depth_precision)))
  {
    return false;
  }
  // disparity_to_depth_mode
  if (!rosidl_runtime_c__String__copy(
      &(input->disparity_to_depth_mode), &(output->disparity_to_depth_mode)))
  {
    return false;
  }
  // exposure_range_mode
  if (!rosidl_runtime_c__String__copy(
      &(input->exposure_range_mode), &(output->exposure_range_mode)))
  {
    return false;
  }
  // depth_registration
  output->depth_registration = input->depth_registration;
  // align_mode
  if (!rosidl_runtime_c__String__copy(
      &(input->align_mode), &(output->align_mode)))
  {
    return false;
  }
  // align_target_stream
  if (!rosidl_runtime_c__String__copy(
      &(input->align_target_stream), &(output->align_target_stream)))
  {
    return false;
  }
  // frame_aggregate_mode
  if (!rosidl_runtime_c__String__copy(
      &(input->frame_aggregate_mode), &(output->frame_aggregate_mode)))
  {
    return false;
  }
  // enable_frame_sync
  output->enable_frame_sync = input->enable_frame_sync;
  // time_domain
  if (!rosidl_runtime_c__String__copy(
      &(input->time_domain), &(output->time_domain)))
  {
    return false;
  }
  // sync_mode
  if (!rosidl_runtime_c__String__copy(
      &(input->sync_mode), &(output->sync_mode)))
  {
    return false;
  }
  // intra_camera_sync_reference
  if (!rosidl_runtime_c__String__copy(
      &(input->intra_camera_sync_reference), &(output->intra_camera_sync_reference)))
  {
    return false;
  }
  // data_json
  if (!rosidl_runtime_c__String__copy(
      &(input->data_json), &(output->data_json)))
  {
    return false;
  }
  // success
  output->success = input->success;
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  return true;
}

orbbec_camera_msgs__srv__GetDeviceConfig_Response *
orbbec_camera_msgs__srv__GetDeviceConfig_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  orbbec_camera_msgs__srv__GetDeviceConfig_Response * msg = (orbbec_camera_msgs__srv__GetDeviceConfig_Response *)allocator.allocate(sizeof(orbbec_camera_msgs__srv__GetDeviceConfig_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(orbbec_camera_msgs__srv__GetDeviceConfig_Response));
  bool success = orbbec_camera_msgs__srv__GetDeviceConfig_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
orbbec_camera_msgs__srv__GetDeviceConfig_Response__destroy(orbbec_camera_msgs__srv__GetDeviceConfig_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    orbbec_camera_msgs__srv__GetDeviceConfig_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
orbbec_camera_msgs__srv__GetDeviceConfig_Response__Sequence__init(orbbec_camera_msgs__srv__GetDeviceConfig_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  orbbec_camera_msgs__srv__GetDeviceConfig_Response * data = NULL;

  if (size) {
    data = (orbbec_camera_msgs__srv__GetDeviceConfig_Response *)allocator.zero_allocate(size, sizeof(orbbec_camera_msgs__srv__GetDeviceConfig_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = orbbec_camera_msgs__srv__GetDeviceConfig_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        orbbec_camera_msgs__srv__GetDeviceConfig_Response__fini(&data[i - 1]);
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
orbbec_camera_msgs__srv__GetDeviceConfig_Response__Sequence__fini(orbbec_camera_msgs__srv__GetDeviceConfig_Response__Sequence * array)
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
      orbbec_camera_msgs__srv__GetDeviceConfig_Response__fini(&array->data[i]);
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

orbbec_camera_msgs__srv__GetDeviceConfig_Response__Sequence *
orbbec_camera_msgs__srv__GetDeviceConfig_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  orbbec_camera_msgs__srv__GetDeviceConfig_Response__Sequence * array = (orbbec_camera_msgs__srv__GetDeviceConfig_Response__Sequence *)allocator.allocate(sizeof(orbbec_camera_msgs__srv__GetDeviceConfig_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = orbbec_camera_msgs__srv__GetDeviceConfig_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
orbbec_camera_msgs__srv__GetDeviceConfig_Response__Sequence__destroy(orbbec_camera_msgs__srv__GetDeviceConfig_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    orbbec_camera_msgs__srv__GetDeviceConfig_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
orbbec_camera_msgs__srv__GetDeviceConfig_Response__Sequence__are_equal(const orbbec_camera_msgs__srv__GetDeviceConfig_Response__Sequence * lhs, const orbbec_camera_msgs__srv__GetDeviceConfig_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!orbbec_camera_msgs__srv__GetDeviceConfig_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
orbbec_camera_msgs__srv__GetDeviceConfig_Response__Sequence__copy(
  const orbbec_camera_msgs__srv__GetDeviceConfig_Response__Sequence * input,
  orbbec_camera_msgs__srv__GetDeviceConfig_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(orbbec_camera_msgs__srv__GetDeviceConfig_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    orbbec_camera_msgs__srv__GetDeviceConfig_Response * data =
      (orbbec_camera_msgs__srv__GetDeviceConfig_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!orbbec_camera_msgs__srv__GetDeviceConfig_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          orbbec_camera_msgs__srv__GetDeviceConfig_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!orbbec_camera_msgs__srv__GetDeviceConfig_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
