import matplotlib.pyplot as plt
import random as rng
import pandas as pd
import csv
import seaborn as sb
import numpy as np
import os

# need [coding of most impt issue, coding of weight, highest coding - 1]


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

directory = 'year_dta_files'
arrays_list = []

# iterate over files in the dta directory
for filename in os.listdir(directory):
    print(filename)
    f = os.path.join(directory, filename)
    if os.path.isfile(f) and filename.endswith('.dta'):
        current_df = f
        current_issue_code = ANES_names[filename][0]
        current_weight_code = ANES_names[filename][1]
        current_highest_coding = ANES_names[filename][2]
        current_year = ANES_names[filename][3]
    

        coding_arr = np.zeros(current_highest_coding)
        total_pop = 0

        data = pd.read_stata(current_df)

        # split file rows by most important issue

        by_MPI = data.groupby(current_issue_code)

        for name, group in by_MPI:
            if not isinstance(name, str):
                if current_weight_code == None:
                    pop = group.shape[0]
                    coding_arr[int(name)] += pop
                    total_pop += pop
                else:
                    pop = group[current_weight_code].sum()
                    coding_arr[int(name)] += pop
                    total_pop += pop

        # create array of proportions for the current survey
        coding_arr /= total_pop
        # pick out issue codes for issues where 
        indices = np.where(coding_arr >= .05)[0]

        # appends each row separately.
        for i in indices:
            arrays_list.append([current_year, i, coding_arr[i]])

        # store in DF with columns: year, issue code, percentage. Can sort by year, then percentage.
        # - Put this in a Google sheet then add issue description, poll presence, disagreement, bill presence, bill year (search congressional records)

data_array = np.array(arrays_list)
column_values = ['Year','Issue_Code','Percent_Response']
issues_frame = pd.DataFrame(data=data_array, columns=column_values)
issues_frame.sort_values(by=['Year', 'Percent_Response'], inplace=True)
issues_frame.to_excel('most_salient.xlsx')