from PySide import QtCore
import collections
import types
from makercad.utils.enum import enum
from makercad.geometry.geometry import Geometry, GeometryType

ParameterType = enum(Integer=0, Float=1)

class Node(QtCore.QObject):
    """docstring for Node"""

    became_dirty = QtCore.Signal(QtCore.QObject, bool)
    
    def __init__(self):
        super(Node, self).__init__()
        self._connectors = list()
        self._parameters = list()
        self._code = None
        self._output = None
        self._revision = 0
    
    def add_connector(self, c):
        assert isinstance(c, Connector), "%s is not a Connector" % str(c)
        assert not c in self._connectors
        c.node = self
        self._connectors.append(c)
        self._update_output()
        c.changed.connect(self._update_output)
    def remove_connector(self, c):
        self._connectors.remove(c)
        self._update_output()
        c.changed.disconnect(self._update_output)
        c.node = None
    def get_connectors(self):
        return tuple(self._connectors)
    connectors = property(get_connectors)

    def get_revision(self):
        return self._revision
    revision = property(get_revision)

    def add_parameter(self, p):
        assert not p in self._parameters
        assert isinstance(p, NodeParameter), \
            "%s is not a NodeParameter" % str(p)
        self._parameters.append(p)
        self._update_output()
        p.changed.connect(self._update_output)
    def remove_parameter(self, p):
        assert p in self._parameters
        p.changed.disconnect(self._update_output)
        self._parameters.remove(p)
        self._update_output()
    def get_parameters(self):
        return tuple(self._parameters)
    parameters = property(get_parameters)

    def get_code(self):
        return self._code
    def set_code(self, code):
        if self._code == code:
            return
        assert isinstance(code, types.FunctionType), \
            "%s is not a function" % str(code)
        self._code = code
        self._update_output()        
    code = property(get_code, set_code)

    def get_output(self):
        return self._output
    output = property(get_output)

    def _set_dirty(self, new_output):
        self._revision += 1
        self._is_dirty = True
        self.became_dirty.emit(self, new_output)

    def handle_dirty_input(self):
        # This node becomes dirty because one of its
        # input nodes became dirty.
        self._set_dirty(False) # Flag updated = False

    def _validate_parameters(self):
        #Check that all parameters have values of correct data type
        for p in self._parameters:
            if not p.datatype_matches_value():
                return False

        #Check that all parameters have unique names
        names = map(lambda p: p.name, self._parameters)
        if None in names:
            return False
        if len(set(names)) != len(names):
            return False

        return True

    def _validate_connectors(self):
        #Check that all connectors have unique names
        names = [c.name for c in self._connectors]
        if None in names:
            return False
        if len(set(names)) != len(names):
            return False

        #check that there is at least one output
        outputs = [c.name for c in self._connectors if not c.is_input]
        if 0 == len(outputs):
            return False

        return True

    def _is_output_computable(self):
        if not self._validate_parameters():
            return False
        if not self._validate_connectors():
            return False
        if None == self._code:
            return False
        return True

    def _update_output(self):
        if not self._is_output_computable():
            self._output = None
            self._set_dirty(True) # Flag updated = True
            return

        #make a dictionary of input placeholders for all input connectors
        input_placeholders = dict()
        for i, c in enumerate(self._connectors):
            input_placeholders[c.name] = InputPlaceholder(i)

        #make a dictionary of name-value pairs for parameters
        parameters = dict()
        for p in self._parameters:
            parameters[p.name] = p.value

        #run the code
        output = self._code(input_placeholders, parameters)
        assert None != output

        #check that the collection of outputs from the code
        #is compatible with the output connectors of this node
        output_connectors = [c for c in self._connectors if not c.is_input]
        output_conn_names = [c.name for c in output_connectors]
        assert set(output.keys()) == set(output_conn_names)

        #go through output connectors to check data types
        for c in output_connectors:
            assert c.datatype == output[c.name].datatype

        self._output = output
        self._set_dirty(True) # Flag updated = True

class NodeParameter(QtCore.QObject):
    """docstring for NodeParameter"""

    changed = QtCore.Signal()

    def __init__(self):
        super(NodeParameter, self).__init__()
        self._name = None
        self._value = None
        self._datatype = None

    def get_name(self):
        return self._name
    def set_name(self, name):
        if self._name == name:
            return
        self._name = name
        self.changed.emit()
    name = property(get_name, set_name)

    def get_value(self):
        return self._value
    def set_value(self, value):
        # Skip only if type AND value is the same. float(1) == 1 in Python.
        if self._value == value and type(self._value) == type(value):
            return
        self._value = value
        self.changed.emit()
    value = property(get_value, set_value)

    def get_datatype(self):
        return self._datatype
    def set_datatype(self, datatype):
        if self._datatype == datatype:
            return
        assert datatype in ParameterType
        self._datatype = datatype
        self.changed.emit()
    datatype = property(get_datatype, set_datatype)

    def datatype_matches_value(self):
        if ParameterType.Float == self._datatype:
            if isinstance(self.value, float):
                return True
        elif ParameterType.Integer == self._datatype:
            if isinstance(self.value, int):
                return True

        return False


class Connector(QtCore.QObject):
    """docstring for Connector"""

    changed = QtCore.Signal()

    def __init__(self, is_input, datatype):
        super(Connector, self).__init__()
        assert isinstance(is_input, bool)
        self._is_input = is_input
        self._datatype = None
        self.set_datatype(datatype)
        self._name = None
        self._node = None
        self._mesh = None

    def get_node(self):
        return self._node
    def set_node(self, node):
        self._node = node
    node = property(get_node, set_node)

    def get_is_input(self):
        return self._is_input
    is_input = property(get_is_input)

    def get_name(self):
        return self._name
    def set_name(self, name):
        if self._name == name:
            return
        self._name = name
        self.changed.emit()
    name = property(get_name, set_name)

    def get_mesh(self):
        return self._mesh
    def set_mesh(self, mesh):
        self._mesh = mesh
        print "I am {0} now have mesh {1}".format(self, mesh)
    mesh = property(get_mesh, set_mesh)

    def get_datatype(self): 
        return self._datatype
    def set_datatype(self, datatype):
        if self._datatype == datatype:
            return
        assert datatype in GeometryType
        self._datatype = datatype
        self.changed.emit()
    datatype = property(get_datatype, set_datatype)

class InputPlaceholder(object):
    """docstring for InputPlaceholder"""
    def __init__(self, connector_index):
        self.connector_index = connector_index