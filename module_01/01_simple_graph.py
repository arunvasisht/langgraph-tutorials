"""
A graph in LangGraph has three main components,
1. State : A python dictionary that stores the state of the graph
2. Nodes: A python function that updates the state of the graph
4. Edges : A python function that represent an edge between two nodes and may have some conditional logic to select a target node.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import random

class State(TypedDict):
    graph_state: str

def node_1(state):
    print("Node 1")
    return {"graph_state": state["graph_state"] + " I am"}

def node_2(state):
    print("Node 2")
    return {"graph_state": state["graph_state"] + " happy."}

def node_3(state):
    print("Node 3")
    return {"graph_state": state["graph_state"] + " sad."}

def decide_node(state):
    user_input = state["graph_state"]
    if random.random() > 0.5:
        return "node_2"
    else:
        return "node_3"


# Create the graph
graph = StateGraph(State)
graph.add_node("node_1", node_1)
graph.add_node("node_2", node_2)
graph.add_node("node_3", node_3)

# Logic
graph.add_edge(START, "node_1")
graph.add_conditional_edges("node_1",decide_node)
graph.add_edge("node_2", END)
graph.add_edge("node_3", END)

# compile the graph
graph = graph.compile()

# Save the graph
graph.get_graph().draw_mermaid_png(output_file_path="01_simple_graph.png")

# Invoke the graph with a user input
output = graph.invoke({"graph_state":"My name is Arun."})

print(output)