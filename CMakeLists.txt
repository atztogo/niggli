cmake_minimum_required(VERSION 2.4)

project(niggli C)
set(CMAKE_MACOSX_RPATH 1)
set(CMAKE_C_FLAGS_RELEASE "-Wall -O2")
set(CMAKE_C_FLAGS_DEBUG "-g -fsanitize=address -DTHMWARNING -DMATWARNING -DKPTWARNING")
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif(NOT CMAKE_BUILD_TYPE)
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")

include(GNUInstallDirs)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)


# Version numbers
file(READ ${PROJECT_SOURCE_DIR}/src/niggli.h version_file)
string(REGEX MATCH "NIGGLI_MAJOR_VERSION ([0-9]+)" niggli_major_version ${version_file})
set(niggli_major_version ${CMAKE_MATCH_1})
string(REGEX MATCH "NIGGLI_MINOR_VERSION ([0-9]+)" niggli_minor_version ${version_file})
set(niggli_minor_version ${CMAKE_MATCH_1})
string(REGEX MATCH "NIGGLI_MICRO_VERSION ([0-9]+)" niggli_micro_version ${version_file})
set(niggli_micro_version ${CMAKE_MATCH_1})
set(serial "${niggli_major_version}.${niggli_minor_version}.${niggli_micro_version}")
set(soserial "1")

# Source code
include_directories("${PROJECT_SOURCE_DIR}/src")
set(SOURCES ${PROJECT_SOURCE_DIR}/src/niggli.c)

# Shared library
add_library(niggli SHARED ${SOURCES})

if(NOT MSVC)
  target_link_libraries(niggli m)
endif()
set_property(TARGET niggli PROPERTY VERSION ${serial})
set_property(TARGET niggli PROPERTY SOVERSION ${soserial})
install(TARGETS niggli LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR})

# Static link library
add_library(niggli_static STATIC ${SOURCES})
set_property(TARGET niggli_static PROPERTY VERSION ${serial})
set_property(TARGET niggli_static PROPERTY SOVERSION ${soserial})
set_property(TARGET niggli_static PROPERTY OUTPUT_NAME niggli)
install(TARGETS niggli_static ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})

# Header file
install(FILES ${PROJECT_SOURCE_DIR}/src/niggli.h DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

# Test: just for checking no crash
add_executable(nigglitest EXCLUDE_FROM_ALL ${PROJECT_SOURCE_DIR}/test/test.c ${SOURCES})
configure_file(${PROJECT_SOURCE_DIR}/test/lattice_ravel.dat ${CMAKE_CURRENT_BINARY_DIR}/lattice_ravel.dat COPYONLY)
configure_file(${PROJECT_SOURCE_DIR}/test/lattice_large_L_ravel.dat ${CMAKE_CURRENT_BINARY_DIR}/lattice_large_L_ravel.dat COPYONLY)
if(NOT MSVC)
  target_link_libraries(nigglitest m)
endif()
enable_testing()
add_test(nigglitest nigglitest)

# cf. https://stackoverflow.com/questions/5709914/using-cmake-how-do-i-get-verbose-output-from-ctest
add_custom_target(check
        ${CMAKE_COMMAND} -E echo CWD=${CMAKE_BINARY_DIR}
        COMMAND ${CMAKE_COMMAND} -E echo CMD=${CMAKE_CTEST_COMMAND} -C $<CONFIG>
        COMMAND ${CMAKE_COMMAND} -E echo ----------------------------------
        COMMAND ${CMAKE_COMMAND} -E env CTEST_OUTPUT_ON_FAILURE=1
            ${CMAKE_CTEST_COMMAND} -C $<CONFIG> --verbose
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    DEPENDS nigglitest
    )
