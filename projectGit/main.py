import pandas as pd
from dateutil.parser import parse as parseDate
import matplotlib.pyplot as plt
import re
from matplotlib.widgets import Slider, RangeSlider
import numpy as np
from matplotlib.widgets import Button


class sliderFormatter:
    def __init__(self, format, datelist):
        self.strf = format
        self.datelist = datelist

    def __mod__(self, num):
        return self.datelist[int(num)].strftime(self.strf)

    def getDate(self, num):
        return self.datelist[int(num)]

# Getting votes between "start" and "end" dates
def slice_by_dt(data, start, end, ness_header):
    date_mask = (data['dt'] >= start) & (data['dt'] < end)
    slice_ = data.loc[date_mask, ness_header]
    return slice_

def graphByPeriodData(data, start, end, periods=10):
    # Soring by date
    data = data.sort_values(by='dt')

    slice = slice_by_dt(data, start, end, ['student', 'dt'])
    slice = slice.drop_duplicates(subset=['student'])

    # Splitting ["start", "end"] to "periods" parts
    datelist = pd.date_range(start, end, periods=periods + 1).tolist()
    pcount = [0] * (len(datelist) - 1)

    # Counting unique students voted in each period
    for i in range(len(datelist) - 1):
        period_mask = (slice.dt > datelist[i]) & (slice.dt < datelist[i + 1])
        period_slice = slice.loc[period_mask,['student']]
        pcount[i] = len(period_slice['student'])

    # Counting summary by each period
    pValues = [0]
    for x in range(len(pcount)):
        pValues.append(pValues[x] + pcount[x])
    pNames = [p.strftime("%m.%y") for p in datelist]

    return pNames, pValues


def graphByPeriod(data, st, en, timeTicks=100, minPeriods=2, maxPeriods=20, doAnnotations=True, periodsInit=10):
    start, end, periods = st, en, periodsInit
    datelist = pd.date_range(st, en, periods=timeTicks).tolist()
    formatter = sliderFormatter('%d-%m-%Y', datelist)

    fig, ax = plt.subplots()
    fig.suptitle('Количество Учащихся, Проголосовавших За Указанные Периоды')

    plt.subplots_adjust(left=0.25, bottom=0.3)

    def drawGraph(names, values):
        ax.cla()
        ax.set_xlabel('Список Периодов')
        ax.set_ylabel('Количество Проголосовавших')
        ax.grid(color='k', linestyle=':', linewidth=1)
        ax.plot(range(len(names)), values, 'ro-', snap=True)
        ax.xaxis.set_ticks(range(len(names)), names, rotation=45)
        if (doAnnotations):
            for x in range(len(names)):
                ax.annotate(
                    str(values[x]),
                    (x, values[x]),
                    textcoords="offset points",
                    xytext=(0, 10),
                    ha='center'
                )

    names, values = graphByPeriodData(data, start, end, periods)
    drawGraph(names, values)

    dates_slider = RangeSlider(
        ax=plt.axes([0.25, 0.1, 0.45, 0.03]),
        label='Time Period: ',
        valmin=0,
        valmax=timeTicks - 1,
        valstep=1,
        valfmt=formatter,
        valinit=(0, timeTicks),
    )

    period_slider = Slider(
        ax=plt.axes([0.1, 0.25, 0.0225, 0.63]),
        label="Slices: ",
        valmin=minPeriods,
        valmax=maxPeriods,
        valinit=periods,
        valstep=1,
        orientation="vertical"
    )

    def update(val):
        periods = period_slider.val
        start, end = dates_slider.val
        names, values = graphByPeriodData(
            data,
            formatter.getDate(start),
            formatter.getDate(end),
            periods
        )

        drawGraph(names, values)

        # fig.canvas.draw_idle()

    dates_slider.on_changed(update)
    period_slider.on_changed(update)

    plt.show()

