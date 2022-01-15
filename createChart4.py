'''
createChart4.py
  Author(s): Anthony Perez-Carey (1137637), Ben Turner-Theijsmeijer (1152536), Connor Schulz (1103003) Matthew Biggins (1136122)

  Project: CIS2250 group project (Kolkata)
  Date of Last Update: April 1, 2021.

  Functional Summary
       createChart4.py reads a CSV file and saves
      a plot based on the data to a PDF file.
      
     Commandline Parameters: 2
        sys.argv[0] = name of file to read
        sys.argv[1] = name of graphics file to create
  Example Run:
    python createChart4.py q4_output.csv q4_chart.pdf
'''

#   Packages and modules
import sys
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


def main(argv):

    #   Check that we have been given the right number of parameters
    if len(argv) != 3:
        print("Usage:",
                "createChart4.py <data file> <graphics file>")
        sys.exit(-1)

    csv_filename = argv[1]
    graphics_filename = argv[2]

    # Open the data file using "pandas", which will attempt to read
    # in the entire CSV file
    try:
        csv_df = pd.read_csv(csv_filename)

    except IOError as err:
        print("Unable to open source file", csv_filename,
                ": {}".format(err), file=sys.stderr)
        sys.exit(-1)
    csv_df["total"] = csv_df.Resolved_Cases + csv_df.Fatal_Cases
    print(csv_df)

    #Set general plot properties
    sns.set_style("white")
    sns.set_context({"figure.figsize": (24, 10)})

    f = plt.figure()

    #Plot 1 - background - "total" (top) series
    sns.barplot(x = csv_df.Age_Group, y = csv_df.total, color = "red")

    #Plot 2 - overlay - "bottom" series
    sns.barplot(x = csv_df.Age_Group, y = csv_df.Resolved_Cases, color = "#0000A3")

    # add graph title and axis labels
    plt.title('Effect Age has on the Mortality Rates of COVID-19 for a Specified Gender and Public Health Unit', fontsize= 20)
    plt.xlabel('Age Group (Years)', fontsize= 16)
    plt.ylabel('Total COVID-19 Cases', fontsize= 16)

    topbar = plt.Rectangle((0,0),1,1,fc="red", edgecolor = 'none')
    bottombar = plt.Rectangle((0,0),1,1,fc='#0000A3',  edgecolor = 'none')
    l = plt.legend([bottombar, topbar], ['Resolved Cases', 'Fatal Cases'], loc=1, ncol = 2, prop={'size':16})
    l.draw_frame(False)

    sns.despine(left=True, bottom=True)

    
    f.savefig(graphics_filename, bbox_inches="tight")

main(sys.argv)

