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


fig, ax = plt.subplots(3,2)
x_counter = 0
y_counter = 0

dono_cutoff = 'PROP_OVER_200'

params_list = [['voting_records/1992.xlsx', 'NAFTA_VOTE'],
               ['voting_records/1992.xlsx', 'RUSSIA_VOTE'],
               ['voting_records/1994.xlsx', 'BOSNIA_VOTE'],
               ['voting_records/1998.xlsx', 'DEFENSE_VOTE'],
               ['voting_records/2000.xlsx', 'VOUCHERS_VOTE']]

for i in params_list:
    current_df = i[0]
    current_votes_col = i[1]

    print('Votes for ' + current_votes_col)

    data = pd.read_excel(current_df)

    test_grpby = data.groupby(['CAND_PTY_AFFILIATION', current_votes_col])

    for name, group in test_grpby:
        print(name, group.shape[0])