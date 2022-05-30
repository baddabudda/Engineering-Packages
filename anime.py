import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.axes_grid1.inset_locator as mpl_il
from pandas.core.dtypes.common import is_numeric_dtype

# ===== 1 =====
animeList = pd.DataFrame(pd.read_csv('anime (1).csv', na_values=['?','-'], thousands=','))
animeList['Airdate'] = animeList['Airdate'].str.replace(' (JST)', '-0900')
animeList['Airdate'] = pd.to_datetime(animeList['Airdate'], errors='coerce')
# ===== 2 =====
print(animeList['Airdate'].head(10))
# ===== 3 =====
for column in animeList.columns:
    print('column name:', column, ';', 'column type:', animeList[column].dtypes, sep=' ')
# ===== 4 =====
animeList.rename(columns=str.lower, inplace=True)
# for column in animeList.columns:
#     print('column name:', column)
animeList['title'] = animeList['title'].astype('string')
for i in range(0, animeList['title'].size):
    animeList['title'][i] = animeList['title'][i].replace(' ', '_')
# ===== 5 =====
for column in animeList.columns:
    if is_numeric_dtype(animeList[column]):
        print(animeList[column].describe())
# ===== 6 =====
for column in animeList.columns:
    if not is_numeric_dtype(animeList[column]):
        print(animeList[column].value_counts())
# ===== 8 =====
fig = plt.figure('Production')
pr = animeList['production'].value_counts()[:30]
pr.plot.barh()
fig = plt.figure('Episodes')
ep = animeList['episodes'].value_counts()[:30]
ep.plot.barh()
fig = plt.figure('Source')
sr = animeList['source'].value_counts()[:30]
sr.plot.barh()
fig = plt.figure('Theme')
fig = plt.figure('Theme')
masked = set(animeList['theme'])
et = set()
for comb in masked:
    if type(comb) == str:
        for s in comb.split(','):
            et.add(s)
genre = dict()
for gen in et:
    genre[gen] = animeList['theme'].str.contains(gen, na=False, regex=False).sum()
t = list()
for key in genre:
    t.append((key, genre[key]))
t = sorted(t, key = lambda x: x[1])
val = list()
label = list()
for tup in t:
    label.append(tup[0])
    val.append(tup[1])
plt.barh(range(len(t)), val, tick_label=label)
fig = plt.figure('Year')
yer = animeList['airdate'].groupby(animeList['airdate'].dt.year).count()
print(yer)
yer.plot.barh()
# ===== 9 =====
companies = animeList['rating'].groupby(animeList['production']).mean()
companies.sort_values(ascending=False, inplace=True)
print(companies)
fig = plt.figure('Mean Company Rating')
companies[:30].plot.barh()
# ===== 10 =====
fig = plt.figure('Rating Intervals')
rt = animeList['rating'].groupby(by=(animeList['rating'].apply(np.floor)), dropna=True).count()
rt.plot.barh()
# ===== 11 =====
fig = plt.figure('Themes Average Rating')
masked = set(animeList['theme'])
et = set()
for comb in masked:
    if type(comb) == str:
        for s in comb.split(','):
            et.add(s)
genre = dict()
for gen in et:
    genre[gen] = animeList['rating'].where(animeList['theme'].str.contains(gen, na=False, regex=False)).mean()
t = list()
for key in genre:
    t.append((key, genre[key]))
t = sorted(t, key=lambda x: x[1])
val = list()
label = list()
for tup in t:
    label.append(tup[0])
    val.append(tup[1])
plt.barh(range(len(t)), val, tick_label=label)
#
fig = plt.figure('Genres Average Rating')
masked = set(animeList['genre'])
et = set()
for comb in masked:
    if type(comb) == str:
        for s in comb.split(','):
            et.add(s)
genre = dict()
for gen in et:
    genre[gen] = animeList['rating'].where(animeList['theme'].str.contains(gen, na=False, regex=False)).mean()
t = list()
for key in genre:
    t.append((key, genre[key]))
t = sorted(t, key=lambda x: x[1])
val = list()
label = list()
for tup in t:
    label.append(tup[0])
    val.append(tup[1])
plt.barh(range(len(t)), val, tick_label=label)
# ===== 12 =====
fig = plt.figure('Correlation: Voters/Rating')
x = list(animeList['voters'])
y = list(animeList['rating'])
plt.plot(x, y)
plt.xlabel('Voters')
plt.ylabel('Rating')

plt.show()
