// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from soarm100_interfaces:srv/SegmentTarget.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__SRV__DETAIL__SEGMENT_TARGET__TRAITS_HPP_
#define SOARM100_INTERFACES__SRV__DETAIL__SEGMENT_TARGET__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "soarm100_interfaces/srv/detail/segment_target__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace soarm100_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const SegmentTarget_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: target_prompt
  {
    out << "target_prompt: ";
    rosidl_generator_traits::value_to_yaml(msg.target_prompt, out);
    out << ", ";
  }

  // member: force_yolo
  {
    out << "force_yolo: ";
    rosidl_generator_traits::value_to_yaml(msg.force_yolo, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SegmentTarget_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: target_prompt
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "target_prompt: ";
    rosidl_generator_traits::value_to_yaml(msg.target_prompt, out);
    out << "\n";
  }

  // member: force_yolo
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "force_yolo: ";
    rosidl_generator_traits::value_to_yaml(msg.force_yolo, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SegmentTarget_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace soarm100_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use soarm100_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const soarm100_interfaces::srv::SegmentTarget_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  soarm100_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use soarm100_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const soarm100_interfaces::srv::SegmentTarget_Request & msg)
{
  return soarm100_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<soarm100_interfaces::srv::SegmentTarget_Request>()
{
  return "soarm100_interfaces::srv::SegmentTarget_Request";
}

template<>
inline const char * name<soarm100_interfaces::srv::SegmentTarget_Request>()
{
  return "soarm100_interfaces/srv/SegmentTarget_Request";
}

template<>
struct has_fixed_size<soarm100_interfaces::srv::SegmentTarget_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<soarm100_interfaces::srv::SegmentTarget_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<soarm100_interfaces::srv::SegmentTarget_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'target_center'
#include "geometry_msgs/msg/detail/pose_stamped__traits.hpp"

namespace soarm100_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const SegmentTarget_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: reason
  {
    out << "reason: ";
    rosidl_generator_traits::value_to_yaml(msg.reason, out);
    out << ", ";
  }

  // member: target_center
  {
    out << "target_center: ";
    to_flow_style_yaml(msg.target_center, out);
    out << ", ";
  }

  // member: score
  {
    out << "score: ";
    rosidl_generator_traits::value_to_yaml(msg.score, out);
    out << ", ";
  }

  // member: bbox_xyxy
  {
    if (msg.bbox_xyxy.size() == 0) {
      out << "bbox_xyxy: []";
    } else {
      out << "bbox_xyxy: [";
      size_t pending_items = msg.bbox_xyxy.size();
      for (auto item : msg.bbox_xyxy) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: mask_topic
  {
    out << "mask_topic: ";
    rosidl_generator_traits::value_to_yaml(msg.mask_topic, out);
    out << ", ";
  }

  // member: debug_json
  {
    out << "debug_json: ";
    rosidl_generator_traits::value_to_yaml(msg.debug_json, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SegmentTarget_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: reason
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "reason: ";
    rosidl_generator_traits::value_to_yaml(msg.reason, out);
    out << "\n";
  }

  // member: target_center
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "target_center:\n";
    to_block_style_yaml(msg.target_center, out, indentation + 2);
  }

  // member: score
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "score: ";
    rosidl_generator_traits::value_to_yaml(msg.score, out);
    out << "\n";
  }

  // member: bbox_xyxy
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.bbox_xyxy.size() == 0) {
      out << "bbox_xyxy: []\n";
    } else {
      out << "bbox_xyxy:\n";
      for (auto item : msg.bbox_xyxy) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: mask_topic
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "mask_topic: ";
    rosidl_generator_traits::value_to_yaml(msg.mask_topic, out);
    out << "\n";
  }

  // member: debug_json
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "debug_json: ";
    rosidl_generator_traits::value_to_yaml(msg.debug_json, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SegmentTarget_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace soarm100_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use soarm100_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const soarm100_interfaces::srv::SegmentTarget_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  soarm100_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use soarm100_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const soarm100_interfaces::srv::SegmentTarget_Response & msg)
{
  return soarm100_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<soarm100_interfaces::srv::SegmentTarget_Response>()
{
  return "soarm100_interfaces::srv::SegmentTarget_Response";
}

template<>
inline const char * name<soarm100_interfaces::srv::SegmentTarget_Response>()
{
  return "soarm100_interfaces/srv/SegmentTarget_Response";
}

template<>
struct has_fixed_size<soarm100_interfaces::srv::SegmentTarget_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<soarm100_interfaces::srv::SegmentTarget_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<soarm100_interfaces::srv::SegmentTarget_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<soarm100_interfaces::srv::SegmentTarget>()
{
  return "soarm100_interfaces::srv::SegmentTarget";
}

template<>
inline const char * name<soarm100_interfaces::srv::SegmentTarget>()
{
  return "soarm100_interfaces/srv/SegmentTarget";
}

template<>
struct has_fixed_size<soarm100_interfaces::srv::SegmentTarget>
  : std::integral_constant<
    bool,
    has_fixed_size<soarm100_interfaces::srv::SegmentTarget_Request>::value &&
    has_fixed_size<soarm100_interfaces::srv::SegmentTarget_Response>::value
  >
{
};

template<>
struct has_bounded_size<soarm100_interfaces::srv::SegmentTarget>
  : std::integral_constant<
    bool,
    has_bounded_size<soarm100_interfaces::srv::SegmentTarget_Request>::value &&
    has_bounded_size<soarm100_interfaces::srv::SegmentTarget_Response>::value
  >
{
};

template<>
struct is_service<soarm100_interfaces::srv::SegmentTarget>
  : std::true_type
{
};

template<>
struct is_service_request<soarm100_interfaces::srv::SegmentTarget_Request>
  : std::true_type
{
};

template<>
struct is_service_response<soarm100_interfaces::srv::SegmentTarget_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // SOARM100_INTERFACES__SRV__DETAIL__SEGMENT_TARGET__TRAITS_HPP_
