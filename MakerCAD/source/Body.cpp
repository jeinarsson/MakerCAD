#include "Body.h"

void Block::Instantiate() 
{
	shape = BRepPrimAPI_MakeBox(a, b, c).Shape();
	is_instantiated = true;
}

void Union::Instantiate()
{
	shape = BRepAlgoAPI_Fuse(b1->get_shape_reference(), b2->get_shape_reference()).Shape();
	is_instantiated = true;
}