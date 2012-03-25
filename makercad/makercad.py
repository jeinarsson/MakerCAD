import makercore
import ctypes

from random import random
#!/usr/bin/env python

"""PySide port of the opengl/hellogl example from Qt v4.x"""

import sys
import math
from PySide import QtCore, QtGui, QtOpenGL

from OpenGL import GL

from OpenGL.GL import shaders


class Window(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.glWidget = GLWidget()

        self.xSlider = self.createSlider(QtCore.SIGNAL("xRotationChanged(int)"),
                                         self.glWidget.setXRotation)
        self.ySlider = self.createSlider(QtCore.SIGNAL("yRotationChanged(int)"),
                                         self.glWidget.setYRotation)
        self.zSlider = self.createSlider(QtCore.SIGNAL("zRotationChanged(int)"),
                                         self.glWidget.setZRotation)

        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addWidget(self.glWidget)
        mainLayout.addWidget(self.xSlider)
        mainLayout.addWidget(self.ySlider)
        mainLayout.addWidget(self.zSlider)
        self.setLayout(mainLayout)

        self.xSlider.setValue(15 * 16)
        self.ySlider.setValue(345 * 16)
        self.zSlider.setValue(0 * 16)

        self.setWindowTitle(self.tr(makercore.hello_from_c()))


    def createSlider(self, changedSignal, setterSlot):
        slider = QtGui.QSlider(QtCore.Qt.Vertical)

        slider.setRange(0, 360 * 16)
        slider.setSingleStep(16)
        slider.setPageStep(15 * 16)
        slider.setTickInterval(15 * 16)
        slider.setTickPosition(QtGui.QSlider.TicksRight)

        self.glWidget.connect(slider, QtCore.SIGNAL("valueChanged(int)"), setterSlot)
        self.connect(self.glWidget, changedSignal, slider, QtCore.SLOT("setValue(int)"))



        return slider


class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)

        self.setAutoBufferSwap(False)

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

        self.lastPos = QtCore.QPoint()

        self.trolltechGreen = QtGui.QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        self.trolltechPurple = QtGui.QColor.fromCmykF(0.39, 0.39, 0.0, 0.0)
        
        self.sizeof_float = 4
        self.sizeof_uint = 4

        
        self.vbo = -1;
        self.ebo = -1;
        

    def xRotation(self):
        return self.xRot

    def yRotation(self):
        return self.yRot

    def zRotation(self):
        return self.zRot

    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)

    def sizeHint(self):
        return QtCore.QSize(400, 400)

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.emit(QtCore.SIGNAL("xRotationChanged(int)"), angle)
            self.model_matrix = self.make_view_matrix();

            self.updateGL()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.emit(QtCore.SIGNAL("yRotationChanged(int)"), angle)
            self.model_matrix = self.make_view_matrix();
            self.updateGL()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.emit(QtCore.SIGNAL("zRotationChanged(int)"), angle)
            self.model_matrix = self.make_view_matrix();
            self.updateGL()


    def create_shaders(self):

        VERTEX_SHADER = shaders.compileShader("""
                #version 120

                uniform mat4 p_matrix, mv_matrix;
                in vec3 position;
                in vec3 normal;
                
                varying vec3 frag_position, frag_normal;

                void main()
                {
                    vec4 eye_position = mv_matrix * vec4(position, 1.0);
                    gl_Position = p_matrix * eye_position;
                    frag_position = eye_position.xyz;
                    frag_normal   = (mv_matrix * vec4(normal, 0.0)).xyz;
                }
            """, shaders.GL_VERTEX_SHADER)
        FRAGMENT_SHADER = shaders.compileShader("""
                #version 120

                uniform mat4 p_matrix, mv_matrix;
                varying vec3 frag_position, frag_normal;
                
                const vec3 light_pos = vec3(7,7, 7);
                const vec4 light_diffuse = vec4(0.9, 0.9, 0.9, 1.0);
                const vec4 light_ambient = vec4(0.5, 0.5, 0.5, 1.0);
                

                void main()
                {
                    vec3 light_dir = normalize(frag_position-light_pos);
                    vec3 normal = normalize(frag_normal);
                    
                    vec4 frag_diffuse = vec4(0.9,0.2,0.2,1.0);
                    vec4 diffuse_factor
                        = max(-dot(normal, light_dir), 0.0) * light_diffuse;
                    vec4 ambient_diffuse_factor
                        = diffuse_factor + light_ambient;
    
                    gl_FragColor = ambient_diffuse_factor * frag_diffuse;
                }

            """, shaders.GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(VERTEX_SHADER,FRAGMENT_SHADER)
        self.shader_uniforms = {
                                'p_matrix': GL.glGetUniformLocation(self.shader, 'p_matrix'),
                                'mv_matrix': GL.glGetUniformLocation(self.shader, 'mv_matrix'),
                                }
        self.shader_attributes = {
                                 'position': GL.glGetAttribLocation(self.shader, 'position'),
                                 'normal': GL.glGetAttribLocation(self.shader, 'normal'),
                                 }         


    def create_buffer(self):

        

        block = makercore.Body.MakeBlock(-0.5+3.0*random(),0.5+3.0*random(),1.+2.0*random());
        block2 = makercore.Body.MakeBlock(0.5+3.0*random(),0.5+3.0*random(),-0.5+2.0*random());
        sak = makercore.Body.DoUnion(block,block2)
        mesh = makercore.TriangleMesh(sak)

        (num_v, fake_v, num_e, fake_e) = mesh.get_buffers_fakepointers()

        ptr_v = ctypes.cast(fake_v, ctypes.POINTER((ctypes.c_float))) 
        ptr_e = ctypes.cast(fake_e, ctypes.POINTER((ctypes.c_int)))
 
        if not self.vbo == -1:
            GL.glDeleteBuffers(2,[self.vbo, self.ebo]);

        self.vbo = self.make_buffer(GL.GL_ARRAY_BUFFER, ptr_v, num_v*self.sizeof_float)
        self.ebo = self.make_buffer(GL.GL_ELEMENT_ARRAY_BUFFER, ptr_e, num_e*self.sizeof_uint)
        self.ebo_count = num_e

#        for i in range(num_v/6):
#            print '{0}, {1}, {2}'.format(ptr_v[6*i+0],ptr_v[6*i+1],ptr_v[6*i+2])

#        for i in range(num_e/3):
#            print '{0}, {1}, {2}'.format(ptr_e[3*i+0],ptr_e[3*i+1],ptr_e[3*i+2])


    def make_buffer(self, target, data_pointer, data_length):
        buffer = GL.glGenBuffers(1)
        GL.glBindBuffer(target, buffer)
        GL.glBufferData(target, data_length, data_pointer, GL.GL_STATIC_DRAW)
        return buffer


    def make_orthographic(self,width,height,near,far):
        
        m = QtGui.QMatrix4x4()
        m.setToIdentity()
        m.ortho(-0.5*width,0.5*width,-0.5*height,0.5*height,near,far)

        return m.copyDataTo()

    def make_projection_matrix(self,width,height, fov, near, far):
        r_xy_factor = min((width, height)) * 1.0/fov
        r_x = r_xy_factor/width
        r_y = r_xy_factor/height
        r_zw_factor = 1.0/(far - near)
        r_z = (near + far)*r_zw_factor
        r_w = -2.0*near*far*r_zw_factor

        matrix = [0.0 for i in range(16)]
        matrix[ 0] = r_x;  matrix[ 1] = 0.0; matrix[ 2] = 0.0; matrix[ 3] = 0.0;
        matrix[ 4] = 0.0; matrix[ 5] = r_y;  matrix[ 6] = 0.0; matrix[ 7] = 0.0;
        matrix[ 8] = 0.0; matrix[ 9] = 0.0; matrix[10] = r_z;  matrix[11] = 1.0;
        matrix[12] = 0.0; matrix[13] = 0.0; matrix[14] = r_w;  matrix[15] = 0.0;

        return matrix


    def make_view_matrix(self):

        rx = QtGui.QMatrix4x4()
        rx.rotate(2*3.1415*self.xRot/180.0,0.0,0.0,1.0)
        ry = QtGui.QMatrix4x4()
        ry.rotate(2*3.1415*self.yRot/180.0,1.0,0.0,0.0)
        rz = QtGui.QMatrix4x4()
        rz.rotate(2*3.1415*self.zRot/180.0,0.0,0.0,1.0)

        trans = rx*ry*rz
        
        return trans.copyDataTo()


    def initializeGL(self):
        self.create_shaders()
        self.create_buffer()
        self.model_matrix = self.make_view_matrix();

        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_CULL_FACE) 
        GL.glCullFace(GL.GL_BACK)

    def paintGL(self):
        
        GL.glClearColor(.7, 0.7, 0.7, 1.0);
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT);
        
        shaders.glUseProgram(self.shader)

        GL.glUniformMatrix4fv(
            self.shader_uniforms['p_matrix'],
            1, GL.GL_FALSE,
            self.projection_matrix
        );

        GL.glUniformMatrix4fv(
            self.shader_uniforms['mv_matrix'],
            1, GL.GL_FALSE,
            self.model_matrix
        );


        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo);

        # format for PNPNPNPN.. buffer
        
        GL.glVertexAttribPointer(self.shader_attributes['position'],
                                 3,
                                 GL.GL_FLOAT,
                                 False,
                                 6*self.sizeof_float, # stride
                                 ctypes.c_void_p(0))
        GL.glEnableVertexAttribArray(self.shader_attributes['position'])

        GL.glVertexAttribPointer(self.shader_attributes['normal'],
                                 3,
                                 GL.GL_FLOAT,
                                 False,
                                 6*self.sizeof_float, # stride
                                 ctypes.c_void_p(3*self.sizeof_float))
        GL.glEnableVertexAttribArray(self.shader_attributes['normal'])


        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ebo);
        GL.glDrawElements(GL.GL_TRIANGLES, self.ebo_count, GL.GL_UNSIGNED_INT, ctypes.c_void_p(0))

        GL.glDisableVertexAttribArray(self.shader_attributes['position'])
        GL.glDisableVertexAttribArray(self.shader_attributes['normal'])
        shaders.glUseProgram(0)
        self.swapBuffers()

    def resizeGL(self, width, height):
        GL.glViewport(0, 0, width, height)
        #self.projection_matrix = self.make_projection_matrix(width,height,0.7,0.0625, 256.0)
        self.projection_matrix = self.make_orthographic(10.0,10.0,-10.0,10.0)

    def mouseDoubleClickEvent(self,event):
        self.create_buffer()
        self.updateGL()

    def mousePressEvent(self, event):
        self.lastPos = QtCore.QPoint(event.pos())

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & QtCore.Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = QtCore.QPoint(event.pos())

    
    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_()) 