#ifndef GEOMETRY_H
#define GEOMETRY_H

#include "OCE.h"

class Geometry
{
public:
	Geometry() : is_instantiated(false) {}
	virtual ~Geometry(){};
	inline TopoDS_Shape& get_shape_reference() { 
		if (!is_instantiated) 
			Instantiate();

		return shape;
	};
	inline TopoDS_Shape get_shape_copy() { 
		if (!is_instantiated) 
			Instantiate();

		return shape;
	};

	virtual void Instantiate() { is_instantiated = true; };

protected:
	bool is_instantiated;
	TopoDS_Shape shape;
};

#endif