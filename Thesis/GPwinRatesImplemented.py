import matplotlib.pyplot as plt
import random as rng
import pandas as pd
import csv
import seaborn as sb


# similar to 'GPwinRates.py, but only counts times when the given class approved of the policy'
data = pd.read_stata('Gilens_Page.dta')
data.to_csv('Gilens_Page.csv')

with open('Gilens_Page.csv') as gp:
    # open data file
    csv_reader = csv.reader(gp, delimiter = ',')
    # make list of column names
    colNames = []
    for row in csv_reader:
        colNames.append(row)
        break
    # note where income differences appear
    ind = colNames[0].index('pred10_sw')
    # note outcome coding
    outcome = colNames[0].index('OUTCOME')
    # note issue area
    category = colNames[0].index('XL_AREA')
    incomeCols = [ind, ind + 1, ind + 2, ind + 3, ind + 4]
    wins = [0,0,0,0,0]
    # skip first row
    first = True
    # i,j is the portion of times income group i won when challenging j
    winHeatmap = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    skips = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    disagreementCount = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    for row in csv_reader:
        if first:
            first = False
        else:
            for i in range(5):
                for j in range(5):
                    # if no data for one group missing, skip
                    if row[incomeCols[i]] == '' or row[incomeCols[j]] == '':
                        skips[i][j] += 1
                    else:
                        # if i wants change but j does not
                        if ((float(row[incomeCols[i]]) >= 0.5) & (float(row[incomeCols[j]]) < 0.5)):
                            # increment disagreement count
                            disagreementCount[i][j] += 1

                            # if change was made, reward i
                            if (float(row[outcome]) > 0):
                                winHeatmap[i][j] += 1

    for i in range(5):
        for j in range(5):
            if (disagreementCount[i][j] != 0):
                winHeatmap[i][j] = winHeatmap[i][j] / disagreementCount[i][j]
    print(disagreementCount)
    print(skips)
    print(winHeatmap)
    sb.heatmap(data=winHeatmap, annot=True)
    plt.show()