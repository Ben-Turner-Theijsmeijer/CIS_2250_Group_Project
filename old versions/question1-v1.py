#!/usr/bin/env python

'''
question1.py
  Author(s): Connor Schulz (1103003) 

  Project: CIS2250 group project (Kolkata)
  Question: How Has Covid 19 Affected Unemployment?
  Date of Last Update: March 25, 2021.

  Functional Summary
      question1.py takes in a unemployment and covid case number data set and processes the data together
     Commandline Parameters: 5
        argv[1] = <Start Month>
        argv[2] = <Start Year>
        argv[3] = <End Month>
        argv[4] = <End Year>
        argv[5] = <Gender>
'''

UN_MAP = {
        "MONTH" :  0,
        "GEOGRAPHY" :  1,
        "DURATION" :  2,
        "AGE GROUP" :  3,
        "Both sexes" :  4,
        "Male" :  5,
        "Female" :  6 }

CASE_MAP = {
        "FILE_DATE" :  0,
        "PHU_NAME" :  1,
        "PHU_NUM" :  2,
        "ACTIVE_CASES" :  3,
        "RESOLVED_CASES" :  4,
        "DEATHS" :  5 }

OUT_MAP = {
        "DATE" :  0,
        "  15-19" :  1,
        "  20-24" :  2,
        "  25-44" :  3,
        "  45-54" :  4,
        "  55-64" :  5,
        "  65 years and over"   :  6,
        "CASES" :  7}

import sys
import csv
import datetime

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

#returns the year from a row of unemployment data
def getUnYear(row):
  try:
    return int(row[UN_MAP["MONTH"]][-4:])
  except ValueError:
    return 0

#returns the month from a row of unemployment data
def getUnMonth(row):
  if row[UN_MAP["MONTH"]][0] == "M":
    return 3
  elif row[UN_MAP["MONTH"]][0] == "J":
    return 6
  elif row[UN_MAP["MONTH"]][0] == "S":
    return 9
  elif row[UN_MAP["MONTH"]][0] == "D":
    return 12
  else:
    return -1
# The unemployment data only updates quarterly, so not all 12 months are present
# this function will return the month closest to the one entered.
# either march, june, september, or december 
def returnNearestMonth(user_month):
  nearestMonth = 100
  prevDistance = 100
  mar, jun, sep, dec = 3, 6, 9, 12
  for csv_month in [mar, jun, sep, dec]:
    if abs(user_month - csv_month) % 11 < prevDistance:
      nearestMonth = csv_month 
    prevDistance = abs(user_month - csv_month) % 11

  return nearestMonth

def handleInput(argv, argNum ,default): 
  try:
    value = argv[argNum]
  except IndexError:
    value = default
  return value





def main(argv):

  if len(argv) < 3 or len(argv) > 6:
    stopExecution("Usage: <Start Month> <Start Year> <End Month> <End Year> <Gender>\n\nRequired Fields: <Start Month> <Start Year>\nDefaults: <End Month> = 9, <End Year> = 2020, <Gender> = Both")
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



  unemploymentFile = openFile("Q1 datasets/unemployment.csv")
  casesFile = openFile("Q1 datasets/cases_by_status_and_phu.csv")

  unemploymentData = csv.reader(unemploymentFile)
  next(unemploymentData)
  casesData = csv.reader(casesFile)
  next(casesData)
  outputdata = [0,0,0,0,0,0,0,0]

  startDate = datetime.datetime(startYear, startMonth, 1)
  endDate = datetime.datetime(endYear, endMonth, 1)

  print("Date, 15-19, 20-24, 25-44, 45-54, 55-64, 65+, covid cases")
 
  for row in unemploymentData:
    cases = 0
    phuNums = []
    currentDate = datetime.datetime(getUnYear(row), getUnMonth(row),1)
    prevDate = 0
    month = getUnMonth(row)
    year = getUnYear(row)
    if currentDate >= startDate and currentDate <= endDate:
        if row[UN_MAP["GEOGRAPHY"]] == "Total, Ontario regions":
          if row[UN_MAP["DURATION"]] == "Average weeks unemployed (no top-code)":
            if row[UN_MAP["AGE GROUP"]][0:5] not in ["Total"," 15-6"]:
              
              outputdata[OUT_MAP[row[UN_MAP["AGE GROUP"]]]] = row[UN_MAP[gender]]
              casesFile = openFile("Q1 datasets/cases_by_status_and_phu.csv")
              casesData = csv.reader(casesFile)
              next(casesData)
              for report in casesData:
                case_date = report[CASE_MAP["FILE_DATE"]].split("-")
                if int(case_date[1]) == int(month) and int(case_date[0]) == int(year):
                  if report[CASE_MAP["PHU_NUM"]] not in phuNums:
                    phuNums.append( report[CASE_MAP["PHU_NUM"]])
                    cases += int(report[CASE_MAP["ACTIVE_CASES"]]) + int(report[CASE_MAP["RESOLVED_CASES"]]) + int(report[CASE_MAP["DEATHS"]])
              casesFile.close()
              outputdata[OUT_MAP["CASES"]] = cases
              if currentDate != outputdata[OUT_MAP["DATE"]]:
                outputdata[OUT_MAP["DATE"]] = currentDate
                print(outputdata)
              prevDate = currentDate


main(sys.argv)