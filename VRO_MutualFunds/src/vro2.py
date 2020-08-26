import numpy as np
import pandas as pd
import pandas_profiling
import matplotlib.pyplot as plt
#%matplotlib inline

## Fund Name,Category,Expense Ratio (%),1 Yr Ret (%)
new_col_names = ["Fund", "Category", "Expense", "1Yr_Returns"]

snapshot = pd.read_csv('all-equity-funds-snapshot.csv', header=6, index_col=0, names=new_col_names)
#print(snapshot.head())

## Fund Name,3 Yr Ret (%),5 Yr Ret (%),10 Yr Ret (%),15 Yr Ret (%),20 Yr Ret (%)
new_col_names2 = ["Fund", "3Yr_Returns", "5Yr_Returns", "10Yr_Returns", "15Yr_Returns", "20Yr_Returns"]
returns = pd.read_csv('all-equity-funds-long-term-returns.csv', header=6, index_col=0, names=new_col_names2)
#print(returns.head())

df = pd.concat([snapshot, returns], axis=1, sort=False)
print(df.describe(include="all"))

pandas_profiling.ProfileReport(df).to_file("profile.report")

print(df['Category'].value_counts())

#df.hist(figsize=(20, 30))
#plt.show()

import seaborn as sns
df_common = df[(df['Category'] == "EQ-LC") | 
               (df['Category'] == "EQ-L&MC") | 
               (df['Category'] == "EQ-MLC") | 
               (df['Category'] == "EQ-MC") |
               (df['Category'] == "EQ-SC") | 
               (df['Category'] == "EQ-THEMATIC") | 
               (df['Category'] == "EQ-ELSS") | 
               (df['Category'] == "EQ-INTL")
              ] 
sns.boxplot(x="Category", y="3Yr_Returns", data=df_common)
plt.show()
sns.boxplot(x="Category", y="5Yr_Returns", data=df_common)
plt.show()
sns.boxplot(x="Category", y="10Yr_Returns", data=df_common)
plt.show()
sns.boxplot(x="Category", y="15Yr_Returns", data=df_common)
plt.show()
sns.boxplot(x="Category", y="20Yr_Returns", data=df_common)
plt.show()
sns.boxplot(x="Category", y="Expense", data=df_common)
plt.show()
sns.jointplot(df_common['Expense'], df_common['20Yr_Returns'], kind='hex')
plt.show()

# Examine thematic funds
df_ret = df[df['Category'] == "EQ-MC"].sort_values("20Yr_Returns", ascending=False)
print(df_ret)

#df_common.hist(by="Category", column="15Yr_Returns")
df_common.hist()

plt.show()
exit()

tenure = int(input('Enter tenure:'))
ret = float(input('Enter return:'))
expense = float(input('Enter the max expense ratio:'))
print("Searching for funds with expense < %f and tenure %d years return > %f: " % (expense, tenure, ret)) 

if (tenure < 1):
	print("Please provide a tenure more than 1")
	tenure = int(input('Enter tenure:'))

if (tenure < 3):
	tenure = 1
elif (tenure < 5):
	tenure = 3
elif (tenure < 10):
	tenure = 5
elif (tenure < 15): 
	tenure = 10
elif (tenure < 20): 
	tenure = 15
else:
	tenure = 20

tenstr = str(tenure) + "Yr_Returns"

df_ret = df[(df[tenstr] > ret) & (df['Expense'] < expense)] 
df_ret = df_ret[['Category','Expense', tenstr]].sort_values(tenstr, ascending=False)
print(df_ret)
print(df_ret.describe())
