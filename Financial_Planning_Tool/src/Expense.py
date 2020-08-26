# This module is the expense holder

import utils

class Expense:
	def __init__(self):
		self.data = dict()
		self.total = 0.0
		
	def add(self, name, value):
		self.data[name] = value
		self.total += value
		
	def add_yearly(self, name, value):
		self.data[name] = value/12
		self.total += value/12
		
	def report(self):
		utils.report("Expenses (monthly)", self.data, self.total)
		
	def project(self, rate, years):
		d = dict()
		d = self.data
		fv = utils.project(d, rate, years)
		utils.report("Projected Expenses", d, fv)
		
	def get_monthly(self):
		return self.total
		
# Test
if __name__ == "__main__":
	e = Expense()
	e.add("groceries", 1000)
	e.add("utilities", 500)
	e.add("household", 500)
	e.add("housing", 2000)
	e.add_yearly("property tax", 7000)
	e.add_yearly("insurance", 3600)
	e.add_yearly("maintenance", 2000)
	e.add_yearly("vacation", 6000)
	e.report()
	e.project(3, 10)
	