import os.path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import re
import matplotlib.ticker as mticker
from matplotlib.dates import HourLocator, DateFormatter,DayLocator,MonthLocator


from datetime import datetime

from pandas import read_csv



def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def makeDailyCharts(x):
    xcopy = x.copy()
    for c in xcopy.select_dtypes(include=np.number).columns:
        stro = 1

        for s in xcopy["date"].dt.date.unique():
            strs = s.strftime("%Y%m%d")
            if stro == 1:
                stro = strs
                t = s
                continue
            daily = xcopy.query("date <= " + strs + " & date >" + stro)
            title = str(c) + " " + stro

            plt.clf()
            plot = sns.lineplot(daily,x="date", y=c)

            #plot.xaxis.set_major_locator(mticker.MaxNLocator(9))
            #ticks_loc = plot.get_xticks().tolist()
            #plot.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
            #plot.set_xticklabels([label_format(h=c) for c in range(0,24,24/ticks_loc.count())])

            plot.xaxis.set_major_locator(HourLocator(interval=2))
            plot.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

            plt.title(title)
            plt.xlabel("Hour")
            plt.ylabel("Power(kwph)")
            plt.xticks(rotation='vertical')
            #plt.locator_params(axis='x', nbins=10)
            plt.tight_layout()
            sns.set_theme(style="whitegrid")



            make_dir(".\Daily Usage\\Customer " +str(c))

            plt.savefig(".\Daily Usage\\Customer " +str(c)+"\\"+ title + ".png")
            t = s
            stro = strs      
    return

def makeMonthlyCharts(x):
    xCopy = x.copy()
    yCopy = x.copy()
    xCopy["date"]= [v.replace(day=1) for v in x["date"].dt.date]
    
    for c in xCopy.select_dtypes(include=np.number).columns:
        
        t= 1
        for s in xCopy["date"].unique()[::-1]:
            Monthly = 0
            if t == 1:
                Monthly = yCopy.query("date > @s")
            else: 
                Monthly = yCopy.query("date > @s & date < @t")
                
            
            title = "Meter Number " + str(c) + " {m}-{y}".format(m=s.strftime("%B"),y=str(s.year))

            plt.clf()
            plot = sns.lineplot(Monthly,x="date", y=c)

            plot.xaxis.set_major_locator(DayLocator(interval=2))
            plot.xaxis.set_major_formatter(DateFormatter('%m-%d-%Y'))

            plt.title(title)
            plt.xlabel("Day")
            plt.ylabel("Power(kw)")
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            sns.set_theme(style="whitegrid")

            make_dir(".\Monthly Usage\\Meter Number " +str(c))
            plt.savefig(".\Monthly Usage\\Meter Number " +str(c)+"\\"+ title + ".png")
            t = s   
    return

def makeAnnualCharts(x):
    xCopy = x.copy()
    
    for c in xCopy.select_dtypes(include=np.number).columns:
            
            title = "Meter Number " + str(c) + " {y}".format(y=str(s.year))

            plt.clf()
            plot = sns.lineplot(xCopy,x="date", y=c)

            plot.xaxis.set_major_locator(MonthLocator(interval=1))
            plot.xaxis.set_major_formatter(DateFormatter('%m-%d-%Y'))

            plt.title(title)
            plt.xlabel("Month")
            plt.ylabel("Power(kw)")
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            sns.set_theme(style="whitegrid")

            make_dir(".\Annual Usage\\Meter Number " +str(c))
            plt.savefig(".\Annual Usage\\Meter Number " +str(c)+"\\"+ title + ".png")  
    return

def main():
    data = read_csv("2021-all-meter.csv", index_col= 0)

    data['AMI Meter ID'] =  pd.to_datetime(data['AMI Meter ID'], format='%Y-%m-%d %H:%M:%S')
    data['date'] =  pd.to_datetime(data['date'], format='%Y-%m-%d %H:%M:%S')

    for i in data.select_dtypes(include=np.number).columns:
        makeDailyCharts(data,i)
        makeMonthlyCharts(data,i)
        makeAnnualCharts(data,i)

    return

if __name__ == "__main__":
    main()
