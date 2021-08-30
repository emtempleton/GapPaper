# Script to divde continuous connection ratings
# and gap length information into different sized-bins.

# Bins are based on time. Therefore, continous connection
# ratings simply get divided by number of bins (because they
# are sampled continuously across convo). However, gap length
# is binned by the number of turns that happen in that bin time
# window. The number of turns that go into each average vary from
# bin to bin and from convo to convo.

# Same as bin_connection_and_gaps_strangers.py but additionally
# computing average gap length for each speaker in each bin

import pandas as pd 
import numpy as np
import os
import glob
import scipy
import random

base_dir = os.path.dirname(os.getcwd())

def find_video(file):
    """Need video name to use key in assign_idenity function.

    """
    id1 = file.split('/')[-1].split('_')[0]
    id2 = file.split('_')[-1].split('.csv')[0]
    video_name_1 = id1 + '_' + id2
    video_name_2 = id2 + '_' + id1
    return video_name_1, video_name_2


def assign_identiy(file):
    """Use key to determine which subject ID corresponds to S1 (speaker 1)
    and which subject ID corresponds to S2 (speaker 2).

    """
    key = pd.read_csv(os.path.join(base_dir, 'Data', 'subject_id_key_strangers.csv'))
    video_name_1, video_name_2 = find_video(file)
    for i in range(len((key))):
        if (key.at[i,'video_name'] == video_name_1) | (key.at[i,'video_name'] == video_name_2):
            subID_S1 = key.at[i,'S1']
            subID_S2 = key.at[i,'S2']
            return subID_S1, subID_S2

flist = glob.glob(os.path.join(base_dir, 'Analyses', 'turn_taking', 'strangers', '*.csv'))

for file in flist:
    
    binned_results = pd.DataFrame()
    binned_results = binned_results.fillna(0)
    
    data_turns = pd.read_csv(file)
    
    name = file.split('/')[-1].split('.csv')[0]

    S1 = data_turns.loc[data_turns['speaker'] == 'S1'].reset_index()
    S2 = data_turns.loc[data_turns['speaker'] == 'S2'].reset_index()

    subID_S1, subID_S2 = assign_identiy(file)
    
    data_connection_S1 = pd.read_csv(os.path.join(base_dir, 'Data', 'continuous_connection_ratings', 'strangers', '{}_{}.csv').format(subID_S1,subID_S2))
    data_connection_S2 = pd.read_csv(os.path.join(base_dir, 'Data', 'continuous_connection_ratings', 'strangers', '{}_{}.csv').format(subID_S2,subID_S1))
    
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
        
        gap_length_binned_mean_S1 = []
        gap_length_binned_median_S1 = []
        
        gap_length_binned_mean_S2 = []
        gap_length_binned_median_S2 = []

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

        bin_size = 600000 / num_bins #600000 is number of milliseconds in 10min convo
        connection_index = 0
        multiplier = 1

        for i in range(num_bins):

            if len(list(np.where(S1['turn_end_msec'] < (bin_size*multiplier))[0])) == 0:
                target_index = 0
            else:
                target_index = (list(np.where(S1['turn_end_msec'] < (bin_size*multiplier))[0])[-1]) + 1
            
            gap_length_binned_mean_S1.append(np.mean(S1['gap_length'][connection_index:target_index]))
            gap_length_binned_median_S1.append(np.median(S1['gap_length'][connection_index:target_index]))

            connection_index = target_index
            multiplier += 1

        bin_size = 600000 / num_bins #600000 is number of milliseconds in 10min convo
        connection_index = 0
        multiplier = 1

        for i in range(num_bins):

            if len(list(np.where(S2['turn_end_msec'] < (bin_size*multiplier))[0])) == 0:
                target_index = 0
            else:
                target_index = (list(np.where(S2['turn_end_msec'] < (bin_size*multiplier))[0])[-1]) + 1
            
            gap_length_binned_mean_S2.append(np.mean(S2['gap_length'][connection_index:target_index]))
            gap_length_binned_median_S2.append(np.median(S2['gap_length'][connection_index:target_index]))

            connection_index = target_index
            multiplier += 1

        for i in range(num_bins):

            binned_results.at[counter, 'subID'] = subID_S1
            binned_results.at[counter, 'partnerID'] = subID_S2
            binned_results.at[counter, 'dyad'] = name
            binned_results.at[counter, 'bin_num'] = i
            binned_results.at[counter, 'gap_length_mean_{}'.format(num_bins)] = gap_length_binned_mean[i]
            binned_results.at[counter, 'gap_length_median_{}'.format(num_bins)] = gap_length_binned_median[i]
            binned_results.at[counter, 'gap_length_mean_speaker_{}'.format(num_bins)] = gap_length_binned_mean_S1[i]
            binned_results.at[counter, 'gap_length_median_speaker_{}'.format(num_bins)] = gap_length_binned_median_S1[i]
            binned_results.at[counter, 'gap_length_mean_partner_{}'.format(num_bins)] = gap_length_binned_mean_S2[i]
            binned_results.at[counter, 'gap_length_median_partner_{}'.format(num_bins)] = gap_length_binned_median_S2[i]

            binned_results.at[counter, 'connection_{}'.format(num_bins)] = connection_S1_binned[i]
            binned_results.at[counter, 'num_turns_{}'.format(num_bins)] = num_turns[i]

            counter = counter + 1

            binned_results.at[counter, 'subID'] = subID_S2
            binned_results.at[counter, 'partnerID'] = subID_S1
            binned_results.at[counter, 'dyad'] = name
            binned_results.at[counter, 'bin_num'] = i
            binned_results.at[counter, 'gap_length_mean_{}'.format(num_bins)] = gap_length_binned_mean[i]
            binned_results.at[counter, 'gap_length_median_{}'.format(num_bins)] = gap_length_binned_median[i]
            binned_results.at[counter, 'gap_length_mean_speaker_{}'.format(num_bins)] = gap_length_binned_mean_S2[i]
            binned_results.at[counter, 'gap_length_median_speaker_{}'.format(num_bins)] = gap_length_binned_median_S2[i]
            binned_results.at[counter, 'gap_length_mean_partner_{}'.format(num_bins)] = gap_length_binned_mean_S1[i]
            binned_results.at[counter, 'gap_length_median_partner_{}'.format(num_bins)] = gap_length_binned_median_S1[i]
            
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
                            'binned_connection_and_gaps_by_speaker_strangers.csv'), encoding='utf-8', index=False)   
