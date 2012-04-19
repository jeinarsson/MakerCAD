#ifndef GEOMETRYDECORATORS_H
#define GEOMETRYDECORATORS_H

#include "Geometry.h"
#include <QObject>

// gives the python interface to Geometry
class GeometryDecorators : public QObject
{
  Q_OBJECT

public slots:
	bool instantiated(Geometry* o) { return o->instantiated(); } 
};



#endif