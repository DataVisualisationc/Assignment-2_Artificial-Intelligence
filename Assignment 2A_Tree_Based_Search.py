import sys
import networkx as nx
import matplotlib.pyplot as plt
import random 
import math

from parser import show_plot



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

#labeling with color for the nodes
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



# BFS

def BFS():
    plt.ion()
    predecessor = {}
    path_cost = 0
    
    # Frontier as a Queue (FIFO)
    frontier = [start_node]
    expanded = []

    while frontier:
        # Pop from the front of the list (FIFO)
        current = frontier.pop(0)

        if current in expanded:
            continue
        expanded.append(current)

        # Update node colors for visualization
        node_list = list(G.nodes())
        for n in frontier:
            idx = node_list.index(n)
            node_colors[idx] = "grey"       # in frontier
        for n in expanded:
            idx = node_list.index(n)
            if n in goals:
                node_colors[idx] = "orange" # goal found
            else:
                node_colors[idx] = "red"    # expanded
        show_plot()

        # Goal check: reach one of the destination nodes
        if current in goals:
            # Number of nodes created = Expanded + Frontier
            nodes_created = len(frontier) + len(expanded) 

            # Reconstruct path by backtracking
            path = []
            node = current
            while node != start_node:
                path.append(node)
                node = predecessor[node]
            path.append(start_node)
            path.reverse()

            path_str = " -> ".join(path)

            # Calculate total path cost
            node = current
            while node != start_node:
                parent = predecessor[node]
                path_cost += int(G[parent][node]['weight'])
                node = parent

            # Final Output Block
            print(f"Starting Node: {start_node}")
            print(f"Destination Node: {current}")
            print(f"Number of nodes created: {nodes_created}")
            print(f"Path: {path_str}")
            print(f"Path Cost: {path_cost}")

            animated_path = []
            animated_edges = []

            for i in range(len(path)):

                animated_path.append(path[i])

                if i > 0:
                    animated_edges.append((path[i-1], path[i]))

                temp_colors = []

                edge_set = set(animated_edges)

                edge_colors = [
                    "green" if e in edge_set else "black"
                    for e in G.edges()
                ]

                for n in G.nodes():

                    if n == path[-1]:

                        if n in animated_path:
                            temp_colors.append("green")
                        else:
                            temp_colors.append("orange")

                    elif n in animated_path:
                        temp_colors.append("green")

                    elif n in expanded:
                        temp_colors.append("red")

                    else:
                        temp_colors.append("gray")

                edge_colors = []

                for edge in G.edges():

                    if edge in animated_edges:
                        edge_colors.append("green")
                    else:
                        edge_colors.append("black")

                plt.clf()

                # 1. draw nodes
                nx.draw_networkx_nodes(G, pos, node_color=temp_colors)
                

                # 2. draw ALL edges (background layer)
                nx.draw_networkx_edges(
                    G,
                    pos,
                    width=2
                )

                # 3. draw ONLY animated edges (foreground layer)
                nx.draw_networkx_edges(
                    G,
                    pos,
                    edgelist=list(edge_set),
                    edge_color="green",
                    width=4
                )

                # 4. labels
                nx.draw_networkx_labels(G, pos)
                nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))

                plt.pause(0.5)
                plt.text(
            0.05, 1.12,
            f"Path: {path_str}",
            transform=plt.gca().transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(facecolor='white')
            )   


            plt.ioff()
            plt.show()  
                                                                                  
                

            return

        # Note 2: Expand nodes in ascending order
        for neighbor in sorted(G.neighbors(current)):
            if neighbor not in expanded and neighbor not in frontier:
                frontier.append(neighbor)
                predecessor[neighbor] = current

    print("No solution found.")
    return

# DFS

