# Script to divde continuous connection ratings
# and gap length information into different sized-bins.

# Bins are based on time. Therefore, continous connection
# ratings simply get divided by number of bins (because they
# are sampled continuously across convo). However, gap length
# is binned by the number of turns that happen in that bin time
# window. The number of turns that go into each average vary from
# bin to bin and from convo to convo.

import pandas as pd 
import numpy as np
import os
import glob
import scipy
import random

base_dir = os.path.dirname(os.getcwd())

flist = glob.glob(os.path.join(base_dir, 'Analyses', 'turn_taking', 'strangers', '*.csv'))

for file in flist:
    
    binned_results = pd.DataFrame()
    binned_results = binned_results.fillna(0)
    
    data_turns = pd.read_csv(file)
    
    id_1 = file.split('/')[-1].split('_')[0]
    id_2 = file.split('_')[-1].split('.csv')[0]
    
    name = file.split('/')[-1].split('.csv')[0]

    
    data_connection_S1 = pd.read_csv(os.path.join(base_dir, 'Data', 'continuous_connection_ratings', 'strangers', '{}_{}.csv').format(id_1,id_2))
    data_connection_S2 = pd.read_csv(os.path.join(base_dir, 'Data', 'continuous_connection_ratings', 'strangers', '{}_{}.csv').format(id_2,id_1))
    
    num_bins_list = [1, 2, 3, 4, 5, 6, 10, 12,
                    15, 20, 24, 30, 40, 60, 120]
    
    for num_bins in num_bins_list:
        
        counter = 0

        # bin connection ratings
        
        bin_size = int(len(data_connection_S1) / num_bins)
        start = 0
        end = bin_size

        connection_S1_binned = []
        connection_S2_binned = []
        
        gap_length_binned_mean = []
        gap_length_binned_median = []

        num_turns = []

        for i in range(num_bins):

            connection_S1_binned.append(np.mean(data_connection_S1['Rating'][start:end]))
            connection_S2_binned.append(np.mean(data_connection_S2['Rating'][start:end]))
            start += bin_size
            end += bin_size

        # bin gap length

        bin_size = 600000 / num_bins #600000 is number of milliseconds in 10min convo
        connection_index = 0
        multiplier = 1

        for i in range(num_bins):
            
            if len(list(np.where(data_turns['turn_end_msec'] < (bin_size*multiplier))[0])) == 0:
                target_index = 0
            else:
                target_index = (list(np.where(data_turns['turn_end_msec'] < (bin_size*multiplier))[0])[-1]) + 1
            
            gap_length_binned_mean.append(np.mean(data_turns['gap_length'][connection_index:target_index]))
            gap_length_binned_median.append(np.median(data_turns['gap_length'][connection_index:target_index]))

            num_turns.append(len(data_turns.iloc[connection_index:target_index]))

            connection_index = target_index
            multiplier += 1

        for i in range(num_bins):

            binned_results.at[counter, 'subID'] = id_1
            binned_results.at[counter, 'partnerID'] = id_2
            binned_results.at[counter, 'dyad'] = id_1 + '_' + id_2
            binned_results.at[counter, 'bin_num'] = i
            binned_results.at[counter, 'gap_length_mean_{}'.format(num_bins)] = gap_length_binned_mean[i]
            binned_results.at[counter, 'gap_length_median_{}'.format(num_bins)] = gap_length_binned_median[i]

            binned_results.at[counter, 'connection_{}'.format(num_bins)] = connection_S1_binned[i]
            binned_results.at[counter, 'num_turns_{}'.format(num_bins)] = num_turns[i]

            counter = counter + 1

            binned_results.at[counter, 'subID'] = id_2
            binned_results.at[counter, 'partnerID'] = id_1
            binned_results.at[counter, 'dyad'] = id_1 + '_' + id_2
            binned_results.at[counter, 'bin_num'] = i
            binned_results.at[counter, 'gap_length_mean_{}'.format(num_bins)] = gap_length_binned_mean[i]
            binned_results.at[counter, 'gap_length_median_{}'.format(num_bins)] = gap_length_binned_median[i]
            
            binned_results.at[counter, 'connection_{}'.format(num_bins)] = connection_S2_binned[i]
            binned_results.at[counter, 'num_turns_{}'.format(num_bins)] = num_turns[i]
            
            counter = counter + 1

        output_dir = os.path.join(base_dir, 'Analyses', 'binned')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_dir = os.path.join(base_dir, 'Analyses', 'binned', 'strangers')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        binned_results.to_csv(os.path.join(output_dir,
                                    '{}.csv'.format(name)),
                                    encoding='utf-8', index=False)

# Combine individual convos into one large
# dataframe to use for analyses

binned_files = glob.glob(os.path.join(output_dir, '*.csv'))
full_df = pd.read_csv(binned_files[0])
for file in binned_files[1:]:
    full_df_2 = pd.read_csv(file)
    full_df = full_df.append(full_df_2, ignore_index=True)
    
full_df.to_csv(os.path.join(base_dir, 'Analyses',
                            'binned_connection_and_gaps_strangers.csv'), encoding='utf-8', index=False)   
