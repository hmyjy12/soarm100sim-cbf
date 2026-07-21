// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from soarm100_interfaces:action/ExecuteGrasp.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_GRASP__STRUCT_HPP_
#define SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_GRASP__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'approximate_target_pose'
#include "geometry_msgs/msg/detail/pose_stamped__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_Goal __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_Goal __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteGrasp_Goal_
{
  using Type = ExecuteGrasp_Goal_<ContainerAllocator>;

  explicit ExecuteGrasp_Goal_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : approximate_target_pose(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->target_prompt = "";
      this->enable_avoidance = false;
    }
  }

  explicit ExecuteGrasp_Goal_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : target_prompt(_alloc),
    approximate_target_pose(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->target_prompt = "";
      this->enable_avoidance = false;
    }
  }

  // field types and members
  using _target_prompt_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _target_prompt_type target_prompt;
  using _enable_avoidance_type =
    bool;
  _enable_avoidance_type enable_avoidance;
  using _approximate_target_pose_type =
    geometry_msgs::msg::PoseStamped_<ContainerAllocator>;
  _approximate_target_pose_type approximate_target_pose;

  // setters for named parameter idiom
  Type & set__target_prompt(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->target_prompt = _arg;
    return *this;
  }
  Type & set__enable_avoidance(
    const bool & _arg)
  {
    this->enable_avoidance = _arg;
    return *this;
  }
  Type & set__approximate_target_pose(
    const geometry_msgs::msg::PoseStamped_<ContainerAllocator> & _arg)
  {
    this->approximate_target_pose = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    soarm100_interfaces::action::ExecuteGrasp_Goal_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::action::ExecuteGrasp_Goal_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_Goal_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_Goal_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecuteGrasp_Goal_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecuteGrasp_Goal_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecuteGrasp_Goal_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecuteGrasp_Goal_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecuteGrasp_Goal_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecuteGrasp_Goal_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_Goal
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_Goal_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_Goal
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_Goal_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteGrasp_Goal_ & other) const
  {
    if (this->target_prompt != other.target_prompt) {
      return false;
    }
    if (this->enable_avoidance != other.enable_avoidance) {
      return false;
    }
    if (this->approximate_target_pose != other.approximate_target_pose) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteGrasp_Goal_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteGrasp_Goal_

// alias to use template instance with default allocator
using ExecuteGrasp_Goal =
  soarm100_interfaces::action::ExecuteGrasp_Goal_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace soarm100_interfaces


// Include directives for member types
// Member 'final_grasp_pose'
// already included above
// #include "geometry_msgs/msg/detail/pose_stamped__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_Result __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_Result __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteGrasp_Result_
{
  using Type = ExecuteGrasp_Result_<ContainerAllocator>;

  explicit ExecuteGrasp_Result_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : final_grasp_pose(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->reason = "";
      this->lift_height = 0.0f;
      this->attempts = 0;
    }
  }

  explicit ExecuteGrasp_Result_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : reason(_alloc),
    final_grasp_pose(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->reason = "";
      this->lift_height = 0.0f;
      this->attempts = 0;
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _reason_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _reason_type reason;
  using _final_grasp_pose_type =
    geometry_msgs::msg::PoseStamped_<ContainerAllocator>;
  _final_grasp_pose_type final_grasp_pose;
  using _lift_height_type =
    float;
  _lift_height_type lift_height;
  using _attempts_type =
    uint8_t;
  _attempts_type attempts;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__reason(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->reason = _arg;
    return *this;
  }
  Type & set__final_grasp_pose(
    const geometry_msgs::msg::PoseStamped_<ContainerAllocator> & _arg)
  {
    this->final_grasp_pose = _arg;
    return *this;
  }
  Type & set__lift_height(
    const float & _arg)
  {
    this->lift_height = _arg;
    return *this;
  }
  Type & set__attempts(
    const uint8_t & _arg)
  {
    this->attempts = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    soarm100_interfaces::action::ExecuteGrasp_Result_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::action::ExecuteGrasp_Result_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_Result_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_Result_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecuteGrasp_Result_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecuteGrasp_Result_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecuteGrasp_Result_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecuteGrasp_Result_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecuteGrasp_Result_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecuteGrasp_Result_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_Result
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_Result_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_Result
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_Result_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteGrasp_Result_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->reason != other.reason) {
      return false;
    }
    if (this->final_grasp_pose != other.final_grasp_pose) {
      return false;
    }
    if (this->lift_height != other.lift_height) {
      return false;
    }
    if (this->attempts != other.attempts) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteGrasp_Result_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteGrasp_Result_

// alias to use template instance with default allocator
using ExecuteGrasp_Result =
  soarm100_interfaces::action::ExecuteGrasp_Result_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace soarm100_interfaces


#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_Feedback __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_Feedback __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteGrasp_Feedback_
{
  using Type = ExecuteGrasp_Feedback_<ContainerAllocator>;

  explicit ExecuteGrasp_Feedback_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->stage = "";
      this->target_visible_score = 0.0f;
      this->grasp_score = 0.0f;
      this->tcp_pos_err = 0.0f;
      this->tcp_ori_err = 0.0f;
      this->sdf_min_dist = 0.0f;
      this->cbf_active = false;
      this->tracking_valid = false;
      this->replan_running = false;
      this->reason = "";
    }
  }

  explicit ExecuteGrasp_Feedback_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stage(_alloc),
    reason(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->stage = "";
      this->target_visible_score = 0.0f;
      this->grasp_score = 0.0f;
      this->tcp_pos_err = 0.0f;
      this->tcp_ori_err = 0.0f;
      this->sdf_min_dist = 0.0f;
      this->cbf_active = false;
      this->tracking_valid = false;
      this->replan_running = false;
      this->reason = "";
    }
  }

  // field types and members
  using _stage_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _stage_type stage;
  using _target_visible_score_type =
    float;
  _target_visible_score_type target_visible_score;
  using _grasp_score_type =
    float;
  _grasp_score_type grasp_score;
  using _tcp_pos_err_type =
    float;
  _tcp_pos_err_type tcp_pos_err;
  using _tcp_ori_err_type =
    float;
  _tcp_ori_err_type tcp_ori_err;
  using _sdf_min_dist_type =
    float;
  _sdf_min_dist_type sdf_min_dist;
  using _cbf_active_type =
    bool;
  _cbf_active_type cbf_active;
  using _tracking_valid_type =
    bool;
  _tracking_valid_type tracking_valid;
  using _replan_running_type =
    bool;
  _replan_running_type replan_running;
  using _reason_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _reason_type reason;

  // setters for named parameter idiom
  Type & set__stage(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->stage = _arg;
    return *this;
  }
  Type & set__target_visible_score(
    const float & _arg)
  {
    this->target_visible_score = _arg;
    return *this;
  }
  Type & set__grasp_score(
    const float & _arg)
  {
    this->grasp_score = _arg;
    return *this;
  }
  Type & set__tcp_pos_err(
    const float & _arg)
  {
    this->tcp_pos_err = _arg;
    return *this;
  }
  Type & set__tcp_ori_err(
    const float & _arg)
  {
    this->tcp_ori_err = _arg;
    return *this;
  }
  Type & set__sdf_min_dist(
    const float & _arg)
  {
    this->sdf_min_dist = _arg;
    return *this;
  }
  Type & set__cbf_active(
    const bool & _arg)
  {
    this->cbf_active = _arg;
    return *this;
  }
  Type & set__tracking_valid(
    const bool & _arg)
  {
    this->tracking_valid = _arg;
    return *this;
  }
  Type & set__replan_running(
    const bool & _arg)
  {
    this->replan_running = _arg;
    return *this;
  }
  Type & set__reason(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->reason = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    soarm100_interfaces::action::ExecuteGrasp_Feedback_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::action::ExecuteGrasp_Feedback_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_Feedback_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_Feedback_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecuteGrasp_Feedback_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecuteGrasp_Feedback_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecuteGrasp_Feedback_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecuteGrasp_Feedback_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecuteGrasp_Feedback_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecuteGrasp_Feedback_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_Feedback
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_Feedback_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_Feedback
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_Feedback_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteGrasp_Feedback_ & other) const
  {
    if (this->stage != other.stage) {
      return false;
    }
    if (this->target_visible_score != other.target_visible_score) {
      return false;
    }
    if (this->grasp_score != other.grasp_score) {
      return false;
    }
    if (this->tcp_pos_err != other.tcp_pos_err) {
      return false;
    }
    if (this->tcp_ori_err != other.tcp_ori_err) {
      return false;
    }
    if (this->sdf_min_dist != other.sdf_min_dist) {
      return false;
    }
    if (this->cbf_active != other.cbf_active) {
      return false;
    }
    if (this->tracking_valid != other.tracking_valid) {
      return false;
    }
    if (this->replan_running != other.replan_running) {
      return false;
    }
    if (this->reason != other.reason) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteGrasp_Feedback_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteGrasp_Feedback_

// alias to use template instance with default allocator
using ExecuteGrasp_Feedback =
  soarm100_interfaces::action::ExecuteGrasp_Feedback_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace soarm100_interfaces


// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'goal'
#include "soarm100_interfaces/action/detail/execute_grasp__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_SendGoal_Request __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_SendGoal_Request __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteGrasp_SendGoal_Request_
{
  using Type = ExecuteGrasp_SendGoal_Request_<ContainerAllocator>;

  explicit ExecuteGrasp_SendGoal_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    goal(_init)
  {
    (void)_init;
  }

  explicit ExecuteGrasp_SendGoal_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init),
    goal(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;
  using _goal_type =
    soarm100_interfaces::action::ExecuteGrasp_Goal_<ContainerAllocator>;
  _goal_type goal;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__goal(
    const soarm100_interfaces::action::ExecuteGrasp_Goal_<ContainerAllocator> & _arg)
  {
    this->goal = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_SendGoal_Request
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_SendGoal_Request
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteGrasp_SendGoal_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->goal != other.goal) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteGrasp_SendGoal_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteGrasp_SendGoal_Request_

// alias to use template instance with default allocator
using ExecuteGrasp_SendGoal_Request =
  soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace soarm100_interfaces


// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_SendGoal_Response __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_SendGoal_Response __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteGrasp_SendGoal_Response_
{
  using Type = ExecuteGrasp_SendGoal_Response_<ContainerAllocator>;

  explicit ExecuteGrasp_SendGoal_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  explicit ExecuteGrasp_SendGoal_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  // field types and members
  using _accepted_type =
    bool;
  _accepted_type accepted;
  using _stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _stamp_type stamp;

  // setters for named parameter idiom
  Type & set__accepted(
    const bool & _arg)
  {
    this->accepted = _arg;
    return *this;
  }
  Type & set__stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->stamp = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_SendGoal_Response
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_SendGoal_Response
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteGrasp_SendGoal_Response_ & other) const
  {
    if (this->accepted != other.accepted) {
      return false;
    }
    if (this->stamp != other.stamp) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteGrasp_SendGoal_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteGrasp_SendGoal_Response_

// alias to use template instance with default allocator
using ExecuteGrasp_SendGoal_Response =
  soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace soarm100_interfaces

namespace soarm100_interfaces
{

namespace action
{

struct ExecuteGrasp_SendGoal
{
  using Request = soarm100_interfaces::action::ExecuteGrasp_SendGoal_Request;
  using Response = soarm100_interfaces::action::ExecuteGrasp_SendGoal_Response;
};

}  // namespace action

}  // namespace soarm100_interfaces


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_GetResult_Request __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_GetResult_Request __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteGrasp_GetResult_Request_
{
  using Type = ExecuteGrasp_GetResult_Request_<ContainerAllocator>;

  explicit ExecuteGrasp_GetResult_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init)
  {
    (void)_init;
  }

  explicit ExecuteGrasp_GetResult_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    soarm100_interfaces::action::ExecuteGrasp_GetResult_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::action::ExecuteGrasp_GetResult_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_GetResult_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_GetResult_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecuteGrasp_GetResult_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecuteGrasp_GetResult_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecuteGrasp_GetResult_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecuteGrasp_GetResult_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecuteGrasp_GetResult_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecuteGrasp_GetResult_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_GetResult_Request
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_GetResult_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_GetResult_Request
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_GetResult_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteGrasp_GetResult_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteGrasp_GetResult_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteGrasp_GetResult_Request_

// alias to use template instance with default allocator
using ExecuteGrasp_GetResult_Request =
  soarm100_interfaces::action::ExecuteGrasp_GetResult_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace soarm100_interfaces


// Include directives for member types
// Member 'result'
// already included above
// #include "soarm100_interfaces/action/detail/execute_grasp__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_GetResult_Response __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_GetResult_Response __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteGrasp_GetResult_Response_
{
  using Type = ExecuteGrasp_GetResult_Response_<ContainerAllocator>;

  explicit ExecuteGrasp_GetResult_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  explicit ExecuteGrasp_GetResult_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  // field types and members
  using _status_type =
    int8_t;
  _status_type status;
  using _result_type =
    soarm100_interfaces::action::ExecuteGrasp_Result_<ContainerAllocator>;
  _result_type result;

  // setters for named parameter idiom
  Type & set__status(
    const int8_t & _arg)
  {
    this->status = _arg;
    return *this;
  }
  Type & set__result(
    const soarm100_interfaces::action::ExecuteGrasp_Result_<ContainerAllocator> & _arg)
  {
    this->result = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    soarm100_interfaces::action::ExecuteGrasp_GetResult_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::action::ExecuteGrasp_GetResult_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_GetResult_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_GetResult_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecuteGrasp_GetResult_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecuteGrasp_GetResult_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecuteGrasp_GetResult_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecuteGrasp_GetResult_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecuteGrasp_GetResult_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecuteGrasp_GetResult_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_GetResult_Response
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_GetResult_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_GetResult_Response
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_GetResult_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteGrasp_GetResult_Response_ & other) const
  {
    if (this->status != other.status) {
      return false;
    }
    if (this->result != other.result) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteGrasp_GetResult_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteGrasp_GetResult_Response_

// alias to use template instance with default allocator
using ExecuteGrasp_GetResult_Response =
  soarm100_interfaces::action::ExecuteGrasp_GetResult_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace soarm100_interfaces

namespace soarm100_interfaces
{

namespace action
{

struct ExecuteGrasp_GetResult
{
  using Request = soarm100_interfaces::action::ExecuteGrasp_GetResult_Request;
  using Response = soarm100_interfaces::action::ExecuteGrasp_GetResult_Response;
};

}  // namespace action

}  // namespace soarm100_interfaces


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'feedback'
// already included above
// #include "soarm100_interfaces/action/detail/execute_grasp__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_FeedbackMessage __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_FeedbackMessage __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecuteGrasp_FeedbackMessage_
{
  using Type = ExecuteGrasp_FeedbackMessage_<ContainerAllocator>;

  explicit ExecuteGrasp_FeedbackMessage_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    feedback(_init)
  {
    (void)_init;
  }

  explicit ExecuteGrasp_FeedbackMessage_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_alloc, _init),
    feedback(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _goal_id_type =
    unique_identifier_msgs::msg::UUID_<ContainerAllocator>;
  _goal_id_type goal_id;
  using _feedback_type =
    soarm100_interfaces::action::ExecuteGrasp_Feedback_<ContainerAllocator>;
  _feedback_type feedback;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__feedback(
    const soarm100_interfaces::action::ExecuteGrasp_Feedback_<ContainerAllocator> & _arg)
  {
    this->feedback = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_FeedbackMessage
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__action__ExecuteGrasp_FeedbackMessage
    std::shared_ptr<soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecuteGrasp_FeedbackMessage_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->feedback != other.feedback) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecuteGrasp_FeedbackMessage_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecuteGrasp_FeedbackMessage_

// alias to use template instance with default allocator
using ExecuteGrasp_FeedbackMessage =
  soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace soarm100_interfaces

#include "action_msgs/srv/cancel_goal.hpp"
#include "action_msgs/msg/goal_info.hpp"
#include "action_msgs/msg/goal_status_array.hpp"

namespace soarm100_interfaces
{

namespace action
{

struct ExecuteGrasp
{
  /// The goal message defined in the action definition.
  using Goal = soarm100_interfaces::action::ExecuteGrasp_Goal;
  /// The result message defined in the action definition.
  using Result = soarm100_interfaces::action::ExecuteGrasp_Result;
  /// The feedback message defined in the action definition.
  using Feedback = soarm100_interfaces::action::ExecuteGrasp_Feedback;

  struct Impl
  {
    /// The send_goal service using a wrapped version of the goal message as a request.
    using SendGoalService = soarm100_interfaces::action::ExecuteGrasp_SendGoal;
    /// The get_result service using a wrapped version of the result message as a response.
    using GetResultService = soarm100_interfaces::action::ExecuteGrasp_GetResult;
    /// The feedback message with generic fields which wraps the feedback message.
    using FeedbackMessage = soarm100_interfaces::action::ExecuteGrasp_FeedbackMessage;

    /// The generic service to cancel a goal.
    using CancelGoalService = action_msgs::srv::CancelGoal;
    /// The generic message for the status of a goal.
    using GoalStatusMessage = action_msgs::msg::GoalStatusArray;
  };
};

typedef struct ExecuteGrasp ExecuteGrasp;

}  // namespace action

}  // namespace soarm100_interfaces

#endif  // SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_GRASP__STRUCT_HPP_
