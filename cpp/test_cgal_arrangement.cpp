#include "utils_cgal.h"

#include <CGAL/Arrangement_2.h>
#include <CGAL/Arr_segment_traits_2.h>

typedef CGAL::Arr_segment_traits_2<K> CGAL_Traits;
typedef CGAL::Arrangement_2<CGAL_Traits> Arrangement;

template<bool print>
size_t compute_crossings() {
	Arrangement arr;
	CGAL::insert(arr, cgal_segments.begin(), cgal_segments.end());

	size_t intersection_points_count = 0;
	for (auto vit = arr.vertices_begin(); vit != arr.vertices_end(); ++vit) {
		if (vit->degree() > 2) { // Vertices with degree > 2 are intersection points
			intersection_points_count++;
			if (print) {
				print_point(CGAL::to_double(vit->point().x()), CGAL::to_double(vit->point().y()));
			}
		}
	}

	return intersection_points_count;
}

#include "main.hpp"
