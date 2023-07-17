cmake_minimum_required(VERSION 3.5)
project(bt_tools_common)
find_package(ament_cmake REQUIRED)
ament_package()
install( # logos
  FILES doc/logo32p.png doc/logo.svg
  DESTINATION share/${PROJECT_NAME}/doc
)