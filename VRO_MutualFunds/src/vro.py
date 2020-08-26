import numpy as np
import pandas as pd

###Fund Name,Rating,Analyst's Choice?,Category,1 Year Returns (%),1 Year Returns (growth of 1 lakh),1 Year SIP Returns (%),1 Year SIP Returns (growth of 10k/mth),3 Year Returns (%),3 Year Returns (growth of 1 lakh),3 Year SIP Returns (%),3 Year SIP Returns (growth of 10k/mth),5 Year Returns (%),5 Year Returns (growth of 1 lakh),5 Year SIP Returns (%),5 Year SIP Returns (growth of 10k/mth),10 Year Returns (%),10 Year Returns (growth of 1 lakh),10 Year SIP Returns (%),10 Year SIP Returns (growth of 10k/mth),Expense Ratio (%)

new_col_names = ["Fund", "Rating", "Analyst", "Category", "1Yr_Percent", "1Yr_Returns", "1Yr_SIP", "1Yr_SIP_Return", "3Yr_Percent", "3Yr_Returns", "3Yr_SIP", "3Yr_SIP_Return", "5Yr_Percent", "5Yr_Returns", "5Yr_SIP", "5Yr_SIP_Return", "10Yr_Percent", "10Yr_Returns", "10Yr_SIP", "10Yr_SIP_Return" , "Expense"]
use_col_names = ["Fund", "Rating", "Category", "3Yr_Percent", "5Yr_Percent", "10Yr_Percent", "Expense"]

wealth_funds = pd.read_csv('wealth-builder-funds-20-Jul-2020--0125.csv', header=2, index_col=0, names=new_col_names, usecols=use_col_names)
print(wealth_funds.head())

aggressive_funds = pd.read_csv('aggressive-growth-funds-20-Jul-2020--0132.csv', header=2, index_col=0, names=new_col_names, usecols=use_col_names)
print(aggressive_funds.head())

df = pd.concat([wealth_funds, aggressive_funds], axis=0, sort=False)
print()
print("All Funds together... ")
print(df.head())

print(df.isna().sum())

# Print all funds with expense ratio < 1.0
print()
print("All funds with expense ratio < 1.0")
dfe = df[df['Expense'] < 1.0]
print(dfe)

print()
print("All funds with 5 year return > 8.0")
dfer = dfe[dfe['5Yr_Percent'] > 8.0]
print(dfer.sort_values(by='Category'))

print()
print("Stats on 5 Year Performance")
print(dfer['5Yr_Percent'].describe())

print("Stats on 3 Year Performance")
print(dfer['3Yr_Percent'].describe())

print("Stats on Expense Ratio")
print(dfer['Expense'].describe())
