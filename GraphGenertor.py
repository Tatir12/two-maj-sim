import networkx as nx
import random
import numpy as np
import pickle as pk
import os
import matplotlib.pyplot as plt


# m(number of nodes in the middle), d(degree), k (how many edges are in between the side and center
# method = 'e' for expander, 'r' for regular
def create_bridge_graph_without_spillover(m,pd,k,method):
    # let n be the number of nodes in one expander graph and m the number of nodes in the center and pd= d/2.
    # then the ratio of edges forces n * k = m*pd
    # For nx.random_regular_expander_graph the degree must be even!
    # Therefore k must be even, therefore we redefine k = 2*k
    k2 = 2*k
    d=2*pd
    n = int(pd*m/k2)

    #Creating the first connected component -> #nodes=pd*m/(2*k)
    if method=='e':
        G1= create_random_regular_expander_graph(n,d-2*k)
        #G1=nx.random_regular_expander_graph(n,d-2*k, max_tries=2**22-1)
    else:
        G1=nx.random_regular_graph(d-2*k,n)

    #Creating the second connected component
    if method=='e':
        G2= create_random_regular_expander_graph(n,d-2*k)
        #G2=nx.random_regular_expander_graph(n,d-2*k, max_tries=2**22-1)
    else:
        G2=nx.random_regular_graph(d-2*k,n)
    relabel_dict = {node: int(node)+len(G1.nodes) for node in G2.nodes}
    G2 = nx.relabel_nodes(G2, relabel_dict)

    #Creating the bigger graph
    G=nx.compose(G1, G2)

    #Creating the middle nodes
    for i in range(0,m):
        G3=nx.Graph()
        G3.add_node(len(G.nodes))
        for j in range(0,pd):
            G3.add_edge(int(j+i*pd/2) % int(pd*m/(2*k)), len(G.nodes))
            G3.add_edge(int(j+i*pd/2) % int(pd*m/(2*k))+len(G1.nodes) , len(G.nodes))
        G=nx.compose(G, G3)
    return G

# n = number of nodes in left and right component
# d = internal degree of left and right component
# k = degree of each node outside component
def create_bridge_graph_with_spillover(n,d,k):

    assert (d+k) % 2 == 0
    # maps nodes to colors
    color_map=[]
    # number of bridge nodes
    m = int(2*n*k/(d+k))
    # number of residual edges
    r = n*k - int(m*(d+k)/2)
    print("Graph Parameters: n = " +str(n)+ ", node_degree = " +str(d+k)+ ", m= " +str(m)+ ", residual edges = "+ str(r))

    G1 = nx.random_regular_graph(d,n)

    G2=nx.random_regular_graph(d,n)
    relabel_dict = {node: int(node)+len(G1.nodes) for node in G2.nodes}
    G2 = nx.relabel_nodes(G2, relabel_dict)

    for node in G1.nodes():
        color_map.append('blue')

    for node in G2.nodes():
        color_map.append('red')

    #Creating the bigger graph
    G=nx.compose(G1, G2)

    # Add bridge Nodes
    for i in range(0,m):
        G3=nx.Graph()
        G3.add_node(len(G.nodes))
        color_map.append('blue')

    G=nx.compose(G, G3)

    # Add edges to bridge nodes and spillover edges

    couter_bridge_node_edges = 0
    counter_bridge_node = 2*n
    for l in range(0,k):
        a = np.random.permutation(n)
        b = np.random.permutation(n)

        for i in range(0,n):
            if counter_bridge_node < 2*n+m:
                G3.add_edge(a[i], counter_bridge_node)
                G3.add_edge(b[i]+n, counter_bridge_node)
                couter_bridge_node_edges = (couter_bridge_node_edges +2) % (d+k)
                if couter_bridge_node_edges == 0:
                    counter_bridge_node+=1
            else:
                G3.add_edge(a[i], b[i]+n)

        G=nx.compose(G, G3)

    print_graph_parameters(G,G1.nodes)

    return G, color_map


