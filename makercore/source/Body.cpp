#include "Body.hpp"

_Body _Body::MakeBlock(double a, double b, double c)
{
	TopoDS_Shape object = BRepPrimAPI_MakeBox(a, b, c);
	return _Body(object);
}
	
_Body _Body::DoUnion(_Body& body1, _Body& body2)
{
	TopoDS_Shape object = BRepAlgoAPI_Fuse(body1.get_shape_reference(), body2.get_shape_reference());
	return _Body(object);
}