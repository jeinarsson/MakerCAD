#include <QtGui/QApplication>

#include "PythonQt.h"
#include "PythonQt_QtAll.h"
#include "gui/PythonQtScriptingConsole.h"

#include "WorkManager.h"

#include "GeometryDecorators.h"
#include "BodyDecorators.h"

int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	
	qRegisterMetaType<GeometryWork>("GeometryWork");
	qRegisterMetaType<Geometry*>("Geometry*");
	qRegisterMetaType<WorkManagerClient*>("WorkManagerClient*");

	PythonQt::init(PythonQt::IgnoreSiteModule | PythonQt::RedirectStdOut);
	PythonQt_QtAll::init();
	
	PythonQt::self()->installDefaultImporter();
	PythonQt::self()->addSysPath(QString("script/"));

	PythonQt::self()->addDecorators(new WorkManagerDecorators());
	PythonQt::self()->registerClass(&WorkManager::staticMetaObject, "makercore");
	PythonQt::self()->registerClass(&WorkManagerClient::staticMetaObject, "makercore");

	PythonQt::self()->addDecorators(new GeometryDecorators());
	PythonQt::self()->registerCPPClass("Geometry","", "makercore");

	PythonQt::self()->addDecorators(new BodyDecorators());
	PythonQt::self()->registerCPPClass("Body","Geometry", "makercore");
	PythonQt::self()->registerCPPClass("Block","Body", "makercore");
	PythonQt::self()->registerCPPClass("Union","Body", "makercore");



	PythonQtObjectPtr __main__ = PythonQt::self()->getMainModule();
	PythonQtScriptingConsole console(NULL, __main__);
	// console shown in mainwindow instead
	// console.show();
	__main__.addObject("console", &console);
	__main__.evalFile(QString("script/main.py"));

	return a.exec();
}
