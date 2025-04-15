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

# Common source files
set(COMMON_SOURCES
        BO/bentley_ottmann.cpp
        BO/bentley_ottmann.hpp
        BO/geometry.cpp
        BO/geometry.hpp
        BO/integer_type.hpp
        BO/structures.hpp
)

# Main executable (SegGen)
add_executable(SegGen main.cpp ${COMMON_SOURCES})
target_link_libraries(SegGen ${Boost_LIBRARIES} ${CGAL_LIBRARIES} ${GEOS_LIB} ogdf geos)

# Create test executables
add_executable(test_cgal_intersector_ud test_cgal_intersector.cpp ${COMMON_SOURCES})
add_executable(test_cgal_arrangement_ud test_cgal_arrangement.cpp ${COMMON_SOURCES})
add_executable(test_cgal_arrangement_ur test_cgal_arrangement_rational.cpp ${COMMON_SOURCES})
# add_executable(test_cgal_arrangement_ur_f test_cgal_arrangement_rational_f.cpp ${COMMON_SOURCES})
add_executable(test_cgal_intersector_ur test_cgal_intersector_rational.cpp ${COMMON_SOURCES})
# add_executable(test_cgal_intersector_ur_f test_cgal_intersector_rational_f.cpp ${COMMON_SOURCES})
add_executable(test_boost_d test_boost.cpp ${COMMON_SOURCES})
add_executable(test_boost_r test_boost_rational.cpp ${COMMON_SOURCES})
# add_executable(test_boost_r_f test_boost_rational_f.cpp ${COMMON_SOURCES})
add_executable(test_ogdf_ud test_ogdf.cpp ${COMMON_SOURCES})
add_executable(ogdf_1 ogdf_1.cpp ${COMMON_SOURCES})
add_executable(ogdf_2 ogdf_2.cpp ${COMMON_SOURCES})
add_executable(test_bo_d test_bo.cpp ${COMMON_SOURCES})
# add_executable(test_geos test_geos.cpp ${COMMON_SOURCES})


add_executable(tester tester.cpp ${COMMON_SOURCES})

# Link libraries for the test executables
target_link_libraries(test_cgal_intersector_ud ${Boost_LIBRARIES} ${CGAL_LIBRARIES} ${GEOS_LIB} ogdf)
target_link_libraries(test_cgal_arrangement_ud ${Boost_LIBRARIES} ${CGAL_LIBRARIES} ${GEOS_LIB} ogdf)
target_link_libraries(test_cgal_arrangement_ur ${Boost_LIBRARIES} ${CGAL_LIBRARIES} ${GEOS_LIB} ogdf)
# target_link_libraries(test_cgal_arrangement_ur_f ${Boost_LIBRARIES} ${CGAL_LIBRARIES} ${GEOS_LIB} ogdf)
target_link_libraries(test_cgal_intersector_ur ${Boost_LIBRARIES} ${CGAL_LIBRARIES} ${GEOS_LIB} ogdf)
# target_link_libraries(test_cgal_intersector_ur_f ${Boost_LIBRARIES} ${CGAL_LIBRARIES} ${GEOS_LIB} ogdf)
target_link_libraries(test_boost_d ${Boost_LIBRARIES} ${CGAL_LIBRARIES} ${GEOS_LIB} ogdf)
target_link_libraries(test_boost_r ${Boost_LIBRARIES} ${CGAL_LIBRARIES} ${GEOS_LIB} ogdf)
# target_link_libraries(test_boost_r_f ${Boost_LIBRARIES} ${CGAL_LIBRARIES} ${GEOS_LIB} ogdf)
target_link_libraries(test_ogdf_ud ${Boost_LIBRARIES} ${CGAL_LIBRARIES} ${GEOS_LIB} ogdf)
target_link_libraries(ogdf_1 ${Boost_LIBRARIES} ${CGAL_LIBRARIES} ${GEOS_LIB} ogdf)
target_link_libraries(ogdf_2 ${Boost_LIBRARIES} ${CGAL_LIBRARIES} ${GEOS_LIB} ogdf)
target_link_libraries(test_bo_d ${Boost_LIBRARIES} ${CGAL_LIBRARIES} ${GEOS_LIB} ogdf)
# target_link_libraries(test_geos ${Boost_LIBRARIES} ${CGAL_LIBRARIES} ${GEOS_LIB} ogdf geos)
