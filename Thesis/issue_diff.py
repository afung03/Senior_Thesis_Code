import matplotlib.pyplot as plt
import random as rng
import pandas as pd
import csv
import seaborn as sb

data = pd.read_stata('Gilens_Page.dta')

data['90pct_50pctdiff'] = (data['pred90_sw'] - data['pred50_sw']).abs()
data['90pct_allpctdiff'] = (data['pred90_sw'] - data['PREDALL_SW']).abs()

#concat_df = data[((data['pred90_sw'] <= .47) & (data['pred50_sw'] >= .53))][['ID8102','YEAR','OUTCOME','switcher','XL_AREA','90pct_50pctdiff', 'pred50_sw', 'pred90_sw', 'PREDALL_SW','QuestionText']]
# | ((data['pred50_sw'] <= .46) & (data['pred90_sw'] >= .54))
#top_issues = concat_df.sort_values('90pct_50pctdiff', ascending=False).head(100)

#top_issues.to_excel('50FAV_ONLY.xlsx')

russia_poll1 = data[data['ID8102'] == 724.0]
russia_poll2 = data[data['ID8102'] == 718.0]

print(russia_poll1['pred90_sw'], russia_poll1['pred50_sw'])
print(russia_poll2['pred90_sw'], russia_poll2['pred50_sw'])

#print(top_issues)