####################################################################
#                                                                  #
#              MIS40550 NETWORK SOFTWARE MODELLING                 #
#                                                                  #
#                          ASSIGNMENT 2                            #
#                                                                  #
# AUTHOR : BANTRA ELPIDA (16200254)                                #
#          GOYAL SHRUTI (16200726)                                 #
#          GUPTA DEEPAK KUMAR (16200660)                           #
#                                                                  #
# SUPERVISOR : Dr. JAMES McDERMOTT                                 #
# Due Date: 19 April, 2017                                         #
#                                                                  #
####################################################################



####################################################################

# Importing essential libraries to run the program                 #
import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np
import unittest
import time

final_list = [0]
# Total number of nodes in graph is 10                             #
n = 10 #No. of Nodes in Graph

####################################################################
# This function will create a fully connected graph which represent#
# the connection among various delivery agents and edge weights are#
# assigned randomly                                                #
####################################################################

def agents():
    # Creating fully connected / complete graph
    A=nx.complete_graph(n)
    # Assigning random weights to each edge in graph
    W = np.random.choice(100,len(A.edges()),replace=False)
    for i, (x, y) in enumerate(A.edges()):
        A[x][y]['w'] = W[i]
    return A

####################################################################
# This function will create customer graph - customer who ordered  #
# product                                                          #
####################################################################

def customer():
    C = nx.Graph()
    C.add_node(n+1)
    C.add_edge(n+1,0)
    return C

####################################################################
# This function will run test cases for the graph generated        #
####################################################################

def test_case():
    G1 = nx.Graph()
    G2 = nx.Graph()
    G3 = nx.Graph()
    C1 = nx.Graph()
    C2 = nx.Graph()
    C3 = nx.Graph()

    G1.add_edge(0, 1, cost=3)  # Adding Edges and cost
    G1.add_edge(0, 2, cost=2)
    G1.add_edge(0, 3, cost=7)
    G1.add_edge(1, 2, cost=4)
    G1.add_edge(1, 3, cost=1)
    G1.add_edge(2, 3, cost=5)
    C1.add_edge(4,0)
    G1.node[0]["state"] = 0
    G1.node[1]["state"] = 0
    G1.node[2]["state"] = 0
    G1.node[3]["state"] = 1


    G2.add_edge(0, 1, cost=3)  # Adding Edges and cost
    G2.add_edge(0, 2, cost=2)
    G2.add_edge(0, 3, cost=7)
    G2.add_edge(1, 2, cost=4)
    G2.add_edge(1, 3, cost=1)
    G2.add_edge(2, 3, cost=5)
    G2.add_edge(0, 4, cost=6)
    G2.add_edge(4, 2, cost=8)
    G2.add_edge(4, 3, cost=9)
    C2.add_edge(5, 0)
    G2.node[0]["state"] = 0
    G2.node[1]["state"] = 0
    G2.node[2]["state"] = 1
    G2.node[3]["state"] = 0
    G2.node[4]["state"] = 0

    G3.add_edge(0, 1, cost=3)  # Adding Edges and cost
    G3.add_edge(0, 2, cost=2)
    G3.add_edge(0, 3, cost=7)
    G3.add_edge(1, 2, cost=4)
    G3.add_edge(1, 3, cost=1)
    G3.add_edge(2, 3, cost=5)
    C3.add_edge(4, 0)
    G3.node[0]["state"] = 0
    G3.node[1]["state"] = 0
    G3.node[2]["state"] = 0
    G3.node[3]["state"] = 0
    return G1,C1,G2,C2, G3, C3

####################################################################
# This function will combine customer and delivery agents graph    #
# that can be displayed al together                                #
####################################################################

def combine(G, C):
    H = nx.compose(G,C)
    pos = nx.spring_layout(H)
    no_node = len(G.nodes())
    nx.draw_networkx_nodes(H, pos, nodelist=[no_node+1], node_color='r', node_size=500, alpha=0.8)
    nx.draw_networkx_nodes(H, pos, nodelist=[0],node_color='g', node_size=500, alpha=0.8)
    nx.draw_networkx_nodes(H, pos, nodelist = range(1,no_node), node_color='b', node_size=500, alpha=0.8)
    nx.draw_networkx_edges(H, pos, width=1.0, alpha=0.5)
    lab = nx.get_edge_attributes(G, 'cost')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=lab)
    labels = {}
    labels[0] = r'$Hub$'
    for i in range(1,no_node):
        labels[i]= r'$A$' + str(i)
    labels[n+1] = r'$C$'
    nx.draw_networkx_labels(H, pos, labels, font_size=12)
    plt.savefig('main.png')
    #plt.show()


