import matplotlib.pyplot as plt
import numpy as np
import random as rng
import pandas as pd
import csv
import seaborn as sb
import statsmodels.api as sm
import sklearn as skl
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import log_loss
from sklearn.metrics import r2_score



'''
$200 in 1992 is:

1992: $200
1994: $211.73
1996: $223.61
1998: $234.03
2000: $244.46
2002: $256.48

Source: bureau of labor statistics. Calculated in January of each year.
https://www.bls.gov/data/inflation_calculator.htm
'''
year = 2000

year_params_dict = {
    1992 : [200, 'weball92.txt', 'cm92.txt', 'itcont92.txt', '92election_winners.xlsx'],
    1994 : [211.73, 'weball94.txt', 'cm94.txt', 'itcont94.txt', '94election_winners.xlsx'],
    1996 : [223.61, 'weball96.txt', 'cm96.txt', 'itcont96.txt', '96election_winners.xlsx'],
    1998 : [234.03, 'weball98.txt', 'cm98.txt', 'itcont98.txt', '98election_winners.xlsx'],
    2000 : [244.46, 'weball00.txt', 'cm00.txt', 'itcont00.txt', '00election_winners.xlsx'],
    2002 : [256.48, 'weball02.txt', 'cm02.txt', 'itcont02.txt', '02election_winners.xlsx']


}

# To change the election year is from, change the three txt file names in the following likes to match that year (i.e. wball00.txt for 2000)
# If you are trying to recreate the regression with the proportion of donations over $200, change 'PROP_DISB' to 'PROP_OVER_200' in lines 265 and 297

data = pd.read_csv(year_params_dict[year][1], sep='|', names = ['CAND_ID','CAND_NAME','CAND_ICI','PTY_CD','CAND_PTY_AFFILIATION',
                                                   'TTL_RECEIPTS','TRANS_FROM_AUTH','TTL_DISB','TRANS_TO_AUTH','COH_BOP',
                                                   'COH_COP','CAND_CONTRIB','CAND_LOANS','OTHER_LOANS','CAND_LOAN_REPAY',
                                                   'OTHER_LOAN_REPAY','DEBTS_OWED_BY','TTL_INDIV_CONTRIB','CAND_OFFICE_ST','CAND_OFFICE_DISTRICT',
                                                   'SPEC_ELECTION','PRIM_ELECTION','RUN_ELECTION','GEN_ELECTION','GEN_ELECTION_PRECENT',
                                                   'OTHER_POL_CMTE_CONTRIB','POL_PTY_CONTRIB','CVG_END_DT','INDIV_REFUNDS','CMTE_REFUNDS'])

links_data = pd.read_csv(year_params_dict[year][2], sep = '|', names = ['CMTE_ID','CMTE_NM','TRES_NM','CMTE_ST1','CMTE_ST2',
                                              'CMTE_CITY','CMTE_ST','CMTE_ZIP','CMTE_DSGN','CMTE_TP',
                                              'CMTE_PTY_AFFILIATION','CMTE_FILING_FREQ','ORG_TP',
                                              'CONNECTED_ORG_NM','CAND_ID'])

donos_data = pd.read_csv(year_params_dict[year][3], sep='|', names = ['CMTE_ID','AMNDT_IND','RPT_TP','TRANSACTION_PGI','IMAGE_NUM',
                                                           'TRANSACTION_TP','ENTITY_TP','NAME','CITY','STATE',
                                                           'ZIP_CODE','EMPLOYER','OCCUPATION','TRANSACTION_DT','TRANSACTION_AMT',
                                                           'OTHER_ID','TRAN_ID','FILE_NUM','MEMO_CD','MEMO_TEXT','SUB_ID'])

# CHANGE THIS VALUE TO ADJUST FOR INFLATION (see values at top of file)
YEAR_MULTIPLIER = year_params_dict[year][0] / 200
cand_coms = links_data[pd.notnull(links_data['CAND_ID'])]

# candidate id : [donos above $200, donos above $500, donos above $1000]
candid_to_200 = {}
candid_to_500 = {}
candid_to_1000 = {}
cid_to_distid = {}

by_candid = data.groupby('CAND_ID')

unused_comids = []
unused_candids = []

for name, group in by_candid:
    candid_to_200[name] = 0
    candid_to_500[name] = 0
    candid_to_1000[name] = 0


# committee id : candidate id
comid_to_candid = {}

for row in links_data.itertuples():
    if pd.notnull(row.CAND_ID):
        comid_to_candid[row.CMTE_ID] = row.CAND_ID
    else:
        comid_to_candid[row.CMTE_ID] = None

# TODO: add comversion rate to whatever year opensecrets uses
for row in donos_data.itertuples():
    if comid_to_candid.get(row.CMTE_ID) != None:
        candid = comid_to_candid[row.CMTE_ID]
        if candid_to_200.get(candid) != None:
            amt =  int(row.TRANSACTION_AMT)
            if amt >= 200.0 * YEAR_MULTIPLIER:
                candid_to_200[candid] += row.TRANSACTION_AMT
            if amt >= 500.0 * YEAR_MULTIPLIER:
                candid_to_500[candid] += row.TRANSACTION_AMT
            if amt >= 1000.0 * YEAR_MULTIPLIER:
                candid_to_1000[candid] += row.TRANSACTION_AMT
        else:
            unused_candids.append(candid)
    else:
        unused_comids.append(row.CMTE_ID)


