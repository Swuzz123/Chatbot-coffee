# agent/state.py
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class OrderState(TypedDict):
  messages: Annotated[list, add_messages]
  order: list[str]
  customer_id: int
  finished: bool