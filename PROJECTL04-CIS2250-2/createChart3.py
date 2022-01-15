'''
createChart3.py
  Author(s): Anthony Perez-Carey (1137637), Ben Turner-Theijsmeijer (1152536), Connor Schulz (1103003) Matthew Biggins (1136122)

  Project: CIS2250 group project (Kolkata)
  Date of Last Update: March 30, 2021.

  Functional Summary
       createChart3.py reads a CSV file and saves
       a plot based on the data to a PDF file.
      
     Commandline Parameters: 2
        sys.argv[0] = name of file to read
        sys.argv[1] = name of graphics file to create
'''
import sys
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

def main(argv):
  csv_filename = argv[1]
  graphics_filename = argv[2] 


  #open the csv file
  try:
      csv_df = pd.read_csv(csv_filename)

  except IOError as err:
      print("Unable to open source file", csv_filename,
              ": {}".format(err), file=sys.stderr)
      sys.exit(-1)

  fig = plt.figure()
  schoolData = csv_df.pivot("Date", "Municipality", "Count")
  schoolData.head()

  #plot covid case data
  ax = sns.lineplot(data=schoolData,legend='full')

  #change x-axis to display every 20 days
  ax.set_xticks(ax.get_xticks()[::20])

  plt.xticks(rotation = 45, ha = 'right')

  #save file
  fig.savefig(graphics_filename, bbox_inches="tight")

main(sys.argv)