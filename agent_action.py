import pickle
import prey
import easilyDistractedPredator
import random
import networkx as nx
import find_path
import math
import overlap

def agent1(graph,state):
    agent_location, prey_location, predator_location = state
    curr_distance_agent_prey = len(find_path.bfs(graph,agent_location,prey_location))
    curr_distance_agent_predator = len(find_path.bfs(graph,agent_location,predator_location))
    agent_neighbor_dist = {}
    
    # Calculating the distance of each neighbors of agent to the prey and predator

    for neighbor in graph.neighbors(agent_location):
        dist = len(find_path.bfs(graph,neighbor,prey_location))
        agent_neighbor_dist[neighbor] = {"Prey_dist":dist}
        dist = len(find_path.bfs(graph,neighbor,predator_location))
        agent_neighbor_dist[neighbor].update({"Predator_dist":dist})

    # print(agent_neighbor_dist)

    # Applying Agent 1 Rule Specified in the writeup

    temp_node = 100
    for n in agent_neighbor_dist:
        if agent_neighbor_dist[n]["Prey_dist"] < curr_distance_agent_prey and agent_neighbor_dist[n]["Predator_dist"] > curr_distance_agent_predator:
            temp_node = n
            break
    if temp_node == 100:
        for n in agent_neighbor_dist:
            if agent_neighbor_dist[n]["Prey_dist"] < curr_distance_agent_prey and agent_neighbor_dist[n]["Predator_dist"] >= curr_distance_agent_predator:
                temp_node = n
                break
    if temp_node == 100:
        for n in agent_neighbor_dist:
            if agent_neighbor_dist[n]["Prey_dist"] <= curr_distance_agent_prey and agent_neighbor_dist[n]["Predator_dist"] > curr_distance_agent_predator:
                temp_node = n
                break
    if temp_node == 100:
        for n in agent_neighbor_dist:
            if agent_neighbor_dist[n]["Prey_dist"] <= curr_distance_agent_prey and agent_neighbor_dist[n]["Predator_dist"] >= curr_distance_agent_predator:
                temp_node = n
                break
    if temp_node == 100:
        for n in agent_neighbor_dist:
            if agent_neighbor_dist[n]["Predator_dist"] > curr_distance_agent_predator:
                temp_node = n
                break 
    if temp_node == 100:
        for n in agent_neighbor_dist:
            if agent_neighbor_dist[n]["Predator_dist"] >= curr_distance_agent_predator:
                temp_node = n
                break 
    if temp_node == 100:
        temp_node = agent_location

    agent_location = temp_node
    return(agent_location)

