# agent/state.py
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class OrderState(TypedDict):
  messages: Annotated[Sequence[BaseMessage], add_messages]
  customer_id: str
  finished: bool