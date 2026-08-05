# generated from rosidl_generator_py/resource/_idl.py.em
# with input from orbbec_camera_msgs:srv/GetDeviceConfig.idl
# generated code does not contain a copyright notice


# Import statements for member types

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_GetDeviceConfig_Request(type):
    """Metaclass of message 'GetDeviceConfig_Request'."""

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
            module = import_type_support('orbbec_camera_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'orbbec_camera_msgs.srv.GetDeviceConfig_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__get_device_config__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__get_device_config__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__get_device_config__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__get_device_config__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__get_device_config__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class GetDeviceConfig_Request(metaclass=Metaclass_GetDeviceConfig_Request):
    """Message class 'GetDeviceConfig_Request'."""

    __slots__ = [
    ]

    _fields_and_field_types = {
    }

    SLOT_TYPES = (
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))

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
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)


# Import statements for member types

import builtins  # noqa: E402, I100

# already imported above
# import rosidl_parser.definition


class Metaclass_GetDeviceConfig_Response(type):
    """Metaclass of message 'GetDeviceConfig_Response'."""

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
            module = import_type_support('orbbec_camera_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'orbbec_camera_msgs.srv.GetDeviceConfig_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__get_device_config__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__get_device_config__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__get_device_config__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__get_device_config__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__get_device_config__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class GetDeviceConfig_Response(metaclass=Metaclass_GetDeviceConfig_Response):
    """Message class 'GetDeviceConfig_Response'."""

    __slots__ = [
        '_schema_version',
        '_device_preset',
        '_preset_version',
        '_color_preset',
        '_depth_precision',
        '_disparity_to_depth_mode',
        '_exposure_range_mode',
        '_depth_registration',
        '_align_mode',
        '_align_target_stream',
        '_frame_aggregate_mode',
        '_enable_frame_sync',
        '_time_domain',
        '_sync_mode',
        '_intra_camera_sync_reference',
        '_data_json',
        '_success',
        '_message',
    ]

    _fields_and_field_types = {
        'schema_version': 'string',
        'device_preset': 'string',
        'preset_version': 'string',
        'color_preset': 'string',
        'depth_precision': 'string',
        'disparity_to_depth_mode': 'string',
        'exposure_range_mode': 'string',
        'depth_registration': 'boolean',
        'align_mode': 'string',
        'align_target_stream': 'string',
        'frame_aggregate_mode': 'string',
        'enable_frame_sync': 'boolean',
        'time_domain': 'string',
        'sync_mode': 'string',
        'intra_camera_sync_reference': 'string',
        'data_json': 'string',
        'success': 'boolean',
        'message': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.schema_version = kwargs.get('schema_version', str())
        self.device_preset = kwargs.get('device_preset', str())
        self.preset_version = kwargs.get('preset_version', str())
        self.color_preset = kwargs.get('color_preset', str())
        self.depth_precision = kwargs.get('depth_precision', str())
        self.disparity_to_depth_mode = kwargs.get('disparity_to_depth_mode', str())
        self.exposure_range_mode = kwargs.get('exposure_range_mode', str())
        self.depth_registration = kwargs.get('depth_registration', bool())
        self.align_mode = kwargs.get('align_mode', str())
        self.align_target_stream = kwargs.get('align_target_stream', str())
        self.frame_aggregate_mode = kwargs.get('frame_aggregate_mode', str())
        self.enable_frame_sync = kwargs.get('enable_frame_sync', bool())
        self.time_domain = kwargs.get('time_domain', str())
        self.sync_mode = kwargs.get('sync_mode', str())
        self.intra_camera_sync_reference = kwargs.get('intra_camera_sync_reference', str())
        self.data_json = kwargs.get('data_json', str())
        self.success = kwargs.get('success', bool())
        self.message = kwargs.get('message', str())

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
        if self.schema_version != other.schema_version:
            return False
        if self.device_preset != other.device_preset:
            return False
        if self.preset_version != other.preset_version:
            return False
        if self.color_preset != other.color_preset:
            return False
        if self.depth_precision != other.depth_precision:
            return False
        if self.disparity_to_depth_mode != other.disparity_to_depth_mode:
            return False
        if self.exposure_range_mode != other.exposure_range_mode:
            return False
        if self.depth_registration != other.depth_registration:
            return False
        if self.align_mode != other.align_mode:
            return False
        if self.align_target_stream != other.align_target_stream:
            return False
        if self.frame_aggregate_mode != other.frame_aggregate_mode:
            return False
        if self.enable_frame_sync != other.enable_frame_sync:
            return False
        if self.time_domain != other.time_domain:
            return False
        if self.sync_mode != other.sync_mode:
            return False
        if self.intra_camera_sync_reference != other.intra_camera_sync_reference:
            return False
        if self.data_json != other.data_json:
            return False
        if self.success != other.success:
            return False
        if self.message != other.message:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def schema_version(self):
        """Message field 'schema_version'."""
        return self._schema_version

    @schema_version.setter
    def schema_version(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'schema_version' field must be of type 'str'"
        self._schema_version = value

    @builtins.property
    def device_preset(self):
        """Message field 'device_preset'."""
        return self._device_preset

    @device_preset.setter
    def device_preset(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'device_preset' field must be of type 'str'"
        self._device_preset = value

    @builtins.property
    def preset_version(self):
        """Message field 'preset_version'."""
        return self._preset_version

    @preset_version.setter
    def preset_version(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'preset_version' field must be of type 'str'"
        self._preset_version = value

    @builtins.property
    def color_preset(self):
        """Message field 'color_preset'."""
        return self._color_preset

    @color_preset.setter
    def color_preset(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'color_preset' field must be of type 'str'"
        self._color_preset = value

    @builtins.property
    def depth_precision(self):
        """Message field 'depth_precision'."""
        return self._depth_precision

    @depth_precision.setter
    def depth_precision(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'depth_precision' field must be of type 'str'"
        self._depth_precision = value

    @builtins.property
    def disparity_to_depth_mode(self):
        """Message field 'disparity_to_depth_mode'."""
        return self._disparity_to_depth_mode

    @disparity_to_depth_mode.setter
    def disparity_to_depth_mode(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'disparity_to_depth_mode' field must be of type 'str'"
        self._disparity_to_depth_mode = value

    @builtins.property
    def exposure_range_mode(self):
        """Message field 'exposure_range_mode'."""
        return self._exposure_range_mode

    @exposure_range_mode.setter
    def exposure_range_mode(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'exposure_range_mode' field must be of type 'str'"
        self._exposure_range_mode = value

    @builtins.property
    def depth_registration(self):
        """Message field 'depth_registration'."""
        return self._depth_registration

    @depth_registration.setter
    def depth_registration(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'depth_registration' field must be of type 'bool'"
        self._depth_registration = value

    @builtins.property
    def align_mode(self):
        """Message field 'align_mode'."""
        return self._align_mode

    @align_mode.setter
    def align_mode(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'align_mode' field must be of type 'str'"
        self._align_mode = value

    @builtins.property
    def align_target_stream(self):
        """Message field 'align_target_stream'."""
        return self._align_target_stream

    @align_target_stream.setter
    def align_target_stream(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'align_target_stream' field must be of type 'str'"
        self._align_target_stream = value

    @builtins.property
    def frame_aggregate_mode(self):
        """Message field 'frame_aggregate_mode'."""
        return self._frame_aggregate_mode

    @frame_aggregate_mode.setter
    def frame_aggregate_mode(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'frame_aggregate_mode' field must be of type 'str'"
        self._frame_aggregate_mode = value

    @builtins.property
    def enable_frame_sync(self):
        """Message field 'enable_frame_sync'."""
        return self._enable_frame_sync

    @enable_frame_sync.setter
    def enable_frame_sync(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'enable_frame_sync' field must be of type 'bool'"
        self._enable_frame_sync = value

    @builtins.property
    def time_domain(self):
        """Message field 'time_domain'."""
        return self._time_domain

    @time_domain.setter
    def time_domain(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'time_domain' field must be of type 'str'"
        self._time_domain = value

    @builtins.property
    def sync_mode(self):
        """Message field 'sync_mode'."""
        return self._sync_mode

    @sync_mode.setter
    def sync_mode(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'sync_mode' field must be of type 'str'"
        self._sync_mode = value

    @builtins.property
    def intra_camera_sync_reference(self):
        """Message field 'intra_camera_sync_reference'."""
        return self._intra_camera_sync_reference

    @intra_camera_sync_reference.setter
    def intra_camera_sync_reference(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'intra_camera_sync_reference' field must be of type 'str'"
        self._intra_camera_sync_reference = value

    @builtins.property
    def data_json(self):
        """Message field 'data_json'."""
        return self._data_json

    @data_json.setter
    def data_json(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'data_json' field must be of type 'str'"
        self._data_json = value

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
    def message(self):
        """Message field 'message'."""
        return self._message

    @message.setter
    def message(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'message' field must be of type 'str'"
        self._message = value


class Metaclass_GetDeviceConfig(type):
    """Metaclass of service 'GetDeviceConfig'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('orbbec_camera_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'orbbec_camera_msgs.srv.GetDeviceConfig')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__get_device_config

            from orbbec_camera_msgs.srv import _get_device_config
            if _get_device_config.Metaclass_GetDeviceConfig_Request._TYPE_SUPPORT is None:
                _get_device_config.Metaclass_GetDeviceConfig_Request.__import_type_support__()
            if _get_device_config.Metaclass_GetDeviceConfig_Response._TYPE_SUPPORT is None:
                _get_device_config.Metaclass_GetDeviceConfig_Response.__import_type_support__()


class GetDeviceConfig(metaclass=Metaclass_GetDeviceConfig):
    from orbbec_camera_msgs.srv._get_device_config import GetDeviceConfig_Request as Request
    from orbbec_camera_msgs.srv._get_device_config import GetDeviceConfig_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
