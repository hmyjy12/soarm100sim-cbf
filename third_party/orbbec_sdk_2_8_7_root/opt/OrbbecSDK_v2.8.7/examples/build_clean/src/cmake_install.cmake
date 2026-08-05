# Install script for directory: /home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/src

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/utils/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/c_examples/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/0.basic.enumerate/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/1.stream.imu/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/2.device.control/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/2.device.firmware_update/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/2.device.forceip/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/2.device.optional_depth_presets_update/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/2.device.record.nogui/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/2.device.hot_plugin/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/3.advanced.point_cloud/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/3.advanced.preset/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/4.misc.logger/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/4.misc.metadata/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/0.basic.quick_start/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/1.stream.depth/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/1.stream.color/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/1.stream.confidence/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/1.stream.infrared/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/1.stream.callback/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/1.stream.multi_streams/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/1.stream.decimation/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/2.device.record/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/2.device.playback/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/3.advanced.common_usages/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/3.advanced.sync_align/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/3.advanced.hw_d2c_align/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/3.advanced.post_processing/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/3.advanced.coordinate_transform/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/3.advanced.hdr/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/3.advanced.laser_interleave/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/3.advanced.multi_devices/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/3.advanced.multi_devices_sync/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/4.misc.save_to_disk/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/5.wrapper.opencv/cmake_install.cmake")
  include("/home/sophie/isaac_lab/isaac_ws/rl_code/soarm100sim/third_party/orbbec_sdk_2_8_7_root/opt/OrbbecSDK_v2.8.7/examples/build_clean/src/lidar_examples/cmake_install.cmake")

endif()

