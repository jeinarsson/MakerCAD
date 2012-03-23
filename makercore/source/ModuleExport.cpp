#include <iostream>
#include <boost/python.hpp>

using namespace boost::python;

void hello_from_c()
{
   std::cout << "Hello from C++!\n";
}

BOOST_PYTHON_MODULE(makercore)
{
   def("hello_from_c",&hello_from_c);
}