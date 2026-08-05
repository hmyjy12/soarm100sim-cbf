// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from soarm100_interfaces:srv/MoveJointDelta.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "soarm100_interfaces/srv/detail/move_joint_delta__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace soarm100_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveJointDelta_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveJointDelta_Request_type_support_ids_t;

static const _MoveJointDelta_Request_type_support_ids_t _MoveJointDelta_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveJointDelta_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveJointDelta_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveJointDelta_Request_type_support_symbol_names_t _MoveJointDelta_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, soarm100_interfaces, srv, MoveJointDelta_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, soarm100_interfaces, srv, MoveJointDelta_Request)),
  }
};

typedef struct _MoveJointDelta_Request_type_support_data_t
{
  void * data[2];
} _MoveJointDelta_Request_type_support_data_t;

static _MoveJointDelta_Request_type_support_data_t _MoveJointDelta_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveJointDelta_Request_message_typesupport_map = {
  2,
  "soarm100_interfaces",
  &_MoveJointDelta_Request_message_typesupport_ids.typesupport_identifier[0],
  &_MoveJointDelta_Request_message_typesupport_symbol_names.symbol_name[0],
  &_MoveJointDelta_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveJointDelta_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveJointDelta_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace soarm100_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<soarm100_interfaces::srv::MoveJointDelta_Request>()
{
  return &::soarm100_interfaces::srv::rosidl_typesupport_cpp::MoveJointDelta_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, soarm100_interfaces, srv, MoveJointDelta_Request)() {
  return get_message_type_support_handle<soarm100_interfaces::srv::MoveJointDelta_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "soarm100_interfaces/srv/detail/move_joint_delta__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace soarm100_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveJointDelta_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveJointDelta_Response_type_support_ids_t;

static const _MoveJointDelta_Response_type_support_ids_t _MoveJointDelta_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveJointDelta_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveJointDelta_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveJointDelta_Response_type_support_symbol_names_t _MoveJointDelta_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, soarm100_interfaces, srv, MoveJointDelta_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, soarm100_interfaces, srv, MoveJointDelta_Response)),
  }
};

typedef struct _MoveJointDelta_Response_type_support_data_t
{
  void * data[2];
} _MoveJointDelta_Response_type_support_data_t;

static _MoveJointDelta_Response_type_support_data_t _MoveJointDelta_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveJointDelta_Response_message_typesupport_map = {
  2,
  "soarm100_interfaces",
  &_MoveJointDelta_Response_message_typesupport_ids.typesupport_identifier[0],
  &_MoveJointDelta_Response_message_typesupport_symbol_names.symbol_name[0],
  &_MoveJointDelta_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t MoveJointDelta_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveJointDelta_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace soarm100_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<soarm100_interfaces::srv::MoveJointDelta_Response>()
{
  return &::soarm100_interfaces::srv::rosidl_typesupport_cpp::MoveJointDelta_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, soarm100_interfaces, srv, MoveJointDelta_Response)() {
  return get_message_type_support_handle<soarm100_interfaces::srv::MoveJointDelta_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "soarm100_interfaces/srv/detail/move_joint_delta__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace soarm100_interfaces
{

namespace srv
{

namespace rosidl_typesupport_cpp
{

typedef struct _MoveJointDelta_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _MoveJointDelta_type_support_ids_t;

static const _MoveJointDelta_type_support_ids_t _MoveJointDelta_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _MoveJointDelta_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _MoveJointDelta_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _MoveJointDelta_type_support_symbol_names_t _MoveJointDelta_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, soarm100_interfaces, srv, MoveJointDelta)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, soarm100_interfaces, srv, MoveJointDelta)),
  }
};

typedef struct _MoveJointDelta_type_support_data_t
{
  void * data[2];
} _MoveJointDelta_type_support_data_t;

static _MoveJointDelta_type_support_data_t _MoveJointDelta_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _MoveJointDelta_service_typesupport_map = {
  2,
  "soarm100_interfaces",
  &_MoveJointDelta_service_typesupport_ids.typesupport_identifier[0],
  &_MoveJointDelta_service_typesupport_symbol_names.symbol_name[0],
  &_MoveJointDelta_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t MoveJointDelta_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_MoveJointDelta_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace srv

}  // namespace soarm100_interfaces

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<soarm100_interfaces::srv::MoveJointDelta>()
{
  return &::soarm100_interfaces::srv::rosidl_typesupport_cpp::MoveJointDelta_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, soarm100_interfaces, srv, MoveJointDelta)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<soarm100_interfaces::srv::MoveJointDelta>();
}

#ifdef __cplusplus
}
#endif
