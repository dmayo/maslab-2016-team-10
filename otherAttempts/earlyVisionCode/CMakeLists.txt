cmake_minimum_required(VERSION 2.8)
project( DetectObjects )
find_package( OpenCV REQUIRED )
add_executable( DetectObjects DetectObjects.cpp )
target_link_libraries( DetectObjects ${OpenCV_LIBS} )
