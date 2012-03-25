#include <iostream>
#include <boost/python.hpp>
#include "Body.hpp"
#include "TriangleMesh.hpp"

using namespace boost::python;

str hello_from_c()
{
   return str("Hello from C++");
}



class RenderObject
{
public:
	float vdata[8];
	unsigned int edata[4];

	RenderObject() {
		vdata[0] = vdata[1] = vdata[3] = vdata[4] = -1.0f;
		vdata[2] = vdata[5] = vdata[6] = vdata[7] = 1.0f;
		for (int i=0; i<4; i++) edata[i] = i;
	};
	virtual ~RenderObject() {};
	
	tuple get_buffers_fakepointers() {
		return make_tuple(fake_pointer(vdata),fake_pointer(edata));
	};

private:
	template <typename T>
	unsigned long fake_pointer(T* ptr)
	{
		return (unsigned long)ptr;
	} 

};





BOOST_PYTHON_MODULE(_makercore)
{
   def("hello_from_c",&hello_from_c);

   class_<Geometry>("Geometry", no_init);

   class_<Body, bases<Geometry>>("Body", no_init)
        .def("MakeBlock", &Body::MakeBlock).staticmethod("MakeBlock")
        .def("DoUnion", &Body::DoUnion).staticmethod("DoUnion");

   class_<TriangleMesh>("TriangleMesh", init<Body&>())
	   .def("get_buffers_fakepointers",&TriangleMesh::get_buffers_fakepointers);

   class_<RenderObject>("RenderObject")
	   .def("get_buffers_fakepointers",&RenderObject::get_buffers_fakepointers);

}