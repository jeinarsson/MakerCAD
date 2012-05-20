from makercad.utils.enum import enum
import types
import collections
from PySide import QtCore

GeometryType = enum(Body3D=0, Shape2D=1)
ParameterType = enum(Integer=0, Float=1)

       
class Node(QtCore.QObject):
    """docstring for Node"""
    
    def __init__(self):
        super(Node, self).__init__()
        self._connectors = list()
        self._parameters = list()
        self._code = None
        self._output = None

    def say_it():
        print "My output was changed!"

    output_changed = QtCore.Signal()
    
    def a(self):
        self.output_changed.connect(self.say_it)
    def add_connector(self, c):
        assert isinstance(c, Connector), "%s is not a Connector" % str(c)
        assert not c in self._connectors
        self._connectors.append(c)
    def remove_connector(self, c):
        self._connectors.remove(c)
    def get_connectors(self):
        return tuple(self._connectors)
    connectors = property(get_connectors)

    def add_parameter(self, p):
        assert not p in self._parameters
        assert isinstance(p, NodeParameter), \
            "%s is not a NodeParameter" % str(p)
        self._parameters.append(p)
        self._update_output()
        p.changed.connect(self._update_output)
    def remove_parameter(self, p):
        p.changed.disconnect(self._update_output)
        self._parameters.remove(p)
        self._update_output()
    def get_parameters(self):
        return tuple(self._parameters)
    parameters = property(get_parameters)

    def get_code(self):
        return self._code
    def set_code(self, code):
        assert isinstance(code, types.FunctionType), \
            "%s is not a function" % str(code)
        self._code = code
        self._update_output()        
    code = property(get_code, set_code)

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
            self.output_changed.emit()
            return

        #make a dictionary of name-number pairs for connectors
        input_placeholders = dict()
        for i, c in enumerate(self._connectors):
            input_placeholders[c.name] = InputPlaceholder(i)

        #make a dictionary of name-value pairs for parameters
        parameters = dict()
        for p in self._parameters:
            parameters[p.name] = p.value

        #run the code
        output = self._code(input_placeholders, parameters)

        #check that the collection of outputs from the code
        #is compatible with the output connectors of this node
        output_connectors = [c for c in self._connectors if not c.is_input]
        output_conn_names = [c.name for c in output_connectors]
        assert set(output.keys()) == set(output_conn_names)

        #go through output connectors to check data types
        for c in output_connectors:
            assert c.datatype != output[c.name].datatype

        self._output = output
        self.output_changed.emit()


class NodeParameter(object):
    """docstring for NodeParameter"""
    def __init__(self):
        self._name = None
        self._value = None
        self._datatype = None
        self.node = None
        pass

    def get_name(self):
        return self._name
    def set_name(self, name):
        self._name = name
        self.changed.emit()
    name = property(get_name, set_name)

    def get_value(self):
        return self._value
    def set_value(self, value):
        self._value = value
        self.changed.emit()
    value = property(get_value, set_value)

    def get_datatype(self):
        return self._datatype
    def set_datatype(self, datatype):
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


class Connector(object):
    """docstring for Connector"""

    def __init__(self, is_input, datatype):
        assert isinstance(is_input, bool)
        self._is_input = is_input
        self.set_datatype(datatype)
        self._links = set()
        self._name = None

    def get_is_input(self):
        return self._is_input
    is_input = property(get_is_input)

    def get_name(self):
        return self._name
    def set_name(self, name):
        self._name = name
    name = property(get_name, set_name)

    def get_datatype(self): 
        return self._datatype
    def set_datatype(self, datatype):
        assert datatype in GeometryType
        self._datatype = datatype
    datatype = property(get_datatype, set_datatype)

    def get_links(self):
        return frozenset(self._links)
    links = property(get_links)

    def connect(self, other):
        assert isinstance(other, Connector)
        assert not other in self.links
        assert (self.is_input ^ other.is_input), \
            "connection needs one output and one input"
        assert not (len(self._links) > 0 and self.is_input), \
            "this connector is an input and already connected"

        #First connect to the other connector.
        self._links.add(other)
        #Make sure that the other connector has a connection to self as well.
        if not self in other.links:
            other.connect(self)


    def disconnect(self, other):
        assert other in self.links, "the specified connector is not connected"

        #First disconnect the other connector.
        self._links.remove(other)
        #Make sure that other does not have a connection to self.
        if self in other.links:
            other.disconnect(self)

class Geometry(object):
    """docstring for Geometry"""
    def __init__(self):
        self._datatype = None

    def get_datatype(self):
        return self._datatype
    datatype = property(get_datatype)

class InputPlaceholder(object):
    """docstring for InputPlaceholder"""
    def __init__(self, connector_index):
        self.connector_index = connector_index
        