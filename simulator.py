import random
import networkx as nx
import copy
import pandas as pd
import pickle as pk
from openpyxl import Workbook
import re
import os
from ColorGenerator import *
import time

def simulate(G, cm):
    color_map= copy.deepcopy(cm)
    steps=0
    productive_steps = 0

    max_steps = 10000 + 100*len(G.nodes)**2

    # print("simulating for "+ str(1000+ len(G.nodes)**3)+ " steps")
    while(not isConsensus(color_map) and steps < max_steps):

        #Select a random node
        node=random.choice([nodes for nodes in G.nodes()])

        #Select two random neighbors of the node
        a=random.choice([neighbor for neighbor in G.neighbors(node)])
        b=random.choice([neighbor for neighbor in G.neighbors(node)])
        steps=steps+1
        #2-maj rule
        if color_map[int(a)]==color_map[int(b)]:
            color_map[int(node)]=color_map[int(a)]
            productive_steps += 1

    return G, color_map, steps, productive_steps

def isConsensus(color_map):
    return calculate_bias(color_map)==1

def calculate_bias(color_map):
    # Count the number of reds and blues
    red_count = sum(1 for color in color_map if color == 'red')

    # Calculate bias
    total_count = len(color_map)
    bias = 2*(abs(red_count - total_count / 2) / total_count)
    return bias

def calculate_conductance(G,m,d,k):
    return nx.conductance(G,list(G.nodes)[0:int(d*m/(2*k))])

def calculate_node_expansion(G,m,d,k):
    return nx.node_expansion(G,list(G.nodes)[0:int(d*m/(2*k))])

def calculate_edge_expansion(G,m,d,k):
    return nx.edge_expansion(G,list(G.nodes)[0:int(d*m/(2*k))])

def get_graph_from_file(file_name):
    return nx.read_adjlist(file_name)

def write_excel_results(df,output_file,sheet,lock):
    with lock:
        if not os.path.exists(output_file):
            df_aux=pd.DataFrame(columns=['m','d','k', 'n','total_steps', 'productive_steps', 'bias_0', 'bias_T','conductance', 'e_exoansion','n_expansion'])
            df_aux_re=pd.DataFrame(columns=['m','d','k', 'n','total_steps', 'productive_steps', 'bias_0', 'bias_T','conductance', 'e_exoansion','n_expansion','j'])
            writer = pd.ExcelWriter(output_file, engine = 'openpyxl',mode='w')
            df_aux.to_excel(writer, index=False, sheet_name = 'expander')
            df_aux.to_excel(writer, index=False, sheet_name = 'regular')
            df_aux.to_excel(writer, index=False, sheet_name = 'half')
            df_aux.to_excel(writer, index=False, sheet_name = 'random')
            df_aux_re.to_excel(writer, index=False, sheet_name = 'recolor_j')
            writer.close()
        writer = pd.ExcelWriter(output_file, engine = 'openpyxl',mode='a', if_sheet_exists='overlay')
        df.to_excel(writer, index=False, sheet_name = sheet, startrow=writer.sheets[sheet].max_row, header=None)
        writer.close()
        time.sleep(1)

def simulate_from_file_and_save(folder_path,output_file,file_name,sheet,lock):
    #Read the graph from a file
    my_graph=get_graph_from_file(folder_path +  file_name)
    m,d,k= [int(t) for t in re.findall(r'\d+',file_name)]
    #read the color map from a file
    my_color=recolor_j(my_graph,m,d,k,0)
    #Simulate and create dataframe
    my_graph, my_color_sim, steps, output=simulate(my_graph, my_color)
    df=pd.DataFrame(columns=['m','d','k', 'n','steps', 'productive_steps', 'bias_0', 'bias_T','conductance', 'e_exoansion','n_expansion'])
    df.loc[len(df.index)]=[m,d,k,len(my_graph.nodes),steps,output,calculate_bias(my_color),calculate_bias(my_color_sim),calculate_conductance(my_graph,m,d,k),calculate_edge_expansion(my_graph,m,d,k),calculate_node_expansion(my_graph,m,d,k)]
    #Save to an excel document
    write_excel_results(df,output_file,sheet,lock)
    return df

def simulate_from_file_and_save_with_given_color(folder_path,output_file,file_name,sheet,lock):
    #Read the graph from a file
    m,d,k= [int(t) for t in re.findall(r'\d+',file_name)]
    my_graph=get_graph_from_file(folder_path + file_name)
    #Simulate and create dataframe
    if sheet=='half':
        my_color=recolor_half_half(my_graph,m,d,k)
        my_graph, my_color_sim, steps, output=simulate(my_graph, my_color)
        df=pd.DataFrame(columns=['m','d','k', 'n','steps', 'productive_steps', 'bias_0', 'bias_T','conductance', 'e_exoansion','n_expansion'])
        df.loc[len(df.index)]=[m,d,k,len(my_graph.nodes),steps,output,calculate_bias(my_color),calculate_bias(my_color_sim), calculate_conductance(my_graph,m,d,k),calculate_edge_expansion(my_graph,m,d,k),calculate_node_expansion(my_graph,m,d,k)]
    if sheet=='random':
        my_color=asign_random_color(my_graph,0.5)
        my_graph, my_color_sim, steps, output=simulate(my_graph, my_color)
        df=pd.DataFrame(columns=['m','d','k', 'n','steps', 'productive_steps', 'bias_0', 'bias_T','conductance', 'e_exoansion','n_expansion'])
        df.loc[len(df.index)]=[m,d,k,len(my_graph.nodes),steps,output,calculate_bias(my_color),calculate_bias(my_color_sim), calculate_conductance(my_graph,m,d,k),calculate_edge_expansion(my_graph,m,d,k),calculate_node_expansion(my_graph,m,d,k)]
    if sheet=='recolor_j':
        j=0
        my_color=recolor_j(my_graph,m,d,k,j)
        my_graph, my_color_sim, steps, output=simulate(my_graph, my_color)
        while(calculate_bias(my_color_sim)!=1):
            j+=1
            my_color=recolor_j(my_graph,m,d,k,j)
            my_graph, my_color_sim, steps, output=simulate(my_graph, my_color)
        df=pd.DataFrame(columns=['m','d','k', 'n','steps', 'productive_steps', 'bias_0', 'bias_T' ,'conductance', 'e_exoansion','n_expansion', 'j'])
        df.loc[len(df.index)]=[m,d,k,len(my_graph.nodes),steps,output,calculate_bias(my_color),calculate_bias(my_color_sim),calculate_conductance(my_graph,m,d,k),calculate_edge_expansion(my_graph,m,d,k),calculate_node_expansion(my_graph,m,d,k),j]
    #Save to an excel document
    write_excel_results(df,output_file,sheet,lock)
    return df

def simulate_all(folder_path,output,f,sheet,lock):
    simulate_from_file_and_save_with_given_color(folder_path,output,f,'half',lock)
    simulate_from_file_and_save_with_given_color(folder_path,output,f,'random',lock)
    simulate_from_file_and_save_with_given_color(folder_path,output,f,'recolor_j',lock)
    simulate_from_file_and_save(folder_path, output,f, sheet,lock)
    return true
