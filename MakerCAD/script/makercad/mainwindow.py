from PythonQt import QtCore, QtGui, makercore
from documentview import DocumentView


class MainWindow(QtGui.QMainWindow):
    def __init__(self, _console_widget):
        super(MainWindow, self).__init__()

        self.console_widget = _console_widget

        self.setWindowTitle("MakerCAD")
        self.set_statusbar_message("Idle.")

        self.create_actions()
        self.initialise_windows()

        self.read_settings()

        self.documents = QtGui.QTabWidget()
        self.setCentralWidget(self.documents)

        self.work_manager = makercore.WorkManager(2)
        self.work_manager.connect('log(QString)', self.log_append)
        
        self.wmc = self.work_manager.register_client()
        self.wmc.connect('work_finished(int,Geometry*)', self.on_work_finished)
        
    def try_workers(self):

        b1 = makercore.Block(1,2,3)
        b2 = makercore.Block(3,4,3)
        b3 = makercore.Union(b1,b2)

        self.log.appendPlainText("b3.instantiated: " + str(b3.instantiated()))
        self.wmc.submit_work(7, b3)

    def on_work_finished(self, n, p):
        self.log.appendPlainText("Got work back(n,p): " + str(n) + ", " + str(p))
        self.log.appendPlainText("p.instantiated: " + str(p.instantiated()))

    def log_append(self, s):
        self.log.appendPlainText(s)

    def initialise_windows(self):

    	dock = QtGui.QDockWidget("Python console", self)
        dock.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        dock.setWidget(self.console_widget)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dock)
        
        dock = QtGui.QDockWidget("Tools", self)
        self.tools = self.create_tools(dock)
        dock.setWidget(self.tools)
        dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
        
        dock = QtGui.QDockWidget("Log", self)
        self.log = QtGui.QPlainTextEdit(dock)
        dock.setWidget(self.log)
        #dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock)

    def create_actions(self):
        self.new_document_action = QtGui.QAction("&New Letter", self)
        self.new_document_action.setStatusTip("Create a new document")
        self.new_document_action.connect('triggered()', self.create_new_document)

    def create_new_document(self):
        print DocumentView
        doc = DocumentView()
        self.documents.addTab(doc, "New document!")

    def create_tools(self, parent):
        ret = QtGui.QWidget(parent)

        layout = QtGui.QVBoxLayout(ret)
        group_primitives = QtGui.QGroupBox("Primitives",ret)
        group_operations = QtGui.QGroupBox("Operations",ret)
        layout.addWidget(group_primitives)
        layout.addWidget(group_operations)
        
        prim_layout = QtGui.QVBoxLayout(group_primitives)
        button = QtGui.QPushButton("Create work", group_primitives)
        button.connect('clicked()', self.create_work)
        prim_layout.addWidget(button)

        return ret


    def create_work(self):
        print "create_work"
        self.work_manager.queue_work(70000, None)
        

    def set_statusbar_message(self, message):
        self.statusBar().showMessage(message) 


    def read_settings(self):
        settings = QtCore.QSettings()
        pos = settings.value("MainWindow.position", QtCore.QPoint(200, 200))
        size = settings.value("MainWindow.size", QtCore.QSize(400, 400))
        self.resize(size)
        self.move(pos)

    def write_settings(self):
        settings = QtCore.QSettings()
        settings.setValue("MainWindow.position", self.pos)
        settings.setValue("MainWindow.size", self.size) 

    def closeEvent(self, event):
        self.write_settings()
