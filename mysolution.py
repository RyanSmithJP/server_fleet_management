
import math
import numpy as np
import pandas as pd
from scipy import stats as st
from seeds import known_seeds
from utils import save_solution
from evaluation import get_actual_demand


def get_my_solution(d):
    # This is just a placeholder.
    # O = Utilisation × Lifespan × Profit
    # We have a parameter d, demand
    # Full csv print(d)
    # We have 10 lists as we have 10 seeds
    # print(d.columns) # All dataframe columns of every list
    # Here we can print each list for a given seed
    # for i in range(len(d)):
    #     print(d.iloc[i])
    # We are given either a gpu or a cpu alongside their sensitivities for low, medium, high latency
    '''SUB-TASK 1: CALCULATE U'''
    '''STEP 1: CALCULATE |I x G| AND GET PAIR VALUES'''
    # Create pairs for latency sens and generation
    latency_types = {'low': [], 'medium': [], 'high': []} 
    low_IG = []
    medium_IG = []
    high_IG = []
    total_pairs = 0
    for g in range(len(d)):
        low_IG.append((d.iloc[g]['server_generation'], d.iloc[g]['low'],d.iloc[g]['time_step']))
        medium_IG.append((d.iloc[g]['server_generation'], d.iloc[g]['medium'],d.iloc[g]['time_step']))
        high_IG.append((d.iloc[g]['server_generation'], d.iloc[g]['high'],d.iloc[g]['time_step']))
    # Expecting 2016 values but to be safe
    total_pairs = len(low_IG)+len(medium_IG)+len(high_IG)
    # print(low_IG)
    # print(total_pairs)
    # We now have 1/(|I x G|) = 1/2016

    '''STEP 2: FAILURE RATE Zfig'''
    #Dig across each timestep

    #Zig capacity can be calculated based on g id
    f_range = (0.05,0.1)
    d_i_g = 0
    mean = 0
    #need d_i_g_t + N: N is a normal distribution
    #Lets make a list for latency average across the 7 servers
    #3 lists needed, sums, counts and means
    #The dictionaries reference the lists
    low_demand_dict = {
        "CPU.S1":[],
        "CPU.S2":[],
        "CPU.S3":[],
        "CPU.S4":[],
        "GPU.S1":[],
        "GPU.S2":[],
        "GPU.S3":[]
    }
    #this will be for dig with N
    low_demand_N = {
        "CPU.S1":[],
        "CPU.S2":[],
        "CPU.S3":[],
        "CPU.S4":[],
        "GPU.S1":[],
        "GPU.S2":[],
        "GPU.S3":[]
    }
    '''ÍMPLEMENT WITH TIMESTEP NEXT!!! '''
    max_ts = 0
    #Get number of timesteps
    for i in range(len(low_IG)):
        if low_IG[i][2]> max_ts:
            max_ts = low_IG[i][2]
        
    #Across all servers
    for pair in range(len(low_IG)):
        # Get demand per server based on id
        d_i_g=low_IG[pair][1]
        server_id = low_IG[pair][0] 
        # #timestep
        # # print(low_IG[pair][0]," ",low_IG[pair][2])
        # if(len(low_demand_dict[server_id])==0):
        #     mean=d_i_g
        #     std=0
        #     N = np.random.normal(mean,std)
        #     d_i_g=d_i_g+N
        # else:
            # Have a list for each server's demand.
            # Mean, etc is calculated off this
        ''''Look here for N'''
            # mean = np.mean(low_demand_dict[server_id])
            # std = np.std(low_demand_dict[server_id])
            # N = np.random.normal(mean,std)
            # d_i_g = low_demand_dict[server_id][-1][0]+N #access only demand
        time_step = low_IG[pair][2]
        low_demand_dict[server_id].append((d_i_g,time_step))
        # #Mean = sum/count of latencies per server
        # #updating dictionary reference
        # low_counts_dict[server_id] = low_counts_dict[server_id] +1
        # my_sum = low_sums_dict[server_id]
        # #calculate sum
        # my_sum = my_sum+d_i_g
        # #update dictionary
        # low_sums_dict[server_id] = my_sum
        # #calculate mean per server
        # mean_l = my_sum/low_counts_dict[server_id]
        # low_means_dict[server_id] = mean_l
        # t=low_IG[pair][2]
        #standard deviation
        # sum_xiu = sum_xiu+(d_i_g-mean_l)**2
        # deviation_l = math.sqrt(d)
        # DEBUG
        # print("Server: ", low_IG[pair][0]
        #     ,"\nLatency gen: ", d_i_g
        #     ,"\nTimestep: ", t
        #     ,"\nLow latency mean: ", low_means_dict[server_id])
    key_index = 0
    d_i_g = 0
    for server_id, data in low_demand_dict.items():
        if not data:
            continue
        '''IMPORTANT'''
        first_timestep = 1
        last_timestep = 168
        #pad data
        final_demand_l = []
        timestep_dict = {timestep: value for value, timestep in data}
        # print(f"Timestep dictionary: {timestep_dict}")
        for timestep in range(first_timestep, last_timestep + 1):
            # If timestep exists, add the corresponding value; otherwise, add (0, timestep)
            if timestep in timestep_dict:
                final_demand_l.append((timestep_dict[timestep], timestep))
            else:
                # print('0 found')
                final_demand_l.append((0, timestep))

        # Update the server's data with the padded list
        low_demand_dict[server_id] = final_demand_l
        # print(low_demand_dict[server_id])
    '''Now we have a list of digs with indices'''
    ''''GET VARIANCE OF DICT'''
    d_i_g = 0
    # mean = np.mean(low_demand_dict[server_id])
    # std = np.std(low_demand_dict[server_id])
    # N = np.random.normal(mean,std)
    # d_i_g = low_demand_dict[server_id][-1][0]+N #access only demand
    for i in low_demand_dict.keys():
        # print(i,": ", low_demand_dict[i])
        arr = low_demand_dict[i]
        server_id = list(low_demand_dict.keys())[key_index]
        for j in arr:
            low_demand_N[server_id] = np.mean(low_demand_N[server_id])
            std = np.std(low_demand_N[server_id])
            N = np.random.normal(mean,std)
            print(arr[key_index])
            low_demand_N[server_id] = d_i_g
            d_i_g = low_demand_N[server_id][-1][0]+N
            key_index = key_index+1
        key_index = 0

    #

    #
    my_sum = 0
    # Return the json generated for a given demand
    print('********************')
    return [{}]


seeds = known_seeds('training')

demand = pd.read_csv('./data/demand.csv')
for seed in seeds:
    # SET THE RANDOM SEED
    np.random.seed(seed)
    # GET THE DEMAND
    actual_demand = get_actual_demand(demand)

    # CALL YOUR APPROACH HERE
    solution = get_my_solution(actual_demand)

    # SAVE YOUR SOLUTION
    # save_solution(solution, f'./output/{seed}.json')