# n = number of nodes in left and right component
# d = internal degree of left and right component
# k = degree of each node outside component
def create_directly_connected_random_regular_graph(n,d,k):
    color_map=[]

    G1 = nx.random_regular_graph(d,n)
    for node in G1.nodes():
        color_map.append('blue')
    G2 = nx.random_regular_graph(d,n)
    relabel_dict = {node: int(node)+len(G1.nodes) for node in G2.nodes}
    G2 = nx.relabel_nodes(G2, relabel_dict)
    for node in G2.nodes():
        color_map.append('red')

    #Creating the bigger graph
    G=nx.compose(G1, G2)

    for l in range(0,k):
        a = np.random.permutation(n)
        b = np.random.permutation(n)

        G3=nx.Graph()
        for i in range(0,n):
            G3.add_edge(a[i], b[i]+n)

        G=nx.compose(G, G3)

    print("Graph Parameters: n = " +str(n)+ ", node_degree = " +str(d+k))
    print_graph_parameters(G,G1.nodes)
    return G, color_map

def create_random_regular_expander_graph(n,d):
    print("start creating random_regular_expander_graph n="+str(n)+" d="+str(d))
    folder_path = 'graphs/regularExpander'
    file_name = ""+str(n)+"_"+str(d) + ".txt"
    file_path = os.path.join(folder_path, file_name)

    folder_path2 = 'graphs/regular/'

    # Sicherstellen, dass der Ordner existiert
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Sicherstellen, dass der Ordner existiert
    if not os.path.exists(folder_path2):
        os.makedirs(folder_path2)

    # Überprüfen, ob die Datei existiert
    if os.path.exists(file_path):
        # Datei existiert, Daten laden
        G1 = nx.read_adjlist(file_path)
        relabel_dict = {node: int(node)for node in G1.nodes}
        G1 = nx.relabel_nodes(G1, relabel_dict)
        print("Loaded Graph")
        return G1

    print("Loadeding Graph not possible")
    G1=nx.random_regular_expander_graph(n,d, max_tries=2**22-1)
    print("created Graph, try to save")

    nx.write_adjlist(G1,file_path)
    print("Created Graph")

    return G1

def generate_and_save_graph(m,pd,k,type):

    file_name1 = "composedGraph"+ str(m)+"_"+str(pd)+"_"+str(k)+".txt"
    file_name2 = "composedGraph"+ str(m)+"_"+str(pd)+"_"+str(k)+"_colormap.txt"
    folder_name_base="graphs/"+type+"/"

    # Sicherstellen, dass der Ordner existiert
    if not os.path.exists(folder_name_base):
        os.makedirs(folder_name_base)


    if type=="bridge_graph_without_spillover":
        if not os.path.exists(folder_name_base+ "expander/"):
            os.makedirs(folder_name_base+ "expander/")
        if not os.path.exists(folder_name_base+ "regular/"):
            os.makedirs(folder_name_base+ "regular/")
        try:
            G = create_bridge_graph_without_spillover(m,pd,k, 'e')
            nx.write_adjlist(G, path=folder_name_base+ "expander/"+ file_name1)
        except nx.NetworkXError:
            G= create_bridge_graph_without_spillover(m,pd,k, 'r')
            nx.write_adjlist(G, path=folder_name_base+ "regular/"+ file_name1)
    if type=="bridge_graph_with_spillover":
        try:
            G, color_map = create_bridge_graph_with_spillover(m,pd,k)
            nx.write_adjlist(G, path=folder_name_base+ file_name1)
            with open(folder_name_base+ file_name2, "wb") as fp:
                pk.dump(color_map, fp)
        except nx.NetworkXError:
            pass
    if type=="directly_connected_random_regular_graph":
        try:
            G, color_map = create_directly_connected_random_regular_graph(m,pd,k)
            nx.write_adjlist(G, path=folder_name_base+ file_name1)
            with open(folder_name_base+ file_name2, "wb") as fp:
                pk.dump(color_map, fp)
        except nx.NetworkXError:
            pass
    return True

def save_graph_picture(G,colors,file_path):
    nx.draw(G, node_color=colors, with_labels=True)
    plt.savefig(file_path)
    plt.close()

def print_graph_parameters(G,nodes):
    print("conductance is at most " + str(nx.conductance(G,nodes)))
    print("edge expansion is at most " + str(nx.edge_expansion(G,nodes)))
    print("node expansion is at most " + str(nx.node_expansion(G,nodes)))


# print(nx.draw(G1, node_color=Color_map, with_labels=True))
# plt.savefig("test.png")
# plt.close()

# save_graph_picture(G1,Color_map,"test2.png")
