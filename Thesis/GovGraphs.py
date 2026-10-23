import matplotlib.pyplot as plt
import random as rng
import pandas as pd
import csv
import seaborn as sb

data = pd.read_stata('Gilens_Page.dta')
data.to_csv('Gilens_Page.csv')

with open('Gilens_Page.csv') as gp:
    csv_reader = csv.reader(gp, delimiter = ',')
    colNames = []
    for row in csv_reader:
        colNames.append(row)
        break
    ind = colNames[0].index('pred10_sw')
    outcome = colNames[0].index('OUTCOME')
    category = colNames[0].index('XL_AREA')
    incomeCols = [ind, ind + 1, ind + 2, ind + 3, ind + 4]
    wins = [0,0,0,0,0]
    first = True
    rowCounter = 0
    '''
    for row in csv_reader:
        if first:
            first = False
        else:
            for i in incomeCols:
                if row[i] == '':
                    pass
                else:
                    if  (float(row[outcome]) > 0) & (row[category] == 'taxation'):
                        rowCounter += 1
                        for i in range(5):
                            if float(row[incomeCols[i]]) > 0.5:
                                wins[i] += 1

    for i in range(5):
        wins[i] = wins[i] / rowCounter
    print(wins)
    print(rowCounter)
    '''
    heat = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    rowCounter = 0
    first = True
    for row in csv_reader:
        if first == True:
            first = False
        else:
            for i in incomeCols:
                if row[i] == '':
                    pass
                else:
                    #rowCounter += 1
                    for i in range(5):
                        for j in range(5):
                            if (float(row[incomeCols[i]]) >= 0.5) & (float(row[incomeCols[j]]) > 0.5):
                                rowCounter += 1
                                heat[i][j] += 1
                            elif(float(row[incomeCols[i]]) < 0.5) & (float(row[incomeCols[j]]) <= 0.5):
                                rowCounter += 1
                                heat[i][j] += 1

    for i in range(5):
        for j in range(5):
            heat[i][j] = heat[i][j] / rowCounter[i][j]
print(heat)
sb.heatmap(data=heat, annot=True)
plt.show()
    
