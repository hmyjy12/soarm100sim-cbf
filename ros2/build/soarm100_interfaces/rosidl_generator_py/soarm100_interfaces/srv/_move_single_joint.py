# generated from rosidl_generator_py/resource/_idl.py.em
# with input from soarm100_interfaces:srv/MoveSingleJoint.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_MoveSingleJoint_Request(type):
    """Metaclass of message 'MoveSingleJoint_Request'."""

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
                'soarm100_interfaces.srv.MoveSingleJoint_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__move_single_joint__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__move_single_joint__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__move_single_joint__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__move_single_joint__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__move_single_joint__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class MoveSingleJoint_Request(metaclass=Metaclass_MoveSingleJoint_Request):
    """Message class 'MoveSingleJoint_Request'."""

    __slots__ = [
        '_joint',
        '_delta_deg',
        '_duration',
        '_hold',
        '_confirmation',
    ]

    _fields_and_field_types = {
        'joint': 'string',
        'delta_deg': 'double',
        'duration': 'double',
        'hold': 'double',
        'confirmation': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.BasicType('double'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.joint = kwargs.get('joint', str())
        self.delta_deg = kwargs.get('delta_deg', float())
        self.duration = kwargs.get('duration', float())
        self.hold = kwargs.get('hold', float())
        self.confirmation = kwargs.get('confirmation', str())

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
        if self.joint != other.joint:
            return False
        if self.delta_deg != other.delta_deg:
            return False
        if self.duration != other.duration:
            return False
        if self.hold != other.hold:
            return False
        if self.confirmation != other.confirmation:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def joint(self):
        """Message field 'joint'."""
        return self._joint

    @joint.setter
    def joint(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'joint' field must be of type 'str'"
        self._joint = value

    @builtins.property
    def delta_deg(self):
        """Message field 'delta_deg'."""
        return self._delta_deg

    @delta_deg.setter
    def delta_deg(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'delta_deg' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'delta_deg' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._delta_deg = value

    @builtins.property
    def duration(self):
        """Message field 'duration'."""
        return self._duration

    @duration.setter
    def duration(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'duration' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'duration' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._duration = value

    @builtins.property
    def hold(self):
        """Message field 'hold'."""
        return self._hold

    @hold.setter
    def hold(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'hold' field must be of type 'float'"
            assert not (value < -1.7976931348623157e+308 or value > 1.7976931348623157e+308) or math.isinf(value), \
                "The 'hold' field must be a double in [-1.7976931348623157e+308, 1.7976931348623157e+308]"
        self._hold = value

    @builtins.property
    def confirmation(self):
        """Message field 'confirmation'."""
        return self._confirmation

    @confirmation.setter
    def confirmation(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'confirmation' field must be of type 'str'"
        self._confirmation = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_MoveSingleJoint_Response(type):
    """Metaclass of message 'MoveSingleJoint_Response'."""

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
                'soarm100_interfaces.srv.MoveSingleJoint_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__move_single_joint__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__move_single_joint__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__move_single_joint__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__move_single_joint__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__move_single_joint__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class MoveSingleJoint_Response(metaclass=Metaclass_MoveSingleJoint_Response):
    """Message class 'MoveSingleJoint_Response'."""

    __slots__ = [
        '_success',
        '_reason',
        '_log_path',
    ]

    _fields_and_field_types = {
        'success': 'boolean',
        'reason': 'string',
        'log_path': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.success = kwargs.get('success', bool())
        self.reason = kwargs.get('reason', str())
        self.log_path = kwargs.get('log_path', str())

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
        if self.log_path != other.log_path:
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
    def log_path(self):
        """Message field 'log_path'."""
        return self._log_path

    @log_path.setter
    def log_path(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'log_path' field must be of type 'str'"
        self._log_path = value


class Metaclass_MoveSingleJoint(type):
    """Metaclass of service 'MoveSingleJoint'."""

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
                'soarm100_interfaces.srv.MoveSingleJoint')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__move_single_joint

            from soarm100_interfaces.srv import _move_single_joint
            if _move_single_joint.Metaclass_MoveSingleJoint_Request._TYPE_SUPPORT is None:
                _move_single_joint.Metaclass_MoveSingleJoint_Request.__import_type_support__()
            if _move_single_joint.Metaclass_MoveSingleJoint_Response._TYPE_SUPPORT is None:
                _move_single_joint.Metaclass_MoveSingleJoint_Response.__import_type_support__()


class MoveSingleJoint(metaclass=Metaclass_MoveSingleJoint):
    from soarm100_interfaces.srv._move_single_joint import MoveSingleJoint_Request as Request
    from soarm100_interfaces.srv._move_single_joint import MoveSingleJoint_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
