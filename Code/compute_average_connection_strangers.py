# compute average connection rating
# for each subject in each conversation

import pandas as pd 
import numpy as np
import os
import glob

connection = pd.DataFrame()
connection = connection.fillna(0)
counter = 0

base_dir = os.path.dirname(os.getcwd())

flist = glob.glob(os.path.join(base_dir, 'Data', 'continuous_connection_ratings', 'strangers', '*.csv'))

for file in flist:

    id_1 = file.split('/')[-1].split('_')[0]
    id_2 = file.split('_')[-1].split('.csv')[0]

    data = pd.read_csv(file)

    connection.at[counter, 'subID'] = str(id_1)
    connection.at[counter, 'partnerID'] = str(id_2)
    connection.at[counter, 'avg_connection'] = np.mean(data['Rating'])

    counter += 1

connection.to_csv(os.path.join(base_dir, 'Analyses', 'connection_strangers.csv'), encoding='utf-8', index=False)