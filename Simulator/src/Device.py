# Class for Device
import numpy as np
import math

def limit(value):
	return value
	if (value < -5.0):
		return -5.0
	elif (value > 5.0):
		return 5.0
	else: 
		return value 
	

class Device:
	
	def __init__(self, card):
		self.name = card['D']
		self.nodes = card['N']
		self.value = float(card['V'])
		self.node_i = list()
		print(card)
		
	def index(self, nodeMap):
		for n in self.nodes:
			self.node_i.append(nodeMap[n])
		
	def stamp(self, matrix, dc):
		if (dc):
			print("DC:- stamped by %s" % (self.name))
		else:
			print("TRAN: stamped by %s" % (self.name))
		matrix.print()
		return False
		
	def print(self):
		print("Device: name: %s nodes: (%s) value: %d" % (self.name, self.node_i, self.value))
		

class Resistor(Device):

	def __init__(self, card, nodeMap):
		super().__init__(card)
		super().index(nodeMap)
		self.n1 = self.node_i[0]
		self.n2 = self.node_i[1]
		
	def stamp(self, matrix, dc):
		matrix.A[self.n1, self.n1] += (1.0/self.value)
		matrix.A[self.n1, self.n2] += -(1.0/self.value)
		matrix.A[self.n2, self.n1] += -(1.0/self.value)
		matrix.A[self.n2, self.n2] += (1.0/self.value)
		super().stamp(matrix, dc)
		return False
		
	def print(self):
		print("Resistor: name: %s nodes: (%s) value: %d" % (self.name, self.node_i, self.value))
		
		
class Isource(Device):

	def __init__(self, card, nodeMap):
		super().__init__(card)
		super().index(nodeMap)
		self.n1 = self.node_i[0]
		self.n2 = self.node_i[1]
		
	def stamp(self, matrix, dc):
		matrix.b[self.n1] += self.value
		matrix.b[self.n2] += -(self.value)
		super().stamp(matrix, dc)
		return False
	
	def print(self):
		print("Isource: name: %s nodes: (%s) value: %d" % (self.name, self.node_i, self.value))
		
		
class Vsource(Device):

	def __init__(self, card, nodeMap, lastnode):
		super().__init__(card)
		super().index(nodeMap)
		self.n1 = self.node_i[0]
		self.n2 = self.node_i[1]
		self.b1 = lastnode
	
	def stamp(self, matrix, dc):
		matrix.A[self.b1, self.n1] += 1.0
		matrix.A[self.b1, self.n2] += -1.0
		matrix.A[self.n1, self.b1] += 1.0
		matrix.A[self.n2, self.b1] += -1.0
		matrix.b[self.b1] += self.value
		super().stamp(matrix, dc)
		return True
		
class CCCS(Device):

	def __init__(self, card, nodeMap, lastnode):
		super().__init__(card)
		super().index(nodeMap)
		self.n1 = self.node_i[0]
		self.n2 = self.node_i[1]
		self.k = self.node_i[2]
		self.l = self.node_i[3]
		self.b1 = lastnode
		
	def stamp(self, matrix, dc):
		matrix.A[self.n1, self.b1] += self.alpha
		matrix.A[self.n2, self.b1] += -(self.alpha)
		matrix.A[self.k, self.b1] += 1.0
		matrix.A[self.l, self.b1] += -(1.0)
		matrix.A[self.b1, self.k] += (self.gkl)
		matrix.A[self.b1, self.l] += -(self.gkl)
		
class NonLinear(Device):

	def __init__(self, card, nodeMap):
		super().__init__(card)
		super().index(nodeMap)
		self.n1 = self.node_i[0]
		self.n2 = self.node_i[1]
		self.n3 = self.node_i[2]
		self.n4 = self.node_i[3]
		
	def stamp(self, matrix, dc):
		# Equation : i(1, 2) = v1^2 + v2^2 + v3 + v4
		v1 = matrix.x[self.n1]
		v2 = matrix.x[self.n2]
		v3 = matrix.x[self.n3]
		v4 = matrix.x[self.n4]
		i0 = v1**2 + v2**2 + v3 + v4
		di_dv1 = 2*v1
		di_dv2 = 2*v2
		di_dv3 = 1
		di_dv4 = 1
		i = -i0 + di_dv1*v1 + di_dv2*v2 + di_dv3*v3 + di_dv4*v4
		
		matrix.A[self.n1, self.n1] += di_dv1
		matrix.A[self.n1, self.n2] += di_dv2
		matrix.A[self.n1, self.n3] += di_dv3
		matrix.A[self.n1, self.n4] += di_dv4
		matrix.A[self.n2, self.n1] += -1.0 * di_dv1
		matrix.A[self.n2, self.n2] += -1.0 * di_dv2
		matrix.A[self.n2, self.n3] += -1.0 * di_dv3
		matrix.A[self.n2, self.n4] += -1.0 * di_dv4
		matrix.b[self.n1] += i
		matrix.b[self.n2] += -i
		super().stamp(matrix, dc)
		print("i from NonLinear: %f, %f (v1:%f v2:%f v3:%f v4:%f)" % (i, i0, v1, v2, v3, v4))