def RatingGraphs(data, descriptions):
    rating = [ [0] * 5 for _ in range(13) ]
    for index, row in data.iterrows():
        rating[int(row['rtype']) - 1][int(row['rvalue']) - 1] += 1
    fig = plt.figure(figsize=(200, 200))
    fig.suptitle('Общие Распределения Оценок По Каждому Показателю')

    for index, row in descriptions.iterrows():
        labels = [x for x in range(1, 6)]
        for i in [x for x in row['descr'].split('. ')]:
            if i.count(' ') > 4:
                labels[int(i[0])-1] = i.replace(' ', '_', 3).replace(' ', '\n', 1).replace('_', ' ', 3)
                continue
            labels[int(i[0]) - 1] = i

        ax = fig.add_subplot(2, 7, index)
        ax.pie(rating[index-1], autopct='%.0f%%', pctdistance=1.4, radius=0.5)
        ax.legend(labels=labels, loc=8, fontsize=8, bbox_to_anchor=(0.5, -0.4))
        ax.set_title(row['name'].replace(' ', '\n', 2), y=0.9)
    fig.tight_layout()
    plt.show()

def Rtype_score(data):
    numTypes = 13

    mean_rtypes = [0] * numTypes
    for t in range(1, numTypes + 1):
        sample = data.loc[(data['rtype'] == t), ['rvalue']]
        mean_rtypes[t-1] = float(round(sample.mean(), 2))
    return mean_rtypes


def ComparisonPerYear(data, descriptions):
    sliced = data[["dt", "rtype", "rvalue"]]

    years = sorted(data['dt'].map(lambda x: x.year).drop_duplicates().to_list())
    types = descriptions['name'].to_list()

    date = parseDate(f'{years[0]}-01-01 00:00:00')
    ONE_YEAR = pd.DateOffset(years=1)
    anMeans = [0] * len(years)
    for j in range(len(years)):
        anMeans[j] = Rtype_score(slice_by_dt(sliced, date, date+ONE_YEAR, ["rtype", "rvalue"]))
        date += ONE_YEAR

    annualMeans = pd.DataFrame(np.transpose(anMeans), index=range(1, len(types)+1), columns=years)


    # creating plot
    min = annualMeans.to_numpy().min()
    max = annualMeans.to_numpy().max()

    plot = annualMeans.plot(kind="bar", title=f"Ежегодная Средняя Оценка По Каждому Показателю ({years[0]} - {years[-1]})",
                     grid=True, yticks=np.arange(min, max + 0.25, 0.25), ylim=(min, max + 0.25),
                     xlabel="Характеристика", ylabel="Оценка", use_index=True)
    plot.grid(linestyle=':', linewidth='1', color='k')
    plot.set_axisbelow(True)
    # adding some comment below the plot
    legend = ' '.join( [ f'{i + 1} - {types[i]};' for i in range(len(types)) ] )

    plt.figtext(0.5, 0.01, legend, wrap=True, horizontalalignment='center', fontsize=10)
    plt.show()

def GlobalRating(data):
    sliced = data.loc[(data["rtype"] == 1), ["dt", "rvalue"]]
    years = sorted(data['dt'].map(lambda x: x.year).drop_duplicates().to_list())

    date = parseDate(f'{years[0]}-01-01 00:00:00')
    ONE_YEAR = pd.DateOffset(years=1)
    anMeans = [0] * len(years)

    # calculating means
    for j in range(len(years)):
        anMeans[j] = round(slice_by_dt(sliced, date, date+ONE_YEAR, ["rvalue"])["rvalue"].mean(), 2)
        date += ONE_YEAR

    fig, ax = plt.subplots()
    fig.suptitle("Рейтинг Преподавательского Состава (2012 - 2022)")
    ax.cla()
    ax.set_xlabel("Годы")
    ax.set_ylabel("Средняя Оценка")
    ax.grid(color='k', linestyle=':', linewidth=1)
    ax.plot(range(len(years)), anMeans, 'ro-', snap=True)
    ax.xaxis.set_ticks(range(len(years)), years, rotation=45)
    for x in range(len(years)):
        ax.annotate(
            str(anMeans[x]),
            (x, anMeans[x]),
            textcoords="offset points",
            xytext=(0, 15),
            ha='center'
        )
    plt.show()

def staffGroups(data):
    slice_ = data[['staff', 'rtype', 'rvalue']]
    staffMeans = []
    for staff_ in slice_['staff'].unique():
        staffMeans.append([staff_, Rtype_score(slice_.loc[(data['staff'] == staff_), ['rtype', 'rvalue']])])
    return staffMeans
