#ifndef BODY_H
#define BODY_H

#include "Geometry.hpp"
#include "OCE.hpp"

class Body : public Geometry
{
public:
	virtual ~Body() {};

	static Body MakeBlock(double a, double b, double c);
	
	static Body DoUnion(Body& body1, Body& body2);


	

protected:
	Body(TopoDS_Shape _shape) : Geometry(_shape) {};
};

#endif