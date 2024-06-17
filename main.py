from GraphGenertor import *
from simulator import *
from os import listdir
from os.path import isfile, join
import re
import multiprocessing
import concurrent.futures


def main():

    folder_path_exp='graphs/bridge_graph_without_spillover/expander/'
    folder_path_reg='graphs/bridge_graph_without_spillover/regular/'
    sorted_files_exp = sorted(listdir(folder_path_exp), key=lambda x: [int(i) for i in re.findall(r'\d+', x)])
    sorted_files_reg = sorted(listdir(folder_path_reg), key=lambda x: [int(i) for i in re.findall(r'\d+', x)])
    m = multiprocessing.Manager()
    lock = m.Lock()

    executor = concurrent.futures.ProcessPoolExecutor(10)
    futures = [executor.submit(simulate_all, folder_path_exp, 'graphs/resultsc.xlsx',f,'expander',lock) for f in sorted_files_exp] + [executor.submit(simulate_all, folder_path_reg, 'graphs/resultsc.xlsx',f,'regular',lock) for f in sorted_files_reg]
    concurrent.futures.wait(futures)
    # for f in sorted_files_exp:
    #     simulate_from_file_and_save_with_given_color(folder_path_exp,'graphs/results.xlsx',f,'half')
    #     simulate_from_file_and_save_with_given_color(folder_path_exp,'graphs/results.xlsx',f,'random')
    #     simulate_from_file_and_save_with_given_color(folder_path_exp,'graphs/results.xlsx',f,'recolor_j')
    #     simulate_from_file_and_save(folder_path_exp, 'graphs/results.xlsx',f,'expander')
    # for f in sorted_files_reg:
    #     simulate_from_file_and_save_with_given_color(folder_path_reg,'graphs/results.xlsx',f,'half')
    #     simulate_from_file_and_save_with_given_color(folder_path_reg,'graphs/results.xlsx',f,'random')
    #     simulate_from_file_and_save_with_given_color(folder_path_reg,'graphs/results.xlsx',f,'recolor_j')
    #     simulate_from_file_and_save(folder_path_reg,'graphs/results.xlsx',f,'regular')


# then the ratio of edges forces n * k = m*d
    # for i in range(0,10):
    #     m=8+12*i
    #     for j in range(0,10):
    #         d=2+12*j
    #         for l in range(0,int(d/2)):
    #             k=1+l
    #             if 2*d-2*k<int(d*m/(2*k)):
    #                 print(m,d,k)
    #                 #try:
    #                 #simulate_from_file_and_save('graphs/sim_results','/graphs/bridge_graph_without_spillover/expander/','expander')
    #                 #except:
    #                 #simulate_from_file_and_save('graphs/sim_results','/graphs/bridge_graph_without_spillover/regular/','regular')
    #                 generate_and_save_graph(m,d,k,"bridge_graph_without_spillover")
    # G1, color_map1 = create_bridge_graph_with_spillover(70,61,11) # does not converge for 70,69,17 # somtimes converges and sometimes not for 70,45,11
    # save_graph_picture(G1,color_map1,"tests/test1")
    # print("initial Bias: " + str(calculate_bias(color_map1)))
    #
    # G2, color_map2, steps, productive_steps = simulate(G1, color_map1)
    # save_graph_picture(G2,color_map2,"tests/test1_after_simulation")
    # print(generate_text_output(color_map2) + ". steps: "+str(steps)+" productive Steps: "+ str(productive_steps))
    # print("Final Bias: " + str(calculate_bias(color_map2)))
    # Add the main logic of your project here

    # G3, color_map3 = create_directly_connected_random_regular_graph(60,59,1) # does not converge for 70,69,17 # somtimes converges and sometimes not for 70,45,11
    # save_graph_picture(G3,color_map3,"tests/test1")
    # print("initial Bias: " + str(calculate_bias(color_map3)))

    # G4, color_map4, steps, productive_steps = simulate(G3, color_map3)
    # save_graph_picture(G4,color_map4,"tests/test1_after_simulation")
    # print(generate_text_output(color_map4) + ". steps: "+str(steps)+" productive Steps: "+ str(productive_steps))
    # print("Final Bias: " + str(calculate_bias(color_map4)))
    # # Add the main logic of your project here

if __name__ == "__main__":
    main()
