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
goals = []
pos = {}      # coordinates
graph = {}      # adjacency list

# STEP 3: Parse file
for line in cleaned_lines:

    # Goals
    if ";" in line:
        goals = line.split(";")

    # Coordinates
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

    # Start node
    else:
        start_node = line

# STEP 4: Debug / Print
def print_data():
    print("Start Node:", start_node)
    print("Goals:", goals)
    print("Coordinates:", pos)
  


def show_plot():
    nx.draw_networkx(G, pos)
    plt.show()

# CLI execution
if method_name == "print":
    print_data()
elif method_name == "show":
    show_plot()

