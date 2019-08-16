cmake_minimum_required(VERSION 2.8)
project( DisplayImage )
find_package( OpenCV REQUIRED )

add_executable( display src/display_img.cpp )
target_link_libraries( display ${OpenCV_LIBS} )

add_executable( detection src/object_detection.cpp )
target_link_libraries( detection ${OpenCV_LIBS} )
