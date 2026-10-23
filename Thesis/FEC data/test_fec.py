import matplotlib.pyplot as plt
import numpy as np
import random as rng
import pandas as pd
import csv
import seaborn as sb

data = pd.read_csv('weball02.txt', sep='|', names = ['CAND_ID','CAND_NAME','CAND_ICI','PTY_CD','CAND_PTY_AFFILIATION',
                                                   'TTL_RECEIPTS','TRANS_FROM_AUTH','TTL_DISB','TRANS_TO_AUTH','COH_BOP',
                                                   'COH_COP','CAND_CONTRIB','CAND_LOANS','OTHER_LOANS','CAND_LOAN_REPAY',
                                                   'OTHER_LOAN_REPAY','DEBTS_OWED_BY','TTL_INDIV_CONTRIB','CAND_OFFICE_ST','CAND_OFFICE_DISTRICT',
                                                   'SPEC_ELECTION','PRIM_ELECTION','RUN_ELECTION','GEN_ELECTION','GEN_ELECTION_PRECENT',
                                                   'OTHER_POL_CMTE_CONTRIB','POL_PTY_CONTRIB','CVG_END_DT','INDIV_REFUNDS','CMTE_REFUNDS'])

house_data = data[data.CAND_ID.str.startswith('H')]
house_general = house_data[pd.notnull(data['GEN_ELECTION'])]
data2 = house_general.groupby(['CAND_OFFICE_ST','CAND_OFFICE_DISTRICT'])

largest = 0
for name, group in data2:
    if group.shape[0] > largest:
        largest = group.shape[0]
print(largest)

# looks like independents and DFL are in a lot of elections. 
# Flip results: estimate 

# there was a 5 candidate race in 00, and a 6 candidate one in 05...