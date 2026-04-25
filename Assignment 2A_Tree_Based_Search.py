import sys
import networkx as nx
import matplotlib.pyplot as plt
import random 
import math



G = nx.DiGraph()


file_name = sys.argv[1]
method_name = sys.argv[2]

cleaned_lines = []

# STEP 1: Read + clean file
with open(file_name, "r") as f:
    for line in f:
        line = line.strip()
        if line:
            cleaned_lines.append(line)






# STEP 2: Initialize structures
start_node = None
goals = []              # since there are multiple goals possible, we make this array
goal = None
pos = {}                # coordinates of the nodes so that it aligns with the x,y
node_colors = []

count = 0

#not yet implment (below)
nodes_created = None    
path = None





# STEP 3: Parse file
for line in cleaned_lines:
    count = count + 1 ## since the script cant detect the goal sometimes, put count to know its from line 2
    # Goals
    if ";" in line or count == 2:
        goals = line.split(";")
        random_num = random.randint(0,len(goals) - 1) #generate random num for 1 random goal included from txt
        goal = goals[random_num]

        

    # Node Coordinates
    elif ":" in line:
        node, coord = line.split(":")
        coord = coord.strip("()")
        x, y = coord.split(",")
        pos[node] = (int(x), int(y))
        G.add_node(node)
        

    # Edges (DIRECTED)
    elif "," in line:
        src, dest, weight = line.split(",")
        G.add_edge(src, dest, weight=weight)

    # Start node if no "symbols"
    else:
        start_node = line

for node in G.nodes():
    if goal == node:
        node_colors.append("green")
    elif start_node == node:
        node_colors.append("red")
    else:
        node_colors.append("blue")

# STEP 4: Search Algorithm Functions 
# Remember to include following inside your algorithm function :
# print(f"Starting Node:{start_node}")
# print(f"Destination Node: {goal}")
# print(f"Number of nodes created: {nodes_created}")
# print(f"Path: {path}")
# print(f"Path Cost: {path_cost}")

def BFS():
    return

def DFS():
    return

def GreedyBFS():
    predecessor = {} #storing predecessor nodes so can access later
    path_cost = 0



    plt.ion() # interactive mode :ON
    #heuristic = straightline distance
    # formula = a^2 + b^2 = c^2 
    for node in pos:
        x1,y1= pos[node]
        x2,y2 = pos[goal]
        x_diff = abs(x1 - x2) 
        y_diff = abs(y1-y2)
        straight_line_distance = math.sqrt(pow(x_diff,2) + pow(y_diff,2) ) 
        G.nodes[node]["heuristic"] = straight_line_distance
    
    frontier = [start_node]
    expanded = []
        
    while frontier:

        # pick node with smallest heuristic
        current = min(frontier, key=lambda n: G.nodes[n]["heuristic"])
        
        frontier.remove(current)
        expanded.append(current)
        

        node_list = list(G.nodes())

        #color for frontier
        for n in frontier:
            idx = node_list.index(n)
            node_colors[idx] = "grey"

        #color for expanded
        for n in expanded:
            idx = node_list.index(n)
            if n == goal:
                node_colors[idx] = "orange"
            else:
                node_colors[idx] = "red"
        
        show_plot()

        if current == goal:
            plt.ioff() #interactive off then show screen, so it doesnt shutdown
            plt.show() 
            nodes_created = len(frontier) + len(expanded) 


            node = goal
            path_cost = 0

            path = []
            node = goal


            #Start from the goal, and keep moving backwards using parent links until reach the start
            while node != start_node: # when node not == start node, loop (we currently at goal node)
                path.append(node)  #add the node to the path
                node = predecessor[node] #this node came from where? C? make node equal C, C node came from where? B.....

            path.append(start_node)
            path.reverse()

            path_str = " -> ".join(path)


            # adding path cost together
            while node != start_node:
                parent = predecessor[node]
                path_cost += int(G[parent][node]['weight'])
                node = parent


            print("FOUND")
            print(f"Starting Node:{start_node}")
            print(f"Destination Node: {goal}")
            print(f"Number of nodes created: {nodes_created}") 
            print(f"Path: {path_str}") 
            print(f"Path Cost: {path_cost}") 
            return
            

        # expand neighbors
        for n in G.neighbors(current):
            if n not in expanded and n not in frontier:
                frontier.append(n) 
                predecessor[n] = current 

        previous = current
    
                    

    return

def A_StarSearch():
    return




#Show drawing
def show_plot():
    plt.clf()  # clear old frame   
    nx.draw(G, pos, with_labels=True, node_color=node_colors)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels) # adding labels
    
    plt.pause(0.5)  # pause so we can SEE updates





# CLI execution
if method_name == "show":
    show_plot()
elif method_name == "BFS":
    BFS()
    show_plot()
elif method_name == "DFS":
    DFS()
    show_plot()
elif method_name == "GreedyBFS":
    GreedyBFS()
    
elif method_name == "A_StarSearch":
    A_StarSearch()
    show_plot()
