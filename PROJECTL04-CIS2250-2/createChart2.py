'''
createChart2.py
  Author(s): Anthony Perez-Carey (1137637), Ben Turner-Theijsmeijer (1152536), Connor Schulz (1103003) Matthew Biggins (1136122)

  Project: CIS2250 group project (Kolkata)
  Date of Last Update: April 1, 2021.

  Functional Summary
       createChart2.py reads a CSV file and saves
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
  #get comand line arguments
  csv_filename = argv[1]
  try:
    graphics_filename = argv[2]
  except IndexError:
    graphics_filename = "Q2_Graph.pdf"

  #open csv file
  try:
      csv_df = pd.read_csv(csv_filename)

  except IOError as err:
      print("Unable to open source file", csv_filename,
              ": {}".format(err), file=sys.stderr)
      sys.exit(-1)

  fig = plt.figure()
  #plot unemployment data
  ax = sns.lineplot(x = "Date", y = "Average_Electric_Usage",data=csv_df,legend='full')
  sns.lineplot(x = "Date", y = "Average_Water_Usage",data=csv_df,legend='full')
  ax.legend(["Average_Electric_Usage","Average_Water_Usage"],loc=(1.2,0.6), title="")
  #rotate x axis labels 45 degrees
  plt.xticks(rotation = 45, ha = 'right')
  '''
  #set the location of the legend
  ax.legend(loc=(1.2,0.6), title="Age Groups")
  '''
  #creates twin axes sharing the "x" axes
  ax2 = ax.twinx()
  

  #plot covid case data
  covidPlot = sns.lineplot(x = "Date", y = "Cases", ax=ax2, color='pink', linewidth=3, data=csv_df,legend='full')
  
  #set the location of the legend
  covidPlot.legend(["Covid Cases"],loc=(1.2,0.5), title="")
  
  #set title and axes labels
  ax.set_title("Water and Electric Usage vs Covid Cases in Ontario")
  ax.set(xlabel="Date", ylabel="Average Usage per Month")
  ax2.set(ylabel="Total Covid Cases")

  
  #save file
  fig.savefig(graphics_filename, bbox_inches="tight")
  
main(sys.argv)