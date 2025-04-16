import os
from langchain.prompts import PromptTemplate

# prompt_template = hub.pull("hwchase17/react")

prompt_template = PromptTemplate.from_template(
    template="""
You are a helpful financial coach named Kingshuk. 
Your client will ask you questions about financial matters.
Try to derive your answers from the given context. 
Please respond in a friendly and professional manner. 
If you don't know the answer, ask to book a free 15 min call at the below url.
https://www.calendly.com/startyourfinancesright/30min

Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}

"""

)

sample_query = "Be my financial coach and tell me how am I doing monthly. Net income = $8000, expense around $3000, debt payment $1000 and housing cost as $2000."
sample_query += "Also tell me what in Trump's latest tarriff laws will affect my finances."
sample_query += "My total savings are $10000, investment are $20000, debt is $5000 and the apr is 5%."
sample_query += "Can you help me in guiding me with my finances?"
sample_query += "\n"

budget_prompt_template = PromptTemplate.from_template(
    template="""
You are an intelligent budget planner. 
always open the budget first and initialize it.
The client will give you his spending as a journal entry.
Try to categorize the spending into one of the below categories.
The categories are:
utilities, housing, groceries, entertainment, insurance, debt payment, savings, investment.
You can look for a tool to use to categorize the spending and update the monthly budget.
Send only one expense at a time to the tool.

Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}

"""

)

sample_budget_query = """
I spent $100 at HEB, $4 at Starbucks, 
paid $300 rent and sent $150 to my savings account. 
Oh, I went back to HEB aand spent $30, then went to a video game parlor to spend $120 
and my kid dropped $20 into her piggy bank.
I checked my bank account and the subscription for Netflix was $19.99. 
"""
sample_budget_query += "Can you help me logging these into my budget and print my overall spending in a table format?"
