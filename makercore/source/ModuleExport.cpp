#include <iostream>
#include <boost/python.hpp>



#include "Body.hpp"

using namespace boost::python;

void hello_from_c()
{
   std::cout << "Hello from C++!\n";
}

BOOST_PYTHON_MODULE(_makercore)
{
   def("hello_from_c",&hello_from_c);

   class_<Geometry>("Geometry", no_init);

   class_<Body, bases<Geometry>>("Body", no_init)
        .def("MakeBlock", &Body::MakeBlock).staticmethod("MakeBlock")
        .def("DoUnion", &Body::DoUnion).staticmethod("DoUnion");

}