import pickle
import prey
import easilyDistractedPredator
import random
import networkx as nx
import find_path
import math

def uStarAgent(graph):

    with open("utility_dict_1st_graph","rb") as handle:
        utility_file_read = pickle.load(handle)

    prey_location = prey.spawn_prey()
    predator_location = easilyDistractedPredator.spawn_predator()
    agent_location = random.choice(range(1,50))
    while utility_file_read [(agent_location,prey_location,predator_location)][0] == math.inf:
        agent_location = random.choice(range(1,50))
    start_state = (agent_location,prey_location,predator_location)
    steps = 0
    while steps < 5000:
        steps = steps + 1

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

        # Checking if agent died or agent caught prey

        if agent_location == prey_location and agent_location == predator_location:
            return("Success",steps)
        elif agent_location == prey_location:
            return("Success",steps)
        elif agent_location == predator_location:
            print(start_state)
            return("Failed",steps)
    
        prey_location = prey.move_prey(graph,prey_location)

        # Checking if prey died

        if agent_location == prey_location and agent_location == predator_location:
            return("Success",steps)
        elif agent_location == prey_location:
            return("Success",steps)
        elif agent_location == predator_location:
            print(start_state)
            return("Failed",steps)

        predator_location = easilyDistractedPredator.move_predator(graph,predator_location,agent_location)

        # Checking if Predator caught agent or agent caught prey

        if agent_location == prey_location and agent_location == predator_location:
            return("Success",steps)
        elif agent_location == prey_location:
            return("Success",steps)
        elif agent_location == predator_location:
            print(start_state,steps)
            return("Failed",steps)
    
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
        temp_out = uStarAgent(graph)  
        output.append(temp_out[0])
        # if temp_out[0] == "Failed":
        #     break
        steps_size.append(temp_out[1])
    with open("./Results/output_ustar_agent.txt","a") as o:
        o.write("{}\n".format(output))
        o.write("Total Number of Steps\n")
        o.write("{}\n".format(steps_size))
        o.write("Success Rate = {}\n".format(output.count("Success")))
        o.write("Hanged Rate = {}\n".format(output.count("Hanged")))
        success_rates = success_rates + output.count("Success")
        hanged = hanged + output.count("Hanged")
        avg_steps_size = sum(steps_size) // 3000
        # total_avg_steps_size = total_avg_steps_size + avg_steps_size
    with open("./Results/output_ustar_agent.txt","a") as o:
        o.write("\n")
        o.write("Total Success Rates = {}\n".format(success_rates))
        o.write("\n")
        o.write("Average Results\n")
        o.write("Average Success Rates = {}\n".format(success_rates / 30))
        o.write("Average Hanged Rates = {}\n".format(hanged))
        o.write("Average Step Size = {}\n".format(avg_steps_size))