def DFS():
    plt.ion()
    predecessor = {}
    path_cost = 0

    frontier = [start_node]
    expanded = []

    while frontier:
        # Pop from top of stack (LIFO = DFS behaviour)
        current = frontier.pop()

        if current in expanded:
            continue
        expanded.append(current)

        # Update node colours for visualisation
        node_list = list(G.nodes())
        for n in frontier:
            idx = node_list.index(n)
            node_colors[idx] = "grey"       # in frontier
        for n in expanded:
            idx = node_list.index(n)
            if n in goals:
                node_colors[idx] = "orange" # goal found
            else:
                node_colors[idx] = "red"    # expanded
        show_plot()

        # Goal check
        if current in goals:
            nodes_created = len(frontier) + len(expanded)


            # Reconstruct path by backtracking through predecessor
            path = []
            node = current
            while node != start_node:
                path.append(node)
                node = predecessor[node]
            path.append(start_node)
            path.reverse()

            path_str = " -> ".join(path)

            # Calculate path cost
            node = current
            while node != start_node:
                parent = predecessor[node]
                path_cost += int(G[parent][node]['weight'])
                node = parent

            print(f"Starting Node: {start_node}")
            print(f"Destination Node: {current}")
            print(f"Number of nodes created: {nodes_created}")
            print(f"Path: {path_str}")
            print(f"Path Cost: {path_cost}")

            animated_path = []
            animated_edges = []

            for i in range(len(path)):

                animated_path.append(path[i])

                if i > 0:
                    animated_edges.append((path[i-1], path[i]))

                temp_colors = []

                edge_set = set(animated_edges)

                edge_colors = [
                    "green" if e in edge_set else "black"
                    for e in G.edges()
                ]

                for n in G.nodes():

                    if n == path[-1]:

                        if n in animated_path:
                            temp_colors.append("green")
                        else:
                            temp_colors.append("orange")

                    elif n in animated_path:
                        temp_colors.append("green")

                    elif n in expanded:
                        temp_colors.append("red")

                    else:
                        temp_colors.append("gray")

                edge_colors = []

                for edge in G.edges():

                    if edge in animated_edges:
                        edge_colors.append("green")
                    else:
                        edge_colors.append("black")

                plt.clf()

                # 1. draw nodes
                nx.draw_networkx_nodes(G, pos, node_color=temp_colors)
                

                # 2. draw ALL edges (background layer)
                nx.draw_networkx_edges(
                    G,
                    pos,
                    width=2
                )

                # 3. draw ONLY animated edges (foreground layer)
                nx.draw_networkx_edges(
                    G,
                    pos,
                    edgelist=list(edge_set),
                    edge_color="green",
                    width=4
                )

                # 4. labels
                nx.draw_networkx_labels(G, pos)
                nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))

                plt.pause(0.5)
                plt.text(
            0.05, 1.12,
            f"Path: {path_str}",
            transform=plt.gca().transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(facecolor='white')
            )   


            plt.ioff()
            plt.show()  
                                                                                  
                

            return

        for neighbor in sorted(G.neighbors(current), reverse=True):
            if neighbor not in expanded and neighbor not in frontier:
                frontier.append(neighbor)
                predecessor[neighbor] = current

    print("No solution found.")
    # return

# A* Search

