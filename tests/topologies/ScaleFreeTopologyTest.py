import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

from islands_desync.islands.topologies.ScaleFreeTopology import ScaleFreeTopology

# Parameters for testing
size = 1000
m0 = 5
m = 2

# Generate topology and build a NetworkX graph
topo = ScaleFreeTopology(size=size, m0=m0, m=m)
adjacency = topo.create()
G = nx.Graph()
for u, nbrs in adjacency.items():
    for v in nbrs:
        G.add_edge(u, v)

# 1. Check for self-loops
selfloops = list(nx.selfloop_edges(G))
print("Number of self-loops:", len(selfloops))

# 2. Check for isolated nodes
isolates = list(nx.isolates(G))
print("Number of isolated nodes:", len(isolates))

# 3. Degree distribution
deg_seq = [d for _, d in G.degree()]
deg_count = Counter(deg_seq)
degrees, freqs = zip(*sorted(deg_count.items()))

# Display distribution as a DataFrame
df = pd.DataFrame({"degree": degrees, "frequency": freqs})
print(df)

# 4. Plot degree distribution on log-log scale
plt.figure()
plt.loglog(degrees, freqs, marker='o')
plt.xlabel("Degree")
plt.ylabel("Frequency")
plt.title("Degree Distribution (log-log)")
plt.tight_layout()
plt.show()
