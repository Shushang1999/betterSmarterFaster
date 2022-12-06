import pickle

with open("utility_dict_2nd_graph","rb") as handle:
    utility_file_read = pickle.load(handle)

for key in utility_file_read:
    print(key,utility_file_read[key])