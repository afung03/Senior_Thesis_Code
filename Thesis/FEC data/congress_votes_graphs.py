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

dono_cutoff = 'PROP_OVER_1000'

params_list = [['voting_records/1992.xlsx', 'NAFTA_VOTE'],
               ['voting_records/1992.xlsx', 'RUSSIA_VOTE'],
               ['voting_records/1994.xlsx', 'BOSNIA_VOTE'],
               ['voting_records/1998.xlsx', 'DEFENSE_VOTE'],
               ['voting_records/2000.xlsx', 'VOUCHERS_VOTE']]

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


print('STARTING OUTPUTS RUN')
for i in params_list:
    current_df = i[0]
    current_votes_col = i[1]

    data = pd.read_excel(current_df)

    data=data[data['CONTESTED'] == 1]

    # test_grpby = data.groupby(['CAND_PTY_AFFILIATION', current_votes_col])

    # want: avg, personal prop 200, prop 200 for ayes and nays. Scatterplot of (both?) these metrics colored green for ayes and red for nays

    by_vote = data.groupby(current_votes_col)

    ayes_avg_pc200 = data[data[current_votes_col] == 'Y'][dono_cutoff].mean()

    nays_avg_pc200 = data[data[current_votes_col] == 'N'][dono_cutoff].mean()

    avg_dono_cutoff = data[dono_cutoff].mean()

    median_dono_cutoff = data[dono_cutoff].median()

    ''' 
    print('Average personal prop 200 among ayes for ' + current_votes_col)
    print(ayes_avg_pp200)

    print('Average personal prop 200 among nays for ' + current_votes_col)
    print(nays_avg_pp200)
    '''

    print('Average campaign prop 200 among yeas for ' + current_votes_col)
    print(ayes_avg_pc200)

    print('Average campaign prop 200 among nays for ' + current_votes_col)
    print(nays_avg_pc200)

    print('Average prop 200 overall for ' + current_votes_col)
    print(avg_dono_cutoff)

    print('Median prop 200 overall for ' + current_votes_col)
    print(median_dono_cutoff)

    # select only those who voted. NO ONE VOTED "PRESENT" IN ANY OF THE ROLL CALLS
    voters = data[data[current_votes_col].isin(['Y','N'])]

    def vote_to_code(vote):
        if vote == 'Y':
            return 1
        else:
            return 0
        
    def inc_to_code(inc):
        if inc == 'I':
            return 1
        else:
            return 0

    voters['VOTE'] = voters[current_votes_col].apply(vote_to_code)
    voters['IS_INC'] = voters['CAND_ICI'].apply(inc_to_code)
    # dono_cutoff, 'PROP_PAC'
    
    sb.scatterplot(data=voters, x=dono_cutoff, y='PROP_PAC', hue=current_votes_col, ax=ax[y_counter,x_counter])
    ax[y_counter,x_counter].axvline(avg_dono_cutoff, color='green')
    ax[y_counter,x_counter].axvline(median_dono_cutoff, color='red')

    # logistic regression on vote 1/0: party, PROP_200, incumbency, 

    voters['IS_DEM_CONG'] = voters['CONG_PTY_AFFILIATION'].apply(is_dem)
    voters['IS_REP_CONG'] = voters['CONG_PTY_AFFILIATION'].apply(is_rep)

    X = sm.add_constant(voters[[dono_cutoff, 'IS_INC', 'IS_DEM_CONG', 'IS_REP_CONG']])
    y = voters[['VOTE']]
    model = sm.Logit(y, X).fit()

    print(current_votes_col + ' lr model:')
    print(model.summary())

    if x_counter == 1:
        x_counter = 0
        y_counter += 1
    else:
        x_counter += 1
fig.delaxes(ax[2,1])
plt.show()