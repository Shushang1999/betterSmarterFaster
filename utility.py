import temp_graph
import find_path
import environment
import networkx as nx
import math
import numpy as np
import pickle

def utility(graph):
    utility_numpy_array = np.zeros(shape=(125000,150))
    utility_rewards = {}
    i = 0
    for agent in graph.nodes():
        for prey in graph.nodes():
            for pred in graph.nodes():
                # utility_numpy_array[0][i] = float(agent,prey,pred)
                i = i + 1
                if agent == prey and agent == pred:
                    utility_rewards[agent,prey,pred] = [0,0]
                elif agent == prey:
                    utility_rewards[agent,prey,pred] = [0,0]
                # elif (agent + 1) % 
                elif agent == pred:
                    utility_rewards[agent,prey,pred] = [0,math.inf]
                else:
                    utility_rewards[agent,prey,pred] = [len(find_path.bfs(graph,prey,agent)) - 1,1]
   
    # for key in utility_rewards:
    #     print(key,utility_rewards[key])

    beta = 0.7

    step_size = 0
    error = True
    while error:
        error = False
        step_size = step_size + 1
        utility_rewards_new = {}
        k = 0
        for key in utility_rewards:
            utility_numpy_array[k][step_size] = utility_rewards[key][0]
            k = k + 1
            reward = utility_rewards[key][1]
            temp_utility = 0

            agent,prey,pred = key

            if agent == prey:
                utility_rewards_new[agent,prey,pred] = [0, reward]
                continue
            elif agent == pred:
                utility_rewards_new[agent,prey,pred] = [math.inf, reward]
                continue

            prey_node_degree = graph.degree(prey) + 1
            prey_transition_prob = 1 / prey_node_degree

            prey_move = {}
            for prey_neighbor in graph.neighbors(prey):
                prey_move[prey_neighbor] = prey_transition_prob
            prey_move[prey] = prey_transition_prob
            
            pred_move = {}
            pred_neighbor_dist = {}
            for pred_neighbor in graph.neighbors(pred):
                pred_neighbor_dist[pred_neighbor] = len(find_path.bfs(graph,pred_neighbor,agent))
            
            min_dist_pred_neighbor_agent = min(list(pred_neighbor_dist.values()))
            min_dist_count = list(pred_neighbor_dist.values()).count(min_dist_pred_neighbor_agent)
            pred_min_dist_probability = 1 / min_dist_count
            pred_normal_probability = 1 / len(pred_neighbor_dist)

            for pred_neighbor in graph.neighbors(pred):
                if pred_neighbor_dist[pred_neighbor] == min_dist_pred_neighbor_agent:
                    pred_move[pred_neighbor] = 0.6 * pred_min_dist_probability + 0.4 * pred_normal_probability
                else:
                    pred_move[pred_neighbor] = 0.4 * pred_normal_probability
            
            agent_move = {}
            agent_node_degree = graph.degree(agent) 
            agent_transition_prob = 1 / agent_node_degree

            for agent_neighbor in graph.neighbors(agent):
                agent_move[agent_neighbor] = agent_transition_prob


            # print(sum(list(agent_move.values())))

            temp_utility_array = []
            for agent_new in agent_move:
                if agent_new == prey:
                    temp_utility = 0
                    temp_utility_array.append(temp_utility)
                    continue
                elif agent_new == pred:
                    temp_utility = math.inf
                    temp_utility_array.append(temp_utility)
                    continue
                temp_utility = 0
                for pred_new in pred_move:
                    for prey_new in prey_move:
                        temp_prob = prey_move[prey_new] * pred_move[pred_new]
                        #  * agent_move[agent_new]
                        temp_utility = temp_utility + (temp_prob * utility_rewards[agent_new,prey_new,pred_new][0])
                        # print((agent_new,prey_new,pred_new),utility_rewards[agent_new,prey_new,pred_new][0])
                temp_utility_array.append(temp_utility)
                        # rewards.append(utility_rewards[agent_new,prey_new,pred_new][1])

            # temp_utility = []

            min_utility = min(temp_utility_array)
            
            utility_rewards_new[agent,prey,pred] = [min_utility + reward, reward]

        for key in utility_rewards:
            if abs(utility_rewards[key][0] - utility_rewards_new[key][0]) > 0.0001:
                print("error",utility_rewards[key][0] - utility_rewards_new[key][0])
                error = True
                break
        utility_rewards = utility_rewards_new

        print(step_size)

    for key in utility_rewards:
        with open("./utility_2ndGraph.txt","a") as o:
            o.write("{}\t".format(key))
            o.write("{}\n".format(utility_rewards[key]))
    
    with open("utility_dict_2nd_graph","wb") as utility_file:
        pickle.dump(utility_rewards,utility_file,protocol=pickle.HIGHEST_PROTOCOL)

    # with open("utility_dict_2nd_graph","rb") as handle:
    #     utility_file_read = pickle.load(handle)

    # for key in utility_file_read:
    #     print(key,utility_file_read[key])

    np.savetxt("test.txt",utility_numpy_array)

if __name__ == "__main__":
    # G = temp_graph.graph_setup()
    G = environment.graph_setup()
    nx.write_gpickle(G,"myGraph2.gpickle")
    # G = nx.read_gpickle("myGraph.gpickle")
    utility(G)