def MeanByPrior(staffMeans, byType):
    ResMean=[]
    for staffRt in staffMeans:
        StMean = []
        for i in range(len(byType)):
            if not pd.isna(staffRt[1][i]):
                for el in range(byType[i]):
                    StMean.append(staffRt[1][i])
        if len(StMean):
            ResMean.append([staffRt[0], float(round(np.mean(StMean), 2))])
        else:
            ResMean.append([staffRt[0], 0.0])
    return ResMean
def MeanByCrit(staffMeans, low=2.5, high=4.5):
    smdf = pd.DataFrame(staffMeans, columns=['staff', 'mean'])
    groups = {
        'low': smdf[smdf['mean'] < low]['staff'].tolist(),
        'avg': smdf[(smdf['mean'] < high) & (smdf['mean'] >= low)]['staff'].tolist(),
        'high': smdf[smdf['mean'] >= high]['staff'].tolist()
    }
    return groups

def GraphbyStaffGroups(data, byType=[1]*13, low=2.5, high=4.5):
    staffMeans = staffGroups(data)

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.5)
    fig.suptitle('Разделение преподавателей на группы по средней оценке')
    Slid = []
    CriteriaSlader = RangeSlider(ax=plt.axes([0.35, 0.34, 0.45, 0.02]),
                                 label='Критерии оценивания \n low - high',
                                 valmin=0,
                                 valmax=5,
                                 valstep=0.1,
                                 valinit=(low, high))

    k=0
    for i in range(len(byType)):
        k+=0.02
        Slid.append(Slider(plt.axes([0.25, k, 0.45, 0.01]), 'rtype:' + str(i+1), 0.0, 2.0, byType[i], valstep=1.0))
    button = Button(plt.axes([0.8, 0.025, 0.1, 0.04]), 'Calculate')

    def readySlider(event):
        ax.cla()
        ax.set_xlabel('Группы преподавателей')
        ax.set_ylabel('Количество преподавателей')
        for i in range(len(byType)):
            byType[i] = int(Slid[i].val)

        low, high = CriteriaSlader.val
        PriorMean = MeanByPrior(staffMeans, byType)
        groups = MeanByCrit(PriorMean, low, high)
        production = []
        color_ = []
        tick_ = []
        print('Приоритетность оценок:', byType)
        print('Критерии оценки преподавателей', CriteriaSlader.val)
        for k in groups.keys():
            production.append(len(groups[k]))
            tick_.append(str(k) + '\n Всего:' + str(production[-1]))
            print(tick_[-1], 'Первые преподаватели в группе: ', groups[k][:5])
            color_.append((production[-1] + 1)/300)
        tick_[0]+= '\n < {:.2f}'.format(low)
        tick_[2]+= '\n >= {:.2f}'.format(high)
        pl = ax.bar(tick_, production, color=color_, bottom=50, edgecolor="black")
        for bar in pl:
            plt.annotate(bar.get_height(), xy=(bar.get_x() - 2, bar.get_height() + 50), fontsize=7)
        plt.ylim([0, 300])
        plt.draw()

    # Call resetSlider function when clicked on button
    button.on_clicked(readySlider)
    CriteriaSlader.on_changed(readySlider)
    plt.show()


if __name__ == '__main__':
    headersSM = ["student", "staff", "dt", "rtype", "rvalue"]
    staffmarks = pd.read_csv('staffmarks.csv', names=headersSM, sep=';')[1:]
    staffmarks['dt'] = staffmarks['dt'].map(lambda x: parseDate(x))
    staffmarks=staffmarks.astype({"staff": str, "rtype": int, "rvalue": int})

    headersRD = ["rtype", "name", "descr"]
    ratingsdecsription = pd.read_csv('ratingsdecsription.csv', names=headersRD, sep=';', encoding='utf-16')[1:]
    ratingsdecsription = ratingsdecsription.astype({"rtype": int, "name": str, "descr": str})
    graphByPeriod(data=staffmarks, st=parseDate('2012-01-01'), en=parseDate('2022-12-31'))
    RatingGraphs(staffmarks, ratingsdecsription)
    ComparisonPerYear(data=staffmarks, descriptions=ratingsdecsription)
    GlobalRating(data=staffmarks)
    GraphbyStaffGroups(data=staffmarks)

