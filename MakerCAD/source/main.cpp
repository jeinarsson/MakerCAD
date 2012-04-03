#include <QtGui/QApplication>

#include "PythonQt.h"
#include "PythonQt_QtAll.h"
#include "gui/PythonQtScriptingConsole.h"

#include "Body.h"

int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	
//	qRegisterMetaType<QSharedPointer<CounterWork> >("QSharedPointer<CounterWork>");

	PythonQt::init(PythonQt::IgnoreSiteModule | PythonQt::RedirectStdOut);
	PythonQt_QtAll::init();

	PythonQtObjectPtr  mainContext = PythonQt::self()->getMainModule();
	PythonQtScriptingConsole console(NULL, mainContext);

	QSharedPointer<Body> some_block = QSharedPointer<Body>(new Block(1.,2.,3.));
	QSharedPointer<Body> another_block = QSharedPointer<Body>(new Block(-1.,2.,1.));
	QSharedPointer<Body> the_union = QSharedPointer<Body>(new Union(some_block.data(), another_block.data()));

	the_union->Instantiate();

	mainContext.evalFile("main.py");

	console.show();

	return a.exec();
}
