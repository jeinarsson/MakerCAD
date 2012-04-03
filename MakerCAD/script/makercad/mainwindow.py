from PythonQt import QtCore, QtGui
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
        button = QtGui.QPushButton("New document", group_primitives)
        button.connect('clicked()', self.new_document_action, 'trigger()')
        prim_layout.addWidget(button)

        return ret


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