def agent2(graph,state):
    agent_location, prey_location, predator_location = state
    overlap_edge = set()
    curr_distance_agent_prey = len(find_path.bfs(graph,agent_location,prey_location))
    curr_distance_agent_predator = len(find_path.bfs(graph,agent_location,predator_location))
    if curr_distance_agent_predator == 2:
        overlap_edge = overlap.overlap_edge(graph)         # Checking for overlap edges
    agent_neighbor_dist = {}
    for neighbor in graph.neighbors(agent_location):
        dist = len(find_path.bfs(graph,neighbor,prey_location))
        agent_neighbor_dist[neighbor] = {"Prey_dist":dist}
        dist = len(find_path.bfs(graph,neighbor,predator_location))
        agent_neighbor_dist[neighbor].update({"Predator_dist":dist})
    temp_node = 100
    if len(overlap_edge) == 0:
        for n in agent_neighbor_dist:
            if agent_neighbor_dist[n]["Prey_dist"] < curr_distance_agent_prey and agent_neighbor_dist[n]["Predator_dist"] > curr_distance_agent_predator:
                temp_node = n
                break
        if temp_node == 100:
            for n in agent_neighbor_dist:
                if agent_neighbor_dist[n]["Prey_dist"] < curr_distance_agent_prey and agent_neighbor_dist[n]["Predator_dist"] >= curr_distance_agent_predator:
                    temp_node = n
                    break
        if temp_node == 100:
            for n in agent_neighbor_dist:
                if agent_neighbor_dist[n]["Prey_dist"] <= curr_distance_agent_prey and agent_neighbor_dist[n]["Predator_dist"] > curr_distance_agent_predator:
                    temp_node = n
                    break
        if temp_node == 100:
            for n in agent_neighbor_dist:
                if agent_neighbor_dist[n]["Prey_dist"] <= curr_distance_agent_prey and agent_neighbor_dist[n]["Predator_dist"] >= curr_distance_agent_predator:
                    temp_node = n
                    break
        if temp_node == 100:
            for n in agent_neighbor_dist:
                if agent_neighbor_dist[n]["Predator_dist"] > curr_distance_agent_predator:
                    temp_node = n
                    break 
        if temp_node == 100:
            for n in agent_neighbor_dist:
                if agent_neighbor_dist[n]["Predator_dist"] >= curr_distance_agent_predator:
                    temp_node = n
                    break 
        if temp_node == 100:
            possible_moves = []
            for neighbors in graph.neighbors(agent_location):
                if n not in overlap_edge:
                    possible_moves.append(neighbors)
            if len(possible_moves) == 0:
                for neighbors in graph.neighbors(agent_location):
                    possible_moves.append(neighbors)
            temp_node = random.choice(possible_moves)
    else:
        # Checking for neighbors according the preference mentioned in the report
        for n in agent_neighbor_dist:
            if agent_neighbor_dist[n]["Prey_dist"] < curr_distance_agent_prey and agent_neighbor_dist[n]["Predator_dist"] > curr_distance_agent_predator and n not in overlap_edge:
                temp_node = n
                break
        if temp_node == 100:
            for n in agent_neighbor_dist:
                if agent_neighbor_dist[n]["Prey_dist"] < curr_distance_agent_prey and agent_neighbor_dist[n]["Predator_dist"] > curr_distance_agent_predator:
                    temp_node = n
                    break
        if temp_node == 100:
            for n in agent_neighbor_dist:
                if agent_neighbor_dist[n]["Prey_dist"] <= curr_distance_agent_prey and agent_neighbor_dist[n]["Predator_dist"] > curr_distance_agent_predator and n not in overlap_edge:
                    temp_node = n
                    break
        if temp_node == 100:
            for n in agent_neighbor_dist:
                if agent_neighbor_dist[n]["Prey_dist"] <= curr_distance_agent_prey and agent_neighbor_dist[n]["Predator_dist"] > curr_distance_agent_predator:
                    temp_node = n
                    break
        if temp_node == 100:
            for n in agent_neighbor_dist:
                if agent_neighbor_dist[n]["Predator_dist"] > curr_distance_agent_predator and n not in overlap_edge:
                    temp_node = n
                    break
        if temp_node == 100:
            for n in agent_neighbor_dist:
                if agent_neighbor_dist[n]["Predator_dist"] > curr_distance_agent_predator:
                    temp_node = n
                    break 
        if temp_node == 100:
            possible_moves = []
            for neighbors in graph.neighbors(agent_location):
                if n not in overlap_edge:
                    possible_moves.append(neighbors)
            if len(possible_moves) == 0:
                for neighbors in graph.neighbors(agent_location):
                    possible_moves.append(neighbors)
            temp_node = random.choice(possible_moves)
    agent_location = temp_node
    return(agent_location)

def uStarAgent(graph,state):

    with open("utility_dict_1st_graph","rb") as handle:
        utility_file_read = pickle.load(handle)

    agent_location, prey_location, predator_location = state
        # curr_distance_agent_prey = len(find_path.bfs(graph,agent_location,prey_location))
        # curr_distance_agent_predator = len(find_path.bfs(graph,agent_location,predator_location))
        # agent_neighbor_dist = {}
        
        # Calculating the distance of each neighbors of agent to the prey and predator

    agent_pos_moves = []
    for neighbor in graph.neighbors(agent_location):
        agent_pos_moves.append(neighbor)


    # print("Agent Loc","Prey Loc","Predator Loc",agent_location,prey_location,predator_location)

    agent_neighbor_utility = {}
    for agent_possible in agent_pos_moves:
        agent_neighbor_utility[agent_possible] = utility_file_read[(agent_possible,prey_location,predator_location)][0]

    # print(agent_neighbor_utility)

    agent_min_utility = min(agent_neighbor_utility.values())

    for key in agent_neighbor_utility:
        if agent_neighbor_utility[key] == agent_min_utility:
            temp_node = key
    # Applying Agent 1 Rule Specified in the writeup


    agent_location = temp_node
    return(agent_location)

if __name__ == "__main__":
    graph = nx.read_gpickle("myGraph.gpickle")
    agent_move = {}
    with open("utility_dict_1st_graph","rb") as handle:
        utility_file_read = pickle.load(handle)
    step = 0
    for key in utility_file_read:
        step = step + 1
        print(step)
        agent_move[key] = {"Agent 1":agent1(graph,key)}
        agent_move[key].update({"Agent 2":agent2(graph,key)})
        agent_move[key].update({"U Star Agent":uStarAgent(graph,key)})
    f = open("agent_move.txt","w")
    f.write(str(agent_move))
    f.close()