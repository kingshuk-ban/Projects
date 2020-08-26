# This module calculates tax on given income
import utils
from Income import Income

TaxSlabs = {
	"rates":            [10,   12,    22,    24,     32,     35,     37],
	"single":           [9700, 39475, 84200, 160725, 204100, 510300, 10000000000],
	"married_joint":    [19400, 78950, 168400, 321450, 408200, 612350, 10000000000],
	"married_separate": [9700, 39475, 84200, 160725, 204100, 306175, 10000000000],
	"head_household":   [13850, 52850, 84200, 160700, 204100, 510300, 10000000000]
}

class Tax:
	def __init__(self):
		self.credits = dict()
		self.taxes = dict()
		self.total = 0.0
		self.nominal = 0.0
		self.filling = ""
	
	def addIncome(self, i):
		self.income = i
		
	def addFilling(self, filling):
		self.filling = filling
	
	def credit(self, name, value):
		self.credits[name] = -value
		
	def report(self):
		utils.report("Taxes", self.taxes, self.total)
		if (len(self.credits.items()) != 0):
			utils.report("Tax credits", self.credits, utils.sum(self.credits))
	
	def project(self, rate, years):
		d = dict()
		d = self.income
		fv = utils.project(d, rate, years)
		t = Tax(d)
		t.credits = self.credits
		t.calculate()
		utils.report("Projected Tax", t.credits, t.total)
	
	def calculate(self):
		col = TaxSlabs[self.filling]
		i = 0
		prev = 0.0
		current = 0.0
		income = utils.sum(self.income)
		self.taxes['Federal Income Tax'] = 0.0
		for rate in TaxSlabs["rates"]:
			current = col[i]
			i = i + 1
			if (income >= current):
				residual = current - prev
			else:
				residual = income - prev
				self.nominal = rate
			self.taxes['Federal Income Tax'] += (rate/100) * residual
			prev = current
			if (prev > income):
				break
		# Social Security Tax
		adjusted_income = min(137700, income)
		self.taxes['Social Security Tax'] = 0.062 * adjusted_income
		self.taxes['Medicare Tax'] = 0.0145 * income
		self.total = utils.sum(self.taxes)
		# adjust the credits
		self.total -= utils.sum(self.credits)
		
	def get_monthly(self):
		return self.total/12
		
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
	t.project(3, 10)
	
	