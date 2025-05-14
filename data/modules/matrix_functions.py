from math import cos, sin
from numpy import array

def translate(pos):
    tx, ty, tz = pos
    return array(
        [
            [1,0,0,0],
            [0,1,0,0],
            [0,0,1,0],
            [tx,ty,tz,1]
        ]
    )
def rotate_x(a):
    return array(
        [[1,0,0,0],
        [0,cos(a),sin(a),0],
        [0,-sin(a),cos(a),0],
        [0,0,0,1]]
    )
def rotate_y(a):
    return array(
        [[cos(a),0,-sin(a),0],
        [0,1,0,0],
        [sin(a),0,cos(a),0],
        [0,0,0,1]]
    )

def rotate_z(a):
    return array(
        [[cos(a),sin(a),0,0],
        [-sin(a),cos(a),0,0],
        [0,0,1,0],
        [0,0,0,1]]
    )

def scale(n):
    return array(
        [[n,0,0,0],
        [0,n,0,0],
        [0,0,n,0],
        [0,0,0,1]]
    )