import networkx as nx
import random
import matplotlib.pyplot as plt
H =  nx.erdos_renyi_graph(7, 0.8)
nx.draw_networkx(H)
plt.show()

