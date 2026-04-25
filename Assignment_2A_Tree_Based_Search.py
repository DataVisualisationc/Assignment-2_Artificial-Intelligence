import sys
import networkx as nx
import matplotlib.pyplot as plt

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
pos = {}                # coordinates of the nodes so that it aligns with the x,y

#not net implment (below)
nodes_created = None    
path = None
path_cost = None




# STEP 3: Parse file
for line in cleaned_lines:

    # Goals
    if ";" in line:
        goals = line.split(";")

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

# STEP 4: Search Algorithm Functions 
# print(f"Starting Node:{start_node}")
# print(f"Destination Node: {goal}")
# print(f"Number of nodes created: {nodes_created}")
# print(f"Path: {path}")
# print(f"Path Cost: {path_cost}")


#Show drawing
def show_plot():
    nx.draw(G, pos, with_labels=True)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()



# CLI execution
if method_name == "show":
    show_plot()
