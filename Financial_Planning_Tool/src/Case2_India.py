# VRO case study
from Income import Income
from Tax import Tax
from Budget import Budget
from Expense import Expense
from Debt import Debt
from Assets import Assets
from Metrics import Metrics
import utils
from Analysis import tortoise_analyze

i = Income() 
i.add("salary", 52000*12)
i.report()

t = Tax(i.data)
#t.calculate()
t.report()

d = Debt()
d.report()

e = Expense()
e.add("household", 20000)
e.add_yearly("premiums", 165000)
e.report()

b = Budget()
b.add(i, t, d, e)
b.report()

a = Assets()
a.add("Plot", 500000, 5)
a.add("cash", 30000, 3)
a.add("Equity", 479000, 10)
a.report()

m = Metrics(i, b, e, d, a)
m.calculate()
m.report()

tortoise_analyze(i, d, b, e, a, m)
