# This module captures all sources of incomes and deductions
import utils
from utils import report
from utils import project

class Income:
	def __init__(self):
		self.data = dict()
		self.total = 0.0
		self.deductions = 0.0
		
	def add(self, name, value):
		self.data[name] = value
		self.total += value
	
	def deduct(self, name, value):
		self.data[name] = -value
		self.total -= value
		self.deductions += value
		
	def report(self):
		utils.report("Income (after deductions but before tax)", self.data, self.total)
	
	def project(self, rate, years):
		d = dict()
		d = self.data
		fv = utils.project(d, rate, years)
		report("Projected Income", d, fv)
		
	def get_monthly(self):
		return self.total/12
		

# Test
if __name__ == "__main__":
	i = Income()
	i.add("w2", 193000)
	i.add("p1", 8500)
	i.deduct("401k", 19500)
	i.report()
	i.project(3, 10)