def A_StarSearch():
    #since a star search has 2 goals, then i added another green
    node_list = list(G.nodes())

    for goal_node in goals:
        idx = node_list.index(goal_node)
        node_colors[idx] = "green"


    predecessor = {} 
    path_cost = 0
    plt.ion() 

    for node in pos:
        x1, y1 = pos[node]
        min_dist = float('inf')
        for g in goals:
            x2, y2 = pos[g]
            dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
            if dist < min_dist:
                min_dist = dist
        G.nodes[node]["heuristic"] = min_dist

    frontier = [(G.nodes[start_node]["heuristic"], start_node)]
    expanded = []
    g_cost = {start_node: 0}

    while frontier:
        frontier.sort(key=lambda x: x[0])
        f_current, current = frontier.pop(0)

        if current in expanded:
            continue
        expanded.append(current)

        node_list = list(G.nodes())

        for _, n in frontier:
            idx = node_list.index(n)
            node_colors[idx] = "grey"

        for n in expanded:
            idx = node_list.index(n)
            if n in goals:
                node_colors[idx] = "orange"
            else:
                node_colors[idx] = "red"

        show_plot()

        if current in goals:
            
            nodes_created = len(frontier) + len (expanded)

            path = []
            node = current
            while node != start_node:
                path.append(node)
                node = predecessor[node]
            path.append(start_node)
            path.reverse()

            path_str = '-> '.join(path)

            node= current
            while node != start_node:
                parent = predecessor[node]
                path_cost += int(G[parent][node]['weight'])
                node = parent

            print(f"> Starting Node: {start_node}")
            print(f"> Destination Node: {current}")
            print(f"> Number of nodes created: {nodes_created}")
            print(f"> pATH: {path_str}")
            print(f"> Path Cost: {path_cost}")

            animated_path = []
            animated_edges = []

            for i in range(len(path)):

                animated_path.append(path[i])

                if i > 0:
                    animated_edges.append((path[i-1], path[i]))

                temp_colors = []

                edge_set = set(animated_edges)

                edge_colors = [
                    "green" if e in edge_set else "black"
                    for e in G.edges()
                ]

                for n in G.nodes():

                    if n == path[-1]:

                        if n in animated_path:
                            temp_colors.append("green")
                        else:
                            temp_colors.append("orange")

                    elif n in animated_path:
                        temp_colors.append("green")

                    elif n in expanded:
                        temp_colors.append("red")

                    else:
                        temp_colors.append("gray")

                edge_colors = []

                for edge in G.edges():

                    if edge in animated_edges:
                        edge_colors.append("green")
                    else:
                        edge_colors.append("black")

                plt.clf()

                # 1. draw nodes
                nx.draw_networkx_nodes(G, pos, node_color=temp_colors)
                

                # 2. draw ALL edges (background layer)
                nx.draw_networkx_edges(
                    G,
                    pos,
                    width=2
                )

                # 3. draw ONLY animated edges (foreground layer)
                nx.draw_networkx_edges(
                    G,
                    pos,
                    edgelist=list(edge_set),
                    edge_color="green",
                    width=4
                )

                # 4. labels
                nx.draw_networkx_labels(G, pos)
                nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))

                plt.pause(0.5)
                plt.text(
            0.05, 1.12,
            f"Path: {path_str}",
            transform=plt.gca().transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(facecolor='white')
            )   


            plt.ioff()
            plt.show()  
                                                                                  
                

            return

        for neighbor in sorted (G.neighbors(current)):
            if neighbor not in expanded:
                new_g = g_cost[current] + int(G[current][neighbor]['weight'])
                if neighbor not in g_cost or new_g < g_cost[neighbor]:
                    g_cost[neighbor] = new_g
                    predecessor[neighbor] = current
                    h = G.nodes[neighbor]["heuristic"]
                    f = new_g + h
                    frontier.append((f, neighbor))

    print("No solution found")
    # return

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
            
            nodes_created = len(frontier) + len(expanded) 


           

            path = []
            node = goal


            #Start from the goal, and keep moving backwards using parent links until reach the start
            while node != start_node: # when node not == start node, loop (we currently at goal node)
                path.append(node)  #add the node to the path
                node = predecessor[node] #this node came from where? C? make node equal C, C node came from where? B.....
            path.append(start_node)
            path.reverse()

            path_str = " -> ".join(path)

            node = goal     #re-initialize because it resets and can backtrack again
            # adding path cost together
            while node != start_node:
                parent = predecessor[node]
                path_cost = path_cost + int(G[parent][node]['weight'])
                node = parent


            print("FOUND")
            print(f"Starting Node:{start_node}")
            print(f"Destination Node: {goal}")
            print(f"Number of nodes created: {nodes_created}") 
            print(f"Path: {path_str}") 
            print(f"Path Cost: {path_cost}") 

            animated_path = []
            animated_edges = []

            for i in range(len(path)):

                animated_path.append(path[i])

                if i > 0:
                    animated_edges.append((path[i-1], path[i]))

                temp_colors = []

                edge_set = set(animated_edges)

                edge_colors = [
                    "green" if e in edge_set else "black"
                    for e in G.edges()
                ]

                for n in G.nodes():

                    if n == path[-1]:

                        if n in animated_path:
                            temp_colors.append("green")
                        else:
                            temp_colors.append("orange")

                    elif n in animated_path:
                        temp_colors.append("green")

                    elif n in expanded:
                        temp_colors.append("red")

                    else:
                        temp_colors.append("gray")

                edge_colors = []

                for edge in G.edges():

                    if edge in animated_edges:
                        edge_colors.append("green")
                    else:
                        edge_colors.append("black")

                plt.clf()

                # 1. draw nodes
                nx.draw_networkx_nodes(G, pos, node_color=temp_colors)
                

                # 2. draw ALL edges (background layer)
                nx.draw_networkx_edges(
                    G,
                    pos,
                    width=2
                )

                # 3. draw ONLY animated edges (foreground layer)
                nx.draw_networkx_edges(
                    G,
                    pos,
                    edgelist=list(edge_set),
                    edge_color="green",
                    width=4
                )

                # 4. labels
                nx.draw_networkx_labels(G, pos)
                nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))

                plt.pause(0.5)
                plt.text(
            0.05, 1.12,
            f"Path: {path_str}",
            transform=plt.gca().transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(facecolor='white')
            )   


            plt.ioff()
            plt.show()  
                                                                                  
                

            return
            

        # expand neighbors
        for n in G.neighbors(current):
            if n not in expanded and n not in frontier:
                frontier.append(n) 
                predecessor[n] = current 

    print("No solution found")
    return


