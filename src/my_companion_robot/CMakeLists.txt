cmake_minimum_required(VERSION 3.8)
project(my_companion_robot)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)

ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/hooks/resource_paths.dsv.in")

install(
  DIRECTORY urdf launch meshes rviz
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
