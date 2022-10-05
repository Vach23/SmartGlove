# This module contains matrix transformations and transformations between matrix and quaternion

from pyrr import *

def transpose_mat(M):
	return  list(map(list, zip(*M)))


def apply_quaternion(verticies, quat):
	new_verticies = []

	M = quat2mat3x3(quat)
	M = transpose_mat(M)
	for k in verticies:
		new_verticies.append(matrix33.apply_to_vector(M, k))

	return new_verticies


def apply_rotation_mat(verticies, M):
	new_verticies = []
	
	for k in verticies:
		new_verticies.append(matrix33.apply_to_vector(M, k))

	return new_verticies


def quat2mat3x3(quat):
	w, x, y, z= quat
	M =[[1 - 2*y**2 - 2*z**2, 2*x*y - 2*z*w, 2*x*z + 2*y*w],
		[2*x*y + 2*z*w, 1 - 2*x**2 - 2*z**2, 2*y*z - 2*x*w],
		[2*x*z - 2*y*w, 2*y*z + 2*x*w, 1 - 2*x**2 - 2*y**2]]
	return M


def quat2mat4x4(quat):
	w, x, y, z= quat
	M =[[1 - 2*y**2 - 2*z**2, 2*x*y - 2*z*w, 2*x*z + 2*y*w,0],
		[2*x*y + 2*z*w, 1 - 2*x**2 - 2*z**2, 2*y*z - 2*x*w,0],
		[2*x*z - 2*y*w, 2*y*z + 2*x*w, 1 - 2*x**2 - 2*y**2,0],
		[0,0,0,1]]
	return M