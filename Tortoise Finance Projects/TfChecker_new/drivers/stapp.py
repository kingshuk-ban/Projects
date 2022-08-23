import streamlit as st
import sys
sys.path.append('../core')
sys.path.append('../outputs')

import utils
utils.set_output("streamlit")

from Personal import Personal
from Income import Income
from Tax import Tax
from Debt import Debt
from Budget import Budget
from Expense import Expense
from Assets import Assets
from Metrics import Metrics
from Analysis import Analysis

st.header("The Tortoise Finance - A road map to financial freedom")

st.sidebar.header("Enter your data here")

# Personal information
st.sidebar.subheader("Personal Information")
st.subheader("Personal Information")
currency = st.sidebar.selectbox("Currency", ['$', 'INR'], 0)
utils.set_currency(currency)
name = st.sidebar.text_input("Name", "Guest")
st.write("Hi ", name)
age = st.sidebar.slider("Age in years", 18, 60, 30, step=1, format="%d")
retire_age = st.sidebar.slider("Age of retirement", age, 75, 60, step=1, format="%d")
st.info("You have %d years to execute a financial plan" % (retire_age - age))
risk = st.sidebar.selectbox("Select your risk tolerance (percent of stocks)",
							[10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
							4)
st.write("Your risk tolerance is selected as: %d percent stocks, %d percent bonds" % (risk, 100 - risk))

p = Personal()
p.add(name, age, retire_age, risk)

# Income
st.sidebar.subheader("Income and Taxation")
st.subheader("Income and Taxation")
#income = st.sidebar.slider("Annual Income (Pre-tax)", 10000, 500000, 50000, step=1000, format="%d")
income = st.sidebar.number_input("Annual Income (Pre-tax)", 50000.0, format="%f")
st.info("Your monthly gross income is: %.2f" % (income/12.0))
#deductions = st.sidebar.slider("Total pre-tax deductions (401k, HSA)", 0, min(income, 19500+7100), step=100, format="%d")
deductions = st.sidebar.number_input("Total pre-tax deductions", 5000.0, income, format="%f")
st.info("Your monthly pre-tax deductions: %.2f " % (deductions/12.0))
st.info("Your monthly pre-tax income: %.2f" % ((income - deductions)/12.0))
tax_status = st.sidebar.selectbox("Tax filling status",
					 ['single', 'married_separate', 'married_joint', 'head_household'],
					 2)
# st.write("Tax filling status: ", tax_status)

i = Income()
i.add("Paycheck", income)
i.deduct("deductions", deductions)

st.subheader("Monthly expenses")
t = Tax()
t.addIncome(i.data)
t.addFilling(tax_status)
t.calculate()

st.info("Your total tax outgo per month: %.2f" % (t.total/12.0))
for n,v in t.taxes.items():
	st.info("%s : %.2f" % (n, v/12.0))

# Expenses
st.sidebar.subheader("Expenses")

#expenses = st.sidebar.slider("Household monthly expenses", 500, 30000, 3000, 100, format="%d")
expenses = st.sidebar.number_input("Household monthly expenses", 1000.0, format="%f")
e = Expense()
e.add("Household", expenses)

# Debt
st.sidebar.subheader("Debt")
#cc_debt = st.sidebar.slider("Credit card debt", 0, 100000, 0, 100, format="%d")
cc_debt = st.sidebar.number_input("Credit card debt", 0.0, format="%f")
cc_rate = st.sidebar.slider("Credit card interest rate", 5.0, 25.0, 10.0, 0.1, format="%f")
#m_debt = st.sidebar.slider("Mortgage Principal", 0, 800000, 0, 10000, format="%d")
m_debt = st.sidebar.number_input("Mortgage Principal", 0.0, format="%f")
m_rate = st.sidebar.slider("Mortgage interest rate", 1.0, 20.0, 4.0, 0.05, format="%f")
m_years = st.sidebar.selectbox("Mortgage tenure", [10, 15, 20, 25, 30], 4)

d = Debt()
d.add_fixed("Mortgage", m_debt, m_rate, m_years)
d.add_variable("Credit card", cc_debt, cc_rate)
d_total = d.calculate()

st.info("Your debt payments are total: %.2f" % (d_total))
for n,v in d.payment.items():
	st.info("%s : %.2f" % (n, v))

# Budget
st.subheader("Your monthly budget")
b = Budget()
b.add(i, t, d, e)
if (b.surplus <= 0.0):
	st.warning("You are not living within your means.")
else:
	st.success("You have %.2f surplus per month" % (b.surplus))
	#st.balloons()
for n,v in b.data.items():
	st.info("%s : %.2f" % (n, v))

# Assets
st.sidebar.subheader("Assets")
st.subheader("Assets")
a = Assets()
stocks = st.sidebar.number_input("Stock Investments", 500.0)
return_exp = st.sidebar.slider("Expected Return from Stocks", 1.0, 20.0, 9.0, 0.5, format="%f")
a.set_stock_rate(return_exp)
a.add("Stocks", stocks, return_exp)
cash = st.sidebar.number_input("Cash and Equivalent", 500.0)
return_exp = st.sidebar.slider("Expected Return from Cash", 0.0, 8.0, 0.5, 0.1, format="%f")
a.set_cash_rate(return_exp)
a.add("Cash", cash, return_exp)
bonds = st.sidebar.number_input("Bonds and similar", 500.0)
return_exp = st.sidebar.slider("Expected Return from Bonds", 0.0, 8.0, 0.5, 0.1, format="%f")
a.set_bond_rate(return_exp)
a.add("Bonds", bonds, return_exp)
assets = sum([stocks, bonds, cash])
st.info("Your total assets are: %.2f" % assets)
st.info("Your total liabilities are: %.2f" % d.total)
st.info("You Net worth is: %.2f" % (assets - d.total))

# Metrics
st.subheader("Financial Metrics")
m = Metrics(i, b, e, d, a)
m.calculate()
for n,v in m.ratios.items():
	st.info("%s : %.2f" % (n, v))

# Analysis
st.subheader("Analyzing your financial situation..")
ana = Analysis(p, i, d, b, e, a, m)
ana.do_all()









