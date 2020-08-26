# This class calculates the metrics
from Personal import Personal
from Income import Income
from Tax import Tax
from Budget import Budget
from Expense import Expense
from Debt import Debt
from Assets import Assets
from Metrics import Metrics
import utils
from Analysis import Analysis

p = Personal()
p.add("kingshuk", 45, 65, 80)

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
d.add_variable("cc1", 6000, 10)
d.add_variable("cc2", 1000, 8)
d.add_variable("cc3", 5000, 16)
pymt = d.calculate()
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
a.add("Stocks", 80000, 8)
a.add("Bonds", 0, 4)
a.report()

m = Metrics(i, b, e, d, a)
m.calculate()
m.report()

ana = Analysis(p, i, d, b, e, a, m)
ana.do_all()