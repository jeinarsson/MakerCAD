#ifndef BODY_H
#define BODY_H

#include "Geometry.hpp"
#include "OCE.hpp"

class _Body : public _Geometry
{
public:
	virtual ~_Body() {};

	static _Body MakeBlock(double a, double b, double c);
	
	static _Body DoUnion(_Body& body1, _Body& body2);

protected:
	_Body(TopoDS_Shape _shape) : _Geometry(_shape) {};
};

#endif