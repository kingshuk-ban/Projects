import os
import gradio as gr
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.messages import SystemMessage, AIMessage, HumanMessage
from langchain.chains.llm_math.base import LLMMathChain
from langchain.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv

# 🔐 Set your API Key
# Load environment variables
load_dotenv()

# 🌐 Tools: Search + Math
search = DuckDuckGoSearchRun()
llm_math_chain = LLMMathChain(llm=ChatOpenAI(temperature=0))
tools = [
    Tool(name="Search", func=search.run, description="Search the web"),
    Tool(name="Calculator", func=llm_math_chain.run, description="Solve math problems"),
]

# 🧠 LLM with streaming
llm = ChatOpenAI(temperature=0, streaming=True)

# 🧵 Memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 💡 Prompt with thinking style
thinking_style = "You are a thoughtful and curious financial guide who loves explaining things in simple language."

# Initialize chat model
# llm = ChatOpenAI(temperature=0.7, model='gpt-4o-mini', streaming=True)

# Initialize Gemini AI Studio chat model
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-002", streaming=True)

# Initialize Gemini AI Studio chat model
llm = ChatOpenAI(streaming=True)

def stream_response(message, history):
    print(f"Input: {message}. History: {history}\n")

    history_langchain_format = []
    history_langchain_format.append(SystemMessage(content=thinking_style))

    for human, ai in history:
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))

    if message is not None:
        history_langchain_format.append(HumanMessage(content=message))
        partial_message = ""
        for response in llm.stream(history_langchain_format):
            partial_message += response.content
            yield partial_message


demo_interface = gr.ChatInterface(

    stream_response,
    textbox=gr.Textbox(placeholder="Send to the LLM...",
                       container=False,
                       autoscroll=True,
                       scale=7),
)

demo_interface.launch(share=True, debug=True)