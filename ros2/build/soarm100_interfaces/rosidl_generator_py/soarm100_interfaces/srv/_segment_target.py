# generated from rosidl_generator_py/resource/_idl.py.em
# with input from soarm100_interfaces:srv/SegmentTarget.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_SegmentTarget_Request(type):
    """Metaclass of message 'SegmentTarget_Request'."""

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
                'soarm100_interfaces.srv.SegmentTarget_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__segment_target__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__segment_target__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__segment_target__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__segment_target__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__segment_target__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class SegmentTarget_Request(metaclass=Metaclass_SegmentTarget_Request):
    """Message class 'SegmentTarget_Request'."""

    __slots__ = [
        '_target_prompt',
        '_force_yolo',
    ]

    _fields_and_field_types = {
        'target_prompt': 'string',
        'force_yolo': 'boolean',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.target_prompt = kwargs.get('target_prompt', str())
        self.force_yolo = kwargs.get('force_yolo', bool())

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
        if self.force_yolo != other.force_yolo:
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
    def force_yolo(self):
        """Message field 'force_yolo'."""
        return self._force_yolo

    @force_yolo.setter
    def force_yolo(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'force_yolo' field must be of type 'bool'"
        self._force_yolo = value


# Import statements for member types

# already imported above
# import builtins

import math  # noqa: E402, I100

# Member 'bbox_xyxy'
import numpy  # noqa: E402, I100

# already imported above
# import rosidl_parser.definition


class Metaclass_SegmentTarget_Response(type):
    """Metaclass of message 'SegmentTarget_Response'."""

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
                'soarm100_interfaces.srv.SegmentTarget_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__segment_target__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__segment_target__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__segment_target__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__segment_target__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__segment_target__response

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


class SegmentTarget_Response(metaclass=Metaclass_SegmentTarget_Response):
    """Message class 'SegmentTarget_Response'."""

    __slots__ = [
        '_success',
        '_reason',
        '_target_center',
        '_score',
        '_bbox_xyxy',
        '_mask_topic',
        '_debug_json',
    ]

    _fields_and_field_types = {
        'success': 'boolean',
        'reason': 'string',
        'target_center': 'geometry_msgs/PoseStamped',
        'score': 'float',
        'bbox_xyxy': 'float[4]',
        'mask_topic': 'string',
        'debug_json': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'PoseStamped'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.Array(rosidl_parser.definition.BasicType('float'), 4),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.success = kwargs.get('success', bool())
        self.reason = kwargs.get('reason', str())
        from geometry_msgs.msg import PoseStamped
        self.target_center = kwargs.get('target_center', PoseStamped())
        self.score = kwargs.get('score', float())
        if 'bbox_xyxy' not in kwargs:
            self.bbox_xyxy = numpy.zeros(4, dtype=numpy.float32)
        else:
            self.bbox_xyxy = kwargs.get('bbox_xyxy')
        self.mask_topic = kwargs.get('mask_topic', str())
        self.debug_json = kwargs.get('debug_json', str())

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
        if self.target_center != other.target_center:
            return False
        if self.score != other.score:
            return False
        if any(self.bbox_xyxy != other.bbox_xyxy):
            return False
        if self.mask_topic != other.mask_topic:
            return False
        if self.debug_json != other.debug_json:
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
    def target_center(self):
        """Message field 'target_center'."""
        return self._target_center

    @target_center.setter
    def target_center(self, value):
        if __debug__:
            from geometry_msgs.msg import PoseStamped
            assert \
                isinstance(value, PoseStamped), \
                "The 'target_center' field must be a sub message of type 'PoseStamped'"
        self._target_center = value

    @builtins.property
    def score(self):
        """Message field 'score'."""
        return self._score

    @score.setter
    def score(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'score' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'score' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._score = value

    @builtins.property
    def bbox_xyxy(self):
        """Message field 'bbox_xyxy'."""
        return self._bbox_xyxy

    @bbox_xyxy.setter
    def bbox_xyxy(self, value):
        if isinstance(value, numpy.ndarray):
            assert value.dtype == numpy.float32, \
                "The 'bbox_xyxy' numpy.ndarray() must have the dtype of 'numpy.float32'"
            assert value.size == 4, \
                "The 'bbox_xyxy' numpy.ndarray() must have a size of 4"
            self._bbox_xyxy = value
            return
        if __debug__:
            from collections.abc import Sequence
            from collections.abc import Set
            from collections import UserList
            from collections import UserString
            assert \
                ((isinstance(value, Sequence) or
                  isinstance(value, Set) or
                  isinstance(value, UserList)) and
                 not isinstance(value, str) and
                 not isinstance(value, UserString) and
                 len(value) == 4 and
                 all(isinstance(v, float) for v in value) and
                 all(not (val < -3.402823466e+38 or val > 3.402823466e+38) or math.isinf(val) for val in value)), \
                "The 'bbox_xyxy' field must be a set or sequence with length 4 and each value of type 'float' and each float in [-340282346600000016151267322115014000640.000000, 340282346600000016151267322115014000640.000000]"
        self._bbox_xyxy = numpy.array(value, dtype=numpy.float32)

    @builtins.property
    def mask_topic(self):
        """Message field 'mask_topic'."""
        return self._mask_topic

    @mask_topic.setter
    def mask_topic(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'mask_topic' field must be of type 'str'"
        self._mask_topic = value

    @builtins.property
    def debug_json(self):
        """Message field 'debug_json'."""
        return self._debug_json

    @debug_json.setter
    def debug_json(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'debug_json' field must be of type 'str'"
        self._debug_json = value


class Metaclass_SegmentTarget(type):
    """Metaclass of service 'SegmentTarget'."""

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
                'soarm100_interfaces.srv.SegmentTarget')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__segment_target

            from soarm100_interfaces.srv import _segment_target
            if _segment_target.Metaclass_SegmentTarget_Request._TYPE_SUPPORT is None:
                _segment_target.Metaclass_SegmentTarget_Request.__import_type_support__()
            if _segment_target.Metaclass_SegmentTarget_Response._TYPE_SUPPORT is None:
                _segment_target.Metaclass_SegmentTarget_Response.__import_type_support__()


class SegmentTarget(metaclass=Metaclass_SegmentTarget):
    from soarm100_interfaces.srv._segment_target import SegmentTarget_Request as Request
    from soarm100_interfaces.srv._segment_target import SegmentTarget_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
