# The parser module
# Input format:
# Personal=<name>:<age>:<retirement_age>:<risk_aversion>
# Income=<name>:<value>,<name>:<value>...
# Deduction=<name>:<value>,...
# Expense=<name>:<value>,<name>:<value>..
# Debt=<name>:<value>,<name>:<value>:<rate>,<name>:<value>:<rate>:<year>
# Asset=<name>:<value>,<name>:<value>:<rate>,<name>:<value>:<rate>:<year>

import re
import sys
import utils
from utils import output
from Personal import Personal
from Income import Income
from Tax import Tax
from Budget import Budget
from Expense import Expense
from Debt import Debt
from Assets import Assets
from Metrics import Metrics
from Analysis import Analysis

rx_dict = {
	'currency': re.compile(r'Currency\s*=\s*(?P<currency>(\S+))\n'),
	'personal': re.compile(r'Personal\s*=\s*(?P<personal>(\S+:\d+:\d+:\d+))\n'),
	'income': re.compile(r'Income\s*=\s*(?P<income>(\S+:\d+))\n'),
	'tax': re.compile(r'Tax\s*=\s*(?P<tax>(single)|(married_separate)|(married_joint)|(head_household))\n'),
	'deduction': re.compile(r'Deduction\s*=\s*(?P<deduction>(\S+:\d+))\n'),
	'expense': re.compile(r'Expense\s*=\s*(?P<expense>(\S+:\d+))\n'),
	'debt': re.compile(r'Debt\s*=\s*(?P<debt>(\S+:\d+)|(\S+:\d+:\d+)|(\S+:\d+:\d+:\d+))\n'),
	'asset': re.compile(r'Asset = (?P<asset>(\S+:\d+)|(\S+:\d+:\d+)|(\S+:\d+:\d+:\d+))\n')
}

def parse_a_line(line):
	for key, rx in rx_dict.items():
		match = rx.search(line)
		if (match):
			return key, match
	return None, None
	
def getMatchedPairs(key, match, line):
	v = ""
	# print(match)
	v = match.group(key)
	items = v.split(',')
	pairs = dict()
	for i in items:
		values = i.split(':')
		pairs[values[0]] = [float(x) for x in values[1:]]
	return pairs
	
def init():
	p = Personal()
	i = Income()
	t = Tax()
	e = Expense()
	d = Debt()
	a = Assets()
	return (p, i, t, d, e, a)
	
def report():
	p.report()
	i.report()
	t.calculate()
	t.report()
	d.report()
	e.report()
	a.report("Initial_Assets")
	
def analyze():
	b = Budget()
	b.add(i, t, d, e)
	b.report()
	m = Metrics(i, b, e, d, a)
	m.calculate()
	m.report()
	ana = Analysis(p, i, d, b, e, a, m)
	ana.do_all()
	
def add_personal(p, pairs):
	for n,v in pairs.items():
		p.add(n, v[0], v[1], v[2])
		
def add_Income(i, pairs):
	for n,v in pairs.items():
		i.add(n, float(v[0]))
		
def add_Tax(i, t, filling):
	t.addIncome(i.data)
	t.addFilling(filling)
		
def add_Deduction(i, pairs):
	for n,v in pairs.items():
		i.deduct(n, float(v[0]))
		
def add_Expense(e, pairs):
	for n,v in pairs.items():
		e.add(n, float(v[0]))
	
def add_Debt(d, pairs):
	for n,v in pairs.items():
		if (len(v) == 2):
			d.add_variable(n, v[0], v[1])
		elif (len(v) == 3):
			d.add_fixed(n, v[0], v[1], v[2])
		elif (len(v) == 1):
			d.add_variable(n, v[0], 10.0)
		d.calculate()
		
def add_Asset(d, pairs):
	for n,v in pairs.items():
		if (len(v) == 1):
			a.add(n, v[0], 0.0)
		elif (len(v) >= 2):
			a.add(n, v[0], v[1])
	
	
if __name__ == "__main__":
	p, i, t, d, e, a = init()
	filepath = sys.argv[1]
	with open(filepath, 'r') as fp:
		line = fp.readline()
		while (line):
			k,match = parse_a_line(line)
			if (match == None):
				print("Syntax error in line: %s" % (line))
				line = fp.readline()
				continue
			pairs = getMatchedPairs(k, match, line)
			if (pairs == None):
				line = fp.readline()
			if (k == 'currency'):
				utils.set_currency(match.group(k))
			if (k == 'personal'):
				add_personal(p, pairs)
			if (k == 'income'):
				add_Income(i, pairs)
			if (k == 'tax'):
				add_Tax(i, t, match.group(k))
			if (k == 'deduction'):
				add_Deduction(i, pairs)
			if (k == 'expense'):
				add_Expense(e, pairs)
			if (k == 'debt'):
				add_Debt(d, pairs)
			if (k == 'asset'):
				add_Asset(a, pairs)
			
			line = fp.readline()
	report()
	analyze()
	output.quit()

	
	

	
