// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from soarm100_interfaces:action/ExecutePlannedGrasp.idl
// generated code does not contain a copyright notice

#ifndef SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_PLANNED_GRASP__STRUCT_HPP_
#define SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_PLANNED_GRASP__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'pregrasp_pose'
// Member 'grasp_pose'
// Member 'tracking_reference_pose'
#include "geometry_msgs/msg/detail/pose_stamped__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_Goal __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_Goal __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecutePlannedGrasp_Goal_
{
  using Type = ExecutePlannedGrasp_Goal_<ContainerAllocator>;

  explicit ExecutePlannedGrasp_Goal_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : pregrasp_pose(_init),
    grasp_pose(_init),
    tracking_reference_pose(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->gripper_width = 0.0f;
      this->enable_avoidance = false;
      this->target_prompt = "";
      this->target_object = "";
      this->target_pos = "";
      this->traj_log = "";
    }
  }

  explicit ExecutePlannedGrasp_Goal_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : pregrasp_pose(_alloc, _init),
    grasp_pose(_alloc, _init),
    tracking_reference_pose(_alloc, _init),
    target_prompt(_alloc),
    target_object(_alloc),
    target_pos(_alloc),
    traj_log(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->gripper_width = 0.0f;
      this->enable_avoidance = false;
      this->target_prompt = "";
      this->target_object = "";
      this->target_pos = "";
      this->traj_log = "";
    }
  }

  // field types and members
  using _pregrasp_pose_type =
    geometry_msgs::msg::PoseStamped_<ContainerAllocator>;
  _pregrasp_pose_type pregrasp_pose;
  using _grasp_pose_type =
    geometry_msgs::msg::PoseStamped_<ContainerAllocator>;
  _grasp_pose_type grasp_pose;
  using _tracking_reference_pose_type =
    geometry_msgs::msg::PoseStamped_<ContainerAllocator>;
  _tracking_reference_pose_type tracking_reference_pose;
  using _gripper_width_type =
    float;
  _gripper_width_type gripper_width;
  using _enable_avoidance_type =
    bool;
  _enable_avoidance_type enable_avoidance;
  using _target_prompt_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _target_prompt_type target_prompt;
  using _target_object_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _target_object_type target_object;
  using _target_pos_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _target_pos_type target_pos;
  using _traj_log_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _traj_log_type traj_log;

  // setters for named parameter idiom
  Type & set__pregrasp_pose(
    const geometry_msgs::msg::PoseStamped_<ContainerAllocator> & _arg)
  {
    this->pregrasp_pose = _arg;
    return *this;
  }
  Type & set__grasp_pose(
    const geometry_msgs::msg::PoseStamped_<ContainerAllocator> & _arg)
  {
    this->grasp_pose = _arg;
    return *this;
  }
  Type & set__tracking_reference_pose(
    const geometry_msgs::msg::PoseStamped_<ContainerAllocator> & _arg)
  {
    this->tracking_reference_pose = _arg;
    return *this;
  }
  Type & set__gripper_width(
    const float & _arg)
  {
    this->gripper_width = _arg;
    return *this;
  }
  Type & set__enable_avoidance(
    const bool & _arg)
  {
    this->enable_avoidance = _arg;
    return *this;
  }
  Type & set__target_prompt(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->target_prompt = _arg;
    return *this;
  }
  Type & set__target_object(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->target_object = _arg;
    return *this;
  }
  Type & set__target_pos(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->target_pos = _arg;
    return *this;
  }
  Type & set__traj_log(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->traj_log = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    soarm100_interfaces::action::ExecutePlannedGrasp_Goal_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::action::ExecutePlannedGrasp_Goal_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Goal_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Goal_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecutePlannedGrasp_Goal_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Goal_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecutePlannedGrasp_Goal_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Goal_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Goal_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Goal_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_Goal
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Goal_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_Goal
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Goal_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecutePlannedGrasp_Goal_ & other) const
  {
    if (this->pregrasp_pose != other.pregrasp_pose) {
      return false;
    }
    if (this->grasp_pose != other.grasp_pose) {
      return false;
    }
    if (this->tracking_reference_pose != other.tracking_reference_pose) {
      return false;
    }
    if (this->gripper_width != other.gripper_width) {
      return false;
    }
    if (this->enable_avoidance != other.enable_avoidance) {
      return false;
    }
    if (this->target_prompt != other.target_prompt) {
      return false;
    }
    if (this->target_object != other.target_object) {
      return false;
    }
    if (this->target_pos != other.target_pos) {
      return false;
    }
    if (this->traj_log != other.traj_log) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecutePlannedGrasp_Goal_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecutePlannedGrasp_Goal_

// alias to use template instance with default allocator
using ExecutePlannedGrasp_Goal =
  soarm100_interfaces::action::ExecutePlannedGrasp_Goal_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace soarm100_interfaces


#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_Result __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_Result __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecutePlannedGrasp_Result_
{
  using Type = ExecutePlannedGrasp_Result_<ContainerAllocator>;

  explicit ExecutePlannedGrasp_Result_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->reason = "";
      this->lift_height = 0.0f;
      this->return_code = 0;
    }
  }

  explicit ExecutePlannedGrasp_Result_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : reason(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->reason = "";
      this->lift_height = 0.0f;
      this->return_code = 0;
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _reason_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _reason_type reason;
  using _lift_height_type =
    float;
  _lift_height_type lift_height;
  using _return_code_type =
    uint8_t;
  _return_code_type return_code;

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
  Type & set__lift_height(
    const float & _arg)
  {
    this->lift_height = _arg;
    return *this;
  }
  Type & set__return_code(
    const uint8_t & _arg)
  {
    this->return_code = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    soarm100_interfaces::action::ExecutePlannedGrasp_Result_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::action::ExecutePlannedGrasp_Result_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Result_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Result_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecutePlannedGrasp_Result_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Result_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecutePlannedGrasp_Result_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Result_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Result_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Result_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_Result
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Result_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_Result
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Result_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecutePlannedGrasp_Result_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->reason != other.reason) {
      return false;
    }
    if (this->lift_height != other.lift_height) {
      return false;
    }
    if (this->return_code != other.return_code) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecutePlannedGrasp_Result_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecutePlannedGrasp_Result_

// alias to use template instance with default allocator
using ExecutePlannedGrasp_Result =
  soarm100_interfaces::action::ExecutePlannedGrasp_Result_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace soarm100_interfaces


#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_Feedback __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_Feedback __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecutePlannedGrasp_Feedback_
{
  using Type = ExecutePlannedGrasp_Feedback_<ContainerAllocator>;

  explicit ExecutePlannedGrasp_Feedback_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->stage = "";
      this->reason = "";
      this->lift_height = 0.0f;
    }
  }

  explicit ExecutePlannedGrasp_Feedback_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stage(_alloc),
    reason(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->stage = "";
      this->reason = "";
      this->lift_height = 0.0f;
    }
  }

  // field types and members
  using _stage_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _stage_type stage;
  using _reason_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _reason_type reason;
  using _lift_height_type =
    float;
  _lift_height_type lift_height;

  // setters for named parameter idiom
  Type & set__stage(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->stage = _arg;
    return *this;
  }
  Type & set__reason(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->reason = _arg;
    return *this;
  }
  Type & set__lift_height(
    const float & _arg)
  {
    this->lift_height = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    soarm100_interfaces::action::ExecutePlannedGrasp_Feedback_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::action::ExecutePlannedGrasp_Feedback_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Feedback_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Feedback_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecutePlannedGrasp_Feedback_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Feedback_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecutePlannedGrasp_Feedback_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Feedback_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Feedback_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Feedback_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_Feedback
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Feedback_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_Feedback
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_Feedback_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecutePlannedGrasp_Feedback_ & other) const
  {
    if (this->stage != other.stage) {
      return false;
    }
    if (this->reason != other.reason) {
      return false;
    }
    if (this->lift_height != other.lift_height) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecutePlannedGrasp_Feedback_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecutePlannedGrasp_Feedback_

// alias to use template instance with default allocator
using ExecutePlannedGrasp_Feedback =
  soarm100_interfaces::action::ExecutePlannedGrasp_Feedback_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace soarm100_interfaces


// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'goal'
#include "soarm100_interfaces/action/detail/execute_planned_grasp__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecutePlannedGrasp_SendGoal_Request_
{
  using Type = ExecutePlannedGrasp_SendGoal_Request_<ContainerAllocator>;

  explicit ExecutePlannedGrasp_SendGoal_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    goal(_init)
  {
    (void)_init;
  }

  explicit ExecutePlannedGrasp_SendGoal_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    soarm100_interfaces::action::ExecutePlannedGrasp_Goal_<ContainerAllocator>;
  _goal_type goal;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__goal(
    const soarm100_interfaces::action::ExecutePlannedGrasp_Goal_<ContainerAllocator> & _arg)
  {
    this->goal = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Request
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecutePlannedGrasp_SendGoal_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->goal != other.goal) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecutePlannedGrasp_SendGoal_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecutePlannedGrasp_SendGoal_Request_

// alias to use template instance with default allocator
using ExecutePlannedGrasp_SendGoal_Request =
  soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace soarm100_interfaces


// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecutePlannedGrasp_SendGoal_Response_
{
  using Type = ExecutePlannedGrasp_SendGoal_Response_<ContainerAllocator>;

  explicit ExecutePlannedGrasp_SendGoal_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
    }
  }

  explicit ExecutePlannedGrasp_SendGoal_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_SendGoal_Response
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecutePlannedGrasp_SendGoal_Response_ & other) const
  {
    if (this->accepted != other.accepted) {
      return false;
    }
    if (this->stamp != other.stamp) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecutePlannedGrasp_SendGoal_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecutePlannedGrasp_SendGoal_Response_

// alias to use template instance with default allocator
using ExecutePlannedGrasp_SendGoal_Response =
  soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace soarm100_interfaces

namespace soarm100_interfaces
{

namespace action
{

struct ExecutePlannedGrasp_SendGoal
{
  using Request = soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Request;
  using Response = soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal_Response;
};

}  // namespace action

}  // namespace soarm100_interfaces


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecutePlannedGrasp_GetResult_Request_
{
  using Type = ExecutePlannedGrasp_GetResult_Request_<ContainerAllocator>;

  explicit ExecutePlannedGrasp_GetResult_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init)
  {
    (void)_init;
  }

  explicit ExecutePlannedGrasp_GetResult_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Request
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecutePlannedGrasp_GetResult_Request_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecutePlannedGrasp_GetResult_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecutePlannedGrasp_GetResult_Request_

// alias to use template instance with default allocator
using ExecutePlannedGrasp_GetResult_Request =
  soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Request_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace soarm100_interfaces


// Include directives for member types
// Member 'result'
// already included above
// #include "soarm100_interfaces/action/detail/execute_planned_grasp__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecutePlannedGrasp_GetResult_Response_
{
  using Type = ExecutePlannedGrasp_GetResult_Response_<ContainerAllocator>;

  explicit ExecutePlannedGrasp_GetResult_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : result(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
    }
  }

  explicit ExecutePlannedGrasp_GetResult_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    soarm100_interfaces::action::ExecutePlannedGrasp_Result_<ContainerAllocator>;
  _result_type result;

  // setters for named parameter idiom
  Type & set__status(
    const int8_t & _arg)
  {
    this->status = _arg;
    return *this;
  }
  Type & set__result(
    const soarm100_interfaces::action::ExecutePlannedGrasp_Result_<ContainerAllocator> & _arg)
  {
    this->result = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_GetResult_Response
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecutePlannedGrasp_GetResult_Response_ & other) const
  {
    if (this->status != other.status) {
      return false;
    }
    if (this->result != other.result) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecutePlannedGrasp_GetResult_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecutePlannedGrasp_GetResult_Response_

// alias to use template instance with default allocator
using ExecutePlannedGrasp_GetResult_Response =
  soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Response_<std::allocator<void>>;

// constant definitions

}  // namespace action

}  // namespace soarm100_interfaces

