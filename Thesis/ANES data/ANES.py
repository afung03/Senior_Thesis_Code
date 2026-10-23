import matplotlib.pyplot as plt
import numpy as np
import random as rng
import pandas as pd
import csv
import seaborn as sb

years = np.arange(1964, 2001, 2)
xaxlen = len(years)

y2i = {}

for i in range(xaxlen):
    y2i[years[i]] = i

def year_to_index(year):
    return y2i[int(year)]

def cohort_to_index(cohort):
    return int(cohort) - 1

def code_to_index(code):
    code = int(code)
    if code == 99:
        return 12
    elif code == 97:
        return 10
    elif code == 98:
        return 11
    else:
        return int(code)
    
# might need to do follow up for more specific codes:
# p. 137 of the appendix file has more specific info.
issue_names = {"1" : "agricultural", 
                   "2" : "ECONOMICS; BUSINESS; CONSUMER ISSUES", 
                   "3" : "FOREIGN AFFAIRS AND NATIONAL DEFENSE",
                   "4" : "GOVERNMENT FUNCTIONING",
                   "5" : "LABOR ISSUES",
                   "6" : "NATURAL RESOURCES",
                   "7" : "PUBLIC ORDER",
                   "8" : "RACIAL PROBLEMS",
                   "9" : "SOCIAL WELFARE",
                   "97" : "OTHER",
                   # missing data
                   "98" : "Don't Know",
                   "99" : "N/A",
                   "0" : "No issues",
                   "INAP" : "not asked",}

# make sure conversion works as intended
anes_df = pd.read_csv('anes_timeseries_cdf_csv_20220916.csv', low_memory=False)

# Sort data by year, income cohort, most important issue.  name is [year, cohort, issue]
response_by_subgroup = anes_df.groupby(["VCF0004", "VCF0114", "VCF0875"])

# 1948, 1952, 1954, 1956, 1958, 1962, 2002, 2004, 2008, 2012, 2016, 2020 lack data on most important issue (2002 lacks income cohort as well)

"""
1. 0 to 16 percentile
2. 17 to 33 percentile
3. 34 to 67 percentile
4. 68 to 95 percentile
5. 96 to 100 percentile
"""

#index by [income bracket][year][issue]
year_issue_counts = np.zeros((5,xaxlen,13))

group_pop = np.zeros((5,xaxlen))

for name, group in response_by_subgroup:
    # include 1964 thru 2000
    if (name[1] != ' ' and name[1] != '0' and name[2] != ' '  and name[2] != '99' and (int(name[0]) >= 1964 and int(name[0]) <= 2000)):
        year_ind = year_to_index(name[0])
        inc_cohort_ind = cohort_to_index(name[1])
        res_is = code_to_index(name[2])
        pop = group['VCF0009z'].sum()
        group_pop[inc_cohort_ind][year_ind] += pop
        year_issue_counts[inc_cohort_ind][year_ind][res_is] += pop

# fix divide by zero errors
group_pop[group_pop==0] = 1

Y00 = np.divide(year_issue_counts[0], group_pop[0].reshape(xaxlen,1))
Y01 = np.divide(year_issue_counts[1], group_pop[1].reshape(xaxlen,1))
Y10 = np.divide(year_issue_counts[2], group_pop[2].reshape(xaxlen,1))
Y11 = np.divide(year_issue_counts[3], group_pop[3].reshape(xaxlen,1))
Y20 = np.divide(year_issue_counts[4], group_pop[4].reshape(xaxlen,1))
Y21 = np.divide(np.sum(year_issue_counts, axis=0), np.sum(group_pop, axis=0).reshape(xaxlen,1))

x = years

fig, ax = plt.subplots(3,2)

labels = ["None", 
          "AGRICULTURAL", 
          "ECONOMICS; BUSINESS; CONSUMER ISSUES", 
          "FOREIGN AFFAIRS AND NATIONAL DEFENSE",
          "GOVERNMENT FUNCTIONING",
          "LABOR ISSUES",
          "NATURAL RESOURCES",
          "PUBLIC ORDER",
          "RACIAL PROBLEMS",
          "SOCIAL WELFARE",
          "OTHER",
          "DON'T KNOW",
          "N/A"
          ]

colors = ["blue",
          "orange",
          "green",
          "red",
          "purple",
          "brown",
          "pink",
          "gray",
          "olive",
          "cyan",
          "maroon",
          "black",
          "lime",
]
# plot data by issue
for j in range(12):
    ax[0,0].plot(x,Y00[:,j], label = labels[j], color = colors[j])
    ax[0,1].plot(x,Y01[:,j], label = labels[j], color = colors[j])
    ax[1,0].plot(x,Y10[:,j], label = labels[j], color = colors[j])
    ax[1,1].plot(x,Y11[:,j], label = labels[j], color = colors[j])
    ax[2,0].plot(x,Y20[:,j], label = labels[j], color = colors[j])
    ax[2,1].plot(x,Y21[:,j], label = labels[j], color = colors[j])
    
ax[0,0].set_title("Fig 6.1: 0-16th income percentile")
ax[0,1].set_title("Fig 6.2: 17-33rd income percentile")
ax[1,0].set_title("Fig 6.3: 34-67th income percentile")
ax[1,1].set_title("Fig 6.4: 68-95th income percentile")
ax[2,0].set_title("Fig 6.5: 96-100th income percentile")
ax[2,1].set_title("Fig 6.6: All respondents")

plt.legend(loc='center', bbox_to_anchor=(-0.1,-0.3),
          fancybox=True, shadow=True, ncol = 4)

plt.subplots_adjust(left=.1, right=.9, 
                    top=.97, bottom=.12, 
                    wspace=.2, hspace=.2)

plt.show()