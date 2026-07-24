# generated from rosidl_generator_py/resource/_idl.py.em
# with input from soarm100_interfaces:action/PlanGrasp.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_PlanGrasp_Goal(type):
    """Metaclass of message 'PlanGrasp_Goal'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('soarm100_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'soarm100_interfaces.action.PlanGrasp_Goal')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__plan_grasp__goal
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__plan_grasp__goal
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__plan_grasp__goal
            cls._TYPE_SUPPORT = module.type_support_msg__action__plan_grasp__goal
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__plan_grasp__goal

            from geometry_msgs.msg import PoseStamped
            if PoseStamped.__class__._TYPE_SUPPORT is None:
                PoseStamped.__class__.__import_type_support__()

            from sensor_msgs.msg import PointCloud2
            if PointCloud2.__class__._TYPE_SUPPORT is None:
                PointCloud2.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class PlanGrasp_Goal(metaclass=Metaclass_PlanGrasp_Goal):
    """Message class 'PlanGrasp_Goal'."""

    __slots__ = [
        '_target_prompt',
        '_approximate_target_pose',
        '_target_cloud',
        '_top_k',
    ]

    _fields_and_field_types = {
        'target_prompt': 'string',
        'approximate_target_pose': 'geometry_msgs/PoseStamped',
        'target_cloud': 'sensor_msgs/PointCloud2',
        'top_k': 'uint16',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'PoseStamped'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['sensor_msgs', 'msg'], 'PointCloud2'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint16'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.target_prompt = kwargs.get('target_prompt', str())
        from geometry_msgs.msg import PoseStamped
        self.approximate_target_pose = kwargs.get('approximate_target_pose', PoseStamped())
        from sensor_msgs.msg import PointCloud2
        self.target_cloud = kwargs.get('target_cloud', PointCloud2())
        self.top_k = kwargs.get('top_k', int())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.target_prompt != other.target_prompt:
            return False
        if self.approximate_target_pose != other.approximate_target_pose:
            return False
        if self.target_cloud != other.target_cloud:
            return False
        if self.top_k != other.top_k:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def target_prompt(self):
        """Message field 'target_prompt'."""
        return self._target_prompt

    @target_prompt.setter
    def target_prompt(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'target_prompt' field must be of type 'str'"
        self._target_prompt = value

    @builtins.property
    def approximate_target_pose(self):
        """Message field 'approximate_target_pose'."""
        return self._approximate_target_pose

    @approximate_target_pose.setter
    def approximate_target_pose(self, value):
        if __debug__:
            from geometry_msgs.msg import PoseStamped
            assert \
                isinstance(value, PoseStamped), \
                "The 'approximate_target_pose' field must be a sub message of type 'PoseStamped'"
        self._approximate_target_pose = value

    @builtins.property
    def target_cloud(self):
        """Message field 'target_cloud'."""
        return self._target_cloud

    @target_cloud.setter
    def target_cloud(self, value):
        if __debug__:
            from sensor_msgs.msg import PointCloud2
            assert \
                isinstance(value, PointCloud2), \
                "The 'target_cloud' field must be a sub message of type 'PointCloud2'"
        self._target_cloud = value

    @builtins.property
    def top_k(self):
        """Message field 'top_k'."""
        return self._top_k

    @top_k.setter
    def top_k(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'top_k' field must be of type 'int'"
            assert value >= 0 and value < 65536, \
                "The 'top_k' field must be an unsigned integer in [0, 65535]"
        self._top_k = value


# Import statements for member types

# already imported above
# import builtins

import math  # noqa: E402, I100

# already imported above
# import rosidl_parser.definition


class Metaclass_PlanGrasp_Result(type):
    """Metaclass of message 'PlanGrasp_Result'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('soarm100_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'soarm100_interfaces.action.PlanGrasp_Result')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__plan_grasp__result
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__plan_grasp__result
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__plan_grasp__result
            cls._TYPE_SUPPORT = module.type_support_msg__action__plan_grasp__result
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__plan_grasp__result

            from geometry_msgs.msg import PoseStamped
            if PoseStamped.__class__._TYPE_SUPPORT is None:
                PoseStamped.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class PlanGrasp_Result(metaclass=Metaclass_PlanGrasp_Result):
    """Message class 'PlanGrasp_Result'."""

    __slots__ = [
        '_success',
        '_reason',
        '_selected_grasp_pose',
        '_selected_pregrasp_pose',
        '_target_center_pose',
        '_grasp_score',
        '_gripper_width',
        '_candidate_count',
    ]

    _fields_and_field_types = {
        'success': 'boolean',
        'reason': 'string',
        'selected_grasp_pose': 'geometry_msgs/PoseStamped',
        'selected_pregrasp_pose': 'geometry_msgs/PoseStamped',
        'target_center_pose': 'geometry_msgs/PoseStamped',
        'grasp_score': 'float',
        'gripper_width': 'float',
        'candidate_count': 'uint16',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'PoseStamped'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'PoseStamped'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'PoseStamped'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint16'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.success = kwargs.get('success', bool())
        self.reason = kwargs.get('reason', str())
        from geometry_msgs.msg import PoseStamped
        self.selected_grasp_pose = kwargs.get('selected_grasp_pose', PoseStamped())
        from geometry_msgs.msg import PoseStamped
        self.selected_pregrasp_pose = kwargs.get('selected_pregrasp_pose', PoseStamped())
        from geometry_msgs.msg import PoseStamped
        self.target_center_pose = kwargs.get('target_center_pose', PoseStamped())
        self.grasp_score = kwargs.get('grasp_score', float())
        self.gripper_width = kwargs.get('gripper_width', float())
        self.candidate_count = kwargs.get('candidate_count', int())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.success != other.success:
            return False
        if self.reason != other.reason:
            return False
        if self.selected_grasp_pose != other.selected_grasp_pose:
            return False
        if self.selected_pregrasp_pose != other.selected_pregrasp_pose:
            return False
        if self.target_center_pose != other.target_center_pose:
            return False
        if self.grasp_score != other.grasp_score:
            return False
        if self.gripper_width != other.gripper_width:
            return False
        if self.candidate_count != other.candidate_count:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def success(self):
        """Message field 'success'."""
        return self._success

    @success.setter
    def success(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'success' field must be of type 'bool'"
        self._success = value

    @builtins.property
    def reason(self):
        """Message field 'reason'."""
        return self._reason

    @reason.setter
    def reason(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'reason' field must be of type 'str'"
        self._reason = value

    @builtins.property
    def selected_grasp_pose(self):
        """Message field 'selected_grasp_pose'."""
        return self._selected_grasp_pose

    @selected_grasp_pose.setter
    def selected_grasp_pose(self, value):
        if __debug__:
            from geometry_msgs.msg import PoseStamped
            assert \
                isinstance(value, PoseStamped), \
                "The 'selected_grasp_pose' field must be a sub message of type 'PoseStamped'"
        self._selected_grasp_pose = value

    @builtins.property
    def selected_pregrasp_pose(self):
        """Message field 'selected_pregrasp_pose'."""
        return self._selected_pregrasp_pose

    @selected_pregrasp_pose.setter
    def selected_pregrasp_pose(self, value):
        if __debug__:
            from geometry_msgs.msg import PoseStamped
            assert \
                isinstance(value, PoseStamped), \
                "The 'selected_pregrasp_pose' field must be a sub message of type 'PoseStamped'"
        self._selected_pregrasp_pose = value

    @builtins.property
    def target_center_pose(self):
        """Message field 'target_center_pose'."""
        return self._target_center_pose

    @target_center_pose.setter
    def target_center_pose(self, value):
        if __debug__:
            from geometry_msgs.msg import PoseStamped
            assert \
                isinstance(value, PoseStamped), \
                "The 'target_center_pose' field must be a sub message of type 'PoseStamped'"
        self._target_center_pose = value

    @builtins.property
    def grasp_score(self):
        """Message field 'grasp_score'."""
        return self._grasp_score

    @grasp_score.setter
    def grasp_score(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'grasp_score' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'grasp_score' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._grasp_score = value

    @builtins.property
    def gripper_width(self):
        """Message field 'gripper_width'."""
        return self._gripper_width

    @gripper_width.setter
    def gripper_width(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'gripper_width' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'gripper_width' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._gripper_width = value

    @builtins.property
    def candidate_count(self):
        """Message field 'candidate_count'."""
        return self._candidate_count

    @candidate_count.setter
    def candidate_count(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'candidate_count' field must be of type 'int'"
            assert value >= 0 and value < 65536, \
                "The 'candidate_count' field must be an unsigned integer in [0, 65535]"
        self._candidate_count = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import math

# already imported above
# import rosidl_parser.definition


class Metaclass_PlanGrasp_Feedback(type):
    """Metaclass of message 'PlanGrasp_Feedback'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('soarm100_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'soarm100_interfaces.action.PlanGrasp_Feedback')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__plan_grasp__feedback
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__plan_grasp__feedback
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__plan_grasp__feedback
            cls._TYPE_SUPPORT = module.type_support_msg__action__plan_grasp__feedback
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__plan_grasp__feedback

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class PlanGrasp_Feedback(metaclass=Metaclass_PlanGrasp_Feedback):
    """Message class 'PlanGrasp_Feedback'."""

    __slots__ = [
        '_stage',
        '_candidate_count',
        '_best_score',
        '_reason',
    ]

    _fields_and_field_types = {
        'stage': 'string',
        'candidate_count': 'uint16',
        'best_score': 'float',
        'reason': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('uint16'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.stage = kwargs.get('stage', str())
        self.candidate_count = kwargs.get('candidate_count', int())
        self.best_score = kwargs.get('best_score', float())
        self.reason = kwargs.get('reason', str())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.stage != other.stage:
            return False
        if self.candidate_count != other.candidate_count:
            return False
        if self.best_score != other.best_score:
            return False
        if self.reason != other.reason:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def stage(self):
        """Message field 'stage'."""
        return self._stage

    @stage.setter
    def stage(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'stage' field must be of type 'str'"
        self._stage = value

    @builtins.property
    def candidate_count(self):
        """Message field 'candidate_count'."""
        return self._candidate_count

    @candidate_count.setter
    def candidate_count(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'candidate_count' field must be of type 'int'"
            assert value >= 0 and value < 65536, \
                "The 'candidate_count' field must be an unsigned integer in [0, 65535]"
        self._candidate_count = value

    @builtins.property
    def best_score(self):
        """Message field 'best_score'."""
        return self._best_score

    @best_score.setter
    def best_score(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'best_score' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'best_score' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._best_score = value

    @builtins.property
    def reason(self):
        """Message field 'reason'."""
        return self._reason

    @reason.setter
    def reason(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'reason' field must be of type 'str'"
        self._reason = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_PlanGrasp_SendGoal_Request(type):
    """Metaclass of message 'PlanGrasp_SendGoal_Request'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('soarm100_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'soarm100_interfaces.action.PlanGrasp_SendGoal_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__plan_grasp__send_goal__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__plan_grasp__send_goal__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__plan_grasp__send_goal__request
            cls._TYPE_SUPPORT = module.type_support_msg__action__plan_grasp__send_goal__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__plan_grasp__send_goal__request

            from soarm100_interfaces.action import PlanGrasp
            if PlanGrasp.Goal.__class__._TYPE_SUPPORT is None:
                PlanGrasp.Goal.__class__.__import_type_support__()

            from unique_identifier_msgs.msg import UUID
            if UUID.__class__._TYPE_SUPPORT is None:
                UUID.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class PlanGrasp_SendGoal_Request(metaclass=Metaclass_PlanGrasp_SendGoal_Request):
    """Message class 'PlanGrasp_SendGoal_Request'."""

    __slots__ = [
        '_goal_id',
        '_goal',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
        'goal': 'soarm100_interfaces/PlanGrasp_Goal',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['soarm100_interfaces', 'action'], 'PlanGrasp_Goal'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())
        from soarm100_interfaces.action._plan_grasp import PlanGrasp_Goal
        self.goal = kwargs.get('goal', PlanGrasp_Goal())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.goal_id != other.goal_id:
            return False
        if self.goal != other.goal:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def goal_id(self):
        """Message field 'goal_id'."""
        return self._goal_id

    @goal_id.setter
    def goal_id(self, value):
        if __debug__:
            from unique_identifier_msgs.msg import UUID
            assert \
                isinstance(value, UUID), \
                "The 'goal_id' field must be a sub message of type 'UUID'"
        self._goal_id = value

    @builtins.property
    def goal(self):
        """Message field 'goal'."""
        return self._goal

    @goal.setter
    def goal(self, value):
        if __debug__:
            from soarm100_interfaces.action._plan_grasp import PlanGrasp_Goal
            assert \
                isinstance(value, PlanGrasp_Goal), \
                "The 'goal' field must be a sub message of type 'PlanGrasp_Goal'"
        self._goal = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_PlanGrasp_SendGoal_Response(type):
    """Metaclass of message 'PlanGrasp_SendGoal_Response'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('soarm100_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'soarm100_interfaces.action.PlanGrasp_SendGoal_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__plan_grasp__send_goal__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__plan_grasp__send_goal__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__plan_grasp__send_goal__response
            cls._TYPE_SUPPORT = module.type_support_msg__action__plan_grasp__send_goal__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__plan_grasp__send_goal__response

            from builtin_interfaces.msg import Time
            if Time.__class__._TYPE_SUPPORT is None:
                Time.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class PlanGrasp_SendGoal_Response(metaclass=Metaclass_PlanGrasp_SendGoal_Response):
    """Message class 'PlanGrasp_SendGoal_Response'."""

    __slots__ = [
        '_accepted',
        '_stamp',
    ]

    _fields_and_field_types = {
        'accepted': 'boolean',
        'stamp': 'builtin_interfaces/Time',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['builtin_interfaces', 'msg'], 'Time'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.accepted = kwargs.get('accepted', bool())
        from builtin_interfaces.msg import Time
        self.stamp = kwargs.get('stamp', Time())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.accepted != other.accepted:
            return False
        if self.stamp != other.stamp:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def accepted(self):
        """Message field 'accepted'."""
        return self._accepted

    @accepted.setter
    def accepted(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'accepted' field must be of type 'bool'"
        self._accepted = value

    @builtins.property
    def stamp(self):
        """Message field 'stamp'."""
        return self._stamp

    @stamp.setter
    def stamp(self, value):
        if __debug__:
            from builtin_interfaces.msg import Time
            assert \
                isinstance(value, Time), \
                "The 'stamp' field must be a sub message of type 'Time'"
        self._stamp = value


class Metaclass_PlanGrasp_SendGoal(type):
    """Metaclass of service 'PlanGrasp_SendGoal'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('soarm100_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'soarm100_interfaces.action.PlanGrasp_SendGoal')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__action__plan_grasp__send_goal

            from soarm100_interfaces.action import _plan_grasp
            if _plan_grasp.Metaclass_PlanGrasp_SendGoal_Request._TYPE_SUPPORT is None:
                _plan_grasp.Metaclass_PlanGrasp_SendGoal_Request.__import_type_support__()
            if _plan_grasp.Metaclass_PlanGrasp_SendGoal_Response._TYPE_SUPPORT is None:
                _plan_grasp.Metaclass_PlanGrasp_SendGoal_Response.__import_type_support__()


class PlanGrasp_SendGoal(metaclass=Metaclass_PlanGrasp_SendGoal):
    from soarm100_interfaces.action._plan_grasp import PlanGrasp_SendGoal_Request as Request
    from soarm100_interfaces.action._plan_grasp import PlanGrasp_SendGoal_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_PlanGrasp_GetResult_Request(type):
    """Metaclass of message 'PlanGrasp_GetResult_Request'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('soarm100_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'soarm100_interfaces.action.PlanGrasp_GetResult_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__plan_grasp__get_result__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__plan_grasp__get_result__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__plan_grasp__get_result__request
            cls._TYPE_SUPPORT = module.type_support_msg__action__plan_grasp__get_result__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__plan_grasp__get_result__request

            from unique_identifier_msgs.msg import UUID
            if UUID.__class__._TYPE_SUPPORT is None:
                UUID.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class PlanGrasp_GetResult_Request(metaclass=Metaclass_PlanGrasp_GetResult_Request):
    """Message class 'PlanGrasp_GetResult_Request'."""

    __slots__ = [
        '_goal_id',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.goal_id != other.goal_id:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def goal_id(self):
        """Message field 'goal_id'."""
        return self._goal_id

    @goal_id.setter
    def goal_id(self, value):
        if __debug__:
            from unique_identifier_msgs.msg import UUID
            assert \
                isinstance(value, UUID), \
                "The 'goal_id' field must be a sub message of type 'UUID'"
        self._goal_id = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_PlanGrasp_GetResult_Response(type):
    """Metaclass of message 'PlanGrasp_GetResult_Response'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('soarm100_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'soarm100_interfaces.action.PlanGrasp_GetResult_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__plan_grasp__get_result__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__plan_grasp__get_result__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__plan_grasp__get_result__response
            cls._TYPE_SUPPORT = module.type_support_msg__action__plan_grasp__get_result__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__plan_grasp__get_result__response

            from soarm100_interfaces.action import PlanGrasp
            if PlanGrasp.Result.__class__._TYPE_SUPPORT is None:
                PlanGrasp.Result.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class PlanGrasp_GetResult_Response(metaclass=Metaclass_PlanGrasp_GetResult_Response):
    """Message class 'PlanGrasp_GetResult_Response'."""

    __slots__ = [
        '_status',
        '_result',
    ]

    _fields_and_field_types = {
        'status': 'int8',
        'result': 'soarm100_interfaces/PlanGrasp_Result',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('int8'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['soarm100_interfaces', 'action'], 'PlanGrasp_Result'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.status = kwargs.get('status', int())
        from soarm100_interfaces.action._plan_grasp import PlanGrasp_Result
        self.result = kwargs.get('result', PlanGrasp_Result())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.status != other.status:
            return False
        if self.result != other.result:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def status(self):
        """Message field 'status'."""
        return self._status

    @status.setter
    def status(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'status' field must be of type 'int'"
            assert value >= -128 and value < 128, \
                "The 'status' field must be an integer in [-128, 127]"
        self._status = value

    @builtins.property
    def result(self):
        """Message field 'result'."""
        return self._result

    @result.setter
    def result(self, value):
        if __debug__:
            from soarm100_interfaces.action._plan_grasp import PlanGrasp_Result
            assert \
                isinstance(value, PlanGrasp_Result), \
                "The 'result' field must be a sub message of type 'PlanGrasp_Result'"
        self._result = value


class Metaclass_PlanGrasp_GetResult(type):
    """Metaclass of service 'PlanGrasp_GetResult'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('soarm100_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'soarm100_interfaces.action.PlanGrasp_GetResult')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__action__plan_grasp__get_result

            from soarm100_interfaces.action import _plan_grasp
            if _plan_grasp.Metaclass_PlanGrasp_GetResult_Request._TYPE_SUPPORT is None:
                _plan_grasp.Metaclass_PlanGrasp_GetResult_Request.__import_type_support__()
            if _plan_grasp.Metaclass_PlanGrasp_GetResult_Response._TYPE_SUPPORT is None:
                _plan_grasp.Metaclass_PlanGrasp_GetResult_Response.__import_type_support__()


class PlanGrasp_GetResult(metaclass=Metaclass_PlanGrasp_GetResult):
    from soarm100_interfaces.action._plan_grasp import PlanGrasp_GetResult_Request as Request
    from soarm100_interfaces.action._plan_grasp import PlanGrasp_GetResult_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_PlanGrasp_FeedbackMessage(type):
    """Metaclass of message 'PlanGrasp_FeedbackMessage'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('soarm100_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'soarm100_interfaces.action.PlanGrasp_FeedbackMessage')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__plan_grasp__feedback_message
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__plan_grasp__feedback_message
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__plan_grasp__feedback_message
            cls._TYPE_SUPPORT = module.type_support_msg__action__plan_grasp__feedback_message
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__plan_grasp__feedback_message

            from soarm100_interfaces.action import PlanGrasp
            if PlanGrasp.Feedback.__class__._TYPE_SUPPORT is None:
                PlanGrasp.Feedback.__class__.__import_type_support__()

            from unique_identifier_msgs.msg import UUID
            if UUID.__class__._TYPE_SUPPORT is None:
                UUID.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class PlanGrasp_FeedbackMessage(metaclass=Metaclass_PlanGrasp_FeedbackMessage):
    """Message class 'PlanGrasp_FeedbackMessage'."""

    __slots__ = [
        '_goal_id',
        '_feedback',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
        'feedback': 'soarm100_interfaces/PlanGrasp_Feedback',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['soarm100_interfaces', 'action'], 'PlanGrasp_Feedback'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())
        from soarm100_interfaces.action._plan_grasp import PlanGrasp_Feedback
        self.feedback = kwargs.get('feedback', PlanGrasp_Feedback())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.goal_id != other.goal_id:
            return False
        if self.feedback != other.feedback:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def goal_id(self):
        """Message field 'goal_id'."""
        return self._goal_id

    @goal_id.setter
    def goal_id(self, value):
        if __debug__:
            from unique_identifier_msgs.msg import UUID
            assert \
                isinstance(value, UUID), \
                "The 'goal_id' field must be a sub message of type 'UUID'"
        self._goal_id = value

    @builtins.property
    def feedback(self):
        """Message field 'feedback'."""
        return self._feedback

    @feedback.setter
    def feedback(self, value):
        if __debug__:
            from soarm100_interfaces.action._plan_grasp import PlanGrasp_Feedback
            assert \
                isinstance(value, PlanGrasp_Feedback), \
                "The 'feedback' field must be a sub message of type 'PlanGrasp_Feedback'"
        self._feedback = value


class Metaclass_PlanGrasp(type):
    """Metaclass of action 'PlanGrasp'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('soarm100_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'soarm100_interfaces.action.PlanGrasp')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_action__action__plan_grasp

            from action_msgs.msg import _goal_status_array
            if _goal_status_array.Metaclass_GoalStatusArray._TYPE_SUPPORT is None:
                _goal_status_array.Metaclass_GoalStatusArray.__import_type_support__()
            from action_msgs.srv import _cancel_goal
            if _cancel_goal.Metaclass_CancelGoal._TYPE_SUPPORT is None:
                _cancel_goal.Metaclass_CancelGoal.__import_type_support__()

            from soarm100_interfaces.action import _plan_grasp
            if _plan_grasp.Metaclass_PlanGrasp_SendGoal._TYPE_SUPPORT is None:
                _plan_grasp.Metaclass_PlanGrasp_SendGoal.__import_type_support__()
            if _plan_grasp.Metaclass_PlanGrasp_GetResult._TYPE_SUPPORT is None:
                _plan_grasp.Metaclass_PlanGrasp_GetResult.__import_type_support__()
            if _plan_grasp.Metaclass_PlanGrasp_FeedbackMessage._TYPE_SUPPORT is None:
                _plan_grasp.Metaclass_PlanGrasp_FeedbackMessage.__import_type_support__()


class PlanGrasp(metaclass=Metaclass_PlanGrasp):

    # The goal message defined in the action definition.
    from soarm100_interfaces.action._plan_grasp import PlanGrasp_Goal as Goal
    # The result message defined in the action definition.
    from soarm100_interfaces.action._plan_grasp import PlanGrasp_Result as Result
    # The feedback message defined in the action definition.
    from soarm100_interfaces.action._plan_grasp import PlanGrasp_Feedback as Feedback

    class Impl:

        # The send_goal service using a wrapped version of the goal message as a request.
        from soarm100_interfaces.action._plan_grasp import PlanGrasp_SendGoal as SendGoalService
        # The get_result service using a wrapped version of the result message as a response.
        from soarm100_interfaces.action._plan_grasp import PlanGrasp_GetResult as GetResultService
        # The feedback message with generic fields which wraps the feedback message.
        from soarm100_interfaces.action._plan_grasp import PlanGrasp_FeedbackMessage as FeedbackMessage

        # The generic service to cancel a goal.
        from action_msgs.srv._cancel_goal import CancelGoal as CancelGoalService
        # The generic message for get the status of a goal.
        from action_msgs.msg._goal_status_array import GoalStatusArray as GoalStatusMessage

    def __init__(self):
        raise NotImplementedError('Action classes can not be instantiated')
