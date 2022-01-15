#!/usr/bin/env python

'''
createChart1.py
  Author(s): Connor Schulz

  Project: CIS2250 group project (Kolkata)
  Date of Last Update: Mar 30, 2021.

  Functional Summary
      createChart1.py reads a CSV file and saves
      a plot based on the data to a PDF file.

     Commandline Parameters: 2
        sys.argv[0] = name of file to read
        sys.argv[1] = name of graphics file to create
'''

#import libraries
import sys
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

def main(argv):
  #check to see if the correct number of command line args are present. Stop execution with a usage message if not.
  if len(argv) < 2 or len(argv) > 3:
    print("Usage: \"data filename\" \"output name\"\n\nRequired Fields: \"data filename\"\nDefaults: \"output name\" = chart1.pdf")
    sys.exit()

  #get command line args
  csv_filename = argv[1]
  try:
    graphics_filename = argv[2]
  except IndexError:
    graphics_filename = "chart1.pdf"

  #open the csv file
  try:
      csv_df = pd.read_csv(csv_filename)

  except IOError as err:
      print("Unable to open source file", csv_filename,
              ": {}".format(err), file=sys.stderr)
      sys.exit(-1)



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
  fig.savefig(graphics_filename, bbox_inches="tight")



main(sys.argv)