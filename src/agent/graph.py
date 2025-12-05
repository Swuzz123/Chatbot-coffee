# agent/graph.py
from typing import Literal
from .tools import tools
from .state import OrderState
from .utils import initModelLLM, SYSTEMP_PROMPT, WELCOME_MSG

from langgraph.prebuilt import ToolNode
from langgraph.graph import START, END, StateGraph
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# ================== NODE FUNCTIONS ==================
tool_node = ToolNode(tools)
llm_with_tools = initModelLLM().bind_tools(tools)

def human_node(state: OrderState) -> OrderState:
    last_msg = state["messages"][-1]
    print("Assistant:", last_msg.content)

    user_input = input("User: ")

    if user_input.lower() in {"q", "quit", "exit", "goodbye", "tạm biệt"}:
      state['finished'] = True

    return state | {"messages": [HumanMessage(content=user_input)]}

def decide_node(state: OrderState) -> Literal["tools", "human"]:  
  last = state["messages"][-1]
  if hasattr(last, "tool_calls") and last.tool_calls:
    return "tools"
  else:
    return "human"

def chat_node(state: OrderState) -> OrderState:  
  if state["messages"]:
    msgs = [SystemMessage(content=SYSTEMP_PROMPT)] + state["messages"]
    output = llm_with_tools.invoke(msgs)
  else:
    output = AIMessage(content=WELCOME_MSG)
    
  return state | {"messages": [output]}

# ================== BUILD GRAPH ==================
builder = StateGraph(OrderState)

builder.add_node("chatbot", chat_node)
builder.add_node("human", human_node)
builder.add_node("tools", tool_node)

builder.add_edge(START, "chatbot")
builder.add_edge("tools", "chatbot")

builder.add_conditional_edges("chatbot", decide_node)
builder.add_conditional_edges(
  "human",
  lambda state: "end" if state.get("finished", False) else "chatbot",
  {
    "chatbot": "chatbot",
    "end": END
  }
)

chat_graph = builder.compile()