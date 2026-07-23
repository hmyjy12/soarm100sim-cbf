// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from soarm100_interfaces:action/ExecutePlannedGrasp.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_PLANNED_GRASP__FUNCTIONS_H_
#define SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_PLANNED_GRASP__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "soarm100_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "soarm100_interfaces/action/detail/execute_planned_grasp__struct.h"

/// Initialize action/ExecutePlannedGrasp message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * soarm100_interfaces__action__ExecutePlannedGrasp_Goal
 * )) before or use
 * soarm100_interfaces__action__ExecutePlannedGrasp_Goal__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_Goal__init(soarm100_interfaces__action__ExecutePlannedGrasp_Goal * msg);

/// Finalize action/ExecutePlannedGrasp message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_Goal__fini(soarm100_interfaces__action__ExecutePlannedGrasp_Goal * msg);

/// Create action/ExecutePlannedGrasp message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_Goal__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
soarm100_interfaces__action__ExecutePlannedGrasp_Goal *
soarm100_interfaces__action__ExecutePlannedGrasp_Goal__create();

/// Destroy action/ExecutePlannedGrasp message.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_Goal__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_Goal__destroy(soarm100_interfaces__action__ExecutePlannedGrasp_Goal * msg);

/// Check for action/ExecutePlannedGrasp message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_Goal__are_equal(const soarm100_interfaces__action__ExecutePlannedGrasp_Goal * lhs, const soarm100_interfaces__action__ExecutePlannedGrasp_Goal * rhs);

/// Copy a action/ExecutePlannedGrasp message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_Goal__copy(
  const soarm100_interfaces__action__ExecutePlannedGrasp_Goal * input,
  soarm100_interfaces__action__ExecutePlannedGrasp_Goal * output);

