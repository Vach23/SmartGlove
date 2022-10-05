import numpy
import pygame
from pygame.locals import *

from verts import *
from quat_mat import *

import serial

RAD_2_DEG = 180/pi
DEG_2_RAD = pi/180

bend_max = 640
bend_min = 290


def calculate_bend(f):
	bend_range = bend_max - bend_min
	bend_step = 1/bend_range
	return (f-bend_min)*bend_step

def MadgwickQuaternionUpdate(q, data, sample_freq):
    beta = 0
    ay, ax, az, gy, gx, gz, my, mx, mz = data
    q1, q2, q3, q4 = q

    gy *= -1 #Kvůli transpozici rotační matice a vykreslení

    #mx *=1
    #my *=1
    mz *=-1

    d = 131/16.4
    gx *=DEG_2_RAD/d
    gy *=DEG_2_RAD/d
    gz *=DEG_2_RAD/d

    _2q1 = 2 * q1
    _2q2 = 2 * q2
    _2q3 = 2 * q3
    _2q4 = 2 * q4
    _2q1q3 = 2 * q1 * q3
    _2q3q4 = 2 * q3 * q4
    q1q1 = q1 * q1
    q1q2 = q1 * q2
    q1q3 = q1 * q3
    q1q4 = q1 * q4
    q2q2 = q2 * q2
    q2q3 = q2 * q3
    q2q4 = q2 * q4
    q3q3 = q3 * q3
    q3q4 = q3 * q4
    q4q4 = q4 * q4

    norm = sqrt(ax * ax + ay * ay + az * az)
    norm = 1/norm
    ax *= norm
    ay *= norm
    az *= norm

    norm = sqrt(mx * mx + my * my + mz * mz)

    norm = 1/norm
    mx *= norm
    my *= norm
    mz *= norm

    #// Reference direction of Earth's magnetic field
    _2q1mx = 2 * q1 * mx
    _2q1my = 2 * q1 * my
    _2q1mz = 2 * q1 * mz
    _2q2mx = 2 * q2 * mx
    hx = mx * q1q1 - _2q1my * q4 + _2q1mz * q3 + mx * q2q2 + _2q2 * my * q3 + _2q2 * mz * q4 - mx * q3q3 - mx * q4q4
    hy = _2q1mx * q4 + my * q1q1 - _2q1mz * q2 + _2q2mx * q3 - my * q2q2 + my * q3q3 + _2q3 * mz * q4 - my * q4q4
    _2bx = sqrt(hx * hx + hy * hy)
    _2bz = -_2q1mx * q3 + _2q1my * q2 + mz * q1q1 + _2q2mx * q4 - mz * q2q2 + _2q3 * my * q4 - mz * q3q3 + mz * q4q4
    _4bx = 2 * _2bx
    _4bz = 2 * _2bz

    #// Gradient decent algorithm corrective step
    s1 = -_2q3 * (2 * q2q4 - _2q1q3 - ax) + _2q2 * (2 * q1q2 + _2q3q4 - ay) - _2bz * q3 * (_2bx * (0.5 - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + (-_2bx * q4 + _2bz * q2) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my) + _2bx * q3 * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz)
    s2 = _2q4 * (2 * q2q4 - _2q1q3 - ax) + _2q1 * (2 * q1q2 + _2q3q4 - ay) - 4 * q2 * (1 - 2 * q2q2 - 2 * q3q3 - az) + _2bz * q4 * (_2bx * (0.5 - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + (_2bx * q3 + _2bz * q1) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my) + (_2bx * q4 - _4bz * q2) * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz)
    s3 = -_2q1 * (2 * q2q4 - _2q1q3 - ax) + _2q4 * (2 * q1q2 + _2q3q4 - ay) - 4 * q3 * (1 - 2 * q2q2 - 2 * q3q3 - az) + (-_4bx * q3 - _2bz * q1) * (_2bx * (0.5 - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + (_2bx * q2 + _2bz * q4) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my) + (_2bx * q1 - _4bz * q3) * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz)
    s4 = _2q2 * (2 * q2q4 - _2q1q3 - ax) + _2q3 * (2 * q1q2 + _2q3q4 - ay) + (-_4bx * q4 + _2bz * q2) * (_2bx * (0.5 - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + (-_2bx * q1 + _2bz * q3) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my) + _2bx * q2 * (_2bx * (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz)
    norm = sqrt(s1 * s1 + s2 * s2 + s3 * s3 + s4 * s4);   # // normalise step magnitude
    norm = 1/norm;
    s1 *= norm;
    s2 *= norm;
    s3 *= norm;
    s4 *= norm;

    #// Compute rate of change of quaternion
    qDot1 = 0.5 * (-q2 * gx - q3 * gy - q4 * gz) - beta * s1
    qDot2 = 0.5 * (q1 * gx + q3 * gz - q4 * gy) - beta * s2
    qDot3 = 0.5 * (q1 * gy - q2 * gz + q4 * gx) - beta * s3
    qDot4 = 0.5 * (q1 * gz + q2 * gy - q3 * gx) - beta * s4

    #// Integrate to yield quaternion
    q1 += qDot1 * 1 /sample_freq
    q2 += qDot2 * 1 /sample_freq
    q3 += qDot3 * 1 /sample_freq
    q4 += qDot4 * 1 /sample_freq
    norm = sqrt(q1 * q1 + q2 * q2 + q3 * q3 + q4 * q4);   # // normalise quaternion
    norm = 1/norm
    q[0] = q1 * norm
    q[1] = q2 * norm
    q[2] = q3 * norm
    q[3] = q4 * norm

    return q


def main():
    ser = serial.Serial('COM5', 115200)
    quat = [1,0,0,0] #Startovní pozice

    flex = bend_min

    pygame.init()
    display = (900,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    gluPerspective(50, (display[0]/display[1]), 0.01, 50.0)
    glTranslatef(0.0, 0.0, -20.0)
    glRotatef(-80,1,0,0)
    glRotatef(50+90,0,0,1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ser.close()
                pygame.quit()
                quit()

        buff = ser.in_waiting
        if buff > 0:
            data = ser.readline()
            #print(data)
            data = str(ser.readline(),'utf-8').split(' ')[0:10]
            data = [float(i) for i in data]
            quat = MadgwickQuaternionUpdate(quat, data[0:9], 250)
            flex = data[9]

        if buff > 50:
            continue 

        #flex = 80

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        vertex_FINGER_t = apply_quaternion(bend_FINGER(calculate_bend(flex)), quat)
        vertex_HAND_t = apply_quaternion(vertex_HAND, quat)
        vertex_IMU_t = apply_quaternion(vertex_IMU, quat)

        render_FINGER(vertex_FINGER_t)
        render_HAND(vertex_HAND_t)
        render_IMU(vertex_IMU_t)


        pygame.display.flip()
        pygame.time.wait(5)

main()