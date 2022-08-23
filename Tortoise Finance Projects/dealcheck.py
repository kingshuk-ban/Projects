import streamlit as st
import numpy as np
import numpy_financial as npf
import webbrowser as web

# This is a real estat deal checker
st.header("The Tortoise Finance Deal Checker")

st.sidebar.header("Enter your parameters here.")

# Inputs
st.sidebar.subheader("The property details")

address = st.sidebar.text_input("Address: ", value="")
city = st.sidebar.text_input("City:", value="none")
state = st.sidebar.text_input("State:", value="none")
zipcode = st.sidebar.number_input("Zipcode:", value=0, format="%d")
nearest_metro = st.sidebar.text_input("Nearest Metro:", value="Dallas,TX")

purchase_price = st.sidebar.number_input("Purchase Price ($)", min_value=10000.0, max_value=600000.0, value=100000.0, step=1000.0, format="%.2f")
property_tax = st.sidebar.number_input("Property Tax ($/year)", min_value=0.0, value=4000.0, step=50.0, format="%.2f")
insurance = st.sidebar.number_input("Insurance ($/year)", min_value=0.0, value=1200.0, step=50.0, format="%.2f")
expected_rent = st.sidebar.number_input("Expected Rent ($/month)", min_value=100.0, value=1000.0, step=25.0, format="%.2f")
property_mgmt = st.sidebar.number_input("Property Management (% of rent)", value=8.0, step=0.25, format="%.2f")
hoa_fees = st.sidebar.number_input("HoA fee per month ($/month)", value=50.0, step=10.0, format="%.2f")
years_to_hold = st.sidebar.number_input("Years you intend to hold this property (yrs)", value=15, format="%d")

st.sidebar.subheader("The mortgage parameters")
down_payment = st.sidebar.number_input("Down payment (%)", value=25, step=5, format="%d")
mortgage_rate = st.sidebar.number_input("Mortgage rate (%)", value=4.0, step=0.01, format="%.2f")
#mortgate_rate = mortgage_rate / 100.0
#mortgage_rate = mortgage_rate / 12
mortgage_term = st.sidebar.number_input("Mortgage term (yrs)", value=30, step=1, format="%d")
closing_costs = st.sidebar.number_input("Closing costs ($)", value=5000.0, step=50.0, format="%.2f")

st.sidebar.subheader("The variable costs")
maintenance_costs = st.sidebar.number_input("Maintance costs (% of rent)", value=10.0, step=1.0, format="%.2f")
vacancy_factor = st.sidebar.number_input("Vacancy costs (% of rent)", value=8.0, step=0.5, format="%.2f")
capex_rate = st.sidebar.number_input("Capex reserves (% of rent)", value=5.0, step=0.5, format="%.2f")

st.sidebar.header("The economic factors")
appreciation_rate = st.sidebar.number_input("Property appreciation rate (%)", value=3.0, step=0.01, format="%.2f")
sales_commission_rate = st.sidebar.number_input("Sales commission rate (%)", value=6.0, step=0.5, format="%.2f")
tax_rate = st.sidebar.number_input("Capital Gains Tax Rate: (%)", value=15.0, step=0.5, format="%.2f")

# Cash flow calculations
down = (down_payment/100.0) * purchase_price
loan = purchase_price - down
#mortgage_payment = float(loan * ((mortgage_rate*((1+mortgage_rate)**(mortgage_term*12))) / ((1+mortgage_rate)**(mortgage_term*12) - 1)))
rate = mortgage_rate/100
# st.info("calculating payment: loan  = %.2f, r = %.2f t = %d" % (loan, rate, mortgage_term))
mortgage_payment = -1 * npf.pmt(rate/12, 12*mortgage_term, loan)
fixed_costs = property_tax/12 + insurance/12 + (property_mgmt/100)*expected_rent + hoa_fees; 
noi = (expected_rent - fixed_costs) * 12
cap_rate = (noi * 100) / purchase_price
monthly_cash_flow_fixed_costs = expected_rent - fixed_costs - mortgage_payment
coc_return_fixed_costs = (monthly_cash_flow_fixed_costs * 12 * 100) / (down + closing_costs)
variable_costs = (maintenance_costs/100)*expected_rent + (vacancy_factor/100)*expected_rent + (capex_rate/100)*expected_rent
monthly_cash_flow_variable_costs = monthly_cash_flow_fixed_costs - variable_costs
coc_return_variable_costs = (monthly_cash_flow_variable_costs * 12 * 100) / (down + closing_costs)

# Appreciation calculations
future_value = npf.fv(appreciation_rate/100, years_to_hold, 0.0, -(purchase_price))
cash_flows = years_to_hold * monthly_cash_flow_variable_costs * 12
total_sale_proceeds = future_value * (1 - sales_commission_rate/100)
debt_remaining = npf.fv((mortgage_rate/100)/12, 12*years_to_hold, mortgage_payment, -loan)
total_return = total_sale_proceeds + cash_flows - debt_remaining
total_profit = total_return - (down + closing_costs)
tax = (tax_rate/100.0) * (total_profit)
net_profit = total_profit - tax
cash_flow_arr = []
cash_flow_arr.append(-(down + closing_costs))
for i in range(years_to_hold):
    cash_flow_arr.append(monthly_cash_flow_variable_costs * 12)