#This is for IDDFS
def depth_limited_search(node, depth_limit, visited_order, visited, counter, predecessor):

    if depth_limit < 0:
        return None

    visited.add(node)
    visited_order.append(node)

    counter.add(node) 

    if node == goal:
        return goal

    if depth_limit == 0:
        return None

    for child in G.neighbors(node):

        if child not in visited:
            predecessor[child] = node

            result = depth_limited_search(
                child,
                depth_limit - 1,
                visited_order,
                visited,
                counter,
                predecessor
            )

            if result == goal:
                return goal

    return None

def IDDFS():
    
    for limit in range(10):
        predecessor = {}


        visited_order = []
        visited = set()
        nodes_created_set = set()

        # fresh colors for EACH iteration so doesnt corrupt our global color
        local_colors = get_fresh_colors()

        result = depth_limited_search(
            start_node,
            limit,
            visited_order,
            visited,
            nodes_created_set,
            predecessor
        )
        nodes_created = len(nodes_created_set)

        #visualize visited nodes for THIS iteration only
        node_list = list(G.nodes())

        

        for n in visited_order:
            idx = node_list.index(n)
            local_colors[idx] = "red"

        print(f"Depth Limit: {limit}")
        print("Visited:", visited_order)

        # draw using local colors (IMPORTANT)
        plt.clf()
        nx.draw(G, pos, with_labels=True, node_color=local_colors)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
        plt.pause(1)

        

        if result == goal:
            path = []
            node = goal

            while node != start_node:
                path.append(node)
                node = predecessor[node]

            path.append(start_node)
            path.reverse()

            path_str = " -> ".join(path)

            path_cost = 0

            for i in range(len(path) - 1):  
                u = path[i]
                v = path[i + 1]
                path_cost += int(G[u][v]['weight'])                                                                                                       

            print("FOUND")
            print(f"Starting Node:{start_node}")
            print(f"Destination Node: {goal}")
            print(f"Number of nodes created: {nodes_created}") 
            print(f"Path: {path_str}") 
            print(f"Path Cost: {path_cost}") 
            animated_path = []
            animated_edges = []

            for i in range(len(path)):

                animated_path.append(path[i])

                if i > 0:
                    animated_edges.append((path[i-1], path[i]))

                temp_colors = []

                edge_set = set(animated_edges)

                edge_colors = [
                    "green" if e in edge_set else "black"
                    for e in G.edges()
                ]

                for n in G.nodes():

                    if n == path[-1]:

                        if n in animated_path:
                            temp_colors.append("green")
                        else:
                            temp_colors.append("orange")

                    elif n in animated_path:
                        temp_colors.append("green")

                    elif n in visited:
                        temp_colors.append("red")

                    else:
                        temp_colors.append("gray")

                edge_colors = []

                for edge in G.edges():

                    if edge in animated_edges:
                        edge_colors.append("green")
                    else:
                        edge_colors.append("black")

                plt.clf()

                # 1. draw nodes
                nx.draw_networkx_nodes(G, pos, node_color=temp_colors)
                

                # 2. draw ALL edges (background layer)
                nx.draw_networkx_edges(
                    G,
                    pos,
                    width=2
                )

                # 3. draw ONLY animated edges (foreground layer)
                nx.draw_networkx_edges(
                    G,
                    pos,
                    edgelist=list(edge_set),
                    edge_color="green",
                    width=4
                )

                # 4. labels
                nx.draw_networkx_labels(G, pos)
                nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))

                plt.pause(0.5)
                plt.text(
            0.05, 1.12,
            f"Path: {path_str}",
            transform=plt.gca().transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(facecolor='white')
            )   


            plt.ioff()
            plt.show()  
            
            return
        
    print("Goal not found")
    return

    #IDA*

