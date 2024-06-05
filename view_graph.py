import networkx as nx
import matplotlib.pyplot as plt

G = nx.read_gpickle("myGraph.gpickle")
nx.draw(G,with_labels = True,pos = nx.circular_layout(G))
plt.show()