namespace soarm100_interfaces
{

namespace action
{

struct ExecutePlannedGrasp_GetResult
{
  using Request = soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Request;
  using Response = soarm100_interfaces::action::ExecutePlannedGrasp_GetResult_Response;
};

}  // namespace action

}  // namespace soarm100_interfaces


// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.hpp"
// Member 'feedback'
// already included above
// #include "soarm100_interfaces/action/detail/execute_planned_grasp__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage __attribute__((deprecated))
#else
# define DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage __declspec(deprecated)
#endif

namespace soarm100_interfaces
{

namespace action
{

// message struct
template<class ContainerAllocator>
struct ExecutePlannedGrasp_FeedbackMessage_
{
  using Type = ExecutePlannedGrasp_FeedbackMessage_<ContainerAllocator>;

  explicit ExecutePlannedGrasp_FeedbackMessage_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : goal_id(_init),
    feedback(_init)
  {
    (void)_init;
  }

  explicit ExecutePlannedGrasp_FeedbackMessage_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    soarm100_interfaces::action::ExecutePlannedGrasp_Feedback_<ContainerAllocator>;
  _feedback_type feedback;

  // setters for named parameter idiom
  Type & set__goal_id(
    const unique_identifier_msgs::msg::UUID_<ContainerAllocator> & _arg)
  {
    this->goal_id = _arg;
    return *this;
  }
  Type & set__feedback(
    const soarm100_interfaces::action::ExecutePlannedGrasp_Feedback_<ContainerAllocator> & _arg)
  {
    this->feedback = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    soarm100_interfaces::action::ExecutePlannedGrasp_FeedbackMessage_<ContainerAllocator> *;
  using ConstRawPtr =
    const soarm100_interfaces::action::ExecutePlannedGrasp_FeedbackMessage_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_FeedbackMessage_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_FeedbackMessage_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecutePlannedGrasp_FeedbackMessage_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_FeedbackMessage_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      soarm100_interfaces::action::ExecutePlannedGrasp_FeedbackMessage_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_FeedbackMessage_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_FeedbackMessage_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_FeedbackMessage_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_FeedbackMessage_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__soarm100_interfaces__action__ExecutePlannedGrasp_FeedbackMessage
    std::shared_ptr<soarm100_interfaces::action::ExecutePlannedGrasp_FeedbackMessage_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ExecutePlannedGrasp_FeedbackMessage_ & other) const
  {
    if (this->goal_id != other.goal_id) {
      return false;
    }
    if (this->feedback != other.feedback) {
      return false;
    }
    return true;
  }
  bool operator!=(const ExecutePlannedGrasp_FeedbackMessage_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ExecutePlannedGrasp_FeedbackMessage_

// alias to use template instance with default allocator
using ExecutePlannedGrasp_FeedbackMessage =
  soarm100_interfaces::action::ExecutePlannedGrasp_FeedbackMessage_<std::allocator<void>>;

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

struct ExecutePlannedGrasp
{
  /// The goal message defined in the action definition.
  using Goal = soarm100_interfaces::action::ExecutePlannedGrasp_Goal;
  /// The result message defined in the action definition.
  using Result = soarm100_interfaces::action::ExecutePlannedGrasp_Result;
  /// The feedback message defined in the action definition.
  using Feedback = soarm100_interfaces::action::ExecutePlannedGrasp_Feedback;

  struct Impl
  {
    /// The send_goal service using a wrapped version of the goal message as a request.
    using SendGoalService = soarm100_interfaces::action::ExecutePlannedGrasp_SendGoal;
    /// The get_result service using a wrapped version of the result message as a response.
    using GetResultService = soarm100_interfaces::action::ExecutePlannedGrasp_GetResult;
    /// The feedback message with generic fields which wraps the feedback message.
    using FeedbackMessage = soarm100_interfaces::action::ExecutePlannedGrasp_FeedbackMessage;

    /// The generic service to cancel a goal.
    using CancelGoalService = action_msgs::srv::CancelGoal;
    /// The generic message for the status of a goal.
    using GoalStatusMessage = action_msgs::msg::GoalStatusArray;
  };
};

typedef struct ExecutePlannedGrasp ExecutePlannedGrasp;

}  // namespace action

}  // namespace soarm100_interfaces

#endif  // SOARM100_INTERFACES__ACTION__DETAIL__EXECUTE_PLANNED_GRASP__STRUCT_HPP_
