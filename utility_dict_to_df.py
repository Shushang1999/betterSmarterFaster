import numpy as np
import matplotlib.pyplot as plt
import pickle
import networkx as nx
import pandas as pd
import find_path

with open("utility_dict_1st_graph","rb") as handle:
    utility_file_read = pickle.load(handle)

graph = nx.read_gpickle("myGraph.gpickle")
data = []
for key in utility_file_read:
    temp = []
    agent,prey,pred = key
    temp.append(len(find_path.bfs(graph,agent,prey))-1)
    temp.append(len(find_path.bfs(graph,agent,pred))-1)
    temp.append(utility_file_read[key][0])
    data.append(temp)


headers = ["Prey Dist","Pred Dist","Utility"]
utility = pd.DataFrame(data,columns=headers)
utility.to_pickle("utility.pkl")
# print(utility.dtypes)

# utility_numpy_array = np.zeros(shape=(125000,150))

