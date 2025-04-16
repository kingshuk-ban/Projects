from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain.schema.messages import SystemMessage, AIMessage, HumanMessage
from langchain.memory import ConversationBufferMemory
import gradio as gr
from gradio import ChatMessage


# My tools and modules
import mytools
from mytools import monthly_ratios, total_ratios, web_search, create_budget

import myragmodule
from myragmodule import prepare_rag, call_rag

from myprompts import prompt_template, sample_query

# Load environment variables
load_dotenv()

# Load the sample query
# You can change this query to anything you want to ask
#query = input( "Enter your query: ")
query = sample_query
rag = True

# Create the RAG output
# This will prepare the RAG and call it with the query
rag_output = ""
if (rag):
    prepare_rag()
    rag_output = call_rag(query)

# Combine the RAG output with the query
# The RAG output will be used to answer the query
query = rag_output + "\n" + query
#print ("\n--- Query ---")
#print(query)

# Create the LLM
# and the agent executor
# Provide the tools  
mytools = [monthly_ratios, total_ratios, create_budget, web_search]

llm = ChatOpenAI(model="gpt-4")

conversational_memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = create_react_agent(llm, mytools, prompt_template)

#agent_executor = AgentExecutor(agent=agent, tools=mytools, verbose=True)
agent_executor = AgentExecutor(agent=agent,
                               tools=mytools,
                               verbose=True,
                               memory=conversational_memory,
                               max_iterations=30,
                               max_execution_time=600,
                               handle_parsing_errors=True)

#agent_executor.invoke({"input": query})

# Define the function for the conversation
def continue_conversation(input, history):
    rag_output = call_rag(input)
    # Combine the RAG output with the query
    input = rag_output + "\n" + input
    
    # Invoke the agent and get the response
    response = agent_executor.invoke({"input": input})
    output = response['output']

    # Append the new input and output to the history
    history.append(f"User: {input}")
    history.append(f"AI Assistant: {output}")

    # Join the history into a single string
    history_text = "\n".join(history)

    # Return the current response and the full history (hidden state)
    return output, history_text, history

#Function call by the clear button to clear the Input textBox.
def clear_input():
    return ""

# Create the Gradio interface
with gr.Blocks() as demo:
  with gr.Row():
    #We use two columns to organize the Gradio Elements.
    with gr.Column():
      # Input textbox
      input_textbox = gr.Textbox(lines=5, placeholder="Type your prompt here...")
      # Conversation history state
      history_state = gr.State([])

      # Outputs
      current_response = gr.Textbox(label="Current Response")
      conversation_history = gr.Textbox(label="Conversation History", lines=10)
    with gr.Column():
    # Buttons
      send_button = gr.Button("Send")
      clear_button = gr.Button("Clear Input")

      # Bind the send button to submit the input
      send_button.click(
          fn=continue_conversation,
          inputs=[input_textbox, history_state],
          outputs=[current_response, conversation_history, history_state]
      )

      # Bind the clear button to clear the input
      clear_button.click(fn=clear_input, inputs=[], outputs=[input_textbox])

      # Alternatively, pressing "Enter" in the input box will also submit
      input_textbox.submit(
          fn=continue_conversation,
          inputs=[input_textbox, history_state],
          outputs=[current_response, conversation_history, history_state]
      )

demo.launch(debug=True)

# Gradio interface
def stream_response(message, history):
    print(f"Input: {message}. History: {history}\n")

    history_langchain_format = []
    history_langchain_format.append(SystemMessage(content=prompt_template.template))

    for human, ai in history:
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))

    if message is not None:
        history_langchain_format.append(HumanMessage(content=message))
        partial_message = ""
        for response in agent_executor.stream(history_langchain_format):
            partial_message += response.content
            yield partial_message


#demo_interface = gr.ChatInterface(

 #   stream_response,
 #   textbox=gr.Textbox(placeholder="Send to the LLM...",
  #                     container=False,
   #                    autoscroll=True,
    #                   scale=7),
#)

#demo_interface.launch(share=True, debug=True)

# Gradio interface
# def chatbot_interface(user_input):
#    response = agent_executor.invoke({"input":user_input})
#    return response

#iface = gr.Interface(fn=chatbot_interface, 
#                     inputs=gr.Textbox(lines=2, placeholder="Ask me anything..."), 
#                     outputs="text", 
#                     title="LangChain Agent with Gradio")

#iface.launch()