cmake_minimum_required(VERSION 3.20)
project(SegGen)
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

add_library(LEDA STATIC IMPORTED)
set_target_properties(LEDA PROPERTIES IMPORTED_LOCATION ${CMAKE_SOURCE_DIR}/../../adapters/deps/leda/libleda.a)
target_include_directories(LEDA INTERFACE ${CMAKE_SOURCE_DIR}/../../adapters/deps/leda/incl)

########################################################################################################################

function(add_gen_executable basename)
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

add_gen_executable(gen_leda_sweep_time_random DEFINES LIBS LEDA)
add_gen_executable(gen_leda_sweep_time_difficult DEFINES LIBS LEDA)
