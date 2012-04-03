#include <QtGui/QApplication>

#include "PythonQt.h"
#include "PythonQt_QtAll.h"
#include "gui/PythonQtScriptingConsole.h"


int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	
//	qRegisterMetaType<QSharedPointer<CounterWork> >("QSharedPointer<CounterWork>");

	PythonQt::init(PythonQt::IgnoreSiteModule | PythonQt::RedirectStdOut);
	PythonQt_QtAll::init();

	PythonQt::self()->installDefaultImporter();
	PythonQt::self()->addSysPath(QString("script/"));

	PythonQtObjectPtr __main__ = PythonQt::self()->getMainModule();
	PythonQtScriptingConsole console(NULL, __main__);

	// console shown in mainwindow instead
	console.show();

	__main__.addObject("console", &console);
	__main__.evalFile(QString("script/main.py"));

	return a.exec();
}
