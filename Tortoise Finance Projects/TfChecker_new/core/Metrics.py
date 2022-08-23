# This class calculates the metrics
from Income import Income
from Tax import Tax
from Budget import Budget
from Expense import Expense
from Debt import Debt
from Assets import Assets
import utils
from utils import output

class Metrics:
	def __init__(self, i, b, e, d, a):
		self.income = i.get_monthly()
		self.budget = b.get_monthly()
		self.expense = e.get_monthly()
		self.debt = d.get_monthly()
		self.debt_balance = d.total
		self.assets = a.get_total()
		self.ratios = dict()
		self.metrics = dict()
		
	def calculate(self):
		self.metrics["Net worth"] = self.assets - self.debt_balance
		self.ratios["Net worth to assets"] = ((self.assets - self.debt_balance) / self.assets) * 100.0
		self.ratios["Debt to Assets"] = (self.debt_balance / self.assets) * 100.0
		self.ratios["Expense to Income"] = (self.expense / self.income) * 100.0
		self.ratios["Debt to Income"] = (self.debt / self.income) * 100.0
		self.ratios["Savings ratio"] = (self.budget / self.income) * 100.0
		
	def report(self):
		output.info("Your net worth is %s%.2f" % (utils.currency_symbol, self.metrics["Net worth"]))
		utils.report("Metrics", self.ratios, 0.0, pre="", post="%")
		
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
	#d.add_variable("cc1", 140000, 10)
	#d.add_variable("cc2", 10000, 8)
	#d.add_variable("cc3", 5000, 16)
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
	
	a = Assets()
	a.add("Cash", 30000, 2)
	a.add("Stocks", 40000, 8)
	a.add("Bonds", 40000, 4)
	a.report()
	
	m = Metrics(i, b, e, d, a)
	m.calculate()
	m.report()
	