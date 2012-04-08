#ifndef BODY_H
#define BODY_H

#include "Geometry.h"
#include "OCE.h"
#include <vector>

class Body : public Geometry
{
public:
	virtual ~Body() {};
	
protected:
};

class Block : public Body
{
public:
	Block(double _a, double _b, double _c) : a(_a), b(_b), c(_c) {}
	virtual void Instantiate();

private:
	double a, b, c;
};

class Union : public Body
{
public:
	Union(Body* _b1, Body* _b2) : b1(_b1), b2(_b2) {}
	virtual void Instantiate();

private:
	Body* b1;
	Body* b2;
};






#endif