def IDAS():
    node_list = list(G.nodes())
    for goal_node in goals:
        idx = node_list.index(goal_node)
        node_colors[idx] = "green"

    # Calculate the heuristic for all nodes
    for node in pos:
        x1, y1 = pos[node]
        min_dist = float('inf')
        for g in goals:
            x2, y2 = pos[g]
            dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
            if dist < min_dist:
                min_dist = dist
        G.nodes[node]["heuristic"] = min_dist

    def search(path, g_cost, threshold):
        current = path[-1]
        f_cost = g_cost + G.nodes[current]["heuristic"]

        if f_cost > threshold:
            return f_cost, None # return the f_cost as the new threshold for the next iteration
        
        if current in goals:
            return -1, path # return -1 to indicate goal found, along with the path
        
        minimum = float('inf')

        for neighbor in sorted(G.neighbors(current)):
            if neighbor not in path:
                cost = int(G[current][neighbor]['weight'])
                path.append(neighbor)
                
                temp_colors = get_fresh_colors()
                node_list = list(G.nodes())

                for n in path:
                    idx = node_list.index(n)
                    temp_colors[idx] = "red"

                plt.clf()

                nx.draw(G, pos, with_labels=True, node_color=temp_colors)

                edge_labels = nx.get_edge_attributes(G, 'weight')
                nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

                plt.pause(0.2)

                result, found_path = search(path, g_cost + cost, threshold)

                if found_path is not None:
                    return -1, found_path
                
                if result < minimum:
                    minimum = result

                path.pop()
            
        return minimum, None
    
    plt.ion()
    threshold = G.nodes[start_node]["heuristic"]
    path = [start_node]
    nodes_created = 1

    while True:
        result, found_path = search(path, 0, threshold)

        if found_path is not None:
            plt.ioff()

            path_cost = 0 # calculates the path cost of the path that is found
            for i in range(len(found_path) - 1):
                path_cost += int(G[found_path[i]][found_path[i+1]]['weight'])

            nodes_created = len(found_path) 
            path_str = " -> ".join(found_path)

            print(f"> Starting Node: {start_node}")
            print(f"> Destination Node: {found_path[-1]}")
            print(f"> Number of nodes created: {nodes_created}")
            print(f"> Path: {path_str}")
            print(f"> Path Cost: {path_cost}")
            animated_path = []
            animated_edges = []

            for i in range(len(found_path)):

                animated_path.append(found_path[i])

                if i > 0:
                    animated_edges.append((found_path[i-1], found_path[i]))

                temp_colors = []

                edge_set = set(animated_edges)

                edge_colors = [
                    "green" if e in edge_set else "black"
                    for e in G.edges()
                ]

                for n in G.nodes():

                    if n == found_path[-1]:

                        if n in animated_path:
                            temp_colors.append("green")
                        else:
                            temp_colors.append("orange")

                    elif n in animated_path:
                        temp_colors.append("green")

                    else:
                        temp_colors.append("gray")

                edge_colors = []

                for edge in G.edges():

                    if edge in animated_edges:
                        edge_colors.append("green")
                    else:
                        edge_colors.append("black")

                plt.clf()

                # 1. draw nodes
                nx.draw_networkx_nodes(G, pos, node_color=temp_colors)
                

                # 2. draw ALL edges (background layer)
                nx.draw_networkx_edges(
                    G,
                    pos,
                    width=2
                )

                # 3. draw ONLY animated edges (foreground layer)
                nx.draw_networkx_edges(
                    G,
                    pos,
                    edgelist=list(edge_set),
                    edge_color="green",
                    width=4
                )

                # 4. labels
                nx.draw_networkx_labels(G, pos)
                nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))

                plt.pause(0.5)
                plt.text(
            0.05, 1.12,
            f"Path: {path_str}",
            transform=plt.gca().transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(facecolor='white')
            )   
                
            plt.ioff()
            plt.show()  
            return
        
        if result == float('inf'):
            print("No solution found")
            plt.ioff()
            plt.close('all')
            return

        if threshold == result:
            print("No solution found")
            plt.ioff()
            plt.close('all')
            return
        
        threshold = result    
        
#This function is used to draw iterative graphs rather than using the global variable to draw
def get_fresh_colors():
    colors = []
    for node in G.nodes():
          


        if node == start_node:
            colors.append("red")
        elif node in goals:
            colors.append("green")
        else:
            colors.append("blue")
    return colors


#Show drawing
def show_plot():
    plt.clf()  # clear old frame   
    nx.draw(G, pos, with_labels=True, node_color=node_colors)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels) # adding labels
    
    plt.pause(0.5)  # pause so we can SEE updates


# Added "cencel" key
def on_key(event):
    if event.key == 'c':   # press q to quit
        print("Exiting...")
        plt.close('all')
        raise SystemExit
    
fig = plt.gcf()
fig.canvas.mpl_connect('key_press_event', on_key)




# CLI execution
if method_name == "show":
    show_plot()
    plt.ioff() 
    plt.show() 

elif method_name == "BFS":
    BFS()
    

elif method_name == "DFS":
    DFS()
    
elif method_name == "GreedyBFS":
    GreedyBFS()
    
elif method_name == "AS":
    A_StarSearch()
elif method_name == "IDDFS":
    IDDFS()
elif method_name == "IDAS":
    IDAS()


