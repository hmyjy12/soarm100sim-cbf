// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from soarm100_interfaces:action/ExecuteGrasp.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "soarm100_interfaces/action/detail/execute_grasp__struct.h"
#include "soarm100_interfaces/action/detail/execute_grasp__type_support.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace soarm100_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _ExecuteGrasp_Goal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ExecuteGrasp_Goal_type_support_ids_t;

static const _ExecuteGrasp_Goal_type_support_ids_t _ExecuteGrasp_Goal_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _ExecuteGrasp_Goal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ExecuteGrasp_Goal_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ExecuteGrasp_Goal_type_support_symbol_names_t _ExecuteGrasp_Goal_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, soarm100_interfaces, action, ExecuteGrasp_Goal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, ExecuteGrasp_Goal)),
  }
};

typedef struct _ExecuteGrasp_Goal_type_support_data_t
{
  void * data[2];
} _ExecuteGrasp_Goal_type_support_data_t;

static _ExecuteGrasp_Goal_type_support_data_t _ExecuteGrasp_Goal_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ExecuteGrasp_Goal_message_typesupport_map = {
  2,
  "soarm100_interfaces",
  &_ExecuteGrasp_Goal_message_typesupport_ids.typesupport_identifier[0],
  &_ExecuteGrasp_Goal_message_typesupport_symbol_names.symbol_name[0],
  &_ExecuteGrasp_Goal_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ExecuteGrasp_Goal_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ExecuteGrasp_Goal_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace soarm100_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, soarm100_interfaces, action, ExecuteGrasp_Goal)() {
  return &::soarm100_interfaces::action::rosidl_typesupport_c::ExecuteGrasp_Goal_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "soarm100_interfaces/action/detail/execute_grasp__struct.h"
// already included above
// #include "soarm100_interfaces/action/detail/execute_grasp__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace soarm100_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _ExecuteGrasp_Result_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ExecuteGrasp_Result_type_support_ids_t;

static const _ExecuteGrasp_Result_type_support_ids_t _ExecuteGrasp_Result_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _ExecuteGrasp_Result_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ExecuteGrasp_Result_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ExecuteGrasp_Result_type_support_symbol_names_t _ExecuteGrasp_Result_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, soarm100_interfaces, action, ExecuteGrasp_Result)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, ExecuteGrasp_Result)),
  }
};

typedef struct _ExecuteGrasp_Result_type_support_data_t
{
  void * data[2];
} _ExecuteGrasp_Result_type_support_data_t;

static _ExecuteGrasp_Result_type_support_data_t _ExecuteGrasp_Result_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ExecuteGrasp_Result_message_typesupport_map = {
  2,
  "soarm100_interfaces",
  &_ExecuteGrasp_Result_message_typesupport_ids.typesupport_identifier[0],
  &_ExecuteGrasp_Result_message_typesupport_symbol_names.symbol_name[0],
  &_ExecuteGrasp_Result_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ExecuteGrasp_Result_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ExecuteGrasp_Result_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace soarm100_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, soarm100_interfaces, action, ExecuteGrasp_Result)() {
  return &::soarm100_interfaces::action::rosidl_typesupport_c::ExecuteGrasp_Result_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "soarm100_interfaces/action/detail/execute_grasp__struct.h"
// already included above
// #include "soarm100_interfaces/action/detail/execute_grasp__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace soarm100_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _ExecuteGrasp_Feedback_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ExecuteGrasp_Feedback_type_support_ids_t;

static const _ExecuteGrasp_Feedback_type_support_ids_t _ExecuteGrasp_Feedback_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _ExecuteGrasp_Feedback_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ExecuteGrasp_Feedback_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ExecuteGrasp_Feedback_type_support_symbol_names_t _ExecuteGrasp_Feedback_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, soarm100_interfaces, action, ExecuteGrasp_Feedback)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, ExecuteGrasp_Feedback)),
  }
};

typedef struct _ExecuteGrasp_Feedback_type_support_data_t
{
  void * data[2];
} _ExecuteGrasp_Feedback_type_support_data_t;

