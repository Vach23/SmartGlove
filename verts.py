# This module contains coordinates of all points and verticies to render the representation of hand rotation

from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

############### FINGER: ###############

l1 = 4
l2 = 2.5
l3 = 2

u1 = 180-103.5
u1 = u1*pi/180
u2 = 180-77.37
u2 = u2*pi/180
u3 = 180-101.5
u3 = u3*pi/180


vertex_FINGER = [
    [4, 2.2, 0],
    [4, 4, 0],
    [4+l1, 4, 0],
    [4+l1+l2, 4, 0],
    [4+l1+l2+l3, 3.7, 0],
    [4+l1+l2+l3, 2.5, 0],
    [4+l1+l2, 2.2, 0],
    [4+l1, 2.2, 0]
    ]

edge_FINGER = [
    [0,1],
    [1,2],
    [2,3],
    [3,4],
    [4,5],
    [5,6],
    [6,7],
    [7,0],
    [2,7],
    [3,6]
    ]

def render_FINGER(verts):
    glBegin(GL_LINES)
    for edge in edge_FINGER:
        for vertex in edge:
            glVertex3fv(verts[vertex])
    glEnd()

def bend_FINGER(b):
    b*=-1
    ll1y = l1*cos(b*u1)
    ll1z = l1*sin(b*u1)

    ll2y = l2*cos(b*(u1+u2))
    ll2z = l2*sin(b*(u1+u2))

    ll3y = l3*cos(b*(u1+u2+u3))
    ll3z = l3*sin(b*(u1+u2+u3))

    bended_vertex_FINGER = [
        [4, 2.2, 0],
        [4, 4, 0],
        [4+ll1y, 4, ll1z],
        [4+ll1y+ll2y, 4, ll1z+ll2z],
        [4+ll1y+ll2y+ll3y, 3.7, ll1z+ll2z+ll3z],
        [4+ll1y+ll2y+ll3y, 2.5, ll1z+ll2z+ll3z],
        [4+ll1y+ll2y, 2.2, ll1z+ll2z],
        [4+ll1y, 2.2,  ll1z]
        ]

    return bended_vertex_FINGER

############### HAND: ###############
vertex_HAND = [
    [0,-4,0],
    [5,-4,0],
    [5, 2.2,0],
    [4, 2.2,0],
    [4, 4,0],
    [0, 4,0],
    [-5, 3,0],
    [-5,-2,0],

    [0,-4,-1],
    [5,-4,-1],
    [5,2.2,-1],
    [4,2.2,-1],
    [4,4,-1],
    [0,4,-1],
    [-5,3,-1],
    [-5,-2,-1]
    ]

edge_HAND = [
    [0,1],
    [1,2],
    [2,3],
    [3,4],
    [4,5],
    [5,6],
    [6,7],
    [7,0],
    [8,9],
    [9,10],
    [10,11],
    [11,12],
    [12,13],
    [13,14],
    [14,15],
    [15,8],
    [0,8],
    [1,9],
    [2,10],
    [3,11],
    [4,12],
    [5,13],
    [6,14],
    [7,15]
    ]

def render_HAND(verts):
    glBegin(GL_LINES)
    for edge in edge_HAND:
        for vertex in edge:
            glVertex3fv(verts[vertex])
    glEnd()

############### IMU: ###############
vertex_IMU = [
    [ 1.25,-0.75, 0],
    [-1.25,-0.75, 0],
    [-1.25, 0.75, 0],
    [ 1.25, 0.75, 0],
    [ 1.25,-0.75,-0.1],
    [-1.25,-0.75,-0.1],
    [-1.25, 0.75,-0.1],
    [ 1.25, 0.75,-0.1],
    [0,0,0],
    [0,-1,0],
    [1,0,0],
    [0,0,1]
    ]

edge_IMU = [
    [0,1],
    [1,2],
    [2,3],
    [3,0],
    [4,5],
    [5,6],
    [6,7],
    [7,4],
    [0,4],
    [1,5],
    [2,6],
    [3,7],
    ]


def render_IMU(verts):
    glBegin(GL_LINES)
    for edge in edge_IMU:
        for vertex in edge:
            glVertex3fv(verts[vertex])
    glEnd()
    glLineWidth(5)
    glBegin(GL_LINES)
    glColor(1,0,0)
    glVertex3fv(verts[8])
    glVertex3fv(verts[9])
    glColor(0,1,0)
    glVertex3fv(verts[8])
    glVertex3fv(verts[10])
    glColor(0,0,1)
    glVertex3fv(verts[8])
    glVertex3fv(verts[11])
    glColor(1,1,1)
    glEnd()
    glLineWidth(1)