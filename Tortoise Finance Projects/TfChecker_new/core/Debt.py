# This module calculates debt
import utils

class Debt:
	def __init__(self):
		self.fixed = dict()
		self.unknown = dict()
		self.total = 0.0
		self.payment = dict()
	
	def add_fixed(self, name, value, rate, years):
		self.fixed[name] = (value, rate, years)
		self.total += value
	
	def add_variable(self, name, value, rate):
		self.unknown[name] = (value, rate, -1)
		self.total += value
		
	def calculate(self):
		for n,v in self.fixed.items():
			self.payment[n] = utils.payment(v[0], v[1], v[2])
		for n,v in self.unknown.items():
			self.payment[n] = utils.payment(v[0], v[1], v[2])
		return utils.sum(self.payment)
	
	def report(self):
		utils.report("Debt payments (monthly)", self.payment, utils.sum(self.payment))
		if (len(self.payment.items()) > 1):
			utils.piechart("Payments", "Your debt payments", [n for n,v in self.payment.items()], [v for n,v in self.payment.items()])
		
	def get_monthly(self):
		return utils.sum(self.payment)
		
		
if __name__ == "__main__":
	d = Debt()
	d.add_fixed("mortgage", 225000, 4.125, 30)
	d.add_variable("cc1", 4000, 10)
	d.add_variable("cc2", 10000, 10)
	p = d.calculate()
	d.report()
	
