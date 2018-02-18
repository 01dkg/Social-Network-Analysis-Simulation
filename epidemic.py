import networkx as nx
import random

# This is an SI epidemic model. Instead of states S and I, we use
# integers, in order to keep track not only of whether each person has
# the disease, but also how long they've had it.

# That is: state = 0 means healthy but susceptible. If a person
# becomes infected by the disease, they get state = 1 (infectious). At
# each time-step, this increases (any positive integer is still
# infectious). At state t, they die, and we give them state = -1 so we
# know not to consider them in future.

# In the step function, we calculate and save all the nodes' new
# states before overwriting them. So all the updates happen
# "simultaneously", that is this is a *synchronous* model. The
# alternative is *asynchronous*, that is each node gets updated as
# soon as its new state is known, which can affect the calculation of
# the new state for a later node within the same time-step. In many
# cases the difference is not important.

# In this model, we can either get a few people dying off, and the
# epidemic then disappearing, or we can get a large-scale die-off and
# only relatively isolated individuals surviving.


n = 100 # number of nodes
pn = 0.1 # per-edge probability of existing
p = 0.1 # probability of acquiring infection from a single neighbour, per time-step
i = 1 # number of nodes initially infected
td = 10 # td time-steps after infection, the individual dies
nsteps = 50 # how many time-steps to run

def infection_init(G):
    """Make a graph with some infected nodes."""
    for u in G.nodes():
        G.node[u]["state"] = 0
    init = random.sample(G.nodes(), i)
    for u in init:
        G.node[u]["state"] = 1

def step(G):
    """Given a graph G, run one time-step."""
    new_state = {}
    for u, d in G.nodes(data=True):
        new_state[u] = infection_update(d["state"],
                                        (G.node[u2]["state"] for u2 in G.neighbors(u)))
    for u in G.nodes():
        G.node[u]["state"] = new_state[u]

def infection_update(s1, ss):
    """Update the state of node s1, given the states of its neighbours ss."""

    if s1 < 0:
        return s1 # s1 < 0 means node has died, so no change
    if s1 > td:
        return -1 # t time steps after infection, node dies
    if s1 > 0:
        return s1 + 1 # one time-step has elapsed

    # if not yet infected, each infected neighbour is a new risk!
    for s in ss:
        if s > 0: # neighbour s is infected but still alive
            if random.random() < p:
                # with probability p, become infected
                return 1
    return 0

def run():
    G = nx.erdos_renyi_graph(n, pn)

    infection_init(G)
    print("Time proportion_alive proportion_infected")
    for i in range(nsteps):
        step(G)
        palive = sum(G.node[i]["state"] >= 0 for i in G.nodes()) / n
        pinf = sum(G.node[i]["state"] > 0 for i in G.nodes()) / n
        print("%2d %.2f %.2f" % (i, palive, pinf))

if __name__ == "__main__":
    run()
