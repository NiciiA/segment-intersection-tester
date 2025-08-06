cmake_minimum_required(VERSION 3.20)
project(SegGen-OGDF)
set(CMAKE_CXX_STANDARD 20)

#cmake_policy(SET CMP0167 NEW) # use non-vendored findBoost on too new CMake versions

if(CMAKE_BUILD_TYPE MATCHES DEBUG)
    add_compile_options(-g -fno-omit-frame-pointer -fno-inline)
    add_compile_options(-fsanitize=address)
    add_link_options(-fsanitize=address)
else()
    # add_compile_options(-g -fno-omit-frame-pointer)
    add_compile_options(-march=native)

    # Force static linking
    set(CMAKE_FIND_LIBRARY_SUFFIXES .a)
    set(BUILD_SHARED_LIBS OFF)
endif()

########################################################################################################################

find_package(OGDF REQUIRED)
find_package(Boost REQUIRED COMPONENTS iostreams)

add_executable(ogdf_to_segint ogdf_converter.cpp)
target_link_libraries(ogdf_to_segint OGDF Boost::iostreams)
