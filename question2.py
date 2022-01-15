'''
question2.py
  Author(s): Anthony Perez-Carey (1137637), 
             Ben Turner-Theijsmeijer (1152536), 
             Connor Schulz (1103003) Matthew Biggins (1136122)

  Project: CIS2250 group project (Kolkata)
  Question:  Has covid changed how much electricity and water
             is used by commercialized buildings?
            
  Date of Last Update: April 1, 2021.

  Functional Summary
      question2.py takes in a starting month and year along with an ending month and year. The program tallies up water and electricity usage into averges for the months in the range specfied while also tallying total COVID-19 cases over time for comparison
     Commandline Parameters: 
        argv[1] = start month
        argv[2] = start year
        argv[3] = end month
        argv[4] = end year
  Example Run:
    python question2.py 1 2020 9 2020 > q2_output.csv
    
    python createChart2.py q2_output.csv
    
'''
import sys
import csv
import pandas as pd
from datetime import date
from io import StringIO

MAP = {
        "Electric" :  0,
        "Water" :  1,
        "Date" :  2,
        }

#Map for case data
CASE_MAP = {
        "FILE_DATE" :  0,
        "PHU_NAME" :  1,
        "PHU_NUM" :  2,
        "ACTIVE_CASES" :  3,
        "RESOLVED_CASES" :  4,
        "DEATHS" :  5 }

def handleInput(argv, argNum ,default): 
  try:
    value = argv[argNum]
  except IndexError:
    value = default
  return value

def main(argv):
  filename = "datasets/largebuildingdata.csv"
  filename1 = "datasets/cases_by_status_and_phu.csv"

  try:
    fh = open(filename, encoding="utf-8-sig")
    fh1 = open(filename1, encoding="utf-8-sig")

    
  except IOError as err:
    print("Unable to open file '{}' : {}".format(
            filename, err), file=sys.stderr)
    sys.exit(1)

  startMonth = int(argv[1])
  startYear = int(argv[2])
  endMonth = int(handleInput(argv,3,1))
  endYear = int(handleInput(argv,4,2021))

  outputString = "Date,Average_Electric_Usage,Average_Water_Usage,Cases\n"

  
  data_reader = csv.reader(fh)
  covid_reader = csv.reader(fh1)

  startDate = date(startYear, startMonth, 1)
  endDate = date(endYear, endMonth, 1) 
  while startDate <= endDate:
    fh.seek(0)
    fh1.seek(0)
    next(data_reader)
    next(covid_reader)
    count = 0
    electricTotal = 0
    waterTotal = 0
    currentCases = 0
    for row in data_reader:
      if "Not Available" not in row:
        qualDate = row[MAP["Date"]].split("-")
        currentDate = date(int(qualDate[0]), int(qualDate[1]),1)
        #print("Current Date: ", currentDate)
        #print(" Start Date: ",startDate)
        if currentDate.month == startDate.month and currentDate.year == startDate.year:
          electricTotal += float(row[MAP["Electric"]])
          waterTotal += float(row[MAP["Water"]])
          count +=1
    for report in covid_reader:
      #split the date so it can be converted into a date object
      caseDate = report[CASE_MAP["FILE_DATE"]].split("-")
      #check if the case date matches the current unemployment date
      if date(int(caseDate[0]),int(caseDate[1]),int(caseDate[2])) == startDate:
        #get the covid case count by adding the active cases, resolved cases, and deaths
        currentCases += int(report[CASE_MAP["ACTIVE_CASES"]]) + int(report[CASE_MAP["RESOLVED_CASES"]]) + int(report[CASE_MAP["DEATHS"]])
    if count != 0 :
      outputString += str(startDate)         + ","
      outputString += str(electricTotal/count)  + ","
      outputString += str(waterTotal/count)     + ","
      outputString += str(currentCases)         + "\n"
    if startDate.month != 12:
      startDate = date(int(startDate.year), startDate.month + 1, 1)
    else:
      startDate = date(int(startDate.year) + 1, 1, 1)
  print(outputString)  

  


  


main(sys.argv)
