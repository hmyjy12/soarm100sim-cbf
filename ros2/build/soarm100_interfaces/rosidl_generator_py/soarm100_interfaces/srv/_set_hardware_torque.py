# generated from rosidl_generator_py/resource/_idl.py.em
# with input from soarm100_interfaces:srv/SetHardwareTorque.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_SetHardwareTorque_Request(type):
    """Metaclass of message 'SetHardwareTorque_Request'."""

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
                'soarm100_interfaces.srv.SetHardwareTorque_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__set_hardware_torque__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__set_hardware_torque__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__set_hardware_torque__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__set_hardware_torque__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__set_hardware_torque__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class SetHardwareTorque_Request(metaclass=Metaclass_SetHardwareTorque_Request):
    """Message class 'SetHardwareTorque_Request'."""

    __slots__ = [
        '_enabled',
        '_confirmation',
    ]

    _fields_and_field_types = {
        'enabled': 'boolean',
        'confirmation': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.enabled = kwargs.get('enabled', bool())
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
        if self.enabled != other.enabled:
            return False
        if self.confirmation != other.confirmation:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def enabled(self):
        """Message field 'enabled'."""
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'enabled' field must be of type 'bool'"
        self._enabled = value

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


class Metaclass_SetHardwareTorque_Response(type):
    """Metaclass of message 'SetHardwareTorque_Response'."""

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
                'soarm100_interfaces.srv.SetHardwareTorque_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__set_hardware_torque__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__set_hardware_torque__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__set_hardware_torque__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__set_hardware_torque__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__set_hardware_torque__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class SetHardwareTorque_Response(metaclass=Metaclass_SetHardwareTorque_Response):
    """Message class 'SetHardwareTorque_Response'."""

    __slots__ = [
        '_success',
        '_reason',
    ]

    _fields_and_field_types = {
        'success': 'boolean',
        'reason': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.success = kwargs.get('success', bool())
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
        if self.success != other.success:
            return False
        if self.reason != other.reason:
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


class Metaclass_SetHardwareTorque(type):
    """Metaclass of service 'SetHardwareTorque'."""

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
                'soarm100_interfaces.srv.SetHardwareTorque')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__set_hardware_torque

            from soarm100_interfaces.srv import _set_hardware_torque
            if _set_hardware_torque.Metaclass_SetHardwareTorque_Request._TYPE_SUPPORT is None:
                _set_hardware_torque.Metaclass_SetHardwareTorque_Request.__import_type_support__()
            if _set_hardware_torque.Metaclass_SetHardwareTorque_Response._TYPE_SUPPORT is None:
                _set_hardware_torque.Metaclass_SetHardwareTorque_Response.__import_type_support__()


class SetHardwareTorque(metaclass=Metaclass_SetHardwareTorque):
    from soarm100_interfaces.srv._set_hardware_torque import SetHardwareTorque_Request as Request
    from soarm100_interfaces.srv._set_hardware_torque import SetHardwareTorque_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
