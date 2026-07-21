# generated from rosidl_generator_py/resource/_idl.py.em
# with input from soarm100_interfaces:action/ExecuteGrasp.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ExecuteGrasp_Goal(type):
    """Metaclass of message 'ExecuteGrasp_Goal'."""

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
                'soarm100_interfaces.action.ExecuteGrasp_Goal')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_grasp__goal
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_grasp__goal
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_grasp__goal
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_grasp__goal
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_grasp__goal

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


class ExecuteGrasp_Goal(metaclass=Metaclass_ExecuteGrasp_Goal):
    """Message class 'ExecuteGrasp_Goal'."""

    __slots__ = [
        '_target_prompt',
        '_enable_avoidance',
        '_approximate_target_pose',
    ]

    _fields_and_field_types = {
        'target_prompt': 'string',
        'enable_avoidance': 'boolean',
        'approximate_target_pose': 'geometry_msgs/PoseStamped',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'PoseStamped'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.target_prompt = kwargs.get('target_prompt', str())
        self.enable_avoidance = kwargs.get('enable_avoidance', bool())
        from geometry_msgs.msg import PoseStamped
        self.approximate_target_pose = kwargs.get('approximate_target_pose', PoseStamped())

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
        if self.enable_avoidance != other.enable_avoidance:
            return False
        if self.approximate_target_pose != other.approximate_target_pose:
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
    def enable_avoidance(self):
        """Message field 'enable_avoidance'."""
        return self._enable_avoidance

    @enable_avoidance.setter
    def enable_avoidance(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'enable_avoidance' field must be of type 'bool'"
        self._enable_avoidance = value

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


# Import statements for member types

# already imported above
# import builtins

import math  # noqa: E402, I100

# already imported above
# import rosidl_parser.definition


class Metaclass_ExecuteGrasp_Result(type):
    """Metaclass of message 'ExecuteGrasp_Result'."""

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
                'soarm100_interfaces.action.ExecuteGrasp_Result')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_grasp__result
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_grasp__result
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_grasp__result
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_grasp__result
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_grasp__result

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


class ExecuteGrasp_Result(metaclass=Metaclass_ExecuteGrasp_Result):
    """Message class 'ExecuteGrasp_Result'."""

    __slots__ = [
        '_success',
        '_reason',
        '_final_grasp_pose',
        '_lift_height',
        '_attempts',
    ]

    _fields_and_field_types = {
        'success': 'boolean',
        'reason': 'string',
        'final_grasp_pose': 'geometry_msgs/PoseStamped',
        'lift_height': 'float',
        'attempts': 'uint8',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'PoseStamped'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.success = kwargs.get('success', bool())
        self.reason = kwargs.get('reason', str())
        from geometry_msgs.msg import PoseStamped
        self.final_grasp_pose = kwargs.get('final_grasp_pose', PoseStamped())
        self.lift_height = kwargs.get('lift_height', float())
        self.attempts = kwargs.get('attempts', int())

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
        if self.final_grasp_pose != other.final_grasp_pose:
            return False
        if self.lift_height != other.lift_height:
            return False
        if self.attempts != other.attempts:
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
    def final_grasp_pose(self):
        """Message field 'final_grasp_pose'."""
        return self._final_grasp_pose

    @final_grasp_pose.setter
    def final_grasp_pose(self, value):
        if __debug__:
            from geometry_msgs.msg import PoseStamped
            assert \
                isinstance(value, PoseStamped), \
                "The 'final_grasp_pose' field must be a sub message of type 'PoseStamped'"
        self._final_grasp_pose = value

    @builtins.property
    def lift_height(self):
        """Message field 'lift_height'."""
        return self._lift_height

    @lift_height.setter
    def lift_height(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'lift_height' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'lift_height' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._lift_height = value

    @builtins.property
    def attempts(self):
        """Message field 'attempts'."""
        return self._attempts

    @attempts.setter
    def attempts(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'attempts' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'attempts' field must be an unsigned integer in [0, 255]"
        self._attempts = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import math

# already imported above
# import rosidl_parser.definition


class Metaclass_ExecuteGrasp_Feedback(type):
    """Metaclass of message 'ExecuteGrasp_Feedback'."""

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
                'soarm100_interfaces.action.ExecuteGrasp_Feedback')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_grasp__feedback
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_grasp__feedback
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_grasp__feedback
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_grasp__feedback
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_grasp__feedback

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ExecuteGrasp_Feedback(metaclass=Metaclass_ExecuteGrasp_Feedback):
    """Message class 'ExecuteGrasp_Feedback'."""

    __slots__ = [
        '_stage',
        '_target_visible_score',
        '_grasp_score',
        '_tcp_pos_err',
        '_tcp_ori_err',
        '_sdf_min_dist',
        '_cbf_active',
        '_tracking_valid',
        '_replan_running',
        '_reason',
    ]

    _fields_and_field_types = {
        'stage': 'string',
        'target_visible_score': 'float',
        'grasp_score': 'float',
        'tcp_pos_err': 'float',
        'tcp_ori_err': 'float',
        'sdf_min_dist': 'float',
        'cbf_active': 'boolean',
        'tracking_valid': 'boolean',
        'replan_running': 'boolean',
        'reason': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.stage = kwargs.get('stage', str())
        self.target_visible_score = kwargs.get('target_visible_score', float())
        self.grasp_score = kwargs.get('grasp_score', float())
        self.tcp_pos_err = kwargs.get('tcp_pos_err', float())
        self.tcp_ori_err = kwargs.get('tcp_ori_err', float())
        self.sdf_min_dist = kwargs.get('sdf_min_dist', float())
        self.cbf_active = kwargs.get('cbf_active', bool())
        self.tracking_valid = kwargs.get('tracking_valid', bool())
        self.replan_running = kwargs.get('replan_running', bool())
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
        if self.target_visible_score != other.target_visible_score:
            return False
        if self.grasp_score != other.grasp_score:
            return False
        if self.tcp_pos_err != other.tcp_pos_err:
            return False
        if self.tcp_ori_err != other.tcp_ori_err:
            return False
        if self.sdf_min_dist != other.sdf_min_dist:
            return False
        if self.cbf_active != other.cbf_active:
            return False
        if self.tracking_valid != other.tracking_valid:
            return False
        if self.replan_running != other.replan_running:
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
    def target_visible_score(self):
        """Message field 'target_visible_score'."""
        return self._target_visible_score

    @target_visible_score.setter
    def target_visible_score(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'target_visible_score' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'target_visible_score' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._target_visible_score = value

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
    def tcp_pos_err(self):
        """Message field 'tcp_pos_err'."""
        return self._tcp_pos_err

    @tcp_pos_err.setter
    def tcp_pos_err(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'tcp_pos_err' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'tcp_pos_err' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._tcp_pos_err = value

    @builtins.property
    def tcp_ori_err(self):
        """Message field 'tcp_ori_err'."""
        return self._tcp_ori_err

    @tcp_ori_err.setter
    def tcp_ori_err(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'tcp_ori_err' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'tcp_ori_err' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._tcp_ori_err = value

    @builtins.property
    def sdf_min_dist(self):
        """Message field 'sdf_min_dist'."""
        return self._sdf_min_dist

    @sdf_min_dist.setter
    def sdf_min_dist(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'sdf_min_dist' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'sdf_min_dist' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._sdf_min_dist = value

    @builtins.property
    def cbf_active(self):
        """Message field 'cbf_active'."""
        return self._cbf_active

    @cbf_active.setter
    def cbf_active(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'cbf_active' field must be of type 'bool'"
        self._cbf_active = value

    @builtins.property
    def tracking_valid(self):
        """Message field 'tracking_valid'."""
        return self._tracking_valid

    @tracking_valid.setter
    def tracking_valid(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'tracking_valid' field must be of type 'bool'"
        self._tracking_valid = value

    @builtins.property
    def replan_running(self):
        """Message field 'replan_running'."""
        return self._replan_running

    @replan_running.setter
    def replan_running(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'replan_running' field must be of type 'bool'"
        self._replan_running = value

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


class Metaclass_ExecuteGrasp_SendGoal_Request(type):
    """Metaclass of message 'ExecuteGrasp_SendGoal_Request'."""

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
                'soarm100_interfaces.action.ExecuteGrasp_SendGoal_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_grasp__send_goal__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_grasp__send_goal__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_grasp__send_goal__request
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_grasp__send_goal__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_grasp__send_goal__request

            from soarm100_interfaces.action import ExecuteGrasp
            if ExecuteGrasp.Goal.__class__._TYPE_SUPPORT is None:
                ExecuteGrasp.Goal.__class__.__import_type_support__()

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


class ExecuteGrasp_SendGoal_Request(metaclass=Metaclass_ExecuteGrasp_SendGoal_Request):
    """Message class 'ExecuteGrasp_SendGoal_Request'."""

    __slots__ = [
        '_goal_id',
        '_goal',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
        'goal': 'soarm100_interfaces/ExecuteGrasp_Goal',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['soarm100_interfaces', 'action'], 'ExecuteGrasp_Goal'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())
        from soarm100_interfaces.action._execute_grasp import ExecuteGrasp_Goal
        self.goal = kwargs.get('goal', ExecuteGrasp_Goal())

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
            from soarm100_interfaces.action._execute_grasp import ExecuteGrasp_Goal
            assert \
                isinstance(value, ExecuteGrasp_Goal), \
                "The 'goal' field must be a sub message of type 'ExecuteGrasp_Goal'"
        self._goal = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_ExecuteGrasp_SendGoal_Response(type):
    """Metaclass of message 'ExecuteGrasp_SendGoal_Response'."""

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
                'soarm100_interfaces.action.ExecuteGrasp_SendGoal_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_grasp__send_goal__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_grasp__send_goal__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_grasp__send_goal__response
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_grasp__send_goal__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_grasp__send_goal__response

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


class ExecuteGrasp_SendGoal_Response(metaclass=Metaclass_ExecuteGrasp_SendGoal_Response):
    """Message class 'ExecuteGrasp_SendGoal_Response'."""

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


class Metaclass_ExecuteGrasp_SendGoal(type):
    """Metaclass of service 'ExecuteGrasp_SendGoal'."""

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
                'soarm100_interfaces.action.ExecuteGrasp_SendGoal')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__action__execute_grasp__send_goal

            from soarm100_interfaces.action import _execute_grasp
            if _execute_grasp.Metaclass_ExecuteGrasp_SendGoal_Request._TYPE_SUPPORT is None:
                _execute_grasp.Metaclass_ExecuteGrasp_SendGoal_Request.__import_type_support__()
            if _execute_grasp.Metaclass_ExecuteGrasp_SendGoal_Response._TYPE_SUPPORT is None:
                _execute_grasp.Metaclass_ExecuteGrasp_SendGoal_Response.__import_type_support__()


class ExecuteGrasp_SendGoal(metaclass=Metaclass_ExecuteGrasp_SendGoal):
    from soarm100_interfaces.action._execute_grasp import ExecuteGrasp_SendGoal_Request as Request
    from soarm100_interfaces.action._execute_grasp import ExecuteGrasp_SendGoal_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_ExecuteGrasp_GetResult_Request(type):
    """Metaclass of message 'ExecuteGrasp_GetResult_Request'."""

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
                'soarm100_interfaces.action.ExecuteGrasp_GetResult_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_grasp__get_result__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_grasp__get_result__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_grasp__get_result__request
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_grasp__get_result__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_grasp__get_result__request

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


class ExecuteGrasp_GetResult_Request(metaclass=Metaclass_ExecuteGrasp_GetResult_Request):
    """Message class 'ExecuteGrasp_GetResult_Request'."""

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


class Metaclass_ExecuteGrasp_GetResult_Response(type):
    """Metaclass of message 'ExecuteGrasp_GetResult_Response'."""

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
                'soarm100_interfaces.action.ExecuteGrasp_GetResult_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_grasp__get_result__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_grasp__get_result__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_grasp__get_result__response
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_grasp__get_result__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_grasp__get_result__response

            from soarm100_interfaces.action import ExecuteGrasp
            if ExecuteGrasp.Result.__class__._TYPE_SUPPORT is None:
                ExecuteGrasp.Result.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ExecuteGrasp_GetResult_Response(metaclass=Metaclass_ExecuteGrasp_GetResult_Response):
    """Message class 'ExecuteGrasp_GetResult_Response'."""

    __slots__ = [
        '_status',
        '_result',
    ]

    _fields_and_field_types = {
        'status': 'int8',
        'result': 'soarm100_interfaces/ExecuteGrasp_Result',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('int8'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['soarm100_interfaces', 'action'], 'ExecuteGrasp_Result'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.status = kwargs.get('status', int())
        from soarm100_interfaces.action._execute_grasp import ExecuteGrasp_Result
        self.result = kwargs.get('result', ExecuteGrasp_Result())

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
            from soarm100_interfaces.action._execute_grasp import ExecuteGrasp_Result
            assert \
                isinstance(value, ExecuteGrasp_Result), \
                "The 'result' field must be a sub message of type 'ExecuteGrasp_Result'"
        self._result = value


class Metaclass_ExecuteGrasp_GetResult(type):
    """Metaclass of service 'ExecuteGrasp_GetResult'."""

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
                'soarm100_interfaces.action.ExecuteGrasp_GetResult')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__action__execute_grasp__get_result

            from soarm100_interfaces.action import _execute_grasp
            if _execute_grasp.Metaclass_ExecuteGrasp_GetResult_Request._TYPE_SUPPORT is None:
                _execute_grasp.Metaclass_ExecuteGrasp_GetResult_Request.__import_type_support__()
            if _execute_grasp.Metaclass_ExecuteGrasp_GetResult_Response._TYPE_SUPPORT is None:
                _execute_grasp.Metaclass_ExecuteGrasp_GetResult_Response.__import_type_support__()


class ExecuteGrasp_GetResult(metaclass=Metaclass_ExecuteGrasp_GetResult):
    from soarm100_interfaces.action._execute_grasp import ExecuteGrasp_GetResult_Request as Request
    from soarm100_interfaces.action._execute_grasp import ExecuteGrasp_GetResult_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_ExecuteGrasp_FeedbackMessage(type):
    """Metaclass of message 'ExecuteGrasp_FeedbackMessage'."""

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
                'soarm100_interfaces.action.ExecuteGrasp_FeedbackMessage')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_grasp__feedback_message
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_grasp__feedback_message
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_grasp__feedback_message
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_grasp__feedback_message
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_grasp__feedback_message

            from soarm100_interfaces.action import ExecuteGrasp
            if ExecuteGrasp.Feedback.__class__._TYPE_SUPPORT is None:
                ExecuteGrasp.Feedback.__class__.__import_type_support__()

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


class ExecuteGrasp_FeedbackMessage(metaclass=Metaclass_ExecuteGrasp_FeedbackMessage):
    """Message class 'ExecuteGrasp_FeedbackMessage'."""

    __slots__ = [
        '_goal_id',
        '_feedback',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
        'feedback': 'soarm100_interfaces/ExecuteGrasp_Feedback',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['soarm100_interfaces', 'action'], 'ExecuteGrasp_Feedback'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())
        from soarm100_interfaces.action._execute_grasp import ExecuteGrasp_Feedback
        self.feedback = kwargs.get('feedback', ExecuteGrasp_Feedback())

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
            from soarm100_interfaces.action._execute_grasp import ExecuteGrasp_Feedback
            assert \
                isinstance(value, ExecuteGrasp_Feedback), \
                "The 'feedback' field must be a sub message of type 'ExecuteGrasp_Feedback'"
        self._feedback = value


class Metaclass_ExecuteGrasp(type):
    """Metaclass of action 'ExecuteGrasp'."""

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
                'soarm100_interfaces.action.ExecuteGrasp')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_action__action__execute_grasp

            from action_msgs.msg import _goal_status_array
            if _goal_status_array.Metaclass_GoalStatusArray._TYPE_SUPPORT is None:
                _goal_status_array.Metaclass_GoalStatusArray.__import_type_support__()
            from action_msgs.srv import _cancel_goal
            if _cancel_goal.Metaclass_CancelGoal._TYPE_SUPPORT is None:
                _cancel_goal.Metaclass_CancelGoal.__import_type_support__()

            from soarm100_interfaces.action import _execute_grasp
            if _execute_grasp.Metaclass_ExecuteGrasp_SendGoal._TYPE_SUPPORT is None:
                _execute_grasp.Metaclass_ExecuteGrasp_SendGoal.__import_type_support__()
            if _execute_grasp.Metaclass_ExecuteGrasp_GetResult._TYPE_SUPPORT is None:
                _execute_grasp.Metaclass_ExecuteGrasp_GetResult.__import_type_support__()
            if _execute_grasp.Metaclass_ExecuteGrasp_FeedbackMessage._TYPE_SUPPORT is None:
                _execute_grasp.Metaclass_ExecuteGrasp_FeedbackMessage.__import_type_support__()


class ExecuteGrasp(metaclass=Metaclass_ExecuteGrasp):

    # The goal message defined in the action definition.
    from soarm100_interfaces.action._execute_grasp import ExecuteGrasp_Goal as Goal
    # The result message defined in the action definition.
    from soarm100_interfaces.action._execute_grasp import ExecuteGrasp_Result as Result
    # The feedback message defined in the action definition.
    from soarm100_interfaces.action._execute_grasp import ExecuteGrasp_Feedback as Feedback

    class Impl:

        # The send_goal service using a wrapped version of the goal message as a request.
        from soarm100_interfaces.action._execute_grasp import ExecuteGrasp_SendGoal as SendGoalService
        # The get_result service using a wrapped version of the result message as a response.
        from soarm100_interfaces.action._execute_grasp import ExecuteGrasp_GetResult as GetResultService
        # The feedback message with generic fields which wraps the feedback message.
        from soarm100_interfaces.action._execute_grasp import ExecuteGrasp_FeedbackMessage as FeedbackMessage

        # The generic service to cancel a goal.
        from action_msgs.srv._cancel_goal import CancelGoal as CancelGoalService
        # The generic message for get the status of a goal.
        from action_msgs.msg._goal_status_array import GoalStatusArray as GoalStatusMessage

    def __init__(self):
        raise NotImplementedError('Action classes can not be instantiated')
