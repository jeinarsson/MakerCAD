from makercad.utils.enum import enum

GeometryType = enum(Body3D=0, Shape2D=1)

class Geometry(object):
    """docstring for Geometry"""
    def __init__(self):
        self._datatype = None
        self._parameters = None
        self._inputs = None

    def get_datatype(self):
        return self._datatype
    datatype = property(get_datatype)

    def get_inputs(self):
        return self._inputs
    inputs = property(get_inputs)

    def get_parameters(self):
        return self._parameters
    parameters = property(get_parameters)

class Body3D(Geometry):
    """docstring for Body3D"""
    def __init__(self):
        super(Body3D, self).__init__()
        self._datatype = GeometryType.Body3D
        

class Box(Body3D):
    """docstring for Box"""
    def __init__(self, a, b, c):
        super(Box, self).__init__()
        self._parameters = dict(a=a, b=b, c=c)
        self._inputs = dict()

class Union(Body3D):
    """docstring for Union"""
    def __init__(self, body1, body2):
        super(Union, self).__init__()
        self._parameters = dict()
        self._inputs = dict(body1=body1, body2=body2)

        
        