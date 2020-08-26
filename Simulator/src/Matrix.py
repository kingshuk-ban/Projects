# This module populates a matrix
import numpy as np
from numpy import zeros
from scipy.linalg import lu
from numpy.linalg import qr
from numpy.linalg import cholesky
from numpy.linalg import eig
from numpy.linalg import svd

class Matrix:
	def __init__(self, size):
		self.size = size
		self.A= zeros((size, size))
		self.x = zeros(size)
		self.b = zeros(size)
		self.C = zeros((size, size))
		self.timestep = 1.0
		self.integration_constant = 2.0 # trapezoidal
	
	def trim(self):
		self.A = self.A[1:, 1:]
		self.C = self.C[1:, 1:]
		self.b = self.b[1:]
		self.b.reshape(len(self.b), 1)
		self.x = self.x[1:]
		
	def stamp_G(self, x, y, v):
		self.A[x, y] += v
		
	def stamp_C(self, x, y, v):
		self.C[x, y] += v
		
	def solve(self, dc=True):
		A = self.A[1:, 1:]
		C = self.C[1:, 1:]
		if (dc):
			M = A
		else:
			M = A + (self.integration_constant/self.timestep) * C 
		b = self.b[1:]
		b.reshape(len(b), 1)
		x = self.x[1:]
		x = np.linalg.solve(M, b)
		return x
		
	def reset(self):
		size = self.size
		self.A = zeros((size, size))
		self.C = zeros((size, size))
		self.b = zeros(size)
		
	def print(self):
		print(self.A)
		print(self.C)
		print(self.x)
		print(self.b)
		
	def factor(self):
		P, L, U = lu(self.A)
		
	def LU(self):
		P, L, U = lu(self.A)
		return P, L, U
	
	def QR(self):
		Q, R = qr(self.A, 'complete')
		return Q, R
		
	def Cholesky(self):
		L = cholesky(self.A)
	
	def Eigen(self):
		values, vectors = eig(self.A)
		return values, vectors
	
	def SVD(self):
		U, s, V = svd(self.A)
		return U, s, V

		
	