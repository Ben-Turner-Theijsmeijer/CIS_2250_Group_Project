#!/usr/bin/env python

'''
question1.py
  Author(s): Connor Schulz (1103003) 

  Project: CIS2250 group project (Kolkata)
  Question: How Has Covid 19 Affected Unemployment?
  Date of Last Update: March 29, 2021.

  Functional Summary
      question1.py takes in a unemployment and covid case number data set and processes the data together
     Commandline Parameters: 5
        argv[1] = <Start Month>
        argv[2] = <Start Year>
        argv[3] = <End Month>
        argv[4] = <End Year>
        argv[5] = "Gender"
'''

#import libraries
import sys
import csv
from datetime import date


UN_MAP = {
        "MONTH" :  0,
        "GEOGRAPHY" :  1,
        "DURATION" :  2,
        "AGE GROUP" :  3,
        "Both sexes" :  4,
        "Male" :  5,
        "Female" :  6 }

OUT_MAP = {
        "DATE"                   : 0,
        "AGE"                    : 1,
        "UNEMPLOYMENT_DURATION"  : 2,
        "CASES"                  : 3}

CASE_MAP = {
        "FILE_DATE" :  0,
        "PHU_NAME" :  1,
        "PHU_NUM" :  2,
        "ACTIVE_CASES" :  3,
        "RESOLVED_CASES" :  4,
        "DEATHS" :  5 }

#prints an error message and stops executing code
def stopExecution(message):
  print(message)
  sys.exit()

# opens a file and returns the file handle. It exits with an message if an error occurs.
def openFile(fileName):
  try:
    fh = open(fileName, encoding="utf-8-sig")
    
  except IOError as err:
    print("Unable to open file '{}' : {}".format(fileName, err), file=sys.stderr)
    sys.exit(1)
  return fh

# gets passed argv, an arg number, and a default value
# if the arg doesnt exist, set the value to the default one 
def handleInput(argv, argNum ,default): 
  try:
    value = argv[argNum]
  except IndexError:
    value = default
  return value

#returns the month from a row of unemployment data
def getUnMonth(unDate):
  if unDate[0] == "M":
    return 3
  elif unDate[0] == "J":
    return 6
  elif unDate[0] == "S":
    return 9
  elif unDate[0] == "D":
    return 12
  else:
    return -1


def main(argv):

  #check for the correct amount of args
  if len(argv) < 3 or len(argv) > 6:
    stopExecution("Usage: <Start Month> <Start Year> <End Month> <End Year> <Gender>\n\nRequired Fields: <Start Month> <Start Year>\nDefaults: <End Month> = 9, <End Year> = 2020, \"Gender\" = Both")
  
  #get args from command line
  try:
    startMonth = int(argv[1])
    startYear = int(argv[2])
    endMonth = int(handleInput(argv,3, 9))
    endYear = int(handleInput(argv,4, 2020))
  except:
    stopExecution("INPUT ERROR: Months and years must be expressed as integers")
  gender = handleInput(argv,5, "Both sexes")

  for month in [startMonth, endMonth]:
    if month < 1 or month > 12:
      stopExecution("INPUT ERROR: Months cannot be less than 1 or greater than 12")
  
  for year in [startYear, endYear]:
    if year < 2001 or year > 2020:
      stopExecution("INPUT ERROR: Years cannot be less than 2001 or greater than 2020")

  if startYear > endYear or (startYear == endYear and startMonth > endMonth):
    stopExecution("INPUT ERROR: Start date cannot be greater than end date")
  
  if gender not in ["Male", "Female", "Both sexes"]:
    stopExecution("INPUT ERROR: Gender must either be: 'Male', 'Female', or 'Both sexes'")

  
  startDate = date(startYear, startMonth, 1)
  endDate = date(endYear, endMonth, 1)

  relevantInfo = ["Total, Ontario regions", "Average weeks unemployed (no top-code)", "Total, 15 years and over", " 15-64 years"]

  unemploymentFile = openFile("Q1 datasets/unemployment.csv")
  casesFile = openFile("Q1 datasets/cases_by_status_and_phu.csv")

  unemploymentData = csv.reader(unemploymentFile)
  casesData = csv.reader(casesFile)
  #skip header line
  next(unemploymentData)
  outputdata = [0,0,0,0]
  print("DATE,AGE,UNEMPLOYMENT_DURATION,CASES")
  for row in unemploymentData:
    casesFile.seek(0)
    currentCases = 0
    currentDate = date(int(row[0][-4:]), getUnMonth(row[0]), 1)
    if currentDate >= startDate and currentDate <= endDate:
      if row[UN_MAP["GEOGRAPHY"]] in relevantInfo and row[UN_MAP["DURATION"]] in relevantInfo and row[UN_MAP["AGE GROUP"]] not in relevantInfo:
        for report in casesData:
          if report[CASE_MAP["FILE_DATE"]] != "FILE_DATE":
            case_date = report[CASE_MAP["FILE_DATE"]].split("-")
            if date(int(case_date[0]),int(case_date[1]),int(case_date[2])) == currentDate:
              currentCases += int(report[CASE_MAP["ACTIVE_CASES"]]) + int(report[CASE_MAP["RESOLVED_CASES"]]) + int(report[CASE_MAP["DEATHS"]])

        outputdata[OUT_MAP["DATE"]] = str(currentDate)
        outputdata[OUT_MAP["AGE"]] = row[UN_MAP["AGE GROUP"]]
        outputdata[OUT_MAP["UNEMPLOYMENT_DURATION"]] = row[UN_MAP[gender]]
        outputdata[OUT_MAP["CASES"]] = currentCases

        print(*outputdata, sep=',')



main(sys.argv)