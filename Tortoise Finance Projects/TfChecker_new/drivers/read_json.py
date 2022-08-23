import json
import sys
sys.path.append('../core')
sys.path.append('../outputs')

# this needs to be at the top for all 
# other modules to use the correct output object
import utils
utils.set_output("html")

from Personal import Personal
from Income import Income
from Tax import Tax
from Expense import Expense
from Debt import Debt
from Budget import Budget
from Assets import Assets
from Metrics import Metrics
from Analysis import Analysis
from utils import output


filename = sys.argv[1]
with open(filename) as f:
	data = json.load(f)

#print(data)

print(json.dumps(data, indent = 4, sort_keys=False))

for k,v in data.items():
	print("%s is:" % (k));
	print(v)

# Add personal information
p = Personal()
p.set_currency(data['personal']['currency'])
person = data['personal']
p.add(person['name'], int(person['age']), int(person['retire']), int(person['risk']))
p.report()

# Add income
i = Income()
for k,v in data['income'].items():
	i.add(k,v)	
for k,v in data['deduction'].items():
	i.deduct(k,v)
i.report()

# Add income to calculate tax
t = Tax()
t.addIncome(i.data)
t.addFilling(data['tax'])
t.calculate()
t.report()

# Add expense before we Budget!
e = Expense()
for k,v in data['expense'].items():
	e.add(k,v)
e.report()

# Adding debt
d = Debt()
for k,v in data['debt'].items():
	if (len(v) == 3):
		d.add_fixed(k, float(v[0]), float(v[1]), float(v[2]))
	elif (len(v) == 2):
		d.add_variable(k, float(v[0]), float(v[1]))
	elif (len(v) == 1):
		d.add_variable(k, float(v[0]), 10.0)
d.calculate()
d.report()

# Finally do a budget
b = Budget()
b.add(i, t, d, e)
b.report()

# Add assets
a = Assets()
for k,v in data['asset'].items():
	a.add(k, float(v[0]), float(v[1]))

# Calculate useful metrics
m = Metrics(i, b, e, d, a)
m.calculate()
m.report()

# Final analysis
ana = Analysis(p, i, d, b, e, a, m)
ana.do_all()

# Generate the output
output.quit()

