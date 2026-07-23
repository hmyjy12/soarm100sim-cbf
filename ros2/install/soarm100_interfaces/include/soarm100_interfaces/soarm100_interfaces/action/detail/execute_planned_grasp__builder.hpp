// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from soarm100_interfaces:action/ExecutePlannedGrasp.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_PLANNED_GRASP__BUILDER_HPP_
#define SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_PLANNED_GRASP__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "soarm100_interfaces/action/detail/execute_planned_grasp__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_ExecutePlannedGrasp_Goal_traj_log
{
public:
  explicit Init_ExecutePlannedGrasp_Goal_traj_log(::soarm100_interfaces::action::ExecutePlannedGrasp_Goal & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::action::ExecutePlannedGrasp_Goal traj_log(::soarm100_interfaces::action::ExecutePlannedGrasp_Goal::_traj_log_type arg)
  {
    msg_.traj_log = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecutePlannedGrasp_Goal msg_;
};

class Init_ExecutePlannedGrasp_Goal_target_pos
{
public:
  explicit Init_ExecutePlannedGrasp_Goal_target_pos(::soarm100_interfaces::action::ExecutePlannedGrasp_Goal & msg)
  : msg_(msg)
  {}
  Init_ExecutePlannedGrasp_Goal_traj_log target_pos(::soarm100_interfaces::action::ExecutePlannedGrasp_Goal::_target_pos_type arg)
  {
    msg_.target_pos = std::move(arg);
    return Init_ExecutePlannedGrasp_Goal_traj_log(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecutePlannedGrasp_Goal msg_;
};

class Init_ExecutePlannedGrasp_Goal_target_object
{
public:
  explicit Init_ExecutePlannedGrasp_Goal_target_object(::soarm100_interfaces::action::ExecutePlannedGrasp_Goal & msg)
  : msg_(msg)
  {}
  Init_ExecutePlannedGrasp_Goal_target_pos target_object(::soarm100_interfaces::action::ExecutePlannedGrasp_Goal::_target_object_type arg)
  {
    msg_.target_object = std::move(arg);
    return Init_ExecutePlannedGrasp_Goal_target_pos(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecutePlannedGrasp_Goal msg_;
};

class Init_ExecutePlannedGrasp_Goal_enable_avoidance
{
public:
  explicit Init_ExecutePlannedGrasp_Goal_enable_avoidance(::soarm100_interfaces::action::ExecutePlannedGrasp_Goal & msg)
  : msg_(msg)
  {}
  Init_ExecutePlannedGrasp_Goal_target_object enable_avoidance(::soarm100_interfaces::action::ExecutePlannedGrasp_Goal::_enable_avoidance_type arg)
  {
    msg_.enable_avoidance = std::move(arg);
    return Init_ExecutePlannedGrasp_Goal_target_object(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecutePlannedGrasp_Goal msg_;
};

class Init_ExecutePlannedGrasp_Goal_gripper_width
{
public:
  explicit Init_ExecutePlannedGrasp_Goal_gripper_width(::soarm100_interfaces::action::ExecutePlannedGrasp_Goal & msg)
  : msg_(msg)
  {}
  Init_ExecutePlannedGrasp_Goal_enable_avoidance gripper_width(::soarm100_interfaces::action::ExecutePlannedGrasp_Goal::_gripper_width_type arg)
  {
    msg_.gripper_width = std::move(arg);
    return Init_ExecutePlannedGrasp_Goal_enable_avoidance(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecutePlannedGrasp_Goal msg_;
};

class Init_ExecutePlannedGrasp_Goal_grasp_pose
{
public:
  explicit Init_ExecutePlannedGrasp_Goal_grasp_pose(::soarm100_interfaces::action::ExecutePlannedGrasp_Goal & msg)
  : msg_(msg)
  {}
  Init_ExecutePlannedGrasp_Goal_gripper_width grasp_pose(::soarm100_interfaces::action::ExecutePlannedGrasp_Goal::_grasp_pose_type arg)
  {
    msg_.grasp_pose = std::move(arg);
    return Init_ExecutePlannedGrasp_Goal_gripper_width(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecutePlannedGrasp_Goal msg_;
};

class Init_ExecutePlannedGrasp_Goal_pregrasp_pose
{
public:
  Init_ExecutePlannedGrasp_Goal_pregrasp_pose()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecutePlannedGrasp_Goal_grasp_pose pregrasp_pose(::soarm100_interfaces::action::ExecutePlannedGrasp_Goal::_pregrasp_pose_type arg)
  {
    msg_.pregrasp_pose = std::move(arg);
    return Init_ExecutePlannedGrasp_Goal_grasp_pose(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecutePlannedGrasp_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::ExecutePlannedGrasp_Goal>()
{
  return soarm100_interfaces::action::builder::Init_ExecutePlannedGrasp_Goal_pregrasp_pose();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_ExecutePlannedGrasp_Result_return_code
{
public:
  explicit Init_ExecutePlannedGrasp_Result_return_code(::soarm100_interfaces::action::ExecutePlannedGrasp_Result & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::action::ExecutePlannedGrasp_Result return_code(::soarm100_interfaces::action::ExecutePlannedGrasp_Result::_return_code_type arg)
  {
    msg_.return_code = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecutePlannedGrasp_Result msg_;
};

class Init_ExecutePlannedGrasp_Result_lift_height
{
public:
  explicit Init_ExecutePlannedGrasp_Result_lift_height(::soarm100_interfaces::action::ExecutePlannedGrasp_Result & msg)
  : msg_(msg)
  {}
  Init_ExecutePlannedGrasp_Result_return_code lift_height(::soarm100_interfaces::action::ExecutePlannedGrasp_Result::_lift_height_type arg)
  {
    msg_.lift_height = std::move(arg);
    return Init_ExecutePlannedGrasp_Result_return_code(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecutePlannedGrasp_Result msg_;
};

class Init_ExecutePlannedGrasp_Result_reason
{
public:
  explicit Init_ExecutePlannedGrasp_Result_reason(::soarm100_interfaces::action::ExecutePlannedGrasp_Result & msg)
  : msg_(msg)
  {}
  Init_ExecutePlannedGrasp_Result_lift_height reason(::soarm100_interfaces::action::ExecutePlannedGrasp_Result::_reason_type arg)
  {
    msg_.reason = std::move(arg);
    return Init_ExecutePlannedGrasp_Result_lift_height(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecutePlannedGrasp_Result msg_;
};

class Init_ExecutePlannedGrasp_Result_success
{
public:
  Init_ExecutePlannedGrasp_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecutePlannedGrasp_Result_reason success(::soarm100_interfaces::action::ExecutePlannedGrasp_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_ExecutePlannedGrasp_Result_reason(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecutePlannedGrasp_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::ExecutePlannedGrasp_Result>()
{
  return soarm100_interfaces::action::builder::Init_ExecutePlannedGrasp_Result_success();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_ExecutePlannedGrasp_Feedback_lift_height
{
public:
  explicit Init_ExecutePlannedGrasp_Feedback_lift_height(::soarm100_interfaces::action::ExecutePlannedGrasp_Feedback & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::action::ExecutePlannedGrasp_Feedback lift_height(::soarm100_interfaces::action::ExecutePlannedGrasp_Feedback::_lift_height_type arg)
  {
    msg_.lift_height = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecutePlannedGrasp_Feedback msg_;
};

class Init_ExecutePlannedGrasp_Feedback_reason
{
public:
  explicit Init_ExecutePlannedGrasp_Feedback_reason(::soarm100_interfaces::action::ExecutePlannedGrasp_Feedback & msg)
  : msg_(msg)
  {}
  Init_ExecutePlannedGrasp_Feedback_lift_height reason(::soarm100_interfaces::action::ExecutePlannedGrasp_Feedback::_reason_type arg)
  {
    msg_.reason = std::move(arg);
    return Init_ExecutePlannedGrasp_Feedback_lift_height(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecutePlannedGrasp_Feedback msg_;
};

class Init_ExecutePlannedGrasp_Feedback_stage
{
public:
  Init_ExecutePlannedGrasp_Feedback_stage()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecutePlannedGrasp_Feedback_reason stage(::soarm100_interfaces::action::ExecutePlannedGrasp_Feedback::_stage_type arg)
  {
    msg_.stage = std::move(arg);
    return Init_ExecutePlannedGrasp_Feedback_reason(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecutePlannedGrasp_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::ExecutePlannedGrasp_Feedback>()
{
  return soarm100_interfaces::action::builder::Init_ExecutePlannedGrasp_Feedback_stage();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_ExecutePlannedGrasp_SendGoal_Request_goal
{
public:
  explicit Init_ExecutePlannedGrasp_SendGoal_Request_goal(::soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Request goal(::soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Request msg_;
};

class Init_ExecutePlannedGrasp_SendGoal_Request_goal_id
{
public:
  Init_ExecutePlannedGrasp_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecutePlannedGrasp_SendGoal_Request_goal goal_id(::soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_ExecutePlannedGrasp_SendGoal_Request_goal(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Request>()
{
  return soarm100_interfaces::action::builder::Init_ExecutePlannedGrasp_SendGoal_Request_goal_id();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_ExecutePlannedGrasp_SendGoal_Response_stamp
{
public:
  explicit Init_ExecutePlannedGrasp_SendGoal_Response_stamp(::soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Response stamp(::soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Response msg_;
};

class Init_ExecutePlannedGrasp_SendGoal_Response_accepted
{
public:
  Init_ExecutePlannedGrasp_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecutePlannedGrasp_SendGoal_Response_stamp accepted(::soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_ExecutePlannedGrasp_SendGoal_Response_stamp(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Response>()
{
  return soarm100_interfaces::action::builder::Init_ExecutePlannedGrasp_SendGoal_Response_accepted();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_ExecutePlannedGrasp_GetResult_Request_goal_id
{
public:
  Init_ExecutePlannedGrasp_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Request goal_id(::soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Request>()
{
  return soarm100_interfaces::action::builder::Init_ExecutePlannedGrasp_GetResult_Request_goal_id();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_ExecutePlannedGrasp_GetResult_Response_result
{
public:
  explicit Init_ExecutePlannedGrasp_GetResult_Response_result(::soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Response result(::soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Response msg_;
};

class Init_ExecutePlannedGrasp_GetResult_Response_status
{
public:
  Init_ExecutePlannedGrasp_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecutePlannedGrasp_GetResult_Response_result status(::soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_ExecutePlannedGrasp_GetResult_Response_result(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Response>()
{
  return soarm100_interfaces::action::builder::Init_ExecutePlannedGrasp_GetResult_Response_status();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_ExecutePlannedGrasp_FeedbackMessage_feedback
{
public:
  explicit Init_ExecutePlannedGrasp_FeedbackMessage_feedback(::soarm100_interfaces::action::ExecutePlannedGrasp_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::action::ExecutePlannedGrasp_FeedbackMessage feedback(::soarm100_interfaces::action::ExecutePlannedGrasp_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecutePlannedGrasp_FeedbackMessage msg_;
};

class Init_ExecutePlannedGrasp_FeedbackMessage_goal_id
{
public:
  Init_ExecutePlannedGrasp_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecutePlannedGrasp_FeedbackMessage_feedback goal_id(::soarm100_interfaces::action::ExecutePlannedGrasp_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_ExecutePlannedGrasp_FeedbackMessage_feedback(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecutePlannedGrasp_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::ExecutePlannedGrasp_FeedbackMessage>()
{
  return soarm100_interfaces::action::builder::Init_ExecutePlannedGrasp_FeedbackMessage_goal_id();
}

}  // namespace soarm100_interfaces

#endif  // SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_PLANNED_GRASP__BUILDER_HPP_
