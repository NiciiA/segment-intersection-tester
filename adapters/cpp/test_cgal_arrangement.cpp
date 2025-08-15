#include "utils_cgal.h"

#include <CGAL/Arrangement_on_surface_with_history_2.h>
#include <CGAL/Arr_segment_traits_2.h>
#include <CGAL/Arrangement_2/Arr_default_planar_topology.h>

typedef CGAL::Arr_segment_traits_2<K> Geom_Traits;
typedef CGAL::Default_planar_topology<
	Geom_Traits, CGAL::Arr_default_dcel<Geom_Traits>>::Traits Top_Traits;
typedef CGAL::Arrangement_on_surface_with_history_2<Geom_Traits, Top_Traits> Arrangement;

template<bool print>
size_t compute_crossings() {
	Arrangement arr;
	CGAL::insert(arr, cgal_segments.begin(), cgal_segments.end());

	size_t intersection_points_count = 0;
	for (auto vit = arr.vertices_begin(); vit != arr.vertices_end(); ++vit) {
		if (vit->degree() > 1 || (!vit->is_isolated() && arr.number_of_originating_curves(
			vit->incident_halfedges()) > 1)) {
			// Vertices with degree > 1 are intersection points
			// Vertices with degree = 1 where multiple curves make up the incident edge are overlaps
			intersection_points_count++;
			if (print) {
				print_point(vit->point().x(), vit->point().y());
			}
		}
	}

	return intersection_points_count;
}

#include "main.hpp"