static _ExecuteGrasp_Feedback_type_support_data_t _ExecuteGrasp_Feedback_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ExecuteGrasp_Feedback_message_typesupport_map = {
  2,
  "soarm100_interfaces",
  &_ExecuteGrasp_Feedback_message_typesupport_ids.typesupport_identifier[0],
  &_ExecuteGrasp_Feedback_message_typesupport_symbol_names.symbol_name[0],
  &_ExecuteGrasp_Feedback_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ExecuteGrasp_Feedback_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ExecuteGrasp_Feedback_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace soarm100_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, soarm100_interfaces, action, ExecuteGrasp_Feedback)() {
  return &::soarm100_interfaces::action::rosidl_typesupport_c::ExecuteGrasp_Feedback_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "soarm100_interfaces/action/detail/execute_grasp__struct.h"
// already included above
// #include "soarm100_interfaces/action/detail/execute_grasp__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace soarm100_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _ExecuteGrasp_SendGoal_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ExecuteGrasp_SendGoal_Request_type_support_ids_t;

static const _ExecuteGrasp_SendGoal_Request_type_support_ids_t _ExecuteGrasp_SendGoal_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _ExecuteGrasp_SendGoal_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ExecuteGrasp_SendGoal_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ExecuteGrasp_SendGoal_Request_type_support_symbol_names_t _ExecuteGrasp_SendGoal_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, soarm100_interfaces, action, ExecuteGrasp_SendGoal_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, ExecuteGrasp_SendGoal_Request)),
  }
};

typedef struct _ExecuteGrasp_SendGoal_Request_type_support_data_t
{
  void * data[2];
} _ExecuteGrasp_SendGoal_Request_type_support_data_t;

static _ExecuteGrasp_SendGoal_Request_type_support_data_t _ExecuteGrasp_SendGoal_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ExecuteGrasp_SendGoal_Request_message_typesupport_map = {
  2,
  "soarm100_interfaces",
  &_ExecuteGrasp_SendGoal_Request_message_typesupport_ids.typesupport_identifier[0],
  &_ExecuteGrasp_SendGoal_Request_message_typesupport_symbol_names.symbol_name[0],
  &_ExecuteGrasp_SendGoal_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ExecuteGrasp_SendGoal_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ExecuteGrasp_SendGoal_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace soarm100_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, soarm100_interfaces, action, ExecuteGrasp_SendGoal_Request)() {
  return &::soarm100_interfaces::action::rosidl_typesupport_c::ExecuteGrasp_SendGoal_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "soarm100_interfaces/action/detail/execute_grasp__struct.h"
// already included above
// #include "soarm100_interfaces/action/detail/execute_grasp__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace soarm100_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _ExecuteGrasp_SendGoal_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ExecuteGrasp_SendGoal_Response_type_support_ids_t;

static const _ExecuteGrasp_SendGoal_Response_type_support_ids_t _ExecuteGrasp_SendGoal_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _ExecuteGrasp_SendGoal_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ExecuteGrasp_SendGoal_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ExecuteGrasp_SendGoal_Response_type_support_symbol_names_t _ExecuteGrasp_SendGoal_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, soarm100_interfaces, action, ExecuteGrasp_SendGoal_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, ExecuteGrasp_SendGoal_Response)),
  }
};

typedef struct _ExecuteGrasp_SendGoal_Response_type_support_data_t
{
  void * data[2];
} _ExecuteGrasp_SendGoal_Response_type_support_data_t;

static _ExecuteGrasp_SendGoal_Response_type_support_data_t _ExecuteGrasp_SendGoal_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ExecuteGrasp_SendGoal_Response_message_typesupport_map = {
  2,
  "soarm100_interfaces",
  &_ExecuteGrasp_SendGoal_Response_message_typesupport_ids.typesupport_identifier[0],
  &_ExecuteGrasp_SendGoal_Response_message_typesupport_symbol_names.symbol_name[0],
  &_ExecuteGrasp_SendGoal_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ExecuteGrasp_SendGoal_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ExecuteGrasp_SendGoal_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace soarm100_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, soarm100_interfaces, action, ExecuteGrasp_SendGoal_Response)() {
  return &::soarm100_interfaces::action::rosidl_typesupport_c::ExecuteGrasp_SendGoal_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "soarm100_interfaces/action/detail/execute_grasp__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace soarm100_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _ExecuteGrasp_SendGoal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ExecuteGrasp_SendGoal_type_support_ids_t;

static const _ExecuteGrasp_SendGoal_type_support_ids_t _ExecuteGrasp_SendGoal_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _ExecuteGrasp_SendGoal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ExecuteGrasp_SendGoal_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ExecuteGrasp_SendGoal_type_support_symbol_names_t _ExecuteGrasp_SendGoal_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, soarm100_interfaces, action, ExecuteGrasp_SendGoal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, ExecuteGrasp_SendGoal)),
  }
};

typedef struct _ExecuteGrasp_SendGoal_type_support_data_t
{
  void * data[2];
} _ExecuteGrasp_SendGoal_type_support_data_t;

