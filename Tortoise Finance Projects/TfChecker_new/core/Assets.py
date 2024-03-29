# This module collects and reports all assets
import utils

class Assets:
	def __init__(self):
		self.data = dict()
		self.val = dict()
		self.wave = dict()
		self.total = 0.0
		self.stock_rate = 9.0
		self.bond_rate = 2.0
		self.cash_rate = 0.5
		self.real_rate = 3.0
		
	def add(self, name, value, rate):
		self.data[name] = (value, rate)
		self.val[name] = value
		self.total += value
	
	def reduce(self, name, take, rate):
		(v, r) = self.data[name]
		self.data[name] = (v - take, rate)
		self.val[name] = v - take
		self.total -= take

	def set_stock_rate(self, rate): 
		self.stock_rate = rate

	def set_bond_rate(self, rate):
		self.bond_rate = rate

	def set_cash_rate(self, rate):
		self.cash_rate = rate

	def set_real_rate(self, rate):
		self.real_rate = rate
		
	def project(self, years):
		fd = dict()
		fv = 0.0
		for n,v in self.data.items():
			d = dict()
			(val, r) = v
			d[n] = val
			fv += utils.project(d, r, years)
			fd[n] = d[n]
		utils.report("Projected Assets", fd, fv)
		return fd
		
	def report(self, title="Assets", file="Assets"):
		utils.report(title, self.val, self.total)
		utils.piechart(file, title, [n for n,v in self.data.items()], [v[0] for n,v in self.data.items()])
		
	def get_total(self):
		return self.total
		
# Test

if __name__ == "__main__":
	a = Assets()
	a.add("Cash", 30000, 2)
	a.add("Stocks", 40000, 8)
	a.add("Bonds", 40000, 4)
	a.report()
	a.project(10)
	
	
	
		
