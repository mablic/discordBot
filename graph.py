import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import os
import re
import datetime
import matplotlib.colors as mcolors
from datetime import datetime, timedelta


def func(pct, allvals):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return "{:.1f}%\n({:d} mins)".format(pct, absolute)

class Graph:

    def __init__(self) -> None:
        self.dataDateFormat = '%Y-%m-%d'
        self.dateFormat = '%Y-%m-%d %H-%M-%S'
        self.filePath = ''

    def get_graph(self, df, userID='0', interval='day', type='line'):

        df.fillna(0)
        columns = df.columns.values.tolist()
        # group by day, week, month
        if interval == 'week':
            df.reset_index()
            df['studyTime'] = df['studyTime'].apply(lambda x : datetime.strftime(datetime.strptime(x, self.dataDateFormat) + timedelta(days=-datetime.strptime(x, self.dataDateFormat).weekday(), weeks=0),self.dataDateFormat))
            df.set_index('studyTime')
        elif interval == 'month':
            df.reset_index()
            df['studyTime'] = df['studyTime'].apply(lambda x : datetime.strftime(datetime.strptime(x,self.dataDateFormat).replace(day=1),self.dataDateFormat))
            df.set_index('studyTime')
        else:
            pass
        df = df.groupby('studyTime')[columns].sum()
        # print(df)

        fig, ax = plt.subplots()
        cCode = [key for key in mcolors.BASE_COLORS]
        if type == 'line':
            # line graph
            # plt.figure(figsize=(5, 2.7), layout='constrained')
            for (columnName, columnData) in df.iteritems():
                ax.plot(df.index, columnData.values, label=columnName)
        elif type == 'bar':
            # bar graph
            width = 0.35
            for i in range(len(df.columns.tolist())):
                if i == 0:
                    ax.bar(df.index, df.iloc[:,i].tolist(), width, color=cCode[i], align = 'center', label=df.columns[i])
                else:
                    ax.bar(df.index, df.iloc[:,i].tolist(), width, color=cCode[i], align = 'center', bottom=df.iloc[:,i-1], label=df.columns[i])
                    df[columns[i+1]] = df[[columns[i], columns[i+1]]].values.max(1)
        else:
            type = 'line'

        plt.gcf().autofmt_xdate()
        plt.xlabel('date')
        plt.ylabel('minutes')
        plt.title("Study Summary by " + interval)
        plt.legend()
        filename = self.save_file(userID, interval)
        plt.savefig(filename)
        return filename
    
    def save_file(self, userID='', interval=''):
        filename = os.getcwd() + '/images/user_' + userID + '_' \
            + interval + '_' + datetime.strftime(datetime.now(),self.dateFormat) + '.png'
        self.filePath = filename
        return filename

    def remove_file(self, filePath):
        os.remove(self.filePath)

    def __del__(self):
        pass
        # os.remove(self.filePath)

    def get_public_graph(self, df, userID='0', day=datetime.strftime(datetime.now(),'%Y-%m-%d')):

        m = re.compile(r'[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}')
        if not m.match(day):
            day = datetime.strftime(datetime.now(), self.dataDateFormat)

        try:
            df.fillna(0)
            columns = df.columns.values.tolist()
            df = df.groupby('studyTime')[columns].sum()
            df = df.loc[day]
        except Exception as e:
            print(f"Keys {day} error with message: {str(e)}.")
            return "No data found!"

        labels = list(df.keys())
        sizes = df.tolist()
        explode = tuple([0.1 if x==max(sizes) else 0 for x in sizes])

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct=lambda pct: func(pct, sizes),
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.gcf().autofmt_xdate()
        plt.title("Study Summary")
        plt.legend()
        filename = self.save_file(userID, 'pie')
        plt.savefig(filename)
        return filename

if __name__ == '__main__':
    
    pass
    # df = pd.DataFrame({'studyTime': ['01/02/2022', '01/04/2022','01/03/2022', '01/04/2022','01/04/2022'],'FRM': [380, 370, 24, 26,21], 'CFA': [np.nan, 370, np.nan, 26,18], 'CPA': [12, 45, 32, 41,5]})
    # df.fillna(0)
    # columns = df.columns.values.tolist()
    # df = df.groupby('studyTime')[columns].sum()
    # df = df.loc['01/04/2022']
    # print(df)

    # labels = list(df.keys())
    # sizes = df.tolist()
    # explode = tuple([0.1 if x==max(sizes) else 0 for x in sizes])

    # fig1, ax1 = plt.subplots()
    # ax1.pie(sizes, explode=explode, labels=labels, autopct=lambda pct: func(pct, sizes),
    #         shadow=True, startangle=90)
    # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # plt.gcf().autofmt_xdate()
    # plt.legend()
    # plt.title("Study Summary")
    # plt.show()
