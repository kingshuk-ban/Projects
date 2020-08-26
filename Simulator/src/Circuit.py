# Circuit to hold the nodes and devices
import numpy as np
from Device import Resistor
from Device import Isource
from Device import Vsource
from Device import NonLinear
from Device import bsource
from Device import Diode
from Device import Capacitor
from Matrix import Matrix
from Waveform import Waveform

class Circuit:
	devices = list()

	def __init__(self, nodes):
		e_list = list(enumerate(nodes))
		self.nodeMap = dict()
		index = 1
		for e in e_list:
			i = e[0]
			n = e[1]
			if (n == '0' or n == 'gnd'):
				self.nodeMap[n] = 0
			else:
				self.nodeMap[n] = index
				index = index + 1
	
	def addDevice(self, card, lastnode):
		branch = False
		name = card['D']
		if (name == 'R'):
			d = Resistor(card, self.nodeMap)
		elif (name == 'I'):
			d = Isource(card, self.nodeMap)
		elif (name == 'V'):
			d = Vsource(card, self.nodeMap, lastnode)
			branch = True
		elif (name == 'N'):
			d = NonLinear(card, self.nodeMap)
		elif (name == 'b'):
			d = bsource(card, self.nodeMap)
		elif (name == 'd'):
			d = Diode(card, self.nodeMap)
		elif (name == 'C'):
			d = Capacitor(card, self.nodeMap)
		d.print()
		self.devices.append(d)
		return branch
			
	def stamp(self, matrix, dc):
		for d in self.devices:
			d.stamp(matrix, dc)
		
	def print(self):
		print("Circuit- Total no. of nodes: %d" % (len(self.nodeMap)))
		print("Circuit- Total no. of devices: %d" % (len(self.devices)))
		print("Circuit- nodeMap...")
		print(self.nodeMap)
		print("Circuit- devices...")
		for d in self.devices:
			d.print()
			
	def output(self, x):
		print("DC solution:")
		print("------------")
		for n,i in self.nodeMap.items():
			value = x[i]
			print("V(%s)=%f" % (n, value))
			
	def start_tran(self):
		self.f = open('tran.out', 'w')
		self.wave = Waveform(self.nodeMap)
		
	def end_tran(self):
		self.f.close()
		self.wave.plot()
			
	def tran_output(self, x, time):
		print("@%f -> " % (time))
		print("------------")
		self.f.write("t=%f" % (time))
		for n,i in self.nodeMap.items():
			value = x[i]
			print("V(%s)=%f" % (n, value))
			self.f.write("	V(%s)=%f" % (n, value))
		self.f.write("\n")
		self.wave.addWave(x, time)
		
		