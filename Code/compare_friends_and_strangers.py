# For subjects that participated in Study 1
# and Study 2, compute the mean of their gaps across
# all of their convos in Study 1 and the mean of their
# gaps across al of their convos in Study 2.

import glob
import os
import re
import pandas as pd
import numpy as np

base_dir = os.path.dirname(os.getcwd())

stranger_data = pd.read_csv(os.path.join(base_dir, 'Analyses', 'turn_taking_strangers.csv'))
friend_data = pd.read_csv(os.path.join(base_dir,'Analyses', 'turn_taking_friends.csv'))

unique_ids = list(set(friend_data['subID']))
unique_ids_friends = [num for num in unique_ids if num < 200]

sub_list = []
friend_list_mean = []
stranger_list_mean = []
friend_list_median = []
stranger_list_median = []

for targetID in unique_ids_friends:
    friend_list_target_mean = []
    stranger_list_target_mean = []
    friend_list_target_median = []
    stranger_list_target_median = []
    for i in range(len(friend_data)):
        if (friend_data['subID'][i] == targetID):
            friend_list_target_mean.append(friend_data.at[i, 'mean_gap_convo'])
            friend_list_target_median.append(friend_data.at[i, 'median_gap_convo'])
    for i in range(len(stranger_data)):
        if (stranger_data['subID'][i] == targetID):
            stranger_list_target_mean.append(stranger_data.at[i, 'mean_gap_convo'])
            stranger_list_target_median.append(stranger_data.at[i, 'median_gap_convo'])
    friend_list_mean.append(np.mean(friend_list_target_mean))
    stranger_list_mean.append(np.mean(stranger_list_target_mean))
    friend_list_median.append(np.mean(friend_list_target_median))
    stranger_list_median.append(np.mean(stranger_list_target_median))
    sub_list.append(targetID)
    
d = {'subID':sub_list,'mean_gap_friends':friend_list_mean, 'mean_gap_strangers':stranger_list_mean,
    'median_gap_friends':friend_list_median, 'median_gap_strangers':stranger_list_median}
df = pd.DataFrame(d)

df.to_csv(os.path.join(base_dir, 'Analyses', 'friends_vs_strangers.csv'), index=False)