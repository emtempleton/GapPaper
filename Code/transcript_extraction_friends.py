# This script takes timing information from the transcripts
# and uses it to generate gap length information for each turn.

# Then, it stores the average gap length information for
# each conversation.

# We aren't releasing the transcripts from this study, but
# an example of how our transcripts were formatted can be
# found in Supplementary Materials.

import glob
import os
import re
import pandas as pd
import numpy as np
from scipy.stats import linregress
from scipy.stats import kurtosis, skew

base_dir = os.path.dirname(os.getcwd())


def compute_millisecond_difference(first_turn_end, second_turn_start, second_turn_end):
    """Convert the timestamps in the transcript to start time and end time
    in milliseconds. Store millisecond difference.

    """  
    if first_turn_end.count(':') == 1:
        turn_end_min = int(first_turn_end.split(':')[0])
        turn_end_sec = int(first_turn_end.split(':')[1].split('.')[0])
        turn_end_msec = int(first_turn_end.split(':')[1].split('.')[1])
    if first_turn_end.count(':') == 2:
        turn_end_min = int(first_turn_end.split(':')[1])
        turn_end_sec = int(first_turn_end.split(':')[2].split('.')[0])
        turn_end_msec = int(first_turn_end.split(':')[2].split('.')[1])
        
    turn_start_min = int(second_turn_start.split(':')[0])
    turn_start_sec = int(second_turn_start.split(':')[1].split('.')[0])
    turn_start_msec = int(second_turn_start.split(':')[1].split('.')[1])
    
    if second_turn_end.count(':') == 1:
        second_turn_end_min = int(second_turn_end.split(':')[0])
        second_turn_end_sec = int(second_turn_end.split(':')[1].split('.')[0])
        second_turn_end_msec = int(second_turn_end.split(':')[1].split('.')[1])
    if second_turn_end.count(':') == 2:
        second_turn_end_min = int(second_turn_end.split(':')[1])
        second_turn_end_sec = int(second_turn_end.split(':')[2].split('.')[0])
        second_turn_end_msec = int(second_turn_end.split(':')[2].split('.')[1])
        
    millisecond_difference = 0
    if turn_start_min != turn_end_min:
        millisecond_difference += ((turn_start_min - turn_end_min) * 60000)
        millisecond_difference += ((turn_start_sec - turn_end_sec) * 1000)
        millisecond_difference += (turn_start_msec - turn_end_msec)
        
    else:
        if turn_start_sec != turn_end_sec:
            millisecond_difference += ((turn_start_sec - turn_end_sec) * 1000)
            millisecond_difference += (turn_start_msec - turn_end_msec)
        else:
            millisecond_difference += (turn_start_msec - turn_end_msec)

    start_time_in_msec = (turn_start_min * 60000) + (turn_start_sec * 1000) + turn_start_msec
    end_time_in_msec = (second_turn_end_min * 60000) + (second_turn_end_sec * 1000) + second_turn_end_msec

    
    return millisecond_difference, start_time_in_msec, end_time_in_msec


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
    key = pd.read_csv(os.path.join(base_dir, 'Data', 'subject_id_key_friends.csv'))
    video_name_1, video_name_2 = find_video(file)
    for i in range(len((key))):
        if (key.at[i,'video_name'] == video_name_1) | (key.at[i,'video_name'] == video_name_2):
            subID_S1 = key.at[i,'S1']
            subID_S2 = key.at[i,'S2']
            return subID_S1, subID_S2


def preprocess_documents(document):
    """Very simple preprocessing to remove the words that are
    in brackets (and the brakets themselves).

    """
    s = re.sub("[\(\[].*?[\)\]]", "", document)
    s = re.sub(r'\s([?.!"](?:\s|$))', r'\1', s)
    
    return s


# Create dataframe for each convo
# that has info for every turn
# Stored in 'transcripts_turns' directory

output_dir = os.path.join(base_dir, 'Analyses', 'turn_taking', 'friends')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

flist = glob.glob(os.path.join(base_dir, 'Data', 'transcripts', 'friend_transcripts', '*.txt')) 
for transcript in flist:
    
    name = transcript.split('/subs')[-1].split('.txt')[0] 

    transcript_text = [line.rstrip('\n') for line in open(transcript)]

    timestamp_df = pd.DataFrame()
    timestamp_df = timestamp_df.fillna(0)

    counter = 0
    turn_end_previous = '00:00.000'

    for turn in transcript_text:

        if 'END' in turn:

            turn_start = ':'.join(turn.split()[1].split(':')[1:])
            turn_end = turn.split()[-2]
            turn_latency, start_time_in_msec, end_time_in_msec = compute_millisecond_difference(turn_end_previous, turn_start, turn_end)
            doc = preprocess_documents(' '.join(turn.split()[2:-3]))

            timestamp_df.at[counter, 'turn_num'] = str(counter)
            timestamp_df.at[counter, 'speaker'] = turn.split()[0].split(':')[0]
            timestamp_df.at[counter, 'turn_start'] = turn_start
            timestamp_df.at[counter, 'turn_end'] = turn_end
            timestamp_df.at[counter, 'gap_length'] = int(turn_latency)
            timestamp_df.at[counter, 'turn_start_msec'] = int(start_time_in_msec)
            timestamp_df.at[counter, 'turn_end_msec'] = int(end_time_in_msec)
            timestamp_df.at[counter, 'number_of_words'] = len(doc.split())

            counter += 1
            turn_end_previous = turn_end
            
    
    timestamp_df.to_csv(os.path.join(output_dir, '{0}.csv').format(name), index=False)

# for each convo, store the mean latency.

summary = pd.DataFrame()
summary = summary.fillna(0)

counter = 0

flist = glob.glob(os.path.join(output_dir, '*.csv'))

for file in flist:
    
    data = pd.read_csv(file)
    
    sub_1 = file.split('/')[-1].split('_')[0]
    sub_2 = file.split('_')[-1].split('.csv')[0]

    S1 = data.loc[data['speaker'] == 'S1'].reset_index()
    S2 = data.loc[data['speaker'] == 'S2'].reset_index()

    subID_S1, subID_S2 = assign_identiy(file)
    
    summary.at[counter, 'subID'] = str(subID_S1)
    summary.at[counter, 'partnerID'] = str(subID_S2)
    summary.at[counter, 'num_turns_convo'] = len(data)
    summary.at[counter, 'num_turns_speaker'] = len(S1)
    summary.at[counter, 'mean_gap_convo'] = np.mean(data['gap_length'])
    summary.at[counter, 'median_gap_convo'] = np.median(data['gap_length'])
    summary.at[counter, 'mean_gap_speaker'] = np.mean(S1['gap_length'])
    summary.at[counter, 'median_gap_speaker'] = np.median(S1['gap_length'])
    
    counter = counter + 1
    
    summary.at[counter, 'subID'] = str(subID_S2)
    summary.at[counter, 'partnerID'] = str(subID_S1)
    summary.at[counter, 'num_turns_convo'] = len(data)
    summary.at[counter, 'num_turns_speaker'] = len(S2)
    summary.at[counter, 'mean_gap_convo'] = np.mean(data['gap_length'])
    summary.at[counter, 'median_gap_convo'] = np.median(data['gap_length'])
    summary.at[counter, 'mean_gap_speaker'] = np.mean(S2['gap_length'])
    summary.at[counter, 'median_gap_speaker'] = np.median(S2['gap_length'])

    
    counter = counter + 1
    
summary.to_csv(os.path.join(base_dir, 'Analyses',
                        'turn_taking_friends.csv'),
                        encoding='utf-8', index=False)   

