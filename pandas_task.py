# -*- coding: utf-8 -*-
"""
Deepak_Task.ipynb

"""

import pandas as pd

data_1 = pd.read_excel('./dataset.xlsx')

data_1 = data_1.dropna()

"""# Task_1"""

Acceptence = data_1['Accepted Compound ID']
index_PC = Acceptence.str.endswith('PC')
index_LPC = Acceptence.str.endswith('LPC')
index_plasmalogen = Acceptence.str.endswith('plasmalogen')

"""#### LPC Dataframe"""

data_LPC = data_1.loc[index_LPC]
data_LPC.to_excel('data_LPC.xlsx')

"""### Dataframe PC"""

data_PC = data_1.loc[index_PC]
data_PC.head()
data_PC.to_excel('data_PC.xlsx')

"""# Data Frame"""

data_plasmogen = data_1.loc[index_plasmalogen]
data_plasmogen.head()
data_plasmogen.to_excel('data_plasmogen.xlsx')

"""# Task_2"""

data_1['Retention Time Roundoff (in mins)']  = data_1.round({'Retention time (min)':0})['Retention time (min)']

data_1['Retention Time Roundoff (in mins)'].value_counts()

"""# Task_3"""

task_3_data = data_1.drop(['m/z', 'Retention time (min)', 'Accepted Compound ID',], axis=1)

mean_dataframe= task_3_data.groupby(task_3_data['Retention Time Roundoff (in mins)'])
mean_dataframe = mean_dataframe.mean()
mean_dataframe = mean_dataframe.reset_index()

mean_dataframe.to_excel('mean.xlsx')

"""
END
"""