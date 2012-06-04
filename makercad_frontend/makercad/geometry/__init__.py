from makercad.utils.enum import enum

GeometryType = enum(Body3D=0, Shape2D=1)

class Geometry(object):
    """docstring for Geometry"""
    def __init__(self):
        self._datatype = None

    def get_datatype(self):
        return self._datatype
    datatype = property(get_datatype)