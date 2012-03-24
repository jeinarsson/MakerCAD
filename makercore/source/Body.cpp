#include "Body.hpp"

Body Body::MakeBlock(double a, double b, double c)
{
	TopoDS_Shape object = BRepPrimAPI_MakeBox(a, b, c);
	return Body(object);
}
	
Body Body::DoUnion(Body& body1, Body& body2)
{
	TopoDS_Shape object = BRepAlgoAPI_Fuse(body1.get_shape_reference(), body2.get_shape_reference());
	return Body(object);
}
