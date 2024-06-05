import environment
import find_path
import prey
import predator
import random
import networkx as nx
import matplotlib.pyplot as plt
import beliefSystem
import pickle
import math
import pandas as pd

def agentUpartial(graph):
    with open("utility_dict_1st_graph","rb") as handle:
        utility_file_read = pickle.load(handle)

    prey_location = prey.spawn_prey()
    predator_location = predator.spawn_predator()
    agent_location = random.choice(range(1,50))
    while utility_file_read [(agent_location,prey_location,predator_location)][0] == math.inf:
        agent_location = random.choice(range(1,50))
    steps = 0
    exact_prey_location_found = 0
    prey_prob = beliefSystem.prey_initialisation(graph,agent_location)
    expected_utility = []
    while steps <= 5000:
        # print("Prey" , prey_location)
        # print("Predator", predator_location)
        # print("Agent",agent_location)
        steps = steps + 1
        # print("Loop Start prob",prey_prob)
        # print("Sum =" ,sum(prey_prob[1:]))
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
        # print("max Prob index to move agent",prey_max_prob_index)

        # Agent Movement
        agent_pos_moves = []
        for neighbor in graph.neighbors(agent_location):
            agent_pos_moves.append(neighbor)


        # print("Agent Loc","Prey Loc","Predator Loc",agent_location,prey_location,predator_location)

        agent_neighbor_utility = {}
        for agent_possible in agent_pos_moves:
            utility_states_list = []
            temp_utility = 0
            expected_dist = 0
            for i in range(1,len(prey_prob)):
                expected_dist += prey_prob[i] * (len(find_path.bfs(graph,agent_possible,i)) - 1)
                if utility_file_read[(agent_possible,i,predator_location)][0] == math.inf:
                    if prey_prob[i] == 0:
                        continue
                    else:
                        temp_utility = math.inf
                        break
                temp_utility = temp_utility + ( utility_file_read[(agent_possible,i,predator_location)][0] * prey_prob[i] )
            utility_states_list.append(expected_dist)
            utility_states_list.append(len(find_path.bfs(graph,agent_possible,predator_location))-1)
            utility_states_list.append(temp_utility)
            agent_neighbor_utility[agent_possible] = temp_utility
            expected_utility.append(utility_states_list)

        # print(agent_neighbor_utility)

        agent_min_utility = min(agent_neighbor_utility.values())

        # print(agent_min_utility)

        for key in agent_neighbor_utility:
            if agent_neighbor_utility[key] == agent_min_utility:
                temp_node = key
        

        agent_location = temp_node

        # Terminal Condition Check
        if agent_location == prey_location and agent_location == predator_location:
            return("Failed",steps,exact_prey_location_found,expected_utility)
        elif agent_location == prey_location:
            # print("Prey" , prey_location)
            # print("Predator", predator_location)
            # print("Agent",agent_location)
            return("Success",steps,exact_prey_location_found,expected_utility)
        elif agent_location == predator_location:
            return("Failed",steps,exact_prey_location_found,expected_utility)
        prey_prob = beliefSystem.preyNotFound(graph,prey_prob,agent_location)
        # print("Prey prob after agent move",prey_prob)
        # print("Sum =" ,sum(prey_prob[1:]))
        prey_location = prey.move_prey(graph,prey_location)
        if agent_location == prey_location and agent_location == predator_location:
            return("Failed",steps,exact_prey_location_found,expected_utility)
        elif agent_location == prey_location:
            return("Success",steps,exact_prey_location_found,expected_utility)
        elif agent_location == predator_location:
            return("Failed",steps,exact_prey_location_found,expected_utility)
        prey_prob = beliefSystem.preyTransitionProb(graph,prey_prob)
        # print("Prey prob after prey move",prey_prob)
        # print("Sum =" ,sum(prey_prob[1:]))
        predator_location = predator.move_predator(graph,predator_location,agent_location)
        if agent_location == prey_location and agent_location == predator_location:
            return("Failed",steps,exact_prey_location_found,expected_utility)
        elif agent_location == prey_location:
            # print("Prey" , prey_location)
            # print("Predator", predator_location)
            # print("Agent",agent_location)
            return("Success",steps,exact_prey_location_found,expected_utility)
        elif agent_location == predator_location:
            return("Failed",steps,exact_prey_location_found,expected_utility)
        prey_prob = beliefSystem.preyNotFound(graph,prey_prob,agent_location)
    
    return("Hanged",steps,exact_prey_location_found,expected_utility)
        

if __name__ == "__main__":
    # graph = nx.read_gpickle("myGraph.gpickle")
    # print(agent3(graph))


    success_rates = 0 
    hanged = 0 
    total_avg_steps_size = 0 
    total_avg_prey_found = 0
    # graph = environment.graph_setup()
    graph = nx.read_gpickle("myGraph.gpickle")
    output = []
    steps_size = []
    prey_found = []
    data = []
    for _ in range(0,3000):
        print(_)
        temp_out = agentUpartial(graph) 
        output.append(temp_out[0])
        steps_size.append(temp_out[1])
        prey_found.append(temp_out[2])
        for item in (temp_out[3]):
            data.append(item)
    headers = ["Prey Dist","Pred Dist","Utility"]
    expected_utility = pd.DataFrame(data,columns=headers)
    expected_utility.to_pickle("Partial_Utility.pkl")

    for key in data:
        with open("./Expected_utility.txt","a") as o:
            o.write("{}\n".format(key))

    with open("./Results/output_upartial_agent.txt","a") as o:
        o.write("{}\n".format(output))
        o.write("Total Number of Steps\n")
        o.write("{}\n".format(steps_size))
        o.write("Total number of times prey was found\n")
        o.write("{}\n".format(prey_found))
        o.write("Success Rate = {}\n".format(output.count("Success") / 30))
        o.write("Hanged Rate = {}\n".format(output.count("Hanged") / 30 ))
        success_rates = success_rates + output.count("Success")
        hanged = hanged + output.count("Hanged")
        avg_steps_size = sum(steps_size) // 3000
        avg_prey_found = sum(prey_found) // 3000
        o.write("Average step size = {}\n".format(avg_steps_size))
        o.write("Avg Prey Found = {}\n".format(avg_prey_found))



    # with open("./Results/output_agent3.txt","a") as o:
    #     o.write("\n")
    #     o.write("Total Success Rates = {}\n".format(success_rates))
    #     o.write("\n")
    #     o.write("Average Results\n")
    #     o.write("Average Success Rates = {}\n".format(success_rates // 30))
    #     o.write("Average Hanged Rates = {}\n".format(hanged / 30))
    #     o.write("Average Step Size = {}\n".format(total_avg_steps_size / 30))
    #     o.write("Average Prey Found = {}\n".format(total_avg_prey_found / 30))

