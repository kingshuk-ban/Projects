# analysis
import numpy as np

class Analysis:
	def __init__(self, circuit, matrix):
		self.circuit = circuit
		self.matrix = matrix
	
	def linear_dc(self):
		m = self.matrix
		c = self.circuit
		x = m.x[1:]
		c.stamp(m)
		x = m.solve()
		m.x[1:] = x
		c.output(m.x)
		
	def diff_x(self, x, old_x):
		d = x - old_x
		d = abs(d)
		print("x:")
		print(x)
		print("old_x:")
		
		print(old_x)
		print("diff_x:")
		print(d)
		for x in d:
			if (x > 0.001):
				return True
		return False
		
	def NewtonRaphson(self, dc=True, maxiter=10):
		m = self.matrix
		c = self.circuit
		x = m.x[1:]
		old_x = np.array(x + 0.1)
		iter = 0
		while (self.diff_x(x, old_x) and (iter <= maxiter)):
			m.reset()
			old_x = x.copy()
			c.stamp(m, dc)
			x = m.solve(dc)
			iter = iter + 1
			m.x[1:] = x
			c.output(m.x)
		c.output(m.x)
		if (iter < maxiter):
			return (True, iter)
		else: 
			return (False, iter)
		
	def Transient(self, stop=20.0, step=0.001):
		c_time = 0.0
		print("Starting transient analysis for stop=%f" % (stop))
		self.circuit.start_tran()
		#self.matrix.x = np.zeros(self.matrix.x.size)
		while (c_time < stop):
			self.matrix.timestep = step
			c_time += step
			self.NewtonRaphson(False, 10)
			self.circuit.tran_output(self.matrix.x, c_time)
		self.circuit.end_tran()
		