static _ExecuteGrasp_SendGoal_type_support_data_t _ExecuteGrasp_SendGoal_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ExecuteGrasp_SendGoal_service_typesupport_map = {
  2,
  "soarm100_interfaces",
  &_ExecuteGrasp_SendGoal_service_typesupport_ids.typesupport_identifier[0],
  &_ExecuteGrasp_SendGoal_service_typesupport_symbol_names.symbol_name[0],
  &_ExecuteGrasp_SendGoal_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t ExecuteGrasp_SendGoal_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ExecuteGrasp_SendGoal_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace soarm100_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, soarm100_interfaces, action, ExecuteGrasp_SendGoal)() {
  return &::soarm100_interfaces::action::rosidl_typesupport_c::ExecuteGrasp_SendGoal_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "soarm100_interfaces/action/detail/execute_grasp__struct.h"
// already included above
// #include "soarm100_interfaces/action/detail/execute_grasp__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace soarm100_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _ExecuteGrasp_GetResult_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ExecuteGrasp_GetResult_Request_type_support_ids_t;

static const _ExecuteGrasp_GetResult_Request_type_support_ids_t _ExecuteGrasp_GetResult_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _ExecuteGrasp_GetResult_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ExecuteGrasp_GetResult_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ExecuteGrasp_GetResult_Request_type_support_symbol_names_t _ExecuteGrasp_GetResult_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, soarm100_interfaces, action, ExecuteGrasp_GetResult_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, ExecuteGrasp_GetResult_Request)),
  }
};

typedef struct _ExecuteGrasp_GetResult_Request_type_support_data_t
{
  void * data[2];
} _ExecuteGrasp_GetResult_Request_type_support_data_t;

static _ExecuteGrasp_GetResult_Request_type_support_data_t _ExecuteGrasp_GetResult_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ExecuteGrasp_GetResult_Request_message_typesupport_map = {
  2,
  "soarm100_interfaces",
  &_ExecuteGrasp_GetResult_Request_message_typesupport_ids.typesupport_identifier[0],
  &_ExecuteGrasp_GetResult_Request_message_typesupport_symbol_names.symbol_name[0],
  &_ExecuteGrasp_GetResult_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ExecuteGrasp_GetResult_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ExecuteGrasp_GetResult_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace soarm100_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, soarm100_interfaces, action, ExecuteGrasp_GetResult_Request)() {
  return &::soarm100_interfaces::action::rosidl_typesupport_c::ExecuteGrasp_GetResult_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "soarm100_interfaces/action/detail/execute_grasp__struct.h"
// already included above
// #include "soarm100_interfaces/action/detail/execute_grasp__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace soarm100_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _ExecuteGrasp_GetResult_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ExecuteGrasp_GetResult_Response_type_support_ids_t;

static const _ExecuteGrasp_GetResult_Response_type_support_ids_t _ExecuteGrasp_GetResult_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _ExecuteGrasp_GetResult_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ExecuteGrasp_GetResult_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ExecuteGrasp_GetResult_Response_type_support_symbol_names_t _ExecuteGrasp_GetResult_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, soarm100_interfaces, action, ExecuteGrasp_GetResult_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, ExecuteGrasp_GetResult_Response)),
  }
};

typedef struct _ExecuteGrasp_GetResult_Response_type_support_data_t
{
  void * data[2];
} _ExecuteGrasp_GetResult_Response_type_support_data_t;

static _ExecuteGrasp_GetResult_Response_type_support_data_t _ExecuteGrasp_GetResult_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ExecuteGrasp_GetResult_Response_message_typesupport_map = {
  2,
  "soarm100_interfaces",
  &_ExecuteGrasp_GetResult_Response_message_typesupport_ids.typesupport_identifier[0],
  &_ExecuteGrasp_GetResult_Response_message_typesupport_symbol_names.symbol_name[0],
  &_ExecuteGrasp_GetResult_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ExecuteGrasp_GetResult_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ExecuteGrasp_GetResult_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace soarm100_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, soarm100_interfaces, action, ExecuteGrasp_GetResult_Response)() {
  return &::soarm100_interfaces::action::rosidl_typesupport_c::ExecuteGrasp_GetResult_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "soarm100_interfaces/action/detail/execute_grasp__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace soarm100_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _ExecuteGrasp_GetResult_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ExecuteGrasp_GetResult_type_support_ids_t;

static const _ExecuteGrasp_GetResult_type_support_ids_t _ExecuteGrasp_GetResult_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _ExecuteGrasp_GetResult_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ExecuteGrasp_GetResult_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ExecuteGrasp_GetResult_type_support_symbol_names_t _ExecuteGrasp_GetResult_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, soarm100_interfaces, action, ExecuteGrasp_GetResult)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, ExecuteGrasp_GetResult)),
  }
};

