import networkx as nx
import matplotlib.pyplot as plt
import random

def graph_setup():
    G = nx.Graph()
    for i in range(1,6):
        G.add_node(i)
    for i in range(1,5):
        G.add_edge(i,i+1)
    G.add_edge(5,1)
    return G

if __name__ == "__main__":
    G = graph_setup()
    nx.draw(G,with_labels = True,pos = nx.circular_layout(G))
    plt.show()
    print(G.number_of_edges())