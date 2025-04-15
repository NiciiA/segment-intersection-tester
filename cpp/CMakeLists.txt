cmake_minimum_required(VERSION 3.26)
project(SegGen)
set(CMAKE_CXX_STANDARD 20)

# Force static linking
set(CMAKE_FIND_LIBRARY_SUFFIXES .a)  # Prefer static libraries
set(BUILD_SHARED_LIBS OFF)           # Disable shared libraries

# Find OGDF
include_directories(${PROJECT_SOURCE_DIR}/OGDF/include)
link_directories(${PROJECT_SOURCE_DIR}/OGDF)

# Find Boost
find_package(Boost REQUIRED COMPONENTS filesystem system)
include_directories(${Boost_INCLUDE_DIRS})
link_directories(${Boost_LIBRARY_DIRS})

# Find CGAL
find_package(CGAL REQUIRED)
include_directories(${CGAL_INCLUDE_DIRS})

# Find GEOS
find_library(GEOS_LIB geos)

#add_executable(test_boost_r test_boost_x.cpp)
#target_compile_definitions(test_boost_r PRIVATE "NUMBER_TYPE=Rational")
#add_executable(test_boost_d test_boost_x.cpp)
#target_compile_definitions(test_boost_d PRIVATE "NUMBER_TYPE=Double")

# Create test executables
add_executable(test_cgal_intersector_ud test_cgal_intersector.cpp)
add_executable(test_cgal_arrangement_ud test_cgal_arrangement.cpp)
add_executable(test_cgal_arrangement_ur test_cgal_arrangement_rational.cpp)
add_executable(test_cgal_intersector_ur test_cgal_intersector_rational.cpp)
add_executable(test_cgal_pairwise_ud test_cgal_pairwise.cpp)
add_executable(test_cgal_pairwise_ur test_cgal_pairwise_rational.cpp)
add_executable(test_boost_d test_boost.cpp)
add_executable(test_boost_r test_boost_rational.cpp)
add_executable(test_ogdf_ud test_ogdf.cpp)
add_executable(test_geos test_geos.cpp)

# Link libraries for the test executables
target_link_libraries(test_cgal_intersector_ud ${CGAL_LIBRARIES})
target_link_libraries(test_cgal_arrangement_ud ${CGAL_LIBRARIES})
target_link_libraries(test_cgal_arrangement_ur ${CGAL_LIBRARIES})
target_link_libraries(test_cgal_intersector_ur ${CGAL_LIBRARIES})
target_link_libraries(test_cgal_pairwise_ud ${CGAL_LIBRARIES})
target_link_libraries(test_cgal_pairwise_ur ${CGAL_LIBRARIES})

target_link_libraries(test_boost_d ${Boost_LIBRARIES})
target_link_libraries(test_boost_r ${Boost_LIBRARIES} ${CGAL_LIBRARIES})

target_link_libraries(test_ogdf_ud ogdf)
target_link_libraries(test_geos ${GEOS_LIB} geos)
