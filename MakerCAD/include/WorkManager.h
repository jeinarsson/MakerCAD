#ifndef WORKMANAGER_H
#define WORKMANAGER_H

#include "Geometry.h"
#include <QtCore/QObject>
#include <QThread>
#include <QSharedPointer>
#include <QMetaMethod>

class GeometryWork {
public:
	GeometryWork(){}
	GeometryWork(int reference_id_, Geometry* geometry_):reference_id(reference_id_), geometry(geometry_){}

	int reference_id;
	Geometry* geometry;
};

class Worker : public QObject
{ Q_OBJECT

public:
	Worker();
	virtual ~Worker();

public slots:
	void work(GeometryWork work);

signals:
	void work_finished(GeometryWork work);

private:
	QThread thread;
};




class WorkManager : public QObject 
{ Q_OBJECT

private:
	QList<Worker* > free_workers;
	QList<Worker* > busy_workers;
	QList<GeometryWork> work_queue;

	int handle_work_index;
	inline void invoke_worker(Worker* worker, GeometryWork work);
	
	void init(int n);
public:
	WorkManager() {init(2);}
	WorkManager(int n) {init(n);}
	virtual ~WorkManager();
	
public:
	void queue_work(int reference_id, Geometry* geometry);
	
public slots:
	void handle_finished_work(GeometryWork work);

signals:
	void work_finished(int reference_id, Geometry* geometry);
	void log(QString text);
};

class WorkManagerDecorators : public QObject
{
  Q_OBJECT

public slots:
	WorkManager* new_WorkManager(int n) { return new WorkManager(n); }
	void queue_work(WorkManager* o, int reference_id, Geometry* geometry) { o->queue_work(reference_id, geometry); }
};




#endif