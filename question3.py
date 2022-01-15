#!/usr/bin/env python

'''
question3.py
  Author(s): Anthony Perez-Carey (1137637), 
             Ben Turner-Theijsmeijer (1152536), 
             Connor Schulz (1103003) Matthew Biggins (1136122)

  Project: CIS2250 group project (Kolkata)
  Question: How does the number of Covid cases in schools compare 
            between municipalities in Ontario?

  Date of Last Update: March 25, 2021.

  Functional Summary
    question3.py takes two municipalites as command line arguments and compares
    the number of covid cases in public schools between them
  Commandline Parameters: 2
    argv[1] = municipality1
    argv[2] = municipality2
  Example Run:
    python question3.py ottawa waterloo > q3_output.txt
    python createChart3.py q3_output.txt q3_chart.pdf

'''

#import libraries
import sys
import csv

INDEX_MAP = {
        "collected_date" : 0,
        "reported_date" : 1,
        "school_board" : 2,
        "school_id" : 3,
        "school" : 4,
        "municipality" : 5,
        "confirmed_student_cases" : 6,
        "confirmed_staff_cases" : 7,
        "confirmed_unspecified_cases" : 8,
        "total_confirmed_cases" : 9}

def main(argv):

  filename = "datasets/schoolsactivecovid.csv"
  # check to make sure there are the correct number of parameters
  if len(argv) != 3:
    print("Usage: <municipality#1> <municipality#2>")
    sys.exit(1)
  
  # assign args to a variable
  municipality1 = argv[1]
  municipality2 = argv[2]
  municipality1.lower()
  municipality1.lower()

  casesMunicipality1 = 0
  casesMunicipality2 = 0

  arrayMunicipality1 = []
  arrayMunicipality2 = []
  dates = []

  # open the file
  try:
    fh = open(filename, encoding="utf-8-sig")
    
  except IOError as err:
    print("Unable to open file '{}' : {}".format(
            filename, err), file=sys.stderr)
    sys.exit(1)

  data_reader = csv.reader(fh)
  next(data_reader)
  # first date in file
  currentDate = "2020-09-10"
  # read all rows of the file
  for row in data_reader:
    previousDate = currentDate
    # update the current date
    currentDate = row[INDEX_MAP["collected_date"]]
    # checks if the date has changed since the previous row
    if (currentDate != previousDate):
      # adds the daily cases to the appropriate array
      arrayMunicipality1.append(casesMunicipality1)
      arrayMunicipality2.append(casesMunicipality2)
      casesMunicipality1 = 0
      casesMunicipality2 = 0
      dates.append(currentDate)
    # checks if the rows municipality matches the first input municipality
    if (row[INDEX_MAP["municipality"]]).lower() == municipality1:
      casesMunicipality1 = casesMunicipality1 + int(row[INDEX_MAP["total_confirmed_cases"]])
    # checks if the rows municipality matches the second input municipality
    elif (row[INDEX_MAP["municipality"]]).lower() == municipality2:
      casesMunicipality2 = casesMunicipality2 + int(row[INDEX_MAP["total_confirmed_cases"]])

  print("Date,Municipality,Count")
  for i in range(len(dates)):
    print("{}, {}, {}".format(dates[i], municipality1, arrayMunicipality1[i]))
    print("{}, {}, {}".format(dates[i], municipality2, arrayMunicipality2[i]))
main(sys.argv)

