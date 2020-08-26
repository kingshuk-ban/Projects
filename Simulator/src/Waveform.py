from matplotlib import pyplot

class Waveform: 

	def __init__(self, nodeMap):
		self.time = list()
		self.nodeMap = nodeMap
		self.values = dict()
		for n,i in self.nodeMap.items():
			self.values[n] = list()
			
	def addWave(self, x, time):
		self.time.append(time)
		for n,i in self.nodeMap.items():
			self.values[n].append(x[i])
			
	def plot(self):
		fig, p = pyplot.subplots(len(self.values), sharex=True)
		c = 0
		fig.suptitle('Waveform of all nodes')
		for n,i in self.nodeMap.items():
			p[c].plot(self.time, self.values[n])
			p[c].set(xlabel='time', ylabel='V(%s)'%(n))
			c = c + 1
		pyplot.show()
		