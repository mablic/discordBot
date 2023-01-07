import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import os
import datetime
import matplotlib.colors as mcolors
from datetime import datetime, timedelta


# matplotlib.use('Agg')

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
        print(df)

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
        filename = os.getcwd() + '/images/user_' + userID + '_' \
            + interval + '_' + datetime.strftime(datetime.now(),self.dateFormat) + '.png'
        plt.legend()
        plt.savefig(filename)
        self.filePath = filename
        return filename

    def remove_file(self, filePath):
        os.remove(self.filePath)

    def __del__(self):
        pass
        # os.remove(self.filePath)


if __name__ == '__main__':
    
    pass