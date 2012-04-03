#ifndef TRIANGLEMESH_H
#define TRIANGLEMESH_H

#include "OCE.h"
#include "Body.h"
#include <vector>

/*
Triangle mesh stored as one PNPNPNPN.. vertex buffer and
one element buffer.
*/
class TriangleMesh
{
public:
	virtual ~TriangleMesh() {};
	TriangleMesh(Body& b);

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