house_data = data[data.CAND_ID.str.startswith('H')]
# TODO: add high dollar dono amounts onto dataset
house_data['OVER_200'] = house_data['CAND_ID'].map(candid_to_200)
house_data['OVER_500'] = house_data['CAND_ID'].map(candid_to_500)
house_data['OVER_1000'] = house_data['CAND_ID'].map(candid_to_1000)

# take only general election canidates
house_general = house_data[pd.notnull(data['GEN_ELECTION'])]


# From "regressions.py" - add in control variables for regression
house_general['CONTESTED'] = 0
house_general['PROP_DISB'] = 0
house_general['PROP_MAX'] = 0
house_general['PROP_OVER_200'] = 0
house_general['PROP_OVER_500'] = 0
house_general['PROP_OVER_1000'] = 0
house_general['PROP_PAC'] = 0

# subset only house candidates who were in the general election and were contested
by_district = house_general.groupby(['CAND_OFFICE_ST','CAND_OFFICE_DISTRICT'])

cid_to_contested = {}
cid_to_pdisb = {}
cid_to_pmax = {}
cid_to_200 = {}
cid_to_500 = {}
cid_to_1000 = {}
cid_to_distid = {}
cid_to_pacprop = {}

# counter for variable assignment
counter = 0

# consider somehow controlling per district or by number of people in the race?
# can I fix the nonindependence issue by randomly selecting a candidate from each district? and batching?

for name, group in by_district:
    if group.shape[0] >= 2:
        total_disb = group['TTL_DISB'].sum()
        max_disb = group['TTL_DISB'].max()
        over_200_ttl = max(group['OVER_200'].sum(), 1)
        over_500_ttl = max(group['OVER_500'].sum(), 1)
        over_1000_ttl = max(group['OVER_1000'].sum(), 1)
        PAC_ttl = max(group['OTHER_POL_CMTE_CONTRIB'].sum(),1)
        for row in group.itertuples():
            cid = row.CAND_ID
            cid_to_contested[cid] = 1
            cid_to_pdisb[cid] = row.TTL_DISB / total_disb
            cid_to_pmax[cid] = row.TTL_DISB / max_disb
            cid_to_200[cid] = row.OVER_200 / over_200_ttl
            cid_to_500[cid] = row.OVER_500 / over_500_ttl
            cid_to_1000[cid] = row.OVER_1000 / over_1000_ttl
            cid_to_distid[cid] = counter
            cid_to_pacprop[cid] = row.OTHER_POL_CMTE_CONTRIB / PAC_ttl
    else:
        for row in group.itertuples():
            cid = row.CAND_ID
            cid_to_contested[cid] = 0
            cid_to_pdisb[cid] = 1
            cid_to_pmax[cid] = 1
            cid_to_200[cid] = 1
            cid_to_500[cid] = 1
            cid_to_1000[cid] = 1
            cid_to_distid[cid] = counter
            cid_to_pacprop[cid] = 1
    counter += 1

print('recombining groups')

# recombine groups into single df
group_list = []
for name, group in by_district:
    group_list.append(group)

house_general_ungrouped = pd.concat(group_list)

# assign contested, measure of expenditure, measures of high dollar donos raised.
house_general_ungrouped['CONTESTED'] = house_general_ungrouped['CAND_ID'].map(cid_to_contested)
house_general_ungrouped['PROP_DISB'] = house_general_ungrouped['CAND_ID'].map(cid_to_pdisb)
house_general_ungrouped['PROP_MAX'] = house_general_ungrouped['CAND_ID'].map(cid_to_pmax)
house_general_ungrouped['PROP_OVER_200'] = house_general_ungrouped['CAND_ID'].map(cid_to_200)
house_general_ungrouped['PROP_OVER_500'] = house_general_ungrouped['CAND_ID'].map(cid_to_500)
house_general_ungrouped['PROP_OVER_1000'] = house_general_ungrouped['CAND_ID'].map(cid_to_1000)
house_general_ungrouped['DIST_ID'] = house_general_ungrouped['CAND_ID'].map(cid_to_distid)
house_general_ungrouped['PROP_PAC'] = house_general_ungrouped['CAND_ID'].map(cid_to_pacprop)

print('recoding values for regression')
# subset only candidates who won
house_general_victors = house_general_ungrouped[house_general_ungrouped['GEN_ELECTION'] == 'W']
# house_general_specials_winners = house_general_ungrouped[house_general_ungrouped['SPEC_ELECTION'] == 'W']
# house_general_specials_winners.to_excel('92specials.xlsx')

print(house_general_victors.shape[0])

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
house_general_victors['IS_DEM'] = house_general_victors['CAND_PTY_AFFILIATION'].apply(is_dem)
house_general_victors['IS_REP'] = house_general_victors['CAND_PTY_AFFILIATION'].apply(is_rep)
house_general_victors['IS_OTH'] = house_general_victors['CAND_PTY_AFFILIATION'].apply(is_oth)

# assign general election ids
house_general_victors['HAD_PRIM'] = house_general_victors['PRIM_ELECTION'].apply(had_primary)

# assign incumbent advantage scale
house_general_victors['INC_ADV'] = house_general_victors['CAND_ICI'].apply(incumbent_scale)

# assign win id
house_general_victors['WIN'] = house_general_victors['GEN_ELECTION'].apply(code_win)

house_general_victors['PERSONAL_PROP_200'] = house_general_victors['OVER_200'] / house_general_victors['TTL_INDIV_CONTRIB']

house_general_victors_alphabetical = house_general_victors.sort_values('CAND_NAME')

house_general_victors_alphabetical.to_excel(year_params_dict[year][4])