import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('titanic.csv')

classes = ['cool dudes','middle ish','pathetic']
fig = plt.figure('every')

classesCount = df['Pclass'].value_counts().sort_index()
plt.subplot(1, 3, 1)
plt.bar(range(len(classesCount)), classesCount.values, tick_label = classes)
plt.title('all', fontsize=10)

classesCountAlive = df['Pclass'].where(df['Survived'] == 1).value_counts().sort_index()
plt.subplot(1, 3, 2)
plt.bar(range(len(classesCountAlive)), classesCountAlive.values, tick_label = classes)
plt.title('alive', fontsize=10)

classesCountDead = df['Pclass'].where(df['Survived'] == 0).value_counts().sort_index()
plt.subplot(1, 3, 3)
plt.bar(range(len(classesCountDead)), classesCountDead.values, tick_label = classes)
plt.title('dead', fontsize=10)

fig = plt.figure('gender')
genders = df['Sex'].value_counts().sort_index()
plt.subplot(1, 3, 1)
genders.plot.bar()
plt.xticks(rotation=60, fontsize=10)
plt.title('genders', fontsize=10)

genders = df['Sex'].where(df['Survived'] == 1).value_counts().sort_index()
plt.subplot(1, 3, 2)
genders.plot.bar()
plt.xticks(rotation=60, fontsize=10)
plt.title('genders alive', fontsize=10)

genders = df['Sex'].where(df['Survived'] == 0).value_counts().sort_index()
plt.subplot(1, 3, 3)
genders.plot.bar()
plt.xticks(rotation=60, fontsize=10)
plt.title('genders dead', fontsize=10)

fig, axs = plt.subplots(1, 1)
axs.remove()
genders = [0] * 2
genders[0] = df['Sex'].where(df['Survived'] == 0).value_counts().sort_index()
genders[1] = df['Sex'].where(df['Survived'] == 1).value_counts().sort_index()
plt.table(cellText=genders, loc = 'center', rowLabels = ['male','female'], colLabels = ['alive','dead'])


plt.show()