####################################################################
# This function will assign states to the delivery agents          #
# Available - 1                                                    #
# Not Available - 0                                                #
####################################################################

def  agent_status(G):
    #Possible states of any agents
    # 0 : Not available for work or Busy in delivering a product
    # 1 : Available    G= agents()
    for u in G.nodes():
        G.node[u]["state"] = 0
    init = random.sample(G.nodes(), int(n/2))
    for u in init:
        G.node[u]["state"] = 1

####################################################################
# This function will create a list of the agents who are available #
# for delivery from the graph                                      #
####################################################################

def select_available_agent(G):
    agent_available = []
    for i in G.nodes():
        if G.node[i]["state"]==1:
            agent_available.append(i)
    if agent_available == []:
        print("No Delivery Agents are Available")
    else:
        del agent_available[0]
        print("Available Agent are", agent_available)
    return agent_available

####################################################################
# This function will randomly allot a delivery agent amongst all   #
# other agents to start delivery with                              #
####################################################################

def random_allot():
    #Hub will randomly select an delivery agent
    initial_node = random.randint(1,n-1)
    print("Randomly Assigned Delivery Agent:", initial_node)
    return initial_node

####################################################################
# This function will find the available agent who is available to  #
# deliver the product to customer                                  #
#                                                                  #
# If the first allotted random agent is available then delivery    #
# will be done by first agent but if the agent status is not       #
# available then it will move nearest next neighbour whose edge    #
# weight is least and so on until the available agent is found     #
####################################################################

def find_agent(start,G):
    print("Start Agent:",start)
    initial = start
    if G.node[initial]["state"]==1: #Available
        print("Product Will be Delivered by Agent:", initial)
        final_list[0]=initial
    elif G.node[initial]["state"]==0: # Not Available
        next = next_node_cost(initial,G)
        G.remove_node(start)
        find_agent(next,G)
    else:
        print("Available Agents Do Not Want Go")
        exit(0)

####################################################################
# This function will find the next delivery agent according to     #
# nearest neighbour                                                #
####################################################################

def next_node_cost(start,G):
    neighbours= G.neighbors(start)
    neighbours.remove(0)
    W = {}
    print("Source", "Target", "Cost")
    for index,neighbour in enumerate(neighbours):
        W[neighbour]= nx.shortest_path_length(G, source=start, target=neighbour,weight='w')
        print(start,"\t\t",
              neighbour,"\t\t",
              W[neighbour])
    min_cost = min(sorted(W.values()))
    print("Minimum Cost: ",min_cost)
    next= list(W.keys())[list(W.values()).index(min_cost)]
    print("Next Delivery Agent :",next)
    print("-----------------------------------------------------")
    return next

class test_Case(unittest.TestCase):

    def __init__(self,testname, G):
        super(test_Case, self).__init__(testname)
        self.G = G
    def test_find_agent_G1(self):
        print("-------------------  Case One    -------------------")
        sTime = time.clock()
        print(self.G.nodes())
        agent = find_agent(3, self.G)
        self.assertEqual(final_list[0],3)
        ttime = time.clock() - sTime
        print("Time Taken", round(ttime, 6), " seconds\n")

    def test_find_agent_G2(self):
        print("--------------------  Case Two ---------------------")
        print(self.G.nodes())
        sTime = time.clock()
        agent1 = find_agent(3, self.G)
        self.assertEqual(final_list[0],2)
        ttime = time.clock() - sTime
        print("Time Taken", round(ttime, 6), " seconds\n")


    def test_select_available_agent(self):
        print("-------------------  Case Three   -------------------")
        select_available_agent(self.G)

####################################################################
# Main function to call the program                                #
####################################################################

def main(G,C,start):
    print("-------------------  Start of Main  -------------------")
    agent_status(G)
    select_available_agent(G)
    print(G.nodes())
    #combine(G, C )
    find_agent(start,G)
    print("-------------------   End of Main   -------------------")

if __name__ == "__main__":

    start = random_allot()
    sTime = time.clock()
    main(agents(),customer(),start)
    ttime = time.clock() - sTime
    print("Time Taken", round(ttime, 6), " seconds\n")
    print("------------------  Start of Testing ---------------")
    G1, C1, G2, C2, G3, C3 = test_case()
    suite = unittest.TestSuite()
    suite.addTest(test_Case("test_find_agent_G1", G1))
    suite.addTest(test_Case("test_find_agent_G2", G2))
    suite.addTest(test_Case("test_select_available_agent", G3))
    unittest.TextTestRunner().run(suite)
