import matplotlib.pyplot as plt
import random as rng
import pandas as pd
import csv
import seaborn as sb
import numpy as np
import os


# fileName : [coding of most impt issue, coding of weight, highest coding - 1, year]

ANES_names = {
    'NES1980.dta' : ['V800979', None, 1000, 1980], # no weights
    'NES1982.dta' : ['V820299', None, 1000, 1982],
    'NES1984.dta' : ['V840993', None, 1000, 1984],
    'NES1986.dta' : ['V860306', None, 1000, 1986], # used most impt natl issue instead of most impt problem to you
    'NES1988.dta' : ['V880702', None, 1000, 1988],
    'NES1990.dta' : ['V900326', None, 1000, 1990], # also asked to list other problems, but does not indicate quantity of importance? (not all surveys list other types of problems)
    'NES1992.dta' : ['V900326', 'V927000', 1000, 1992],   # start using weights
    'NES1994.dta' : ['V940706', 'V940006a', 1000, 1994],
    'NES1996.dta' : ['V961141', 'V960005', 1000, 1996],
    'NES1998.dta' : ['V980346', 'V980002', 1000, 1998],
    'NES2000.dta' : ['V000436', 'V000002', 1000, 2000]
}

# issue name : [issue code, year, file name, weight code, income code]
bills = {
    'Sanction_SA' :         ['V860490', 1986, 'year_dta_files/NES1986.dta', None, 'V860733'], #Happened, likely?
    'forces_to_PG' :        ['V912408', 1992, 'year_dta_files/NES1992.dta', 'V927000', 'V924104'], #Happened
    'Gulf_war' :            ['V912500', 1992, 'year_dta_files/NES1992.dta', 'V927000', 'V924104'], #Happened
    'aid_postcommunist' :   ['V912401', 1992, 'year_dta_files/NES1992.dta', 'V927000', 'V900694'], #Happened
    'Clinton_crime_bill' :  ['V941040', 1994, 'year_dta_files/NES1994.dta', 'V940006a', 'V941404'], #Happened, likely? 
    'School_prayer' :       ['V941020', 1994, 'year_dta_files/NES1994.dta', 'V940006a', 'V941404'],
    'term_limits' :         ['V960412', 1996, 'year_dta_files/NES1996.dta', 'V960005', 'V960701'],
    'fed_death_penalty' :   ['V961197', 1996, 'year_dta_files/NES1996.dta', 'V960005', 'V960701'], #Happened, likely?
    '2yr_welf_limit' :      ['V961323', 1996, 'year_dta_files/NES1996.dta', 'V960005', 'V960701'],
    'ban_late_abortion' :   ['V980511', 1998, 'year_dta_files/NES1998.dta', 'V980002', 'V980652'],
    'ban_partial_birth' :   ['V000703', 2000, 'year_dta_files/NES2000.dta', 'V000002', 'V001040'],
    'school_vouchers' :     ['V000742', 2000, 'year_dta_files/NES2000.dta', 'V000002', 'V001040']
}

def code_to_op(issue, code):
    if issue == 'Sanction_SA':
        if code == 1: return 1
        elif code == 5: return 0
        else: return None
    elif issue == 'forces_to_PG':
        if code == 1: return 1
        elif code == 5: return 0
        else: return None
    # coded extremely poorly by ANES
    elif issue == 'Gulf_war':
        if code == 1: return 0
        elif code == 5: return 1
        else: return None
    elif issue == 'aid_postcommunist':
        if code == 1: return 1
        elif code == 5: return 0
        else: return None
    elif issue == 'Clinton_crime_bill':
        if code == 1: return 1
        elif code == 5: return 0
        else: return None
    elif issue == 'School_prayer':
        if code == 1: return 1
        elif code == 5 or code == 3 or code == 4: return 0
        else: return None
    elif issue == 'term_limits':
        if code == 1: return 1
        elif code == 2: return 2
        else: return None
    elif issue == 'fed_death_penalty':
        if code == 1: return 1
        elif code == 5: return 0
        else: return None
    elif issue == '2yr_welf_limit':
        if code == 1: return 1
        elif code == 5: return 0
        else: return None
    elif issue == 'ban_late_abortion':
        if code == 1: return 1
        elif code == 5: return 0
        else: return None
    elif issue == 'ban_partial_birth':
        if code == 1: return 1
        elif code == 5: return 0
        else: return None
    elif issue == 'school_vouchers':
        if code == 1: return 1
        elif code == 5: return 0
        else: return None
    else:
        print(issue)
    


# using data from US Census
def inc_to_quint(year, code):
    if year == 1986:
        if code >= 88: return None
        elif code >= 19: return 4
        elif code >= 16: return 3
        elif code >= 13: return 2
        elif code >= 6: return 1
        elif code >= 1: return 0
        else: return None
    elif year == 1992:
        # 1989 data
        if code >= 88: return None
        elif code >= 21: return 4
        elif code >= 18: return 3
        elif code >= 15: return 2
        elif code >= 11: return 1
        elif code >= 1: return 0
        else: return None

max_income_coding = 30 #?


pttls = []
issue_names = []
fav_opp_graphs = []
other_graphs = []
x_axis = np.arange(30)

#iterate over issues, codidng up favor/oppose for each income class
for key, value in bills.items():
    print(value[1])

    # code for column of current_issue
    current_issue_code = value[0]
    current_df = value[2]
    current_weight_code = value[3]

    # TODO: find the income code
    current_inc_code = value[4]
    current_year = 0

    # coding this at 30 for now idk.
    support = np.zeros(max_income_coding)
    pop_totals = np.zeros(max_income_coding)
    oth_tot = np.zeros(max_income_coding)
    other = np.zeros(max_income_coding)

    data = pd.read_stata(current_df)

    # split data into opinion on given issue and income class code
    by_opinion = data.groupby([current_issue_code, current_inc_code])

    for name, group in by_opinion:
        # count up weighted population
        if current_weight_code == None:
            pop = group.shape[0]
        else:
            pop = group[current_weight_code].sum()

        clipped_opinion = int(str(name[0]).split('.')[0])
        clipped_income = int(str(name[1]).split('.')[0])

        # TODO: check how favor/oppose is coded and check how class is coded.
        if clipped_opinion < 30 and clipped_income < 30:
            if code_to_op(key, clipped_opinion) == 1:
                support[clipped_income] += pop
                pop_totals[clipped_income] += pop
            elif code_to_op(key, clipped_opinion) == 0:
                pop_totals[clipped_income] += pop
            else:
                other[clipped_income] += pop
                oth_tot[clipped_income] = pop
    pop_totals = np.where(pop_totals == 0, 1, pop_totals)
    pttls.append(pop_totals)
    fav_opp_graphs.append(np.divide(support, pop_totals))
    other_graphs.append(np.divide(other,(oth_tot + pop_totals)))
    issue_names.append(key)

fig, ax = plt.subplots(4,3)

x_counter = 0
y_counter = 0
for i in range(len(fav_opp_graphs)):
    curr_graph = fav_opp_graphs[i]
    ax[x_counter, y_counter].plot(x_axis[:len(curr_graph)],curr_graph,label = issue_names[i])
    ax[x_counter, y_counter].set_title('percent favorable by income for ' + issue_names[i])
    if x_counter == 3:
        x_counter = 0
        y_counter += 1
    else:
        x_counter += 1

plt.subplots_adjust(hspace=0.5)
plt.show()