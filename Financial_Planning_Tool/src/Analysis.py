# Algorithm to analyze the financial situation
import sys
import utils
#from utils import action, info, warn, error, quit, section_start, section_end
from matplotlib import pyplot
from utils import output
import numpy as np
from Asset_Allocation import Asset_Allocation
	
HIGH_INTEREST_RATE = 4.0
EMERGENCY_FUND_MONTHS = 6

# TODO :
# 1. Debt payoff and emergency fund schedule not taken into account.
# 2. Need to add the surplus back when done for investment,
# 3. Budget - need to reduce the debt payment once debt free.
# 4. Mortgage payoff plan
# 5. 401k and other pre-tax investments not taken into account.
# 		- debt payoff
#       - asset growth
# 6. Bonus allocation

class Analysis:
	def __init__(self, p, i, d, b, e, a, m):
		self._p = p
		self._i = i
		self._d = d
		self._b = b
		self._e = e
		self._a = a
		self._m = m
		self.surplus = self._b.get_monthly()
		self.m_for_ef_debt = 0
		self.allocation = dict()
		
	def live_below_means(self):
		print("\n")
		output.section_start("Its good to live within your means...")
		output.info("ANALYSIS - Checking living below means....")
		excess = self._b.get_monthly()
		if (self._b.get_monthly() <= 0.0):
			output.warn("Live below your means!!")
			output.action("You need to reduce your expenses by at least $%.2f" % (-(excess)))
			return False
		else:
			output.info("You are living below your means by $%.2f" % (excess))
		output.info("ANALYSIS - Done living below means....")
		output.section_end()
		return True

	def emergency_fund(self):
		print("\n")
		output.section_start("Emergency Fund means sleep in peace...")
		output.info("ANALYSIS - Checking and allocating emergency fund....")
		a = self._a
		b = self._b
		e = self._e
		expenses = e.get_monthly()
		required = expenses * EMERGENCY_FUND_MONTHS
		self.allocation['Emergency Fund'] = 0.0

		if (required < a.total):
			output.info("You have enough emergency fund %.2f in your assets %.2f." % (required, a.total))
		output.info("Allocating your assets to build emergency fund %.2f" % (required))
		output.action("Build or allocate emergency fund.")

		for n,v in sorted(a.data.items(), key=lambda x:x[1][1]):
			if (required <= 0.0):
				break
			(val, rate) = v
			take = min(val, required)
			output.action("Move %.2f from %s to emergency fund." % (take, n))
			a.reduce(n, take, rate)
			required -= take
			self.allocation['Emergency Fund'] += take
	
		if (required > 0.0):
			output.warn("Need monthly budget to build remaining emergency fund %.2f." % (required))
			months = int((required + b.get_monthly()) / b.get_monthly()); 
			#print("		No. of months - %d" % (months))
			output.action("You need to first build your emergency fund for the next %d months." % (months))
			self.m_for_ef_debt = months
			self._b.add_expense("Emergency Fund", b.get_monthly())
			self._b.report()
			#quit()
		else: 
			output.info("Your emergency fund is built now.")
		
		output.info("ANALYSIS - Done allocating emergency fund....")
		output.section_end()

	def check_pay_debt(self):
		print("\n")
		output.section_start("Debt free life means Freedom...")
		output.info("ANALYSIS - Checking your debt and a payoff plan....")
		# check for consumer debt
		d = self._d.unknown
		b = self._b
		a = self._a
		total = 0.0
		self.allocation['Debt Payoff'] = 0.0
		debt_payment = 0.0
		for n,v in d.items():
			(val, rate, y) = v
			if (rate > HIGH_INTEREST_RATE):
				output.warn("High interest rate for %s: $%.2f @ %.2f" % (n, val, rate))
				total += val
				debt_payment += self._d.payment[n]
	
		if (total == 0.0):
			output.info("Congratulations - You are debt free.")
			output.info("You can invest %.2f per month and grow your assets." % (b.get_monthly()))
			output.info("Your current assets")
			a.report("Assets_after_debt_free")
		else:
			#print("\n")
			output.action("Pay the debt $%.2f in order - " % (total))
			for n,v in sorted(d.items(), key=lambda x:x[1][0]):
				print("	n:%s rate:%.2f value:$%.2f" % (n, v[1], v[0]))
			
			# check assets for paying off debt
			for n,v in sorted(a.data.items(), key=lambda x:x[1][1]):
				if (total <= 0.0):
					break
				(val, rate) = v
				if (val <= 0.0):
					continue
				take = min(val, total)
				output.action("Use the %s to pay off debt with value $%.2f" % (n, take))
				total -= val
				a.reduce(n, take, rate)
				self.allocation['Debt Payoff'] += take
				
			#print("\n")
			output.info("Assets after paying off debt.")
			a.report("Assets_after_paying_off_debt")
			
			if (total > 0.0):
				if (b.get_monthly() <= 0.0):
					if (self.surplus > 0.0):
						output.warn("You can pay off debt only after the emergency fund is built.")
						output.action("Need monthly budget $%.2f to pay off remaining debt $%.2f" % (self.surplus, total))
						months = int((total + self.surplus) / self.surplus);
						self.m_for_ef_debt += months
						output.info("You will be debt free in %d months." % (self.m_for_ef_debt))
						output.info("You will save %s%.2f of debt payments every month." % (utils.get_currency(), debt_payment))
						self.surplus += debt_payment
					else:
						output.warn("You do not have surplus left in your budget to pay off debt. Reduce your expenses.")
				else:
					output.action("Need monthly budget $%.2f to pay off remaining debt $%.2f" % (b.get_monthly(), total))
					months = int((total + b.get_monthly()) / b.get_monthly());
					print("		No. of months - %d" % (months))
					output.info("You will be debt free in %d months." % (months))
					output.info("You will save %s%.2f of debt payments every month." % (utils.get_currency(), debt_payment))
					self.m_for_ef_debt = months
					self._b.add_expense("Debt Payoff", b.get_monthly())
					self.surplus += debt_payment
			else: 
				output.info("You can be debt-free now.")
		output.info("ANALYSIS - Done debt payoff plan....")
		output.section_end()

	def grow_assets(self):
		print("\n")
		output.section_start("Building wealth steadily is not difficult...")
		output.info("ANALYSIS - Projecting growth of assets")
		p = self._p
		b = self._b
		a = self._a
		x = list()
		y = list()
		y_ = list()
		start = p.getCurrentAge() + (self.m_for_ef_debt/12)
		monthly_surplus = b.get_monthly()
		if (start > p.getCurrentAge()):
			output.info("You can start investing only at the age of %d years after emergency fund and/or debt payoff." % (start))
			monthly_surplus = self.surplus
		if (start > p.getRetireAge()):
			output.warn("Unfortunately time to pay off debt or building emergency fund exceeds your retirement age %d." % (p.getRetireAge()))
			output.warn("You need to delay your retirement by few more years.")
			quit()
		time_to_grow = p.getRetireAge() - p.getCurrentAge() - (self.m_for_ef_debt/12)
		risk = p.getRiskNumber()
		# Take 401k etc. into account
		monthly_surplus += (self._i.deductions)/12
		output.info("Your assets will grow in next %.2f years if you regularly invest %s%.2f every month" %
			 (time_to_grow, utils.get_currency(), monthly_surplus))
		output.info("Invest %.2f per month for next %.2f years" % (monthly_surplus, time_to_grow))
		d = dict()
		d = a.data.copy()
		t = utils.fv(d, monthly_surplus/len(d), time_to_grow)
		if (t > 100000):
			output.info("You will be a MILLIONAIRE")
		else:
			if (t > 900000):
				output.info("You will be very close to a millionaire")
		utils.report("If you invest %s%.2f regularly, your assets will be" %(utils.get_currency(), monthly_surplus), d, t)
		utils.piechart("FV_regular", "Future Value of Assets if you invest regularly", [n for n,v in d.items()], [v for n,v in d.items()])
		e = dict()
		e = a.data.copy()
		t = utils.fv(e, 0.0, time_to_grow)
		utils.report("If you do not invest the surplus, your assets will remain", e, t)
		utils.piechart("FV_static", "Future Value of Assets if you do not invest anymore", [n for n,v in e.items()], [v for n,v in e.items()])
		output.info("ANALYSIS - Asset projection done....")
		x = [i for i in range(1, int(time_to_grow))]
		for j in x:
			f = a.data.copy()
			y.append(utils.fv(f, monthly_surplus/len(f),j))
			f = a.data.copy()
			y_.append(utils.fv(f, 0.0,j))
		#print(x, y, y_)
		output.section_end()
		# update self.surplus for asset allocation
		self.surplus = monthly_surplus
		return x, y, y_

	def mortgage_pay(self):
		mortgage = self._d.fixed
		time_before_retire = self._p.getRetireAge() - self._p.getCurrentAge()
		time = int(time_before_retire * 12)
		for n, v in mortgage.items():
			(val, rate, years) = v
			utils.mortgage_payment(val, time, rate, years)

	def do_all(self):
		cont = self.live_below_means()
		if (cont == False):
			return
		self.emergency_fund()
		self.check_pay_debt()
		l1 = [n for n, v in self.allocation.items()] + [n1 for n1, v1 in self._a.data.items()]
		val1 = [v for n, v in self.allocation.items()] + [v1[0] for n1, v1 in self._a.data.items()]
		print(l1)
		print(val1)
		utils.piechart("allocation", "Asset Allocation", l1, val1)
		(x, y, y_) = self.grow_assets()
		self.view(x, y, y_)
		#self.mortgage_pay()
		asset_alloc = Asset_Allocation(self._a, self.surplus, self._d.fixed, self._p, self._e)
		asset_alloc.allocate()
		#output.close()
		
	def view(self, x, y, y_):
		pyplot.xlabel('Years')
		pyplot.ylabel('Assets')
		pyplot.title('Growth of Assets over time with regular vs. no investing')
		pyplot.plot(x, y)
		pyplot.plot(x, y_)
		pyplot.savefig("project.png")
		output.image("project.png")
		#pyplot.show()
		pyplot.clf()
		pyplot.cla()
		pyplot.close()

		
### THE END ###

	
		
