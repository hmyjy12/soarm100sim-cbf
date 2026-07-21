// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from soarm100_interfaces:action/ExecuteGrasp.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_GRASP__BUILDER_HPP_
#define SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_GRASP__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "soarm100_interfaces/action/detail/execute_grasp__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_ExecuteGrasp_Goal_approximate_target_pose
{
public:
  explicit Init_ExecuteGrasp_Goal_approximate_target_pose(::soarm100_interfaces::action::ExecuteGrasp_Goal & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::action::ExecuteGrasp_Goal approximate_target_pose(::soarm100_interfaces::action::ExecuteGrasp_Goal::_approximate_target_pose_type arg)
  {
    msg_.approximate_target_pose = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_Goal msg_;
};

class Init_ExecuteGrasp_Goal_enable_avoidance
{
public:
  explicit Init_ExecuteGrasp_Goal_enable_avoidance(::soarm100_interfaces::action::ExecuteGrasp_Goal & msg)
  : msg_(msg)
  {}
  Init_ExecuteGrasp_Goal_approximate_target_pose enable_avoidance(::soarm100_interfaces::action::ExecuteGrasp_Goal::_enable_avoidance_type arg)
  {
    msg_.enable_avoidance = std::move(arg);
    return Init_ExecuteGrasp_Goal_approximate_target_pose(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_Goal msg_;
};

class Init_ExecuteGrasp_Goal_target_prompt
{
public:
  Init_ExecuteGrasp_Goal_target_prompt()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteGrasp_Goal_enable_avoidance target_prompt(::soarm100_interfaces::action::ExecuteGrasp_Goal::_target_prompt_type arg)
  {
    msg_.target_prompt = std::move(arg);
    return Init_ExecuteGrasp_Goal_enable_avoidance(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::ExecuteGrasp_Goal>()
{
  return soarm100_interfaces::action::builder::Init_ExecuteGrasp_Goal_target_prompt();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_ExecuteGrasp_Result_attempts
{
public:
  explicit Init_ExecuteGrasp_Result_attempts(::soarm100_interfaces::action::ExecuteGrasp_Result & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::action::ExecuteGrasp_Result attempts(::soarm100_interfaces::action::ExecuteGrasp_Result::_attempts_type arg)
  {
    msg_.attempts = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_Result msg_;
};

class Init_ExecuteGrasp_Result_lift_height
{
public:
  explicit Init_ExecuteGrasp_Result_lift_height(::soarm100_interfaces::action::ExecuteGrasp_Result & msg)
  : msg_(msg)
  {}
  Init_ExecuteGrasp_Result_attempts lift_height(::soarm100_interfaces::action::ExecuteGrasp_Result::_lift_height_type arg)
  {
    msg_.lift_height = std::move(arg);
    return Init_ExecuteGrasp_Result_attempts(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_Result msg_;
};

class Init_ExecuteGrasp_Result_final_grasp_pose
{
public:
  explicit Init_ExecuteGrasp_Result_final_grasp_pose(::soarm100_interfaces::action::ExecuteGrasp_Result & msg)
  : msg_(msg)
  {}
  Init_ExecuteGrasp_Result_lift_height final_grasp_pose(::soarm100_interfaces::action::ExecuteGrasp_Result::_final_grasp_pose_type arg)
  {
    msg_.final_grasp_pose = std::move(arg);
    return Init_ExecuteGrasp_Result_lift_height(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_Result msg_;
};

class Init_ExecuteGrasp_Result_reason
{
public:
  explicit Init_ExecuteGrasp_Result_reason(::soarm100_interfaces::action::ExecuteGrasp_Result & msg)
  : msg_(msg)
  {}
  Init_ExecuteGrasp_Result_final_grasp_pose reason(::soarm100_interfaces::action::ExecuteGrasp_Result::_reason_type arg)
  {
    msg_.reason = std::move(arg);
    return Init_ExecuteGrasp_Result_final_grasp_pose(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_Result msg_;
};

class Init_ExecuteGrasp_Result_success
{
public:
  Init_ExecuteGrasp_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteGrasp_Result_reason success(::soarm100_interfaces::action::ExecuteGrasp_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_ExecuteGrasp_Result_reason(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::ExecuteGrasp_Result>()
{
  return soarm100_interfaces::action::builder::Init_ExecuteGrasp_Result_success();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_ExecuteGrasp_Feedback_reason
{
public:
  explicit Init_ExecuteGrasp_Feedback_reason(::soarm100_interfaces::action::ExecuteGrasp_Feedback & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::action::ExecuteGrasp_Feedback reason(::soarm100_interfaces::action::ExecuteGrasp_Feedback::_reason_type arg)
  {
    msg_.reason = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_Feedback msg_;
};

class Init_ExecuteGrasp_Feedback_replan_running
{
public:
  explicit Init_ExecuteGrasp_Feedback_replan_running(::soarm100_interfaces::action::ExecuteGrasp_Feedback & msg)
  : msg_(msg)
  {}
  Init_ExecuteGrasp_Feedback_reason replan_running(::soarm100_interfaces::action::ExecuteGrasp_Feedback::_replan_running_type arg)
  {
    msg_.replan_running = std::move(arg);
    return Init_ExecuteGrasp_Feedback_reason(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_Feedback msg_;
};

class Init_ExecuteGrasp_Feedback_tracking_valid
{
public:
  explicit Init_ExecuteGrasp_Feedback_tracking_valid(::soarm100_interfaces::action::ExecuteGrasp_Feedback & msg)
  : msg_(msg)
  {}
  Init_ExecuteGrasp_Feedback_replan_running tracking_valid(::soarm100_interfaces::action::ExecuteGrasp_Feedback::_tracking_valid_type arg)
  {
    msg_.tracking_valid = std::move(arg);
    return Init_ExecuteGrasp_Feedback_replan_running(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_Feedback msg_;
};

class Init_ExecuteGrasp_Feedback_cbf_active
{
public:
  explicit Init_ExecuteGrasp_Feedback_cbf_active(::soarm100_interfaces::action::ExecuteGrasp_Feedback & msg)
  : msg_(msg)
  {}
  Init_ExecuteGrasp_Feedback_tracking_valid cbf_active(::soarm100_interfaces::action::ExecuteGrasp_Feedback::_cbf_active_type arg)
  {
    msg_.cbf_active = std::move(arg);
    return Init_ExecuteGrasp_Feedback_tracking_valid(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_Feedback msg_;
};

class Init_ExecuteGrasp_Feedback_sdf_min_dist
{
public:
  explicit Init_ExecuteGrasp_Feedback_sdf_min_dist(::soarm100_interfaces::action::ExecuteGrasp_Feedback & msg)
  : msg_(msg)
  {}
  Init_ExecuteGrasp_Feedback_cbf_active sdf_min_dist(::soarm100_interfaces::action::ExecuteGrasp_Feedback::_sdf_min_dist_type arg)
  {
    msg_.sdf_min_dist = std::move(arg);
    return Init_ExecuteGrasp_Feedback_cbf_active(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_Feedback msg_;
};

class Init_ExecuteGrasp_Feedback_tcp_ori_err
{
public:
  explicit Init_ExecuteGrasp_Feedback_tcp_ori_err(::soarm100_interfaces::action::ExecuteGrasp_Feedback & msg)
  : msg_(msg)
  {}
  Init_ExecuteGrasp_Feedback_sdf_min_dist tcp_ori_err(::soarm100_interfaces::action::ExecuteGrasp_Feedback::_tcp_ori_err_type arg)
  {
    msg_.tcp_ori_err = std::move(arg);
    return Init_ExecuteGrasp_Feedback_sdf_min_dist(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_Feedback msg_;
};

class Init_ExecuteGrasp_Feedback_tcp_pos_err
{
public:
  explicit Init_ExecuteGrasp_Feedback_tcp_pos_err(::soarm100_interfaces::action::ExecuteGrasp_Feedback & msg)
  : msg_(msg)
  {}
  Init_ExecuteGrasp_Feedback_tcp_ori_err tcp_pos_err(::soarm100_interfaces::action::ExecuteGrasp_Feedback::_tcp_pos_err_type arg)
  {
    msg_.tcp_pos_err = std::move(arg);
    return Init_ExecuteGrasp_Feedback_tcp_ori_err(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_Feedback msg_;
};

class Init_ExecuteGrasp_Feedback_grasp_score
{
public:
  explicit Init_ExecuteGrasp_Feedback_grasp_score(::soarm100_interfaces::action::ExecuteGrasp_Feedback & msg)
  : msg_(msg)
  {}
  Init_ExecuteGrasp_Feedback_tcp_pos_err grasp_score(::soarm100_interfaces::action::ExecuteGrasp_Feedback::_grasp_score_type arg)
  {
    msg_.grasp_score = std::move(arg);
    return Init_ExecuteGrasp_Feedback_tcp_pos_err(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_Feedback msg_;
};

class Init_ExecuteGrasp_Feedback_target_visible_score
{
public:
  explicit Init_ExecuteGrasp_Feedback_target_visible_score(::soarm100_interfaces::action::ExecuteGrasp_Feedback & msg)
  : msg_(msg)
  {}
  Init_ExecuteGrasp_Feedback_grasp_score target_visible_score(::soarm100_interfaces::action::ExecuteGrasp_Feedback::_target_visible_score_type arg)
  {
    msg_.target_visible_score = std::move(arg);
    return Init_ExecuteGrasp_Feedback_grasp_score(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_Feedback msg_;
};

class Init_ExecuteGrasp_Feedback_stage
{
public:
  Init_ExecuteGrasp_Feedback_stage()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteGrasp_Feedback_target_visible_score stage(::soarm100_interfaces::action::ExecuteGrasp_Feedback::_stage_type arg)
  {
    msg_.stage = std::move(arg);
    return Init_ExecuteGrasp_Feedback_target_visible_score(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::ExecuteGrasp_Feedback>()
{
  return soarm100_interfaces::action::builder::Init_ExecuteGrasp_Feedback_stage();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_ExecuteGrasp_SendGoal_Request_goal
{
public:
  explicit Init_ExecuteGrasp_SendGoal_Request_goal(::soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request goal(::soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request msg_;
};

class Init_ExecuteGrasp_SendGoal_Request_goal_id
{
public:
  Init_ExecuteGrasp_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteGrasp_SendGoal_Request_goal goal_id(::soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_ExecuteGrasp_SendGoal_Request_goal(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request>()
{
  return soarm100_interfaces::action::builder::Init_ExecuteGrasp_SendGoal_Request_goal_id();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_ExecuteGrasp_SendGoal_Response_stamp
{
public:
  explicit Init_ExecuteGrasp_SendGoal_Response_stamp(::soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response stamp(::soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response msg_;
};

class Init_ExecuteGrasp_SendGoal_Response_accepted
{
public:
  Init_ExecuteGrasp_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteGrasp_SendGoal_Response_stamp accepted(::soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_ExecuteGrasp_SendGoal_Response_stamp(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response>()
{
  return soarm100_interfaces::action::builder::Init_ExecuteGrasp_SendGoal_Response_accepted();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_ExecuteGrasp_GetResult_Request_goal_id
{
public:
  Init_ExecuteGrasp_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::soarm100_interfaces::action::ExecuteGrasp_GetResult_Request goal_id(::soarm100_interfaces::action::ExecuteGrasp_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::ExecuteGrasp_GetResult_Request>()
{
  return soarm100_interfaces::action::builder::Init_ExecuteGrasp_GetResult_Request_goal_id();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_ExecuteGrasp_GetResult_Response_result
{
public:
  explicit Init_ExecuteGrasp_GetResult_Response_result(::soarm100_interfaces::action::ExecuteGrasp_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::action::ExecuteGrasp_GetResult_Response result(::soarm100_interfaces::action::ExecuteGrasp_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_GetResult_Response msg_;
};

class Init_ExecuteGrasp_GetResult_Response_status
{
public:
  Init_ExecuteGrasp_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteGrasp_GetResult_Response_result status(::soarm100_interfaces::action::ExecuteGrasp_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_ExecuteGrasp_GetResult_Response_result(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::ExecuteGrasp_GetResult_Response>()
{
  return soarm100_interfaces::action::builder::Init_ExecuteGrasp_GetResult_Response_status();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_ExecuteGrasp_FeedbackMessage_feedback
{
public:
  explicit Init_ExecuteGrasp_FeedbackMessage_feedback(::soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage feedback(::soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage msg_;
};

class Init_ExecuteGrasp_FeedbackMessage_goal_id
{
public:
  Init_ExecuteGrasp_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ExecuteGrasp_FeedbackMessage_feedback goal_id(::soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_ExecuteGrasp_FeedbackMessage_feedback(msg_);
  }

private:
  ::soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage>()
{
  return soarm100_interfaces::action::builder::Init_ExecuteGrasp_FeedbackMessage_goal_id();
}

}  // namespace soarm100_interfaces

#endif  // SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_GRASP__BUILDER_HPP_
