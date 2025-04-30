cmake_minimum_required(VERSION 3.30)
project(SegGen)
set(CMAKE_CXX_STANDARD 20)

cmake_policy(SET CMP0167 NEW) # use non-vendored findBoost

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

find_package(OGDF REQUIRED)

find_package(Boost REQUIRED COMPONENTS filesystem system)
#target_include_directories(${Boost_INCLUDE_DIRS})
#target_link_directories(${Boost_LIBRARY_DIRS})

find_package(CGAL REQUIRED)
#target_include_directories(${CGAL_INCLUDE_DIRS})

find_package(GEOS CONFIG REQUIRED)

########################################################################################################################

add_library(LEDA STATIC IMPORTED)
set_target_properties(LEDA PROPERTIES IMPORTED_LOCATION ${CMAKE_SOURCE_DIR}/../leda/libleda.a)
target_include_directories(LEDA INTERFACE ${CMAKE_SOURCE_DIR}/../leda/incl)

########################################################################################################################

function(add_test_executable basename)
    set(multiValueArgs DEFINES LIBS INCLS)
    cmake_parse_arguments(PARSE_ARGV 1 arg
            "" "SUFFIX" "${multiValueArgs}")

    if (NOT DEFINED arg_SUFFIX)
        SET(targetname "${basename}")
    else ()
        SET(targetname "${basename}-${arg_SUFFIX}")
    endif ()

    add_executable("${targetname}" "${basename}.cpp")
    if (DEFINED arg_DEFINES)
        target_compile_definitions("${targetname}" PRIVATE ${arg_DEFINES})
    endif ()
    if (DEFINED arg_LIBS)
        target_link_libraries("${targetname}" ${arg_LIBS})
    endif ()
    if (DEFINED arg_INCLS)
        target_include_directories("${targetname}" ${arg_INCLS})
    endif ()
endfunction()

########################################################################################################################

add_test_executable(test_boost SUFFIX d DEFINES NUMBER_TYPE=Double LIBS ${Boost_LIBRARIES})
add_test_executable(test_boost SUFFIX r DEFINES NUMBER_TYPE=Rational LIBS ${Boost_LIBRARIES})
add_test_executable(test_cgal_arrangement LIBS ${CGAL_LIBRARIES})
add_test_executable(test_cgal_intersector LIBS ${CGAL_LIBRARIES})
add_test_executable(test_cgal_pairwise LIBS ${CGAL_LIBRARIES})
add_test_executable(test_leda SUFFIX mm-d DEFINES ALGO=MULMULEY_SEGMENTS ALGO_GRAPH LIBS LEDA)
add_test_executable(test_leda SUFFIX bo-d DEFINES ALGO=SWEEP_SEGMENTS ALGO_GRAPH LIBS LEDA)
add_test_executable(test_leda SUFFIX ba-d DEFINES ALGO=BALABAN_SEGMENTS ALGO_REPORT LIBS LEDA)
add_test_executable(test_leda SUFFIX tr-d DEFINES ALGO=TRIVIAL_SEGMENTS ALGO_REPORT LIBS LEDA)
add_test_executable(test_leda SUFFIX pw-d DEFINES LIBS LEDA)
add_test_executable(test_leda SUFFIX mm-r DEFINES ALGO=MULMULEY_SEGMENTS ALGO_GRAPH RATIONAL LIBS LEDA)
add_test_executable(test_leda SUFFIX bo-r DEFINES ALGO=SWEEP_SEGMENTS ALGO_GRAPH RATIONAL LIBS LEDA)
add_test_executable(test_leda SUFFIX ba-r DEFINES ALGO=BALABAN_SEGMENTS ALGO_REPORT RATIONAL LIBS LEDA)
add_test_executable(test_leda SUFFIX tr-r DEFINES ALGO=TRIVIAL_SEGMENTS ALGO_REPORT RATIONAL LIBS LEDA)
add_test_executable(test_leda SUFFIX pw-r DEFINES RATIONAL LIBS LEDA)
add_test_executable(test_ogdf LIBS OGDF)
add_test_executable(test_geos LIBS GEOS::geos)
