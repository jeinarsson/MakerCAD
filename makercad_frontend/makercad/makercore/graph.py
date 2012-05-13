from makercad.utils.enum import enum
import types
import collections
from PySide import QtCore

ConnectorDatatype = enum(Body3D=0, Shape2D=1)
ParameterDatatype = enum(Integer=0, Float=1, String=3)

class Node(object):
    """docstring for Node"""
    
    def __init__(self):
        self._connectors = list()
        self._parameters = list()
        self._code = None

    def add_connector(self, c):
        if c in self._connectors:
            raise ValueError("%s is already a connector in %s" % (c, self))
        if not isinstance(c, Connector):
            raise TypeError("%s is not a Connector" % str(c))
        self._connectors.append(c)

    def remove_connector(self, c):
        self._connectors.remove(c)

    def get_connectors(self):
        return self._connectors
    connectors = property(get_connectors)


    def add_parameter(self, p):
        if p in self._parameters:
            raise ValueError("%s is already a parameter in %s" % (p, self))
        if not isinstance(p, NodeParameter):
            raise TypeError("%s is not a NodeParameter" % str(p))
        self._parameters.append(p)

    def remove_parameter(self, p):
        self._parameters.remove(p)

    def get_parameters(self):
        return self._parameters
    parameters = property(get_parameters)


    def get_code(self):
        return self._code
    def set_code(self, code):
        if not isinstance(code, types.FunctionType):
            raise TypeError("%s is not a function" % str(code))
        self._code = code
    code = property(get_code, set_code)


    def compute_output(self):
        if None == self._code:
            raise Exception("the code for %s is not defined" % self)

        d = dict()
        for p in self._parameters:
            d[p.name] = p.value

        return self._code(**d)


class NodeParameter(object):
    """docstring for NodeParameter"""
    def __init__(self):
        self._name = None
        self._value = None
        self._datatype = None
        pass

    def get_name(self):
        return self._name
    def set_name(self, name):
        self._name = name
    name = property(get_name, set_name)

    def get_value(self):
        return self._value
    def set_value(self, value):
        self._value = value
    value = property(get_value, set_value)

    def get_datatype(self):
        return self._datatype
    def set_datatype(self, datatype):
        if not datatype in ParameterDatatype:
            raise ValueError(
                "%s is not a ParameterDatatype value" % str(datatype))
        self._datatype = datatype
    datatype = property(get_datatype, set_datatype)




        


class Connector(object):
    """docstring for Connector"""

    def __init__(self, is_input, datatype):
        self.set_datatype(datatype)
        self._set_is_input(is_input)
        self._links = set()


    def get_is_input(self):
        return self._is_input
    def _set_is_input(self, is_input):
        if not isinstance(is_input, bool):
            raise TypeError("%s is not a boolean" % str(is_input))
        self._is_input = is_input
    is_input = property(get_is_input)


    def get_datatype(self): 
        return self._datatype
    def set_datatype(self, datatype):
        if not datatype in ConnectorDatatype:
            raise ValueError(
                "%s is not a ConnectorDatatype value" % str(datatype))
        self._datatype = datatype
    datatype = property(get_datatype, set_datatype)


    def get_links(self):
        return frozenset(self._links)
    links = property(get_links)

    def connect(self, other):
        if other in self.links:
            raise ValueError("the specified connector is already connected")
        if not isinstance(other, Connector):
            raise TypeError("%s is not a Connector" % str(other))
        if not (self.is_input ^ other.is_input):
            raise ValueError("connection needs one output and one input")

        #First connect to the other connector.
        self._links.add(other)

        #Make sure that other has a connection to self as well.
        if not self in other.links:
            other.connect(self)

    def disconnect(self, other):
        if not other in self.links:
            raise ValueError("the specified connector is not connected")

        #First disconnect the other connector.
        self._links.remove(other)

        #Make sure that other does not have a connection to self.
        if self in other.links:
            other.disconnect(self)



        