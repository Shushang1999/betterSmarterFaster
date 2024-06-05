import pickle
import prey
import easilyDistractedPredator
import random
import networkx as nx
import find_path
import math
from neuralNet import forwardPropogation
import pandas as pd
import numpy as np
import beliefSystem

def VAgent(graph):

    with open("utility_dict_1st_graph","rb") as handle:
        utility_file_read = pickle.load(handle)

    with open("neural_weights_1","rb") as handle:
        weights = pickle.load(handle)

    prey_location = prey.spawn_prey()
    predator_location = easilyDistractedPredator.spawn_predator()
    agent_location = random.choice(range(1,50))
    while utility_file_read [(agent_location,prey_location,predator_location)][0] == math.inf:
        agent_location = random.choice(range(1,50))
    start_state = (agent_location,prey_location,predator_location)
    steps = 0
    exact_prey_location_found = 0
    prey_prob = beliefSystem.prey_initialisation(graph,agent_location)
    while steps < 5000:
        steps = steps + 1
        max_prob = max(prey_prob[1:])
        # print("max Prob",max_prob)
        if max_prob != 1:
            max_index = []
            for i in range(0,51):
                if prey_prob[i] == max_prob:
                    max_index.append(i)
            index_to_survey = random.choice(max_index)
            if index_to_survey == prey_location:
                exact_prey_location_found = exact_prey_location_found + 1
                prey_prob = beliefSystem.preyFound(prey_prob,prey_location)
                # print("Prey prob after survey prey found",prey_location,prey_prob)
                # print("Sum =" ,sum(prey_prob[1:]))
            else:
                prey_prob = beliefSystem.preyNotFound(graph,prey_prob,index_to_survey)
                # print("Prey prob after survey prey not found",index_to_survey,prey_prob)
                # print("Sum =" ,sum(prey_prob[1:]))
            max_prob = max(prey_prob[1:])
            max_index = []
            for i in range(0,51):
                if prey_prob[i] == max_prob:
                    max_index.append(i)
            # print("max Prob",max_prob)
            prey_max_prob_index = random.choice(max_index)
        else:
            prey_max_prob_index = prey_prob.index(1)
            exact_prey_location_found = exact_prey_location_found + 1
        
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
            x_list = []
            expected_dist = 0
            for i in range(1,len(prey_prob)):
                expected_dist += prey_prob[i] * (len(find_path.bfs(graph,agent_possible,i)) - 1)
            x_list.append(expected_dist)
            x_list.append(len(find_path.bfs(graph,agent_possible,predator_location)) - 1)
            x = pd.DataFrame(x_list).transpose()
            y,inter_params = forwardPropogation(x,weights)
            # print(y)
            agent_neighbor_utility[agent_possible] = y[0][0]

        # print(agent_neighbor_utility)

        agent_min_utility = min(agent_neighbor_utility.values())

        for key in agent_neighbor_utility:
            if agent_neighbor_utility[key] == agent_min_utility:
                temp_node = key
        # Applying Agent 1 Rule Specified in the writeup


        agent_location = temp_node

        # Checking if agent died or agent caught prey

        if agent_location == prey_location and agent_location == predator_location:
            return("Success",steps)
        elif agent_location == prey_location:
            return("Success",steps)
        elif agent_location == predator_location:
            print(start_state)
            return("Failed",steps)
        prey_prob = beliefSystem.preyNotFound(graph,prey_prob,agent_location)
    
        prey_location = prey.move_prey(graph,prey_location)

        # Checking if prey died

        if agent_location == prey_location and agent_location == predator_location:
            return("Success",steps)
        elif agent_location == prey_location:
            return("Success",steps)
        elif agent_location == predator_location:
            print(start_state)
            return("Failed",steps)
        prey_prob = beliefSystem.preyTransitionProb(graph,prey_prob)

        predator_location = easilyDistractedPredator.move_predator(graph,predator_location,agent_location)

        # Checking if Predator caught agent or agent caught prey

        if agent_location == prey_location and agent_location == predator_location:
            return("Success",steps)
        elif agent_location == prey_location:
            return("Success",steps)
        elif agent_location == predator_location:
            print(start_state,steps)
            return("Failed",steps)
        prey_prob = beliefSystem.preyNotFound(graph,prey_prob,agent_location)
    
    return("Hanged",steps)


if __name__ == "__main__":
    success_rates = 0
    hanged = 0 
    total_avg_steps_size = 0 
    graph = nx.read_gpickle("myGraph.gpickle")
    output = []
    steps_size = []
    for _ in range(0,3000):

        # print(uStarAgent(graph))

        print(_)
        temp_out = VAgent(graph)  
        output.append(temp_out[0])
        # if temp_out[0] == "Failed":
        #     break
        steps_size.append(temp_out[1])
    with open("./Results/output_V_partial_using_V.txt","a") as o:
        o.write("{}\n".format(output))
        o.write("Total Number of Steps\n")
        o.write("{}\n".format(steps_size))
        o.write("Success Rate = {}\n".format(output.count("Success")))
        o.write("Hanged Rate = {}\n".format(output.count("Hanged")))
        success_rates = success_rates + output.count("Success")
        hanged = hanged + output.count("Hanged")
        avg_steps_size = sum(steps_size) // 3000
        # total_avg_steps_size = total_avg_steps_size + avg_steps_size
    with open("./Results/output_V_partial_using_V.txt","a") as o:
        o.write("\n")
        o.write("Total Success Rates = {}\n".format(success_rates))
        o.write("\n")
        o.write("Average Results\n")
        o.write("Average Success Rates = {}\n".format(success_rates / 30))
        o.write("Average Hanged Rates = {}\n".format(hanged))
        o.write("Average Step Size = {}\n".format(avg_steps_size))


