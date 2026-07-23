# generated from rosidl_generator_py/resource/_idl.py.em
# with input from soarm100_interfaces:action/ExecutePlannedGrasp.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ExecutePlannedGrasp_Goal(type):
    """Metaclass of message 'ExecutePlannedGrasp_Goal'."""

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
                'soarm100_interfaces.action.ExecutePlannedGrasp_Goal')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_planned_grasp__goal
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_planned_grasp__goal
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_planned_grasp__goal
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_planned_grasp__goal
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_planned_grasp__goal

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


class ExecutePlannedGrasp_Goal(metaclass=Metaclass_ExecutePlannedGrasp_Goal):
    """Message class 'ExecutePlannedGrasp_Goal'."""

    __slots__ = [
        '_pregrasp_pose',
        '_grasp_pose',
        '_gripper_width',
        '_enable_avoidance',
        '_target_object',
        '_target_pos',
        '_traj_log',
    ]

    _fields_and_field_types = {
        'pregrasp_pose': 'geometry_msgs/PoseStamped',
        'grasp_pose': 'geometry_msgs/PoseStamped',
        'gripper_width': 'float',
        'enable_avoidance': 'boolean',
        'target_object': 'string',
        'target_pos': 'string',
        'traj_log': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'PoseStamped'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'PoseStamped'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from geometry_msgs.msg import PoseStamped
        self.pregrasp_pose = kwargs.get('pregrasp_pose', PoseStamped())
        from geometry_msgs.msg import PoseStamped
        self.grasp_pose = kwargs.get('grasp_pose', PoseStamped())
        self.gripper_width = kwargs.get('gripper_width', float())
        self.enable_avoidance = kwargs.get('enable_avoidance', bool())
        self.target_object = kwargs.get('target_object', str())
        self.target_pos = kwargs.get('target_pos', str())
        self.traj_log = kwargs.get('traj_log', str())

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
        if self.pregrasp_pose != other.pregrasp_pose:
            return False
        if self.grasp_pose != other.grasp_pose:
            return False
        if self.gripper_width != other.gripper_width:
            return False
        if self.enable_avoidance != other.enable_avoidance:
            return False
        if self.target_object != other.target_object:
            return False
        if self.target_pos != other.target_pos:
            return False
        if self.traj_log != other.traj_log:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def pregrasp_pose(self):
        """Message field 'pregrasp_pose'."""
        return self._pregrasp_pose

    @pregrasp_pose.setter
    def pregrasp_pose(self, value):
        if __debug__:
            from geometry_msgs.msg import PoseStamped
            assert \
                isinstance(value, PoseStamped), \
                "The 'pregrasp_pose' field must be a sub message of type 'PoseStamped'"
        self._pregrasp_pose = value

    @builtins.property
    def grasp_pose(self):
        """Message field 'grasp_pose'."""
        return self._grasp_pose

    @grasp_pose.setter
    def grasp_pose(self, value):
        if __debug__:
            from geometry_msgs.msg import PoseStamped
            assert \
                isinstance(value, PoseStamped), \
                "The 'grasp_pose' field must be a sub message of type 'PoseStamped'"
        self._grasp_pose = value

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
    def target_object(self):
        """Message field 'target_object'."""
        return self._target_object

    @target_object.setter
    def target_object(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'target_object' field must be of type 'str'"
        self._target_object = value

    @builtins.property
    def target_pos(self):
        """Message field 'target_pos'."""
        return self._target_pos

    @target_pos.setter
    def target_pos(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'target_pos' field must be of type 'str'"
        self._target_pos = value

    @builtins.property
    def traj_log(self):
        """Message field 'traj_log'."""
        return self._traj_log

    @traj_log.setter
    def traj_log(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'traj_log' field must be of type 'str'"
        self._traj_log = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import math

# already imported above
# import rosidl_parser.definition


class Metaclass_ExecutePlannedGrasp_Result(type):
    """Metaclass of message 'ExecutePlannedGrasp_Result'."""

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
                'soarm100_interfaces.action.ExecutePlannedGrasp_Result')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_planned_grasp__result
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_planned_grasp__result
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_planned_grasp__result
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_planned_grasp__result
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_planned_grasp__result

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ExecutePlannedGrasp_Result(metaclass=Metaclass_ExecutePlannedGrasp_Result):
    """Message class 'ExecutePlannedGrasp_Result'."""

    __slots__ = [
        '_success',
        '_reason',
        '_lift_height',
        '_return_code',
    ]

    _fields_and_field_types = {
        'success': 'boolean',
        'reason': 'string',
        'lift_height': 'float',
        'return_code': 'uint8',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.success = kwargs.get('success', bool())
        self.reason = kwargs.get('reason', str())
        self.lift_height = kwargs.get('lift_height', float())
        self.return_code = kwargs.get('return_code', int())

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
        if self.lift_height != other.lift_height:
            return False
        if self.return_code != other.return_code:
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
    def return_code(self):
        """Message field 'return_code'."""
        return self._return_code

    @return_code.setter
    def return_code(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'return_code' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'return_code' field must be an unsigned integer in [0, 255]"
        self._return_code = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import math

# already imported above
# import rosidl_parser.definition


class Metaclass_ExecutePlannedGrasp_Feedback(type):
    """Metaclass of message 'ExecutePlannedGrasp_Feedback'."""

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
                'soarm100_interfaces.action.ExecutePlannedGrasp_Feedback')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_planned_grasp__feedback
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_planned_grasp__feedback
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_planned_grasp__feedback
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_planned_grasp__feedback
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_planned_grasp__feedback

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ExecutePlannedGrasp_Feedback(metaclass=Metaclass_ExecutePlannedGrasp_Feedback):
    """Message class 'ExecutePlannedGrasp_Feedback'."""

    __slots__ = [
        '_stage',
        '_reason',
        '_lift_height',
    ]

    _fields_and_field_types = {
        'stage': 'string',
        'reason': 'string',
        'lift_height': 'float',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.stage = kwargs.get('stage', str())
        self.reason = kwargs.get('reason', str())
        self.lift_height = kwargs.get('lift_height', float())

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
        if self.reason != other.reason:
            return False
        if self.lift_height != other.lift_height:
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


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_ExecutePlannedGrasp_SendGoal_Request(type):
    """Metaclass of message 'ExecutePlannedGrasp_SendGoal_Request'."""

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
                'soarm100_interfaces.action.ExecutePlannedGrasp_SendGoal_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_planned_grasp__send_goal__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_planned_grasp__send_goal__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_planned_grasp__send_goal__request
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_planned_grasp__send_goal__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_planned_grasp__send_goal__request

            from soarm100_interfaces.action import ExecutePlannedGrasp
            if ExecutePlannedGrasp.Goal.__class__._TYPE_SUPPORT is None:
                ExecutePlannedGrasp.Goal.__class__.__import_type_support__()

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


class ExecutePlannedGrasp_SendGoal_Request(metaclass=Metaclass_ExecutePlannedGrasp_SendGoal_Request):
    """Message class 'ExecutePlannedGrasp_SendGoal_Request'."""

    __slots__ = [
        '_goal_id',
        '_goal',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
        'goal': 'soarm100_interfaces/ExecutePlannedGrasp_Goal',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['soarm100_interfaces', 'action'], 'ExecutePlannedGrasp_Goal'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())
        from soarm100_interfaces.action._execute_planned_grasp import ExecutePlannedGrasp_Goal
        self.goal = kwargs.get('goal', ExecutePlannedGrasp_Goal())

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
            from soarm100_interfaces.action._execute_planned_grasp import ExecutePlannedGrasp_Goal
            assert \
                isinstance(value, ExecutePlannedGrasp_Goal), \
                "The 'goal' field must be a sub message of type 'ExecutePlannedGrasp_Goal'"
        self._goal = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_ExecutePlannedGrasp_SendGoal_Response(type):
    """Metaclass of message 'ExecutePlannedGrasp_SendGoal_Response'."""

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
                'soarm100_interfaces.action.ExecutePlannedGrasp_SendGoal_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_planned_grasp__send_goal__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_planned_grasp__send_goal__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_planned_grasp__send_goal__response
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_planned_grasp__send_goal__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_planned_grasp__send_goal__response

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


class ExecutePlannedGrasp_SendGoal_Response(metaclass=Metaclass_ExecutePlannedGrasp_SendGoal_Response):
    """Message class 'ExecutePlannedGrasp_SendGoal_Response'."""

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


class Metaclass_ExecutePlannedGrasp_SendGoal(type):
    """Metaclass of service 'ExecutePlannedGrasp_SendGoal'."""

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
                'soarm100_interfaces.action.ExecutePlannedGrasp_SendGoal')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__action__execute_planned_grasp__send_goal

            from soarm100_interfaces.action import _execute_planned_grasp
            if _execute_planned_grasp.Metaclass_ExecutePlannedGrasp_SendGoal_Request._TYPE_SUPPORT is None:
                _execute_planned_grasp.Metaclass_ExecutePlannedGrasp_SendGoal_Request.__import_type_support__()
            if _execute_planned_grasp.Metaclass_ExecutePlannedGrasp_SendGoal_Response._TYPE_SUPPORT is None:
                _execute_planned_grasp.Metaclass_ExecutePlannedGrasp_SendGoal_Response.__import_type_support__()


class ExecutePlannedGrasp_SendGoal(metaclass=Metaclass_ExecutePlannedGrasp_SendGoal):
    from soarm100_interfaces.action._execute_planned_grasp import ExecutePlannedGrasp_SendGoal_Request as Request
    from soarm100_interfaces.action._execute_planned_grasp import ExecutePlannedGrasp_SendGoal_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_ExecutePlannedGrasp_GetResult_Request(type):
    """Metaclass of message 'ExecutePlannedGrasp_GetResult_Request'."""

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
                'soarm100_interfaces.action.ExecutePlannedGrasp_GetResult_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_planned_grasp__get_result__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_planned_grasp__get_result__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_planned_grasp__get_result__request
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_planned_grasp__get_result__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_planned_grasp__get_result__request

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


class ExecutePlannedGrasp_GetResult_Request(metaclass=Metaclass_ExecutePlannedGrasp_GetResult_Request):
    """Message class 'ExecutePlannedGrasp_GetResult_Request'."""

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


class Metaclass_ExecutePlannedGrasp_GetResult_Response(type):
    """Metaclass of message 'ExecutePlannedGrasp_GetResult_Response'."""

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
                'soarm100_interfaces.action.ExecutePlannedGrasp_GetResult_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_planned_grasp__get_result__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_planned_grasp__get_result__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_planned_grasp__get_result__response
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_planned_grasp__get_result__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_planned_grasp__get_result__response

            from soarm100_interfaces.action import ExecutePlannedGrasp
            if ExecutePlannedGrasp.Result.__class__._TYPE_SUPPORT is None:
                ExecutePlannedGrasp.Result.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ExecutePlannedGrasp_GetResult_Response(metaclass=Metaclass_ExecutePlannedGrasp_GetResult_Response):
    """Message class 'ExecutePlannedGrasp_GetResult_Response'."""

    __slots__ = [
        '_status',
        '_result',
    ]

    _fields_and_field_types = {
        'status': 'int8',
        'result': 'soarm100_interfaces/ExecutePlannedGrasp_Result',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('int8'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['soarm100_interfaces', 'action'], 'ExecutePlannedGrasp_Result'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.status = kwargs.get('status', int())
        from soarm100_interfaces.action._execute_planned_grasp import ExecutePlannedGrasp_Result
        self.result = kwargs.get('result', ExecutePlannedGrasp_Result())

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
            from soarm100_interfaces.action._execute_planned_grasp import ExecutePlannedGrasp_Result
            assert \
                isinstance(value, ExecutePlannedGrasp_Result), \
                "The 'result' field must be a sub message of type 'ExecutePlannedGrasp_Result'"
        self._result = value


class Metaclass_ExecutePlannedGrasp_GetResult(type):
    """Metaclass of service 'ExecutePlannedGrasp_GetResult'."""

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
                'soarm100_interfaces.action.ExecutePlannedGrasp_GetResult')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__action__execute_planned_grasp__get_result

            from soarm100_interfaces.action import _execute_planned_grasp
            if _execute_planned_grasp.Metaclass_ExecutePlannedGrasp_GetResult_Request._TYPE_SUPPORT is None:
                _execute_planned_grasp.Metaclass_ExecutePlannedGrasp_GetResult_Request.__import_type_support__()
            if _execute_planned_grasp.Metaclass_ExecutePlannedGrasp_GetResult_Response._TYPE_SUPPORT is None:
                _execute_planned_grasp.Metaclass_ExecutePlannedGrasp_GetResult_Response.__import_type_support__()


class ExecutePlannedGrasp_GetResult(metaclass=Metaclass_ExecutePlannedGrasp_GetResult):
    from soarm100_interfaces.action._execute_planned_grasp import ExecutePlannedGrasp_GetResult_Request as Request
    from soarm100_interfaces.action._execute_planned_grasp import ExecutePlannedGrasp_GetResult_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_ExecutePlannedGrasp_FeedbackMessage(type):
    """Metaclass of message 'ExecutePlannedGrasp_FeedbackMessage'."""

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
                'soarm100_interfaces.action.ExecutePlannedGrasp_FeedbackMessage')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__action__execute_planned_grasp__feedback_message
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__action__execute_planned_grasp__feedback_message
            cls._CONVERT_TO_PY = module.convert_to_py_msg__action__execute_planned_grasp__feedback_message
            cls._TYPE_SUPPORT = module.type_support_msg__action__execute_planned_grasp__feedback_message
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__action__execute_planned_grasp__feedback_message

            from soarm100_interfaces.action import ExecutePlannedGrasp
            if ExecutePlannedGrasp.Feedback.__class__._TYPE_SUPPORT is None:
                ExecutePlannedGrasp.Feedback.__class__.__import_type_support__()

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


class ExecutePlannedGrasp_FeedbackMessage(metaclass=Metaclass_ExecutePlannedGrasp_FeedbackMessage):
    """Message class 'ExecutePlannedGrasp_FeedbackMessage'."""

    __slots__ = [
        '_goal_id',
        '_feedback',
    ]

    _fields_and_field_types = {
        'goal_id': 'unique_identifier_msgs/UUID',
        'feedback': 'soarm100_interfaces/ExecutePlannedGrasp_Feedback',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['unique_identifier_msgs', 'msg'], 'UUID'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['soarm100_interfaces', 'action'], 'ExecutePlannedGrasp_Feedback'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from unique_identifier_msgs.msg import UUID
        self.goal_id = kwargs.get('goal_id', UUID())
        from soarm100_interfaces.action._execute_planned_grasp import ExecutePlannedGrasp_Feedback
        self.feedback = kwargs.get('feedback', ExecutePlannedGrasp_Feedback())

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
            from soarm100_interfaces.action._execute_planned_grasp import ExecutePlannedGrasp_Feedback
            assert \
                isinstance(value, ExecutePlannedGrasp_Feedback), \
                "The 'feedback' field must be a sub message of type 'ExecutePlannedGrasp_Feedback'"
        self._feedback = value


class Metaclass_ExecutePlannedGrasp(type):
    """Metaclass of action 'ExecutePlannedGrasp'."""

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
                'soarm100_interfaces.action.ExecutePlannedGrasp')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_action__action__execute_planned_grasp

            from action_msgs.msg import _goal_status_array
            if _goal_status_array.Metaclass_GoalStatusArray._TYPE_SUPPORT is None:
                _goal_status_array.Metaclass_GoalStatusArray.__import_type_support__()
            from action_msgs.srv import _cancel_goal
            if _cancel_goal.Metaclass_CancelGoal._TYPE_SUPPORT is None:
                _cancel_goal.Metaclass_CancelGoal.__import_type_support__()

            from soarm100_interfaces.action import _execute_planned_grasp
            if _execute_planned_grasp.Metaclass_ExecutePlannedGrasp_SendGoal._TYPE_SUPPORT is None:
                _execute_planned_grasp.Metaclass_ExecutePlannedGrasp_SendGoal.__import_type_support__()
            if _execute_planned_grasp.Metaclass_ExecutePlannedGrasp_GetResult._TYPE_SUPPORT is None:
                _execute_planned_grasp.Metaclass_ExecutePlannedGrasp_GetResult.__import_type_support__()
            if _execute_planned_grasp.Metaclass_ExecutePlannedGrasp_FeedbackMessage._TYPE_SUPPORT is None:
                _execute_planned_grasp.Metaclass_ExecutePlannedGrasp_FeedbackMessage.__import_type_support__()


class ExecutePlannedGrasp(metaclass=Metaclass_ExecutePlannedGrasp):

    # The goal message defined in the action definition.
    from soarm100_interfaces.action._execute_planned_grasp import ExecutePlannedGrasp_Goal as Goal
    # The result message defined in the action definition.
    from soarm100_interfaces.action._execute_planned_grasp import ExecutePlannedGrasp_Result as Result
    # The feedback message defined in the action definition.
    from soarm100_interfaces.action._execute_planned_grasp import ExecutePlannedGrasp_Feedback as Feedback

    class Impl:

        # The send_goal service using a wrapped version of the goal message as a request.
        from soarm100_interfaces.action._execute_planned_grasp import ExecutePlannedGrasp_SendGoal as SendGoalService
        # The get_result service using a wrapped version of the result message as a response.
        from soarm100_interfaces.action._execute_planned_grasp import ExecutePlannedGrasp_GetResult as GetResultService
        # The feedback message with generic fields which wraps the feedback message.
        from soarm100_interfaces.action._execute_planned_grasp import ExecutePlannedGrasp_FeedbackMessage as FeedbackMessage

        # The generic service to cancel a goal.
        from action_msgs.srv._cancel_goal import CancelGoal as CancelGoalService
        # The generic message for get the status of a goal.
        from action_msgs.msg._goal_status_array import GoalStatusArray as GoalStatusMessage

    def __init__(self):
        raise NotImplementedError('Action classes can not be instantiated')