/// Initialize array of action/ExecutePlannedGrasp messages.
/**
 * It allocates the memory for the number of elements and calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_Goal__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence__init(soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence * array, size_t size);

/// Finalize array of action/ExecutePlannedGrasp messages.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_Goal__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence__fini(soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence * array);

/// Create array of action/ExecutePlannedGrasp messages.
/**
 * It allocates the memory for the array and calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence *
soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence__create(size_t size);

/// Destroy array of action/ExecutePlannedGrasp messages.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence__destroy(soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence * array);

/// Check for action/ExecutePlannedGrasp message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence__are_equal(const soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence * lhs, const soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence * rhs);

/// Copy an array of action/ExecutePlannedGrasp messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence__copy(
  const soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence * input,
  soarm100_interfaces__action__ExecutePlannedGrasp_Goal__Sequence * output);

/// Initialize action/ExecutePlannedGrasp message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * soarm100_interfaces__action__ExecutePlannedGrasp_Result
 * )) before or use
 * soarm100_interfaces__action__ExecutePlannedGrasp_Result__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_Result__init(soarm100_interfaces__action__ExecutePlannedGrasp_Result * msg);

/// Finalize action/ExecutePlannedGrasp message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_Result__fini(soarm100_interfaces__action__ExecutePlannedGrasp_Result * msg);

/// Create action/ExecutePlannedGrasp message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_Result__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
soarm100_interfaces__action__ExecutePlannedGrasp_Result *
soarm100_interfaces__action__ExecutePlannedGrasp_Result__create();

/// Destroy action/ExecutePlannedGrasp message.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_Result__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_Result__destroy(soarm100_interfaces__action__ExecutePlannedGrasp_Result * msg);

/// Check for action/ExecutePlannedGrasp message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_Result__are_equal(const soarm100_interfaces__action__ExecutePlannedGrasp_Result * lhs, const soarm100_interfaces__action__ExecutePlannedGrasp_Result * rhs);

/// Copy a action/ExecutePlannedGrasp message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_Result__copy(
  const soarm100_interfaces__action__ExecutePlannedGrasp_Result * input,
  soarm100_interfaces__action__ExecutePlannedGrasp_Result * output);

/// Initialize array of action/ExecutePlannedGrasp messages.
/**
 * It allocates the memory for the number of elements and calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_Result__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence__init(soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence * array, size_t size);

/// Finalize array of action/ExecutePlannedGrasp messages.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_Result__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence__fini(soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence * array);

/// Create array of action/ExecutePlannedGrasp messages.
/**
 * It allocates the memory for the array and calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence *
soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence__create(size_t size);

/// Destroy array of action/ExecutePlannedGrasp messages.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence__destroy(soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence * array);

/// Check for action/ExecutePlannedGrasp message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence__are_equal(const soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence * lhs, const soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence * rhs);

/// Copy an array of action/ExecutePlannedGrasp messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence__copy(
  const soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence * input,
  soarm100_interfaces__action__ExecutePlannedGrasp_Result__Sequence * output);

/// Initialize action/ExecutePlannedGrasp message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * soarm100_interfaces__action__ExecutePlannedGrasp_Feedback
 * )) before or use
 * soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__init(soarm100_interfaces__action__ExecutePlannedGrasp_Feedback * msg);

/// Finalize action/ExecutePlannedGrasp message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__fini(soarm100_interfaces__action__ExecutePlannedGrasp_Feedback * msg);

/// Create action/ExecutePlannedGrasp message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
soarm100_interfaces__action__ExecutePlannedGrasp_Feedback *
soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__create();

/// Destroy action/ExecutePlannedGrasp message.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__destroy(soarm100_interfaces__action__ExecutePlannedGrasp_Feedback * msg);

/// Check for action/ExecutePlannedGrasp message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__are_equal(const soarm100_interfaces__action__ExecutePlannedGrasp_Feedback * lhs, const soarm100_interfaces__action__ExecutePlannedGrasp_Feedback * rhs);

/// Copy a action/ExecutePlannedGrasp message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__copy(
  const soarm100_interfaces__action__ExecutePlannedGrasp_Feedback * input,
  soarm100_interfaces__action__ExecutePlannedGrasp_Feedback * output);

/// Initialize array of action/ExecutePlannedGrasp messages.
/**
 * It allocates the memory for the number of elements and calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence__init(soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence * array, size_t size);

/// Finalize array of action/ExecutePlannedGrasp messages.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence__fini(soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence * array);

/// Create array of action/ExecutePlannedGrasp messages.
/**
 * It allocates the memory for the array and calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence *
soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence__create(size_t size);

/// Destroy array of action/ExecutePlannedGrasp messages.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence__destroy(soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence * array);

/// Check for action/ExecutePlannedGrasp message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence__are_equal(const soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence * lhs, const soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence * rhs);

/// Copy an array of action/ExecutePlannedGrasp messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence__copy(
  const soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence * input,
  soarm100_interfaces__action__ExecutePlannedGrasp_Feedback__Sequence * output);

/// Initialize action/ExecutePlannedGrasp message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request
 * )) before or use
 * soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__init(soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request * msg);

/// Finalize action/ExecutePlannedGrasp message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__fini(soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request * msg);

/// Create action/ExecutePlannedGrasp message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request *
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__create();

/// Destroy action/ExecutePlannedGrasp message.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__destroy(soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request * msg);

/// Check for action/ExecutePlannedGrasp message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__are_equal(const soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request * lhs, const soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request * rhs);

/// Copy a action/ExecutePlannedGrasp message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__copy(
  const soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request * input,
  soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request * output);

/// Initialize array of action/ExecutePlannedGrasp messages.
/**
 * It allocates the memory for the number of elements and calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence__init(soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence * array, size_t size);

/// Finalize array of action/ExecutePlannedGrasp messages.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence__fini(soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence * array);

/// Create array of action/ExecutePlannedGrasp messages.
/**
 * It allocates the memory for the array and calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence *
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence__create(size_t size);

/// Destroy array of action/ExecutePlannedGrasp messages.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence__destroy(soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence * array);

/// Check for action/ExecutePlannedGrasp message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence__are_equal(const soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence * lhs, const soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence * rhs);

/// Copy an array of action/ExecutePlannedGrasp messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence__copy(
  const soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence * input,
  soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request__Sequence * output);

/// Initialize action/ExecutePlannedGrasp message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response
 * )) before or use
 * soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__init(soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response * msg);

/// Finalize action/ExecutePlannedGrasp message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__fini(soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response * msg);

/// Create action/ExecutePlannedGrasp message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response *
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__create();

/// Destroy action/ExecutePlannedGrasp message.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__destroy(soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response * msg);

/// Check for action/ExecutePlannedGrasp message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__are_equal(const soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response * lhs, const soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response * rhs);

/// Copy a action/ExecutePlannedGrasp message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__copy(
  const soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response * input,
  soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response * output);

/// Initialize array of action/ExecutePlannedGrasp messages.
/**
 * It allocates the memory for the number of elements and calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence__init(soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence * array, size_t size);

/// Finalize array of action/ExecutePlannedGrasp messages.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence__fini(soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence * array);

/// Create array of action/ExecutePlannedGrasp messages.
/**
 * It allocates the memory for the array and calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence *
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence__create(size_t size);

/// Destroy array of action/ExecutePlannedGrasp messages.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence__destroy(soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence * array);

/// Check for action/ExecutePlannedGrasp message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence__are_equal(const soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence * lhs, const soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence * rhs);

/// Copy an array of action/ExecutePlannedGrasp messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence__copy(
  const soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence * input,
  soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response__Sequence * output);

/// Initialize action/ExecutePlannedGrasp message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request
 * )) before or use
 * soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__init(soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request * msg);

/// Finalize action/ExecutePlannedGrasp message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__fini(soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request * msg);

/// Create action/ExecutePlannedGrasp message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request *
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__create();

/// Destroy action/ExecutePlannedGrasp message.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__destroy(soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request * msg);

/// Check for action/ExecutePlannedGrasp message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__are_equal(const soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request * lhs, const soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request * rhs);

/// Copy a action/ExecutePlannedGrasp message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__copy(
  const soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request * input,
  soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request * output);

/// Initialize array of action/ExecutePlannedGrasp messages.
/**
 * It allocates the memory for the number of elements and calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence__init(soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence * array, size_t size);

/// Finalize array of action/ExecutePlannedGrasp messages.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence__fini(soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence * array);

/// Create array of action/ExecutePlannedGrasp messages.
/**
 * It allocates the memory for the array and calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence *
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence__create(size_t size);

/// Destroy array of action/ExecutePlannedGrasp messages.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence__destroy(soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence * array);

/// Check for action/ExecutePlannedGrasp message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence__are_equal(const soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence * lhs, const soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence * rhs);

/// Copy an array of action/ExecutePlannedGrasp messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence__copy(
  const soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence * input,
  soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request__Sequence * output);

/// Initialize action/ExecutePlannedGrasp message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response
 * )) before or use
 * soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__init(soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response * msg);

/// Finalize action/ExecutePlannedGrasp message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__fini(soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response * msg);

/// Create action/ExecutePlannedGrasp message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response *
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__create();

/// Destroy action/ExecutePlannedGrasp message.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__destroy(soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response * msg);

/// Check for action/ExecutePlannedGrasp message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__are_equal(const soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response * lhs, const soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response * rhs);

/// Copy a action/ExecutePlannedGrasp message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__copy(
  const soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response * input,
  soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response * output);

/// Initialize array of action/ExecutePlannedGrasp messages.
/**
 * It allocates the memory for the number of elements and calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence__init(soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence * array, size_t size);

/// Finalize array of action/ExecutePlannedGrasp messages.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence__fini(soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence * array);

/// Create array of action/ExecutePlannedGrasp messages.
/**
 * It allocates the memory for the array and calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence *
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence__create(size_t size);

/// Destroy array of action/ExecutePlannedGrasp messages.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence__destroy(soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence * array);

/// Check for action/ExecutePlannedGrasp message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence__are_equal(const soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence * lhs, const soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence * rhs);

/// Copy an array of action/ExecutePlannedGrasp messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence__copy(
  const soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence * input,
  soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response__Sequence * output);

/// Initialize action/ExecutePlannedGrasp message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage
 * )) before or use
 * soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__init(soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage * msg);

/// Finalize action/ExecutePlannedGrasp message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__fini(soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage * msg);

/// Create action/ExecutePlannedGrasp message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage *
soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__create();

/// Destroy action/ExecutePlannedGrasp message.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__destroy(soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage * msg);

/// Check for action/ExecutePlannedGrasp message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__are_equal(const soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage * lhs, const soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage * rhs);

/// Copy a action/ExecutePlannedGrasp message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__copy(
  const soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage * input,
  soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage * output);

/// Initialize array of action/ExecutePlannedGrasp messages.
/**
 * It allocates the memory for the number of elements and calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence__init(soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence * array, size_t size);

/// Finalize array of action/ExecutePlannedGrasp messages.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence__fini(soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence * array);

/// Create array of action/ExecutePlannedGrasp messages.
/**
 * It allocates the memory for the array and calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence *
soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence__create(size_t size);

/// Destroy array of action/ExecutePlannedGrasp messages.
/**
 * It calls
 * soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
void
soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence__destroy(soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence * array);

/// Check for action/ExecutePlannedGrasp message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence__are_equal(const soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence * lhs, const soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence * rhs);

/// Copy an array of action/ExecutePlannedGrasp messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_soarm100_interfaces
bool
soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence__copy(
  const soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence * input,
  soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_PLANNED_GRASP__FUNCTIONS_H_
