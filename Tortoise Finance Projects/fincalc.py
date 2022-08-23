import streamlit as st


st.header("The Tortoise Finance Calculator")
st.subheader("Use the below calculators for your various personal financial decisions")

st.write("**I have a lumpsum amount to invest. Help me project a future value.**")
V0 = st.number_input("I want to invest ", value=10000, format="%f")
t = st.number_input("for no. of years ", value=10, format="%d")
r = st.number_input("at an interest rate of ", value=8.0, format="%f")
Vt = V0*(1 + r/100.0)**t
st.info("You will get %.2f after %d years." % (Vt, t))

st.write("**I want to have a certain amount in a few years. How much should I allocate for it now?**")
Vt = st.number_input("I want to get ", value=50000, format="%f")
t = st.number_input("after no. of years ", value=10, format="%d")
r = st.number_input("growing at an interest rate of ", value=8.0, format="%f")
V0 = Vt/(1 + r/100.0)**t
st.info("You will need %.2f and keep it invested for %d years." % (V0, t))

st.write("**I can invest a certain amount per month. Help me figure out how much it will grow.**")
p = st.number_input("Invest per month ", value=1000, format="%f")
t = st.number_input("regularly for no. of years ", value=10, format="%d")
t = t * 12
r = st.number_input("compounding at an interest rate of ", value=8.0, format="%f")
r = r/100.0
r = r/12.0
Vt = p*(((1+r)**(t) - 1)/(r))
st.info("You will have %.2f after %d years." % (Vt, t/12))

st.write("**I want to have a certain amount in a few years. How much should I save per month for it?**")
Vt = st.number_input("Future Value ", value=50000, format="%f")
t = st.number_input("in no. of years ", value=10, format="%d")
r = st.number_input("invested at an interest rate of ", value=8.0, format="%f")
t = t * 12
r = r /100.0
r = r /12.0
p = Vt * (r / ((1 + r)**t - 1) )
st.info("You will have to invest %.2f per month to get %.2f after %d years" % (p, Vt, t/12))

st.write("**I want to withdraw a monthly sum for no. of years, how much corpus do I need?**")
p = st.number_input("Withdraw per month ", value=1000, format="%f")
t = st.number_input("for no. of years every month ", value=10, format="%d")
r = st.number_input("kept at an interest rate of ", value=4.0, format="%f")
t = t * 12
r = r /100.0
r = r /12.0
V0 = p * (((1 + r)**t - 1) / (r*((1+r)**t))) 
st.info("You will need corpus of %.2f" % (V0))

st.write("**How much do I need to pay monthly sum to pay off a loan (or mortgage)**")
V0 = st.number_input("Loan amount ", value=10000, format="%f")
t = st.number_input("term of loan ", value=15, step=1, format="%d")
r = st.number_input("interest rate of loan ", value=3.0, format="%f")
t = t * 12
r = r /100.0
r = r /12.0
p = V0 * ( (r*((1+r)**t)) / ((1+r)**t - 1) )
st.info("You will have a payment of %.2f per month for loan of %.2f at %.2f rate for %d years" % (p, V0, r*100*12, t/12))


