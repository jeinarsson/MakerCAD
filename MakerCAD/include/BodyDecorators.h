#ifndef BODYDECORATORS_H
#define BODYDECORATORS_H

#include "Body.h"
#include <QObject>

// gives the python interface to Body
class BodyDecorators : public QObject
{
  Q_OBJECT

public slots:
	Block* new_Block(double a, double b, double c) { return new Block(a, b, c); }
	Union* new_Union(Block* b1, Block* b2) { return new Union(b1, b2); }
};



#endif