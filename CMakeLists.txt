cmake_minimum_required(VERSION 3.5 FATAL_ERROR)
project(analyzer LANGUAGES CXX)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/bin")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/lib")

if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
  message(STATUS "Configuring on/for Linux")
endif()

find_package(ROOT 6 REQUIRED)
find_package(yaml-cpp REQUIRED)
find_package(Boost REQUIRED
  COMPONENTS program_options
)


set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

#add_compile_options(-Wall -Wextra -pedantic)

add_library(utils STATIC 
  src/FileInPath.cc
  src/Options.cc)
target_include_directories(utils PUBLIC include)
target_link_libraries(utils
  PRIVATE stdc++fs
  PUBLIC Boost::boost Boost::program_options
  PUBLIC yaml-cpp
)

add_executable(tuple src/analyzer.cc)
add_executable(plotter src/plotter.cc)
target_link_libraries(tuple
  PRIVATE utils
  PUBLIC ROOT::Hist ROOT::ROOTDataFrame ROOT::Tree
)
target_link_libraries(plotter
  PRIVATE utils
  PUBLIC ROOT::Hist
)
