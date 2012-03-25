#ifndef TRIANGLEMESH_H
#define TRIANGLEMESH_H

#include "OCE.hpp"
#include <boost/python.hpp>
#include "Body.hpp"
#include <vector>


using namespace boost::python;


/*
Triangle mesh stored as one PNPNPNPN.. vertex buffer and
one element buffer.
*/
class TriangleMesh
{
public:
	virtual ~TriangleMesh() {};
	TriangleMesh(Body& b);
	tuple get_buffers_fakepointers() {
		return make_tuple(vertexbuffer.size(), fake_pointer(vertexbuffer.data()),elementbuffer.size(), fake_pointer(elementbuffer.data()));
	};


protected:

	std::vector<float> vertexbuffer;
	std::vector<unsigned int> elementbuffer;

	template <typename T>
	unsigned long fake_pointer(T* ptr)
	{
		return (unsigned long)ptr;
	} 

};

#endif