import matplotlib.pyplot as plt
import random as rng
import pandas as pd
import csv
import seaborn as sb
import numpy as np
import os

df = pd.read_stata('year_dta_files/NES1992.dta')
grps = df.groupby('V900326')
for name, group in grps:
    print(type(name))