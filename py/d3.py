source = ['node A','node F','node B','node B','node B','node A','node C','node Z']
target = ['node F','node B','node J','node F','node F','node M','node M','node A']
weight = [5.56, 0.5, 0.64, 0.23, 0.9,3.28,0.5,0.45]

# Import library
from d3graph import d3graph, vec2adjmat

# Convert to adjacency matrix
adjmat = vec2adjmat(source, target, weight=weight)
print(adjmat)
# target  node A  node B  node F  node J  node M  node C  node Z
# source                                                        
# node A    0.00     0.0    5.56    0.00    3.28     0.0     0.0
# node B    0.00     0.0    1.13    0.64    0.00     0.0     0.0
# node F    0.00     0.5    0.00    0.00    0.00     0.0     0.0
# node J    0.00     0.0    0.00    0.00    0.00     0.0     0.0
# node M    0.00     0.0    0.00    0.00    0.00     0.0     0.0
# node C    0.00     0.0    0.00    0.00    0.50     0.0     0.0
# node Z    0.45     0.0    0.00    0.00    0.00     0.0     0.0

# Example A: simple interactive network
out = d3graph(adjmat)

# Example B: Color nodes
out = d3graph(adjmat, node_color=adjmat.columns.values)

# Example C: include node size
node_size = [10,20,10,10,15,10,5]
out = d3graph(adjmat, node_color=adjmat.columns.values, node_size=node_size)

# Example D: include node-edge-size
out = d3graph(adjmat, node_color=adjmat.columns.values, node_size=node_size, node_size_edge=node_size[::-1], cmap='Set2')

# Example E: include node-edge color
out = d3graph(adjmat, node_color=adjmat.columns.values, node_size=node_size, node_size_edge=node_size[::-1], node_color_edge='#00FFFF')

# Example F: Change colormap
out = d3graph(adjmat, node_color=adjmat.columns.values, node_size=node_size, node_size_edge=node_size[::-1], node_color_edge='#00FFFF', cmap='Set2')

# Example H: Include directed links. Arrows are set from source -> target
out = d3graph(adjmat, node_color=adjmat.columns.values, node_size=node_size, node_size_edge=node_size[::-1], node_color_edge='#00FFFF', cmap='Set2', directed=True)