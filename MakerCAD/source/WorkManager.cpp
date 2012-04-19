#include "WorkManager.h"

#include <QtAlgorithms>

Worker::Worker()
{
	this->moveToThread(&thread);
	thread.start(QThread::Priority::LowPriority);
}

Worker::~Worker()
{
	if (thread.isRunning()) {
		thread.quit();
		thread.wait();
	}
}

void Worker::work(GeometryWork work)
{
/* // Dummy work
	double x=0.6;
	for (int i=0; i<10000; i++){
		for (int j=0; j<work.reference_id; j++){
			x+=0.1;
		}
	}
	work.reference_id = (int)x;
*/
	work.geometry->Instantiate();

	emit work_finished(work);
}



void WorkManager::init(int n)
{

	handle_work_index = Worker::staticMetaObject.indexOfMethod("work(GeometryWork)");
	
	free_workers.reserve(n);
	busy_workers.reserve(n);

	for (int i=0; i<n; i++) {
		Worker* w = new Worker();
		this->connect(w, SIGNAL(work_finished(GeometryWork)), SLOT(handle_finished_work(GeometryWork)));
		free_workers.append(w);
	}

}

WorkManager::~WorkManager()
{
	qDeleteAll(free_workers);
	qDeleteAll(busy_workers);
/*
	while(!free_workers.empty()) {
		delete free_workers.takeFirst();
	}
	while(!busy_workers.empty()) {
		delete busy_workers.takeFirst();
	}
*/
}


inline void WorkManager::invoke_worker(Worker *worker, GeometryWork work)
{

	bool success = Worker::staticMetaObject.method(handle_work_index).invoke(worker, Q_ARG(GeometryWork, work));
	emit log(QString("Invoking worker method %2, success: %1").arg(success).arg(handle_work_index));

}


void WorkManager::submit_work(WorkManagerClient* client, int reference_id, Geometry *geometry)
{
	
	GeometryWork new_work(client, reference_id, geometry);

	if (free_workers.empty())
	{
		emit log(QString("No free workers, queueing work.."));
		work_queue.append(new_work);
	}
	else
	{
		emit log(QString("Launching worker."));
		Worker* w = free_workers.takeFirst();
		busy_workers.append(w);
		invoke_worker(w, new_work);
	}
}

void WorkManager::handle_finished_work(GeometryWork work)
{
	work.client->emit_work_finished(work.reference_id, work.geometry);

	Worker* w = (Worker*)QObject::sender();
	if (!work_queue.empty())
	{
		GeometryWork new_work = work_queue.takeFirst();
		invoke_worker(w, new_work);
	}
	else
	{
		busy_workers.removeOne(w);
		free_workers.append(w);
	}


}

WorkManagerClient* WorkManager::register_client()
{
	WorkManagerClient* new_client = new WorkManagerClient();
	new_client->parent = this;
	registered_clients.append(new_client);
	return new_client;
}

void WorkManager::deregister_client(WorkManagerClient* wmc)
{
	registered_clients.removeOne(wmc);
	delete wmc;
}

void WorkManagerClient::submit_work(int reference_id, Geometry* geometry)
{
	parent->submit_work(this, reference_id, geometry);
}