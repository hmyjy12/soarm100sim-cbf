// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from orbbec_camera_msgs:msg/DepthFilterState.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "orbbec_camera_msgs/msg/detail/depth_filter_state__struct.h"
#include "orbbec_camera_msgs/msg/detail/depth_filter_state__functions.h"

#include "rosidl_runtime_c/string.h"
#include "rosidl_runtime_c/string_functions.h"

#include "rosidl_runtime_c/primitives_sequence.h"
#include "rosidl_runtime_c/primitives_sequence_functions.h"

// Nested array functions includes
#include "orbbec_camera_msgs/msg/detail/depth_filter_param__functions.h"
// end nested array functions include
bool orbbec_camera_msgs__msg__depth_filter_param__convert_from_py(PyObject * _pymsg, void * _ros_message);
PyObject * orbbec_camera_msgs__msg__depth_filter_param__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool orbbec_camera_msgs__msg__depth_filter_state__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[60];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("orbbec_camera_msgs.msg._depth_filter_state.DepthFilterState", full_classname_dest, 59) == 0);
  }
  orbbec_camera_msgs__msg__DepthFilterState * ros_message = _ros_message;
  {  // filter_name
    PyObject * field = PyObject_GetAttrString(_pymsg, "filter_name");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->filter_name, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // enabled
    PyObject * field = PyObject_GetAttrString(_pymsg, "enabled");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->enabled = (Py_True == field);
    Py_DECREF(field);
  }
  {  // params
    PyObject * field = PyObject_GetAttrString(_pymsg, "params");
    if (!field) {
      return false;
    }
    PyObject * seq_field = PySequence_Fast(field, "expected a sequence in 'params'");
    if (!seq_field) {
      Py_DECREF(field);
      return false;
    }
    Py_ssize_t size = PySequence_Size(field);
    if (-1 == size) {
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    if (!orbbec_camera_msgs__msg__DepthFilterParam__Sequence__init(&(ros_message->params), size)) {
      PyErr_SetString(PyExc_RuntimeError, "unable to create orbbec_camera_msgs__msg__DepthFilterParam__Sequence ros_message");
      Py_DECREF(seq_field);
      Py_DECREF(field);
      return false;
    }
    orbbec_camera_msgs__msg__DepthFilterParam * dest = ros_message->params.data;
    for (Py_ssize_t i = 0; i < size; ++i) {
      if (!orbbec_camera_msgs__msg__depth_filter_param__convert_from_py(PySequence_Fast_GET_ITEM(seq_field, i), &dest[i])) {
        Py_DECREF(seq_field);
        Py_DECREF(field);
        return false;
      }
    }
    Py_DECREF(seq_field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * orbbec_camera_msgs__msg__depth_filter_state__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of DepthFilterState */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("orbbec_camera_msgs.msg._depth_filter_state");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "DepthFilterState");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  orbbec_camera_msgs__msg__DepthFilterState * ros_message = (orbbec_camera_msgs__msg__DepthFilterState *)raw_ros_message;
  {  // filter_name
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->filter_name.data,
      strlen(ros_message->filter_name.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "filter_name", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // enabled
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->enabled ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "enabled", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // params
    PyObject * field = NULL;
    size_t size = ros_message->params.size;
    field = PyList_New(size);
    if (!field) {
      return NULL;
    }
    orbbec_camera_msgs__msg__DepthFilterParam * item;
    for (size_t i = 0; i < size; ++i) {
      item = &(ros_message->params.data[i]);
      PyObject * pyitem = orbbec_camera_msgs__msg__depth_filter_param__convert_to_py(item);
      if (!pyitem) {
        Py_DECREF(field);
        return NULL;
      }
      int rc = PyList_SetItem(field, i, pyitem);
      (void)rc;
      assert(rc == 0);
    }
    assert(PySequence_Check(field));
    {
      int rc = PyObject_SetAttrString(_pymessage, "params", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
