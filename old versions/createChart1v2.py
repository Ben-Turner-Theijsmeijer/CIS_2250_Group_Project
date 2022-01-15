#!/usr/bin/env python

'''
createChart1.py
  Author(s): Connor Schulz

  Project: CIS2250 group project (Kolkata)
  Date of Last Update: Mar 31, 2021.

  Functional Summary
      createChart1.py reads a string in csv format and filename and saves a 
      chart with the csv data to a file with filename

'''

#import libraries
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

def createChart(dataString, fileName):

  #read string as csv
  csv_df = pd.read_csv(dataString)

  fig = plt.figure()

  unemploymentData = csv_df.pivot("DATE", "AGE", "UNEMPLOYMENT_DURATION")
  unemploymentData.head()

  #plot unemployment data
  ax = sns.lineplot(data=unemploymentData,legend='full')
  
  #rotate x axis labels 45 degrees
  plt.xticks(rotation = 45, ha = 'right')
  #set the location of the legend
  ax.legend(loc=(1.2,0.6), title="Age Groups")

  #creates twin axes sharing the "x" axes
  ax2 = ax.twinx()
  
  #plot covid case data
  covidPlot = sns.lineplot(x = "DATE", y = "CASES", ax=ax2, color='pink', linewidth=3, data=csv_df,legend='full')
  
  #set the location of the legend
  covidPlot.legend(["Covid Cases"],loc=(1.2,0.5), title="")
  
  #set title and axes labels
  ax.set_title("Average Unemployment Duration vs Covid Cases in Ontario")
  ax.set(xlabel="Date", ylabel="Average Unemployment Duration (Weeks)")
  ax2.set(ylabel="Total Covid Cases")
  
  
  #save file
  fig.savefig(fileName, bbox_inches="tight")



