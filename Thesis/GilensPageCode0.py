import matplotlib.pyplot as plt
import random as rng
import pandas as pd
import csv
import seaborn as sb


with open('Gilens_Page.csv') as gp:
    csv_reader = csv.reader(gp, delimiter = ',')
    colNames = []
    for row in csv_reader:
        colNames.append(row)
        break
    policyCategories = []
    ind = colNames[0].index('pred10_sw')
    outcome = colNames[0].index('OUTCOME')
    category = colNames[0].index('XL_AREA')
    incomeCols = [ind, ind + 1, ind + 2, ind + 3, ind + 4]
    wins = [0,0,0,0,0]
    rowCounter = 0
    policyCategories = ['taxation', 'foreign pol', 'soc welfare', 
                        'environment', 'govt reform', 'econ & labor', 
                        'camp finance', 'defense', 'misc others', 
                        'welf reform', 'budget', 'health', 'race', 
                        'religious', 'guns', 'civil rts', 'terrorism', 
                        'immigration', 'education']
    winRates = []
    l = len(policyCategories)
    catCounter = [0]*l
    polCatDict = {}
    for i in range(l):
        polCatDict[policyCategories[i]]= i
    for i in range(l):
        winRates.append([0]*5)
    #construct catCounter, winRates
    first = True
    for row in csv_reader:
        if first:
            first = False
        else:
            for i in incomeCols:
                if row[i] == '':
                    pass
                else:
                    if (float(row[i]) >= 0.5) & (float(row[outcome]) > 0):
                        winRates[polCatDict[row[category]]][i - ind] += 1
                    elif (float(row[i]) <= 0.5) & (float(row[outcome]) == 0):
                        winRates[polCatDict[row[category]]][i - ind] += 1
                #print(polCatDict[row[category]])
            catCounter[polCatDict[row[category]]] += 1
    for i in range(l):
        for j in range(5):
            winRates[i][j] = winRates[i][j] / catCounter[i]
    print(policyCategories)
    print(winRates)
    print(catCounter)
'''
[[0.5699300699300699, 0.5664335664335665, 0.548951048951049, 0.5384615384615384, 0.5559440559440559], taxation, N = 286
 [0.5132450331125827, 0.5165562913907285, 0.5562913907284768, 0.5695364238410596, 0.5993377483443708], foreign pol, N = 302
 [0.6102941176470589, 0.5588235294117647, 0.5147058823529411, 0.49264705882352944, 0.45588235294117646], soc welfare, N = 136
 [0.6984126984126984, 0.6984126984126984, 0.6825396825396826, 0.6666666666666666, 0.6507936507936508], environment, N = 63
 [0.5384615384615384, 0.5384615384615384, 0.5384615384615384, 0.5128205128205128, 0.5128205128205128], govt reform, N = 39
 [0.6160714285714286, 0.5982142857142857, 0.625, 0.625, 0.6517857142857143], econ & labor, N = 112
 [0.296875, 0.296875, 0.3125, 0.28125, 0.21875], camp finance, N = 64
 [0.546875, 0.578125, 0.625, 0.640625, 0.671875], defense, N = 64
 [0.46153846153846156, 0.46153846153846156, 0.47863247863247865, 0.49572649572649574, 0.49572649572649574], misc others, N = 117
 [0.5873015873015873, 0.6349206349206349, 0.6349206349206349, 0.7142857142857143, 0.7301587301587301], welf reform, N = 63
 [0.2, 0.2, 0.12, 0.12, 0.16], budget, N = 25
 [0.4177215189873418, 0.3987341772151899, 0.3987341772151899, 0.3987341772151899, 0.3924050632911392], health, N = 158
 [0.7, 0.65, 0.6, 0.6, 0.65], race, N = 20
 [0.48936170212765956, 0.46808510638297873, 0.5, 0.5212765957446809, 0.48936170212765956], religious, N = 94
 [0.36, 0.42, 0.43, 0.43, 0.41], guns, N = 100
 [0.5434782608695652, 0.5869565217391305, 0.6086956521739131, 0.6521739130434783, 0.6956521739130435], civil rts, N = 46
 [0.5882352941176471, 0.6235294117647059, 0.6352941176470588, 0.6352941176470588, 0.6352941176470588], terrorism, N = 85
 [0.4782608695652174, 0.391304347826087, 0.30434782608695654, 0.34782608695652173, 0.391304347826087], immigration, N = 23
 [0.5076923076923077, 0.5538461538461539, 0.5692307692307692, 0.6153846153846154, 0.5692307692307692]] education, N = 65
'''
#from 0:
#Wealthy win more: Foreign pol 302, Defence 64, Welf Reform 63, civil rights 46
#Slightly: econ & labor 112

#Poor win more: Soc Welfare 136, 
#Slightly: environment 63, immigration 23,

