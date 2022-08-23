# This module calculates the budget
import utils
from utils import output
from Income import Income
from Expense import Expense
from Tax import Tax
from Debt import Debt

class Budget:
	def __init__(self):
		self.data = dict()
		self.surplus = 0.0
		
	def add(self, i, t, d, e):
		self.data["income"] = i.get_monthly()
		self.data["tax"] = -(t.get_monthly())
		self.data["debt payment"] = -(d.get_monthly())
		self.data["expenses"] = -(e.get_monthly())
		self.surplus = utils.sum(self.data)

	def add_expense(self, name, value):
		self.data[name] = -(value)
		self.surplus = utils.sum(self.data)
		
	def report(self):
		utils.report("Budget (monthly)", self.data, self.surplus)
		if (self.surplus < 0.0):
			output.warn("Spending exceeds available income by %.2f. Please readjust." % -(self.surplus))
		else:
			output.info("You have surplus %.2f to invest." % (self.surplus))
		pie_n = [n for n,v in self.data.items() if (n != "income")]
		pie_v = [abs(v) for n,v in self.data.items() if (n != "income")]
		pie_n.append("surplus")
		pie_v.append(self.surplus)
		utils.piechart("Budget", "Budget Allocation", pie_n, pie_v)
		
	def get_monthly(self):
		return self.surplus
		
# Test
if __name__ == "__main__":
	i = Income()
	i.add("w2", 193000)
	i.deduct("401k", 19500)
	i.deduct("hsa", 7100)
	i.report()
	
	t = Tax(i.data)
	t.credit("child1", 500)
	t.credit("child2", 500)
	t.calculate()
	t.report()
	
	d = Debt()
	d.add_fixed("mortgage", 225000, 4.125, 30)
	d.add_variable("cc1", 4000, 10)
	d.add_variable("cc2", 10000, 10)
	p = d.calculate()
	d.report()
	
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
	
	b = Budget()
	b.add(i, t, d, e)
	b.report()
	