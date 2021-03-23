cmake_minimum_required(VERSION 3.0.2)
project(flask_sdp_main)
find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  flask_msgs
)
include_directories(
#include
  ${catkin_INCLUDE_DIRS}
)

