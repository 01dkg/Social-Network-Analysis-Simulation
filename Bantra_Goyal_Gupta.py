import networkx as nx
import random
import matplotlib.pyplot as plt
import operator

n = 10 #No. of Nodes in Graph

def agents():
    # G = nx.Graph()    #
    # G.add_edge(0, 1, dist=0.8)
    # G.add_edge(1, 2, dist=0.9)
    # G.add_edge(0, 4, dist=1.1)
    # G.add_edge(1, 4, dist=0.7)
    # G.add_edge(1, 3, dist=0.1)
    # G.add_edge(3, 6, dist=0.2)
    # G.add_edge(3, 5, dist=0.5)
    # G.add_edge(4, 5, dist=0.3)
    H =  nx.erdos_renyi_graph(n, 0.3)
    return H



def customer():
    G = nx.Graph()
    H = agents()
    print(nx.nodes(H))
    G.add_edge(11,0)
    return G

def combine():
    A= agents()
    C=customer()
    H = nx.compose(A,C)
    pos = nx.spring_layout(H)
    nx.draw_networkx_nodes(H, pos,
                           nodelist=[11],
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
combine()


def agents_status():
    G = agents()
    Avail = {}
    for i in G.nodes():
        Avail[i] = random.randint(0, 1)
    return Avail

agent_available_status = agents_status()


def agent_status_update(node):
    agent_available_status[node]=0


def select_available_agent():
    agent_available = []
    for i in agents().nodes():
        if agent_available_status[i]==1:
            agent_available.append(i)
    del agent_available[0]
    print("Agent available", agent_available)
    return agent_available


def best_agent():
    agent_available = select_available_agent()
    path_node ={}
    for i,values in enumerate(agent_available):
        dist = nx.dijkstra_path_length(agents(),i,0)
        path_node[values] = dist
    node= max(path_node, key=path_node.get)
    return node,agent_available


def product_delivery():
    node,agent_is = best_agent()
    print(node, "agent will deliver the product")
    print("Current Status of Agent",node," is",agent_available_status[node])
    agent_status_update(node)
    print("Current Status of Agent",node," is",agent_available_status[node])
    print("Product has been delivered successfully")

#Mention about customer status as well
product_delivery()