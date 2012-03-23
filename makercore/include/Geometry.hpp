#ifndef GEOMETRY_H
#define GEOMETRY_H

#include "OCE.hpp"

class _Geometry
{
public:
	_Geometry(){};
	virtual ~_Geometry(){};

protected:
	TopoDS_Shape shape;
};

#endif