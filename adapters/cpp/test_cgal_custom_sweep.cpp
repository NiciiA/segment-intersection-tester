#include "utils_cgal.h"

#include <CGAL/Surface_sweep_2_algorithms.h>
#include <CGAL/Surface_sweep_2/Surface_sweep_2_utils.h>

template<bool print>
struct my_visitor : CGAL::Ss2::Default_visitor<
			my_visitor<print>, CGAL::Default_arr_traits<CGAL_Segment>::Traits> {
	using Base = CGAL::Ss2::Default_visitor<
		my_visitor, CGAL::Default_arr_traits<CGAL_Segment>::Traits>;
	using typename Base::Geometry_traits_2;
	using typename Base::Surface_sweep_2;
	using typename Base::Event;
	using typename Base::Subcurve;
	typedef Subcurve::Status_line_iterator Status_line_iterator;
	typedef Geometry_traits_2::X_monotone_curve_2 X_monotone_curve_2;
	typedef Geometry_traits_2::Point_2 Point_2;

	template<typename CurveIterator>
	void sweep(CurveIterator begin, CurveIterator end) {
		std::vector<X_monotone_curve_2> curves_vec;
		std::vector<Point_2> points_vec;

		curves_vec.reserve(std::distance(begin, end));
		CGAL::Ss2::make_x_monotone(
			begin, end,
			std::back_inserter(curves_vec),
			std::back_inserter(points_vec),
			this->traits());

		Surface_sweep_2* sl = this->surface_sweep();
		sl->sweep(curves_vec.begin(), curves_vec.end(),
		          points_vec.begin(), points_vec.end());
	}

	size_t res = 0;

	bool after_handle_event(Event* event, Status_line_iterator iter, bool flag) {
		if ((event->is_intersection() || event->is_weak_intersection() || event->is_overlap()) &&
			event->is_closed()
		) {
			res++;
			if (print) {
				print_point(event->point().x(), event->point().y());
			}
		}
		return true; // can dealloc event
	}
};

template<bool print>
size_t compute_crossings() {
	my_visitor<print> visitor;
	typename my_visitor<print>::Geometry_traits_2 traits;
	typedef CGAL::Ss2::Surface_sweep_2<my_visitor<print>> Sweep;

	Sweep surface_sweep(&traits, &visitor);
	visitor.sweep(cgal_segments.begin(), cgal_segments.end());
	return visitor.res;
}

#include "main.hpp"