typedef struct _ExecuteGrasp_GetResult_type_support_data_t
{
  void * data[2];
} _ExecuteGrasp_GetResult_type_support_data_t;

static _ExecuteGrasp_GetResult_type_support_data_t _ExecuteGrasp_GetResult_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ExecuteGrasp_GetResult_service_typesupport_map = {
  2,
  "soarm100_interfaces",
  &_ExecuteGrasp_GetResult_service_typesupport_ids.typesupport_identifier[0],
  &_ExecuteGrasp_GetResult_service_typesupport_symbol_names.symbol_name[0],
  &_ExecuteGrasp_GetResult_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t ExecuteGrasp_GetResult_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ExecuteGrasp_GetResult_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace soarm100_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, soarm100_interfaces, action, ExecuteGrasp_GetResult)() {
  return &::soarm100_interfaces::action::rosidl_typesupport_c::ExecuteGrasp_GetResult_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "soarm100_interfaces/action/detail/execute_grasp__struct.h"
// already included above
// #include "soarm100_interfaces/action/detail/execute_grasp__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace soarm100_interfaces
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _ExecuteGrasp_FeedbackMessage_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ExecuteGrasp_FeedbackMessage_type_support_ids_t;

static const _ExecuteGrasp_FeedbackMessage_type_support_ids_t _ExecuteGrasp_FeedbackMessage_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _ExecuteGrasp_FeedbackMessage_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ExecuteGrasp_FeedbackMessage_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ExecuteGrasp_FeedbackMessage_type_support_symbol_names_t _ExecuteGrasp_FeedbackMessage_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, soarm100_interfaces, action, ExecuteGrasp_FeedbackMessage)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, soarm100_interfaces, action, ExecuteGrasp_FeedbackMessage)),
  }
};

typedef struct _ExecuteGrasp_FeedbackMessage_type_support_data_t
{
  void * data[2];
} _ExecuteGrasp_FeedbackMessage_type_support_data_t;

static _ExecuteGrasp_FeedbackMessage_type_support_data_t _ExecuteGrasp_FeedbackMessage_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ExecuteGrasp_FeedbackMessage_message_typesupport_map = {
  2,
  "soarm100_interfaces",
  &_ExecuteGrasp_FeedbackMessage_message_typesupport_ids.typesupport_identifier[0],
  &_ExecuteGrasp_FeedbackMessage_message_typesupport_symbol_names.symbol_name[0],
  &_ExecuteGrasp_FeedbackMessage_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ExecuteGrasp_FeedbackMessage_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ExecuteGrasp_FeedbackMessage_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace soarm100_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, soarm100_interfaces, action, ExecuteGrasp_FeedbackMessage)() {
  return &::soarm100_interfaces::action::rosidl_typesupport_c::ExecuteGrasp_FeedbackMessage_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

#include "action_msgs/msg/goal_status_array.h"
#include "action_msgs/srv/cancel_goal.h"
#include "soarm100_interfaces/action/execute_grasp.h"
// already included above
// #include "soarm100_interfaces/action/detail/execute_grasp__type_support.h"

static rosidl_action_type_support_t _soarm100_interfaces__action__ExecuteGrasp__typesupport_c;

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_action_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__ACTION_SYMBOL_NAME(
  rosidl_typesupport_c, soarm100_interfaces, action, ExecuteGrasp)()
{
  // Thread-safe by always writing the same values to the static struct
  _soarm100_interfaces__action__ExecuteGrasp__typesupport_c.goal_service_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(
    rosidl_typesupport_c, soarm100_interfaces, action, ExecuteGrasp_SendGoal)();
  _soarm100_interfaces__action__ExecuteGrasp__typesupport_c.result_service_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(
    rosidl_typesupport_c, soarm100_interfaces, action, ExecuteGrasp_GetResult)();
  _soarm100_interfaces__action__ExecuteGrasp__typesupport_c.cancel_service_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(
    rosidl_typesupport_c, action_msgs, srv, CancelGoal)();
  _soarm100_interfaces__action__ExecuteGrasp__typesupport_c.feedback_message_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c, soarm100_interfaces, action, ExecuteGrasp_FeedbackMessage)();
  _soarm100_interfaces__action__ExecuteGrasp__typesupport_c.status_message_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c, action_msgs, msg, GoalStatusArray)();

  return &_soarm100_interfaces__action__ExecuteGrasp__typesupport_c;
}

#ifdef __cplusplus
}
#endif
