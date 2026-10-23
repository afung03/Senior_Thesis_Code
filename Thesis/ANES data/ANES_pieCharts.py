import matplotlib.pyplot as plt
import numpy as np
import random as rng
import pandas as pd

#df_1966 = pd.read_stata('anes1966dta/NES1966.dta')
df_1974 = pd.read_stata('anes1974dta/NES1974.dta')
df_1978 = pd.read_stata('anes1978dta/NES1978.dta')
df_1982 = pd.read_stata('anes1982dta/NES1982.dta')
df_1994 = pd.read_stata('anes1994dta/NES1994.dta')
df_1996 = pd.read_stata('anes1996dta/NES96.dta')

#fig, ax = plt.subplots(3,2)

dfs = [df_1974, df_1978, df_1982, df_1994, df_1996]

#df_1974.to_csv('testData.csv')
#print(df_1966['V660019a'].unique())
'''
# most impt problem code
print(df_1974['V742079'].unique())
print(df_1978['V780315'].unique())
print(df_1982['V820299'].unique())
print(df_1994['V940706'].unique())
# survey also includes respondent's judgement of govt handling of problem
print(df_1996['V961141'].unique())
'''
arr_1974 = np.zeros(len(df_1974['V742079'].unique()))
df_1974.groupby['']
    

'''
for frame in dfs:
    no_responses = len(row['660019C'].unique())
    for row in frame.itertuples():
        row.
'''

#plt.show()