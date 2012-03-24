#ifndef GEOMETRY_H
#define GEOMETRY_H

#include "OCE.hpp"

class Geometry
{
public:
	virtual ~Geometry(){};
	TopoDS_Shape& get_shape_reference() { return shape; };
	TopoDS_Shape get_shape_copy() { return shape; };

protected:
	Geometry(TopoDS_Shape _shape){ shape = _shape; };
	TopoDS_Shape shape;
};

#endif