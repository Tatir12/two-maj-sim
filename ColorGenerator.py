import random
import numpy as np
import random
import networkx as nx

def asign_random_color(G,p):
    colors=['red', 'blue']
    values=np.random.choice(2, len(G.nodes()), p=[p,1-p])
    return [colors[i] for i in values]
# G1, Color_map = create_mid_connected_graph_with_spillover(10,9,1)

def recolor_half_half(G,m,d,k):
    color_map=['blue' for i in range(0,len(G.nodes))]
    index=np.random.choice(int(d*m/(2*k)), size=int(d*m/(4*k)), replace=False)
    for i in index:
        color_map[i]='red'
    index=np.random.choice(int(d*m/(2*k)), size=int(d*m/(4*k)), replace=False)
    for i in index:
        color_map[i+int(d*m/(2*k))]='red'
    index=np.random.choice(m, size=int(m/2), replace=False)
    for i in index:
        color_map[i+2*int(d*m/(2*k))]='red'
    return color_map

#with j=0, the initial color we had before
def recolor_j(G,m,d,k,j):
    color_map=[]
    for i in range(0,int(d*m/(2*k))):
        color_map.append('blue')
    for i in range(int(d*m/(2*k)),int(d*m/(2*k))+j):
        color_map.append('blue')
    for i in range(int(d*m/(2*k))+j,2*int(d*m/(2*k))):
        color_map.append('red')
    for i in range(2*int(d*m/(2*k)),len(G.nodes)):
        color_map.append('blue')
    return color_map