class bsource(Device):
	def __init__(self, card, nodeMap):
		super().__init__(card)
		super().index(nodeMap)
		self.n1 = self.node_i[0]
		self.n2 = self.node_i[1]
		self.n3 = self.node_i[2]
		self.n4 = self.node_i[3]
		
	def stamp(self, matrix, dc):
		# Equation : B1 (d s)  i=k((vg – vs- vt)(vd-vs) -0.5*(vd-vs)2)
		vd = matrix.x[self.n1]
		vs = matrix.x[self.n2]
		vg = matrix.x[self.n3]
		vt = matrix.x[self.n4]
		k = 0.3 
		i0 = limit(k * ((vg - vs - vt)*(vd - vs) - 0.5*(vd - vs)**2))
	
		di_dvd = limit(k * ((vg - vs - vt) - (vd - vs))) 
		di_dvg = limit(k * (vd - vs)); 
		di_dvs = limit(k * (-(vg - vs - vt) - (vd - vs) + (vd - vs)))
		di_dvt = limit(k * ((vg - vs - vt) - (vd - vs) + (vd - vs)))
		i = -i0 + di_dvg*vg + di_dvs*vs + di_dvd*vd
		
		matrix.A[self.n1, self.n1] += di_dvd
		matrix.A[self.n1, self.n2] += di_dvs
		matrix.A[self.n1, self.n3] += di_dvg
		matrix.A[self.n1, self.n4] += di_dvt
		matrix.A[self.n2, self.n1] += -1.0 * di_dvd
		matrix.A[self.n2, self.n2] += -1.0 * di_dvs
		matrix.A[self.n2, self.n3] += -1.0 * di_dvg
		matrix.A[self.n2, self.n4] += -1.0 * di_dvt
		matrix.b[self.n1] += i
		matrix.b[self.n2] += -i
		super().stamp(matrix, dc)
		print("i from NonLinear: %f (vd:%f vs:%f vg:%f vt:%f)" % (i, vd, vs, vg, vt))
		
class Diode(Device):
	def __init__(self, card, nodeMap):
		super().__init__(card)
		super().index(nodeMap)
		self.n1 = self.node_i[0]
		self.n2 = self.node_i[1]
		
	def stamp(self, matrix, dc):
		# Equation : i = Is*exp(V/VT - 1)
		#            Is = 1e-14, VT = 25mV
		VT = 0.025
		Is = 1e-14
		va = matrix.x[self.n1]
		vb = matrix.x[self.n2]
		V = va - vb
		if (V > 0.5):
			i0 = (V - 0.5) * 0.1
			di_dv = 0.1
		else:
			i0 = Is * math.exp(V/VT - 1)
			di_dv = (1.0/VT)*Is*math.exp(V/VT)
		
		i = i0 - di_dv*V
		print("diode: va:%f vb:%f i0:%f di_dv:%f i:%f" % (va, vb, i0, di_dv, i))
	
		matrix.A[self.n1, self.n1] += di_dv
		matrix.A[self.n1, self.n2] += -1.0 * di_dv
		matrix.A[self.n2, self.n1] += -1.0 * di_dv
		matrix.A[self.n2, self.n2] += di_dv
		matrix.b[self.n1] += i
		matrix.b[self.n2] += -i
		super().stamp(matrix, dc)
		#print("i from NonLinear: %f (V:%f)" % (i, V))
		
class Capacitor(Device):
	def __init__(self, card, nodeMap):
		super().__init__(card)
		super().index(nodeMap)
		self.n1 = self.node_i[0]
		self.n2 = self.node_i[1]
		self.q_p = 0.0
		
	def stamp(self, matrix, dc):
		if (dc):
			return
		V = matrix.x[self.n1] - matrix.x[self.n2]
		h = matrix.timestep
		q = self.value * V
		dq_dv = self.value
		dq_dt = (q - self.q_p)/h
		K = matrix.integration_constant
		rhs = (K*q/h) + dq_dt
		self.q_p = q
	
		matrix.C[self.n1, self.n1] += self.value
		matrix.C[self.n1, self.n2] += -1.0 * self.value
		matrix.C[self.n2, self.n1] += -1.0 * self.value
		matrix.C[self.n2, self.n2] += self.value
		matrix.b[self.n1] += rhs
		matrix.b[self.n2] += -(rhs)
		super().stamp(matrix, dc)
		print("q: %f (V:%f)" % (q, V))
		
