"""Main entry point of the pipeline."""

from langgraph.graph import START, END, StateGraph

from core.nodes.research import research_node



def main():

    builder = StateGraph() 
    builder.add_node('researher', research_node)

    builder.add_edge(START, 'researcher')
    builder.add_edge('researcher', END)

    graph = builder.compile()
    
    
if __name__ == "__main__":
    main()















#GRAPH

# builder = StateGraph(state)

# builder.add_node('perspective', planner)
# builder.add_node('researcher', researcher)
# builder.add_node('compiler', compiler)


# builder.add_edge(START, 'perspective')
# builder.add_conditional_edges('perspective', fan_out_node)
# builder.add_edge('researcher', 'compiler')
# builder.add_edge('compiler', END)


# graph = builder.compile()

# t = time.time()
# result = graph.invoke(
#     {
#         "topic": topic,
#         "domains": [],
#         "perspectives": [],
#         "summaries": [],
#         "final_report": ""
#     }
# )
# print('Total Agents Time: ', time.time() - t)
# print(result)