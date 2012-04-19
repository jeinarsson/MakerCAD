#ifndef WORKMANAGER_H
#define WORKMANAGER_H

#include "Geometry.h"
#include <QtCore/QObject>
#include <QThread>
#include <QSharedPointer>
#include <QMetaMethod>

class WorkManagerClient;

class GeometryWork {
public:
	GeometryWork(){}
	GeometryWork(WorkManagerClient* client_, int reference_id_, Geometry* geometry_):client(client_),reference_id(reference_id_), geometry(geometry_){}

	WorkManagerClient* client;
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
	QList<WorkManagerClient*> registered_clients;

	int handle_work_index;
	inline void invoke_worker(Worker* worker, GeometryWork work);
	
	void init(int n);
public:
	WorkManager() {init(2);}
	WorkManager(int n) {init(n);}
	virtual ~WorkManager();
	
public slots:
	void submit_work(WorkManagerClient* client, int reference_id, Geometry* geometry);
	WorkManagerClient* register_client();
	void deregister_client(WorkManagerClient* wmc);
	
	void handle_finished_work(GeometryWork work);

signals:
	void log(QString text);
};

class WorkManagerClient : public QObject
{ Q_OBJECT

public:
	WorkManagerClient(){};
	virtual ~WorkManagerClient(){};
	WorkManager* parent;
	inline void emit_work_finished(int reference_id, Geometry* geometry) {emit work_finished(reference_id, geometry);}	
	
public slots:
	void submit_work(int reference_id, Geometry* geometry);

signals:
	void work_finished(int reference_id, Geometry* geometry);
};



class WorkManagerDecorators : public QObject
{
  Q_OBJECT

public slots:
	WorkManager* new_WorkManager(int n) { return new WorkManager(n); }
};




#endif