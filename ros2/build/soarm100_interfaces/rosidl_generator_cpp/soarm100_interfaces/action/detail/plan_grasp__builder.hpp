// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from soarm100_interfaces:action/PlanGrasp.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__ACTION__DETAIL__PLAN_GRASP__BUILDER_HPP_
#define SOARM100_INTERFACES__ACTION__DETAIL__PLAN_GRASP__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "soarm100_interfaces/action/detail/plan_grasp__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_PlanGrasp_Goal_top_k
{
public:
  explicit Init_PlanGrasp_Goal_top_k(::soarm100_interfaces::action::PlanGrasp_Goal & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::action::PlanGrasp_Goal top_k(::soarm100_interfaces::action::PlanGrasp_Goal::_top_k_type arg)
  {
    msg_.top_k = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_Goal msg_;
};

class Init_PlanGrasp_Goal_target_cloud
{
public:
  explicit Init_PlanGrasp_Goal_target_cloud(::soarm100_interfaces::action::PlanGrasp_Goal & msg)
  : msg_(msg)
  {}
  Init_PlanGrasp_Goal_top_k target_cloud(::soarm100_interfaces::action::PlanGrasp_Goal::_target_cloud_type arg)
  {
    msg_.target_cloud = std::move(arg);
    return Init_PlanGrasp_Goal_top_k(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_Goal msg_;
};

class Init_PlanGrasp_Goal_approximate_target_pose
{
public:
  explicit Init_PlanGrasp_Goal_approximate_target_pose(::soarm100_interfaces::action::PlanGrasp_Goal & msg)
  : msg_(msg)
  {}
  Init_PlanGrasp_Goal_target_cloud approximate_target_pose(::soarm100_interfaces::action::PlanGrasp_Goal::_approximate_target_pose_type arg)
  {
    msg_.approximate_target_pose = std::move(arg);
    return Init_PlanGrasp_Goal_target_cloud(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_Goal msg_;
};

class Init_PlanGrasp_Goal_target_prompt
{
public:
  Init_PlanGrasp_Goal_target_prompt()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlanGrasp_Goal_approximate_target_pose target_prompt(::soarm100_interfaces::action::PlanGrasp_Goal::_target_prompt_type arg)
  {
    msg_.target_prompt = std::move(arg);
    return Init_PlanGrasp_Goal_approximate_target_pose(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::PlanGrasp_Goal>()
{
  return soarm100_interfaces::action::builder::Init_PlanGrasp_Goal_target_prompt();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_PlanGrasp_Result_candidate_count
{
public:
  explicit Init_PlanGrasp_Result_candidate_count(::soarm100_interfaces::action::PlanGrasp_Result & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::action::PlanGrasp_Result candidate_count(::soarm100_interfaces::action::PlanGrasp_Result::_candidate_count_type arg)
  {
    msg_.candidate_count = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_Result msg_;
};

class Init_PlanGrasp_Result_gripper_width
{
public:
  explicit Init_PlanGrasp_Result_gripper_width(::soarm100_interfaces::action::PlanGrasp_Result & msg)
  : msg_(msg)
  {}
  Init_PlanGrasp_Result_candidate_count gripper_width(::soarm100_interfaces::action::PlanGrasp_Result::_gripper_width_type arg)
  {
    msg_.gripper_width = std::move(arg);
    return Init_PlanGrasp_Result_candidate_count(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_Result msg_;
};

class Init_PlanGrasp_Result_grasp_score
{
public:
  explicit Init_PlanGrasp_Result_grasp_score(::soarm100_interfaces::action::PlanGrasp_Result & msg)
  : msg_(msg)
  {}
  Init_PlanGrasp_Result_gripper_width grasp_score(::soarm100_interfaces::action::PlanGrasp_Result::_grasp_score_type arg)
  {
    msg_.grasp_score = std::move(arg);
    return Init_PlanGrasp_Result_gripper_width(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_Result msg_;
};

class Init_PlanGrasp_Result_target_center_pose
{
public:
  explicit Init_PlanGrasp_Result_target_center_pose(::soarm100_interfaces::action::PlanGrasp_Result & msg)
  : msg_(msg)
  {}
  Init_PlanGrasp_Result_grasp_score target_center_pose(::soarm100_interfaces::action::PlanGrasp_Result::_target_center_pose_type arg)
  {
    msg_.target_center_pose = std::move(arg);
    return Init_PlanGrasp_Result_grasp_score(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_Result msg_;
};

class Init_PlanGrasp_Result_selected_pregrasp_pose
{
public:
  explicit Init_PlanGrasp_Result_selected_pregrasp_pose(::soarm100_interfaces::action::PlanGrasp_Result & msg)
  : msg_(msg)
  {}
  Init_PlanGrasp_Result_target_center_pose selected_pregrasp_pose(::soarm100_interfaces::action::PlanGrasp_Result::_selected_pregrasp_pose_type arg)
  {
    msg_.selected_pregrasp_pose = std::move(arg);
    return Init_PlanGrasp_Result_target_center_pose(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_Result msg_;
};

class Init_PlanGrasp_Result_selected_grasp_pose
{
public:
  explicit Init_PlanGrasp_Result_selected_grasp_pose(::soarm100_interfaces::action::PlanGrasp_Result & msg)
  : msg_(msg)
  {}
  Init_PlanGrasp_Result_selected_pregrasp_pose selected_grasp_pose(::soarm100_interfaces::action::PlanGrasp_Result::_selected_grasp_pose_type arg)
  {
    msg_.selected_grasp_pose = std::move(arg);
    return Init_PlanGrasp_Result_selected_pregrasp_pose(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_Result msg_;
};

class Init_PlanGrasp_Result_reason
{
public:
  explicit Init_PlanGrasp_Result_reason(::soarm100_interfaces::action::PlanGrasp_Result & msg)
  : msg_(msg)
  {}
  Init_PlanGrasp_Result_selected_grasp_pose reason(::soarm100_interfaces::action::PlanGrasp_Result::_reason_type arg)
  {
    msg_.reason = std::move(arg);
    return Init_PlanGrasp_Result_selected_grasp_pose(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_Result msg_;
};

class Init_PlanGrasp_Result_success
{
public:
  Init_PlanGrasp_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlanGrasp_Result_reason success(::soarm100_interfaces::action::PlanGrasp_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_PlanGrasp_Result_reason(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::PlanGrasp_Result>()
{
  return soarm100_interfaces::action::builder::Init_PlanGrasp_Result_success();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_PlanGrasp_Feedback_reason
{
public:
  explicit Init_PlanGrasp_Feedback_reason(::soarm100_interfaces::action::PlanGrasp_Feedback & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::action::PlanGrasp_Feedback reason(::soarm100_interfaces::action::PlanGrasp_Feedback::_reason_type arg)
  {
    msg_.reason = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_Feedback msg_;
};

class Init_PlanGrasp_Feedback_best_score
{
public:
  explicit Init_PlanGrasp_Feedback_best_score(::soarm100_interfaces::action::PlanGrasp_Feedback & msg)
  : msg_(msg)
  {}
  Init_PlanGrasp_Feedback_reason best_score(::soarm100_interfaces::action::PlanGrasp_Feedback::_best_score_type arg)
  {
    msg_.best_score = std::move(arg);
    return Init_PlanGrasp_Feedback_reason(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_Feedback msg_;
};

class Init_PlanGrasp_Feedback_candidate_count
{
public:
  explicit Init_PlanGrasp_Feedback_candidate_count(::soarm100_interfaces::action::PlanGrasp_Feedback & msg)
  : msg_(msg)
  {}
  Init_PlanGrasp_Feedback_best_score candidate_count(::soarm100_interfaces::action::PlanGrasp_Feedback::_candidate_count_type arg)
  {
    msg_.candidate_count = std::move(arg);
    return Init_PlanGrasp_Feedback_best_score(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_Feedback msg_;
};

class Init_PlanGrasp_Feedback_stage
{
public:
  Init_PlanGrasp_Feedback_stage()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlanGrasp_Feedback_candidate_count stage(::soarm100_interfaces::action::PlanGrasp_Feedback::_stage_type arg)
  {
    msg_.stage = std::move(arg);
    return Init_PlanGrasp_Feedback_candidate_count(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::PlanGrasp_Feedback>()
{
  return soarm100_interfaces::action::builder::Init_PlanGrasp_Feedback_stage();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_PlanGrasp_SendGoal_Request_goal
{
public:
  explicit Init_PlanGrasp_SendGoal_Request_goal(::soarm100_interfaces::action::PlanGrasp_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::action::PlanGrasp_SendGoal_Request goal(::soarm100_interfaces::action::PlanGrasp_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_SendGoal_Request msg_;
};

class Init_PlanGrasp_SendGoal_Request_goal_id
{
public:
  Init_PlanGrasp_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlanGrasp_SendGoal_Request_goal goal_id(::soarm100_interfaces::action::PlanGrasp_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_PlanGrasp_SendGoal_Request_goal(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::PlanGrasp_SendGoal_Request>()
{
  return soarm100_interfaces::action::builder::Init_PlanGrasp_SendGoal_Request_goal_id();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_PlanGrasp_SendGoal_Response_stamp
{
public:
  explicit Init_PlanGrasp_SendGoal_Response_stamp(::soarm100_interfaces::action::PlanGrasp_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::action::PlanGrasp_SendGoal_Response stamp(::soarm100_interfaces::action::PlanGrasp_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_SendGoal_Response msg_;
};

class Init_PlanGrasp_SendGoal_Response_accepted
{
public:
  Init_PlanGrasp_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlanGrasp_SendGoal_Response_stamp accepted(::soarm100_interfaces::action::PlanGrasp_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_PlanGrasp_SendGoal_Response_stamp(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::PlanGrasp_SendGoal_Response>()
{
  return soarm100_interfaces::action::builder::Init_PlanGrasp_SendGoal_Response_accepted();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_PlanGrasp_GetResult_Request_goal_id
{
public:
  Init_PlanGrasp_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::soarm100_interfaces::action::PlanGrasp_GetResult_Request goal_id(::soarm100_interfaces::action::PlanGrasp_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::PlanGrasp_GetResult_Request>()
{
  return soarm100_interfaces::action::builder::Init_PlanGrasp_GetResult_Request_goal_id();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_PlanGrasp_GetResult_Response_result
{
public:
  explicit Init_PlanGrasp_GetResult_Response_result(::soarm100_interfaces::action::PlanGrasp_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::action::PlanGrasp_GetResult_Response result(::soarm100_interfaces::action::PlanGrasp_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_GetResult_Response msg_;
};

class Init_PlanGrasp_GetResult_Response_status
{
public:
  Init_PlanGrasp_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlanGrasp_GetResult_Response_result status(::soarm100_interfaces::action::PlanGrasp_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_PlanGrasp_GetResult_Response_result(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::PlanGrasp_GetResult_Response>()
{
  return soarm100_interfaces::action::builder::Init_PlanGrasp_GetResult_Response_status();
}

}  // namespace soarm100_interfaces


namespace soarm100_interfaces
{

namespace action
{

namespace builder
{

class Init_PlanGrasp_FeedbackMessage_feedback
{
public:
  explicit Init_PlanGrasp_FeedbackMessage_feedback(::soarm100_interfaces::action::PlanGrasp_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::soarm100_interfaces::action::PlanGrasp_FeedbackMessage feedback(::soarm100_interfaces::action::PlanGrasp_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_FeedbackMessage msg_;
};

class Init_PlanGrasp_FeedbackMessage_goal_id
{
public:
  Init_PlanGrasp_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlanGrasp_FeedbackMessage_feedback goal_id(::soarm100_interfaces::action::PlanGrasp_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_PlanGrasp_FeedbackMessage_feedback(msg_);
  }

private:
  ::soarm100_interfaces::action::PlanGrasp_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::soarm100_interfaces::action::PlanGrasp_FeedbackMessage>()
{
  return soarm100_interfaces::action::builder::Init_PlanGrasp_FeedbackMessage_goal_id();
}

}  // namespace soarm100_interfaces

#endif  // SOARM100_INTERFACES__ACTION__DETAIL__PLAN_GRASP__BUILDER_HPP_
