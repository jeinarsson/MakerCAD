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

   class_<_Geometry>("Geometry", no_init);

   class_<_Body, bases<_Geometry>>("_Body", no_init)
        .def("MakeBlock", &_Body::MakeBlock).staticmethod("MakeBlock")
        .def("DoUnion", &_Body::DoUnion).staticmethod("DoUnion");
}