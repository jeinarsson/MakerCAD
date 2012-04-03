from PythonQt import QtCore, QtGui
from makercad import MainWindow

QtCore.QCoreApplication.setApplicationName("MakerCAD")
QtCore.QCoreApplication.setOrganizationName("MakerCAD")

# console is automatically exported from C++ program
main_window = MainWindow(console)
main_window.show()
