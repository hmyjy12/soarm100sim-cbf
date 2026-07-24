// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from soarm100_interfaces:msg/TrackedTarget2D.idl
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
#include "soarm100_interfaces/msg/detail/tracked_target2_d__struct.h"
#include "soarm100_interfaces/msg/detail/tracked_target2_d__functions.h"

#include "rosidl_runtime_c/string.h"
#include "rosidl_runtime_c/string_functions.h"

ROSIDL_GENERATOR_C_IMPORT
bool std_msgs__msg__header__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * std_msgs__msg__header__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool soarm100_interfaces__msg__tracked_target2_d__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[59];
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
    assert(strncmp("soarm100_interfaces.msg._tracked_target2_d.TrackedTarget2D", full_classname_dest, 58) == 0);
  }
  soarm100_interfaces__msg__TrackedTarget2D * ros_message = _ros_message;
  {  // header
    PyObject * field = PyObject_GetAttrString(_pymsg, "header");
    if (!field) {
      return false;
    }
    if (!std_msgs__msg__header__convert_from_py(field, &ros_message->header)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // valid
    PyObject * field = PyObject_GetAttrString(_pymsg, "valid");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->valid = (Py_True == field);
    Py_DECREF(field);
  }
  {  // u
    PyObject * field = PyObject_GetAttrString(_pymsg, "u");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->u = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // v
    PyObject * field = PyObject_GetAttrString(_pymsg, "v");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->v = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // reference_u
    PyObject * field = PyObject_GetAttrString(_pymsg, "reference_u");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->reference_u = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // reference_v
    PyObject * field = PyObject_GetAttrString(_pymsg, "reference_v");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->reference_v = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // delta_u
    PyObject * field = PyObject_GetAttrString(_pymsg, "delta_u");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->delta_u = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // delta_v
    PyObject * field = PyObject_GetAttrString(_pymsg, "delta_v");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->delta_v = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // width
    PyObject * field = PyObject_GetAttrString(_pymsg, "width");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->width = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // height
    PyObject * field = PyObject_GetAttrString(_pymsg, "height");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->height = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // image_width
    PyObject * field = PyObject_GetAttrString(_pymsg, "image_width");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->image_width = PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // image_height
    PyObject * field = PyObject_GetAttrString(_pymsg, "image_height");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->image_height = PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // confidence
    PyObject * field = PyObject_GetAttrString(_pymsg, "confidence");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->confidence = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // lost_frames
    PyObject * field = PyObject_GetAttrString(_pymsg, "lost_frames");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->lost_frames = PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // replan_required
    PyObject * field = PyObject_GetAttrString(_pymsg, "replan_required");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->replan_required = (Py_True == field);
    Py_DECREF(field);
  }
  {  // reason
    PyObject * field = PyObject_GetAttrString(_pymsg, "reason");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->reason, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * soarm100_interfaces__msg__tracked_target2_d__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of TrackedTarget2D */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("soarm100_interfaces.msg._tracked_target2_d");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "TrackedTarget2D");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  soarm100_interfaces__msg__TrackedTarget2D * ros_message = (soarm100_interfaces__msg__TrackedTarget2D *)raw_ros_message;
  {  // header
    PyObject * field = NULL;
    field = std_msgs__msg__header__convert_to_py(&ros_message->header);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "header", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // valid
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->valid ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "valid", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // u
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->u);
    {
      int rc = PyObject_SetAttrString(_pymessage, "u", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // v
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->v);
    {
      int rc = PyObject_SetAttrString(_pymessage, "v", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // reference_u
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->reference_u);
    {
      int rc = PyObject_SetAttrString(_pymessage, "reference_u", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // reference_v
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->reference_v);
    {
      int rc = PyObject_SetAttrString(_pymessage, "reference_v", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // delta_u
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->delta_u);
    {
      int rc = PyObject_SetAttrString(_pymessage, "delta_u", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // delta_v
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->delta_v);
    {
      int rc = PyObject_SetAttrString(_pymessage, "delta_v", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // width
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->width);
    {
      int rc = PyObject_SetAttrString(_pymessage, "width", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // height
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->height);
    {
      int rc = PyObject_SetAttrString(_pymessage, "height", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // image_width
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->image_width);
    {
      int rc = PyObject_SetAttrString(_pymessage, "image_width", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // image_height
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->image_height);
    {
      int rc = PyObject_SetAttrString(_pymessage, "image_height", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // confidence
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->confidence);
    {
      int rc = PyObject_SetAttrString(_pymessage, "confidence", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // lost_frames
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->lost_frames);
    {
      int rc = PyObject_SetAttrString(_pymessage, "lost_frames", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // replan_required
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->replan_required ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "replan_required", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // reason
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->reason.data,
      strlen(ros_message->reason.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "reason", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
