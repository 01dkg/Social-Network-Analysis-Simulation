import networkx as nx
import random
import matplotlib.pyplot as plt
import operator

n = 20 #No. of Nodes in Graph

def agents():
    A =  nx.erdos_renyi_graph(n, 0.4)
    return A

def customer():
    C = nx.Graph()
    C.add_edge(n+1,0)
    return C

def combine(G,C):
    H = nx.compose(G,C)
    pos = nx.spring_layout(H)
    nx.draw_networkx_nodes(H, pos,
                           nodelist=[n+1],
                           node_color='r',
                           node_size=500,
                           alpha=0.8)
    nx.draw_networkx_nodes(H, pos,
                           nodelist=[0],
                           node_color='g',
                           node_size=500,
                           alpha=0.8)
    nx.draw_networkx_nodes(H, pos,
                           nodelist = range(1,n),
                           node_color='b',
                           node_size=500,
                           alpha=0.8)
    nx.draw_networkx_edges(H, pos, width=1.0, alpha=0.5)
    labels = {}
    labels[0] = r'$Hub$'

    for i in range(1,n):
        labels[i]= r'$D$' + str(i)
    labels[n+1] = r'$C$'
    nx.draw_networkx_labels(H, pos, labels, font_size=12)
    plt.show()

def  agent_status(G):
    #Possible states of any agents
    # 0 : Not available for work or Busy in delivering a product
    # 1 : Available    G= agents()
    for u in G.nodes():
        G.node[u]["state"] = 0
    init = random.sample(G.nodes(), 5)
    for u in init:
        G.node[u]["state"] = 1

def agent_status_update(node,G):
    #Setting an agent from available state to busy state
    G[node]["state"]=0


def select_available_agent(G):
    agent_available = []
    for i in G.nodes():
        if G.node[i]["state"]==1:
            agent_available.append(i)
    del agent_available[0]
    print("Agent available", agent_available)
    return agent_available


def best_agent(G):
    agent_available = select_available_agent(G)
    path_node ={}
    for i,values in enumerate(agent_available):
        dist = nx.dijkstra_path_length(agents(),i,0)
        path_node[values] = dist
    node= min(path_node, key=path_node.get)
    return node,agent_available

#Mention about customer status as well
def main():
    G=agents()
    C= customer()
    agent_status(G)
    print(G.nodes())
    combine(G,C)
    node, agent_is = best_agent(G)
    print(node, "agent will deliver the product")
    print("Current Status of Agent", node, " is")
    agent_status_update(node, G)
    print("Current Status of Agent", node, " is")
    print("Product has been delivered successfully")

if __name__ == "__main__":
    main()