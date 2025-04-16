from langchain.agents import tool
import json
import os
import re

@tool
def monthly_ratios(params:str) -> str:
        """Get the financial ratios from a monthly perspective given the income, debt, expense and housing costs per month.
            Split the input into four arguments - income, debt, expense and housing and pack into a dictionary.
            The function will return the monthly ratios of income, debt, expense and housing costs."""
        
        #if (len(*args) <= 4):
         #   return "Please provide the income, debt, expense and housing costs in the format: income, debt, expense, housing."
        p = json.loads(params)
        i = float(p["income"])
        d = float(p["debt"])
        e = float(p["expense"])
        h = float(p["housing"])

        reply = f"You are spending {e/i*100.0}% of your income.\n"
        reply += f"Your debt to income ratio is {d/i*100.0}%.\n"
        reply += f"Your housing ratio is {h/i*100.0}%.\n"
        slack = i - d - e - h
        reply += f"Your monthly slack is ${slack}.\n"
        reply += f"Your savings ratio is {slack/i*100.0}%.\n"
        return reply

@tool
def total_ratios(params: str) -> str:
        """Get the financial ratios from a net worth perspective given the total savings, investment, debt and the apr for the debt."""
        p = json.loads(params)

        s = float(p["savings"])
        i = float(p["investment"])
        d = float(p["debt"])
        a = float(p["apr"])
    

        reply = f"Your net worth is ${s + i - d}.\n"
        reply += f"You are paying ${(a/100.0)*d} in debt payments per year.\n"
        reply += f"Your debt to equity ratio is {d/(i+s)*100.0}%.\n"
        return reply

# Using built in LangChain tool integrations
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchResults

wrapper = DuckDuckGoSearchAPIWrapper(max_results=10)
web_search = DuckDuckGoSearchResults(api_wrapper=wrapper)

monthly_budget = dict()
budget_categories = ["utilities", "housing", "groceries", "entertainment", "insurance", "debt payment", "savings", "investment"]

@tool
def remove_budget() -> str:
    """Use this tool to clear or reset the budget for the user."""
    global monthly_budget
    monthly_budget = dict()
    json.dump(monthly_budget, open("budget.json", "w"))
    #remove the json file
    if (os.path.exists("budget.json")):
        os.remove("budget.json")
    return "Your budget has been cleared.\n"

@tool
def initialize_budget() -> str:
    """Check for the budget file and load the budget from the file."""
    global monthly_budget
    global budget_categories

    #load the dict from the disk
    if (os.path.exists("budget.json")):
        monthly_budget = json.load(open("budget.json"))
        for category in budget_categories:
                if category not in monthly_budget:
                        monthly_budget[category] = 0.0
        return "Your budget has been loaded.\n"
    else:
        for category in budget_categories:
                monthly_budget[category] = 0.0
        return "Your budget has been initialized.\n"
    
@tool
def create_budget(item: str) -> str:
    """Extract a category name and the value from the user and create a budget for the user.
        Recognize one of the below categories and convert similar sounding categories to the same category.
        Categories passed to this function should be one of the below and in the form of {"category":"category", "value":"value"}.
        The string that you pass in as argument should be parsable by json.loads.
        The categories are:
        utilities, housing, groceries, entertainment, insurance, debt payment, savings, investment."""
    #item = re.search('({.+})', item).group(0).replace("'", '"').replace("\$", "")
    #print(item)
    i = json.loads(item)
    category = i["category"]
    value = float(i["value"])
    print("\n")
    print("got this category: " + category)
    print("got this value: " + str(value))
    
    #check if the category is in the budget categories
    monthly_budget[category] += value
    return "Your total expense for " + category + " is $" + str(monthly_budget[category]) + ".\n"

@tool
def print_budget() -> str:
    """Use this tool to print the budget for the user in a table format."""
    reply = "Total\t" + str(sum(monthly_budget.values())) + "\n"
    reply += "Your monthly spending so far as a table is:\n"
    reply += "Category\tAmount\n"
    for category in budget_categories:
        reply += f"{category}\t{monthly_budget[category]}\n" 
    print(reply)
    json.dump(monthly_budget, open("budget.json", "w"))
    return reply


