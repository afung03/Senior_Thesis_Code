import matplotlib.pyplot as plt
import random as rng
import pandas as pd
import csv
import seaborn as sb
import numpy as np
import os
from sklearn.linear_model import LogisticRegression
import statsmodels.api as sm
import statsmodels.formula.api as smf

'''
weball92.txt
weball94.txt
weball96.txt
weball98.txt
weball00.txt
weball02.txt
'''

# Change file name based on which file we are regressing.
print('begin data processing')
data = pd.read_csv('weball02.txt', sep='|', names = ['CAND_ID','CAND_NAME','CAND_ICI','PTY_CD','CAND_PTY_AFFILIATION',
                                                   'TTL_RECEIPTS','TRANS_FROM_AUTH','TTL_DISB','TRANS_TO_AUTH','COH_BOP',
                                                   'COH_COP','CAND_CONTRIB','CAND_LOANS','OTHER_LOANS','CAND_LOAN_REPAY',
                                                   'OTHER_LOAN_REPAY','DEBTS_OWED_BY','TTL_INDIV_CONTRIB','CAND_OFFICE_ST','CAND_OFFICE_DISTRICT',
                                                   'SPEC_ELECTION','PRIM_ELECTION','RUN_ELECTION','GEN_ELECTION','GEN_ELECTION_PRECENT',
                                                   'OTHER_POL_CMTE_CONTRIB','POL_PTY_CONTRIB','CVG_END_DT','INDIV_REFUNDS','CMTE_REFUNDS'])

# subset only house races in house
house_data = data[data.CAND_ID.str.startswith('H')]

# subset only house candidates who were in the general election
house_general = house_data[pd.notnull(data['GEN_ELECTION'])]
house_general['CONTESTED'] = 0
house_general['PROP_DISB'] = 0
house_general['PROP_MAX'] = 0

# subset only house candidates who were in the general election and were contested
by_district = house_general.groupby(['CAND_OFFICE_ST','CAND_OFFICE_DISTRICT'])

print('begin variable assignment')

# counter for variable assignment
counter = 0

cid_to_contested = {}
cid_to_pdisb = {}
cid_to_pmax = {}

# consider somehow controlling per district or by number of people in the race?
# can I fix the nonindependence issue by randomly selecting a candidate from each district? and batching?

for name, group in by_district:
    if group.shape[0] >= 2:
        total_disb = group['TTL_DISB'].sum()
        max_disb = group['TTL_DISB'].max()
        for row in group.itertuples():
            cid = row.CAND_ID
            cid_to_contested[cid] = 1
            cid_to_pdisb[cid] = row.TTL_DISB / total_disb
            cid_to_pmax[cid] = row.TTL_DISB / max_disb
    else:
        for row in group.itertuples():
            cid = row.CAND_ID
            cid_to_contested[cid] = 0
            cid_to_pdisb[cid] = 1
            cid_to_pmax[cid] = 1

print('recombining groups')

# recombine groups into single df
group_list = []
for name, group in by_district:
    group_list.append(group)

house_general_ungrouped = pd.concat(group_list)

# assign contested, measure of expenditure
house_general_ungrouped['CONTESTED'] = house_general_ungrouped['CAND_ID'].map(cid_to_contested)
house_general_ungrouped['PROP_DISB'] = house_general_ungrouped['CAND_ID'].map(cid_to_pdisb)
house_general_ungrouped['PROP_MAX'] = house_general_ungrouped['CAND_ID'].map(cid_to_pmax)


print('recoding values for regression')
# subset only contested general elections
house_general_contested = house_general_ungrouped[house_general_ungrouped['CONTESTED'] == 1]


def is_dem(pty):
    if pty == 'DEM':
        return 1
    else:
        return 0
    
def is_rep(pty):
    if pty == 'REP':
        return 1
    else:
        return 0

def is_oth(pty):
    if pty != 'DEM' and pty != 'REP':
        return 1
    else:
        return 0
    
def had_primary(prim_id):
    if prim_id == 'W':
        return 1
    else:
        return 0
    
def incumbent_scale(inc_id):
    if inc_id == 'C':
        return -1
    elif inc_id == 'I':
        return 1
    else:
        return 0
    
def code_win(w_id):
    if w_id == 'W':
        return 1
    else:
        return 0

# assign party ids
house_general_contested['IS_DEM'] = house_general_contested['CAND_PTY_AFFILIATION'].apply(is_dem)
house_general_contested['IS_REP'] = house_general_contested['CAND_PTY_AFFILIATION'].apply(is_rep)
house_general_contested['IS_OTH'] = house_general_contested['CAND_PTY_AFFILIATION'].apply(is_oth)

# assign general election ids
house_general_contested['HAD_PRIM'] = house_general_contested['PRIM_ELECTION'].apply(had_primary)

# assign incumbent advantage scale
house_general_contested['INC_ADV'] = house_general_contested['CAND_ICI'].apply(incumbent_scale)

# assign win id
house_general_contested['WIN'] = house_general_contested['GEN_ELECTION'].apply(code_win)

print('begin model training')
# print(house_general_contested[['PROP_DISB','INC_ADV', 'HAD_PRIM', 'IS_DEM', 'IS_REP', 'IS_OTH']].isnull().values.any())

# need to control for relative expenditure, incumbent, primary, party
#'PROP_DISB',
X = sm.add_constant(house_general_contested[['PROP_DISB','INC_ADV', 'HAD_PRIM', 'IS_DEM', 'IS_REP']]) #, 'IS_OTH'
# X = house_general_contested[['PROP_DISB','INC_ADV', 'HAD_PRIM', 'IS_DEM', 'IS_REP', 'IS_OTH']]
y = house_general_contested['WIN']

data_reg = house_general_contested[['WIN','PROP_DISB','INC_ADV', 'HAD_PRIM', 'IS_DEM', 'IS_REP']] #, 'IS_OTH'

'''def select_random_sample(grpby):
    for'''
'''
B = 1000
for i in range(B):'''


model = sm.Logit(y.astype(float), X.astype(float)).fit()
# model = smf.logit('WIN ~ PROP_DISB + INC_ADV + HAD_PRIM + IS_DEM + IS_REP + IS_OTH', data=data_reg).fit()

#print(np.diag(model.cov_params()))
#print(model.summary())
print('params:')
print(model.params.PROP_DISB)