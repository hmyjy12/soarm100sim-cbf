cmake_minimum_required(VERSION 3.8)
project(so100_plus_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

install(PROGRAMS
  scripts/static_joint_publisher.py
  scripts/compare_fk_mujoco_urdf.py
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY urdf launch rviz
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/../../SO-ARM100/Simulation/SO100/mujoco/assets_plus/
  DESTINATION share/${PROJECT_NAME}/meshes
  FILES_MATCHING PATTERN "*.STL"
)

ament_package()
