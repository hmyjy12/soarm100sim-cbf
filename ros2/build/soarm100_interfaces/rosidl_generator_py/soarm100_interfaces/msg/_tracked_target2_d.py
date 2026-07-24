# generated from rosidl_generator_py/resource/_idl.py.em
# with input from soarm100_interfaces:msg/TrackedTarget2D.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_TrackedTarget2D(type):
    """Metaclass of message 'TrackedTarget2D'."""

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
                'soarm100_interfaces.msg.TrackedTarget2D')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__tracked_target2_d
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__tracked_target2_d
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__tracked_target2_d
            cls._TYPE_SUPPORT = module.type_support_msg__msg__tracked_target2_d
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__tracked_target2_d

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class TrackedTarget2D(metaclass=Metaclass_TrackedTarget2D):
    """Message class 'TrackedTarget2D'."""

    __slots__ = [
        '_header',
        '_valid',
        '_u',
        '_v',
        '_reference_u',
        '_reference_v',
        '_delta_u',
        '_delta_v',
        '_width',
        '_height',
        '_image_width',
        '_image_height',
        '_confidence',
        '_lost_frames',
        '_replan_required',
        '_reason',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'valid': 'boolean',
        'u': 'float',
        'v': 'float',
        'reference_u': 'float',
        'reference_v': 'float',
        'delta_u': 'float',
        'delta_v': 'float',
        'width': 'float',
        'height': 'float',
        'image_width': 'uint32',
        'image_height': 'uint32',
        'confidence': 'float',
        'lost_frames': 'uint32',
        'replan_required': 'boolean',
        'reason': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.valid = kwargs.get('valid', bool())
        self.u = kwargs.get('u', float())
        self.v = kwargs.get('v', float())
        self.reference_u = kwargs.get('reference_u', float())
        self.reference_v = kwargs.get('reference_v', float())
        self.delta_u = kwargs.get('delta_u', float())
        self.delta_v = kwargs.get('delta_v', float())
        self.width = kwargs.get('width', float())
        self.height = kwargs.get('height', float())
        self.image_width = kwargs.get('image_width', int())
        self.image_height = kwargs.get('image_height', int())
        self.confidence = kwargs.get('confidence', float())
        self.lost_frames = kwargs.get('lost_frames', int())
        self.replan_required = kwargs.get('replan_required', bool())
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
        if self.header != other.header:
            return False
        if self.valid != other.valid:
            return False
        if self.u != other.u:
            return False
        if self.v != other.v:
            return False
        if self.reference_u != other.reference_u:
            return False
        if self.reference_v != other.reference_v:
            return False
        if self.delta_u != other.delta_u:
            return False
        if self.delta_v != other.delta_v:
            return False
        if self.width != other.width:
            return False
        if self.height != other.height:
            return False
        if self.image_width != other.image_width:
            return False
        if self.image_height != other.image_height:
            return False
        if self.confidence != other.confidence:
            return False
        if self.lost_frames != other.lost_frames:
            return False
        if self.replan_required != other.replan_required:
            return False
        if self.reason != other.reason:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def header(self):
        """Message field 'header'."""
        return self._header

    @header.setter
    def header(self, value):
        if __debug__:
            from std_msgs.msg import Header
            assert \
                isinstance(value, Header), \
                "The 'header' field must be a sub message of type 'Header'"
        self._header = value

    @builtins.property
    def valid(self):
        """Message field 'valid'."""
        return self._valid

    @valid.setter
    def valid(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'valid' field must be of type 'bool'"
        self._valid = value

    @builtins.property
    def u(self):
        """Message field 'u'."""
        return self._u

    @u.setter
    def u(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'u' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'u' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._u = value

    @builtins.property
    def v(self):
        """Message field 'v'."""
        return self._v

    @v.setter
    def v(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'v' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'v' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._v = value

    @builtins.property
    def reference_u(self):
        """Message field 'reference_u'."""
        return self._reference_u

    @reference_u.setter
    def reference_u(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'reference_u' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'reference_u' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._reference_u = value

    @builtins.property
    def reference_v(self):
        """Message field 'reference_v'."""
        return self._reference_v

    @reference_v.setter
    def reference_v(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'reference_v' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'reference_v' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._reference_v = value

    @builtins.property
    def delta_u(self):
        """Message field 'delta_u'."""
        return self._delta_u

    @delta_u.setter
    def delta_u(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'delta_u' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'delta_u' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._delta_u = value

    @builtins.property
    def delta_v(self):
        """Message field 'delta_v'."""
        return self._delta_v

    @delta_v.setter
    def delta_v(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'delta_v' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'delta_v' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._delta_v = value

    @builtins.property
    def width(self):
        """Message field 'width'."""
        return self._width

    @width.setter
    def width(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'width' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'width' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._width = value

    @builtins.property
    def height(self):
        """Message field 'height'."""
        return self._height

    @height.setter
    def height(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'height' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'height' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._height = value

    @builtins.property
    def image_width(self):
        """Message field 'image_width'."""
        return self._image_width

    @image_width.setter
    def image_width(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'image_width' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'image_width' field must be an unsigned integer in [0, 4294967295]"
        self._image_width = value

    @builtins.property
    def image_height(self):
        """Message field 'image_height'."""
        return self._image_height

    @image_height.setter
    def image_height(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'image_height' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'image_height' field must be an unsigned integer in [0, 4294967295]"
        self._image_height = value

    @builtins.property
    def confidence(self):
        """Message field 'confidence'."""
        return self._confidence

    @confidence.setter
    def confidence(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'confidence' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'confidence' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._confidence = value

    @builtins.property
    def lost_frames(self):
        """Message field 'lost_frames'."""
        return self._lost_frames

    @lost_frames.setter
    def lost_frames(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'lost_frames' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'lost_frames' field must be an unsigned integer in [0, 4294967295]"
        self._lost_frames = value

    @builtins.property
    def replan_required(self):
        """Message field 'replan_required'."""
        return self._replan_required

    @replan_required.setter
    def replan_required(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'replan_required' field must be of type 'bool'"
        self._replan_required = value

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