cash_flow_arr.append(total_sale_proceeds - debt_remaining - tax)

irr = npf.irr(cash_flow_arr)

# Outputs
full_address = address + "," + city + "," + state + "," + str(zipcode)
st.subheader("Analysis of %s" % str(full_address))

st.info("Cap Rate: %.2f %%" % (cap_rate))
st.info("Total down payment including closing costs: $%.2f " % (down + closing_costs))
st.markdown("   **_Cash flow on fixed costs: $%.2f, Cash on cash return: %.2f%%_**" % (monthly_cash_flow_fixed_costs, coc_return_fixed_costs))
st.markdown("   **_Cash flow on variable costs: $%.2f, Cash on cash return: %.2f%%_**" % (monthly_cash_flow_variable_costs, coc_return_variable_costs))
#st.info("   Cash on cash return on variable costs: %.2f%%" % (coc_return_variable_costs))
st.info("Net (after tax) Profit: $%.2f, (%.2f%%) in %d years" % (net_profit, (net_profit * 100.0)/(down + closing_costs), years_to_hold))
st.info("IRR in %d years: %.2f%%" % (years_to_hold, irr*100.0))

# if (st.button("Analyze the neighborhood and city (opens 4 tabs)")):
#    if (city != "none"):
#        web.open_new_tab("https://www.google.com/search?q=" + str(city) + "+top+employers")
#   if (state != "none" and city != "none"):
#        web.open_new_tab("http://www.city-data.com/city/" + str(city) + "-" + str(state) + ".html")
#    if (zipcode > 0.0):
#        web.open_new_tab("https://censusreporter.org/profiles/86000US" + str(zipcode) + "-" + str(zipcode))
#    if (address != "not specified"):
#        web.open_new_tab("https://www.google.com/maps/place/" + str(full_address))

if ((city != "none") and (st.button("Top Employers in %s"%(city)))):
    web.open_new_tab("https://www.google.com/search?q=" + str(city) + "+top+employers")
if ((zipcode > 0.0) and (st.button("Basic information on ZIP code: %s" % str(zipcode)))):
    web.open_new_tab("https://censusreporter.org/profiles/86000US" + str(zipcode) + "-" + str(zipcode))
if ((state != "none" and city != "none") and st.button("Detailed information on %s, %s" % (str(city), str(state)))):
    web.open_new_tab("http://www.city-data.com/city/" + str(city) + "-" + str(state) + ".html")
if ((address != "not specified") and (st.button("Find %s in map" % (str(address))))):
    web.open_new_tab("https://www.google.com/maps/place/" + str(full_address))
if ((address != "not specified") and (st.button("Find distance from %s in map" %(nearest_metro) ))):
    web.open_new_tab("https://www.google.com/maps/dir/" + str(nearest_metro) + "/" + str(full_address))



st.subheader("Fundamentals of the deal...")
st.info("Gross Income: $%.2f" % (expected_rent * 12))
st.info("Total Fixed Expenses: $%.2f" % (fixed_costs * 12))
st.info("Net Operating Income: $%.2f" % (noi))
st.info("Cap Rate: %.2f %%" % (cap_rate))
st.info("Total down payment including closing costs: $%.2f " % (down + closing_costs))
st.info("Mortgate principal: $%.2f" % (loan))
st.info("Debt payment: $%.2f" % (mortgage_payment * 12))
st.info("Net Income after debt payment: $%.2f" % (noi - mortgage_payment*12))

st.subheader("Cash flow analysis of the property...")
# st.info("Cash flow (monthly):")
st.info("   Mortgage payment: $%.2f" % (mortgage_payment))
st.info("   Fixed costs: $%.2f" % (fixed_costs))
st.info("   Variable costs: $%.2f" % (variable_costs))
st.info("   Cash flow on fixed costs: $%.2f" % (monthly_cash_flow_fixed_costs))
st.info("   Cash on cash return on fixed costs: %.2f%%" % (coc_return_fixed_costs))
st.info("   Cash flow on variable costs: $%.2f" % (monthly_cash_flow_variable_costs))
st.info("   Cash on cash return on variable costs: %.2f%%" % (coc_return_variable_costs))

st.info("Please keep $%.2f in reserves for 6 months of costs." % ((mortgage_payment + fixed_costs + variable_costs)*6) )

st.subheader("Appreciation potential in %d years" % (years_to_hold))

st.info("Future Value: $%.2f" % (future_value))
st.info("Total Cash Flows: $%.2f" % (cash_flows))
st.info("Total Sale Proceeds: $%.2f" % (total_sale_proceeds))
st.info("Debt Remaining: $%.2f" % (debt_remaining))
st.info("Total Return: $%.2f" % (total_return))
st.info("Total Profit: $%.2f, (%.2f%%) in %d years" % (total_profit, (total_profit * 100.0)/(down + closing_costs), years_to_hold))
st.info("Tax: %.2f" % (tax))
st.info("Net (after tax) Profit: $%.2f, (%.2f%%) in %d years" % (net_profit, (net_profit * 100.0)/(down + closing_costs), years_to_hold))

st.info("IRR: %.2f%%" % (irr*100.0))



