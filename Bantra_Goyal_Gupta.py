import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np
import unittest

n = 10 #No. of Nodes in Graph

def agents():
    # Creating fully connected / complete graph
    A=nx.complete_graph(n)
    # Assigning random weights to each edge in graph
    W = np.random.choice(100,len(A.edges()),replace=False)
    for i, (x, y) in enumerate(A.edges()):
        A[x][y]['w'] = W[i]
    return A

def customer():
    C = nx.Graph()
    C.add_node(n+1)
    C.add_edge(n+1,0)
    return C


def test_case():
    G1 = nx.Graph()
    G2 = nx.Graph()
    C1 = nx.Graph()
    C2 = nx.Graph()

    G1.add_edge(0, 1, weight=3)  # Adding Edges and weight
    G1.add_edge(0, 2, weight=2)
    G1.add_edge(0, 3, weight=7)
    G1.add_edge(1, 2, weight=4)
    G1.add_edge(1, 3, weight=1)
    G1.add_edge(2, 3, weight=5)
    C1.add_edge(11,0)
    G1.node[0]["state"] = 0
    G1.node[1]["state"] = 1
    G1.node[2]["state"] = 0
    G1.node[3]["state"] = 1


    G2.add_edge(0, 1, weight=3)  # Adding Edges and weight
    G2.add_edge(0, 2, weight=2)
    G2.add_edge(0, 3, weight=7)
    G2.add_edge(1, 2, weight=4)
    G2.add_edge(1, 3, weight=1)
    G2.add_edge(2, 3, weight=5)
    G2.add_edge(0, 4, weight=6)
    G2.add_edge(4, 2, weight=8)
    G2.add_edge(4, 3, weight=9)
    C2.add_edge(11, 0)
    G2.node[0]["state"] = 0
    G2.node[1]["state"] = 0
    G2.node[2]["state"] = 0
    G2.node[3]["state"] = 0
    G2.node[4]["state"] = 1

    return G1,C1,G2,C2

def combine(G,C):
    H = nx.compose(G,C)
    pos = nx.spring_layout(H)
    nx.draw_networkx_nodes(H, pos, nodelist=[n+1], node_color='r', node_size=500, alpha=0.8)
    nx.draw_networkx_nodes(H, pos, nodelist=[0],node_color='g', node_size=500, alpha=0.8)
    nx.draw_networkx_nodes(H, pos, nodelist = range(1,n), node_color='b', node_size=500, alpha=0.8)
    nx.draw_networkx_edges(H, pos, width=1.0, alpha=0.5)
    lab = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=lab)
    labels = {}
    labels[0] = r'$Hub$'
    for i in range(1,n):
        labels[i]= r'$A$' + str(i)
    labels[n+1] = r'$C$'
    nx.draw_networkx_labels(H, pos, labels, font_size=12)
    plt.savefig('main.png')
    #plt.show()


def  agent_status(G):
    #Possible states of any agents
    # 0 : Not available for work or Busy in delivering a product
    # 1 : Available    G= agents()
    for u in G.nodes():
        G.node[u]["state"] = 0
    init = random.sample(G.nodes(), int(n/2))
    for u in init:
        G.node[u]["state"] = 1



def select_available_agent(G):
    agent_available = []
    for i in G.nodes():
        if G.node[i]["state"]==1:
            agent_available.append(i)
    del agent_available[0]
    print("Agent available at the moment", agent_available)
    return agent_available


def random_allot():
    #Hub will randomly select an delivery agent
    initial_node = random.randint(1,n-1)
    print("Randomly Assigned Delivery Agent:", initial_node)
    return initial_node


def find_agent(start,G):
    print("Starting Agent:",start)
    initial = start
    if G.node[initial]["state"]==1: #Available
        print("Product Will be Delivered by:", initial)
        return initial
    elif G.node[initial]["state"]==0: # Not Available
        next = next_node_weight(initial,G)
        G.remove_node(start)
        find_agent(next,G)
    else:
        print("Available Agents Do Not Want Go")
        exit(0)

def next_node_weight(start,G):
    neighbours= G.neighbors(start)
    neighbours.remove(0)
    W = {}
    print("Source", "Target", "Weight")
    for index,neighbour in enumerate(neighbours):
        W[neighbour]= nx.shortest_path_length(G, source=start, target=neighbour,weight='w')
        print(start,"\t\t",
              neighbour,"\t\t",
              W[neighbour])
    wt = min(sorted(W.values()))
    print(wt,"Weight")
    next= list(W.keys())[list(W.values()).index(wt)]
    print("Next Node :",next)
    return next

class test_Case(unittest.TestCase):

    def __init__(self,testname, G):
        super(test_Case, self).__init__(testname)
        self.G = G
    def test_find_agent_G1(self):
        print("-------------------Case One-------------------")
        agent = find_agent(3, self.G)
        self.assertEqual(agent,3)

    def test_find_agent_G2(self):
        print("-------------------Case Two-------------------")
        select_available_agent(self.G)
        agent1 = find_agent(3, self.G)
        self.assertEquals(agent1,3)


#Mention about customer status as well
def main():
    G=agents()
    C= customer()
    agent_status(G)
    print(G.nodes())
    combine(G,C)
    select_available_agent(G)
    start = random_allot()
    find_agent(start,G)
    print("*************************End of Main**********************")

if __name__ == "__main__":
    main()
    print("-------------------Testing Data-------------------")
    G1, C1, G2, C2 = test_case()
    print(G1.nodes())
    select_available_agent(G1)
    suite = unittest.TestSuite()

    suite.addTest(test_Case("test_find_agent_G1", G1))
    suite.addTest(test_Case("test_find_agent_G2", G2))
    unittest.TextTestRunner().run(suite)