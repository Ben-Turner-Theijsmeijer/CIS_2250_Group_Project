#!/usr/bin/env python

'''
question1.py
  Author(s): Connor Schulz (1103003) 

  Project: CIS2250 group project (Kolkata)
  Question: How Has Covid 19 Affected Unemployment?
  Date of Last Update: March 30, 2021.

  Functional Summary
      question1.py takes in a unemployment and covid case number data set and processes the data together
     Commandline Parameters: 5
        argv[1] = <Start Month>
        argv[2] = <Start Year>
        argv[3] = <End Month>
        argv[4] = <End Year>
        argv[5] = "Gender"
        argv[6] = "filename.pdf"
'''

#import libraries
import sys
import csv
from datetime import date
from io import StringIO
import createChart1v2 

#Map for unemployment data
UN_MAP = {
        "MONTH" :  0,
        "GEOGRAPHY" :  1,
        "DURATION" :  2,
        "AGE GROUP" :  3,
        "Both sexes" :  4,
        "Male" :  5,
        "Female" :  6 }
#Map for case data
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
#the only options are March, June, September, an December
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
  if len(argv) < 3 or len(argv) > 7:
    stopExecution("\nUsage: python question1.py <Start Month> <Start Year> <End Month> <End Year> \"Gender\" \"File Name\"\n\nRequired Fields: <Start Month> <Start Year>\nDefaults: <End Month> = 9, <End Year> = 2020, \"Gender\" = Both sexes, \"File Name\" = chartOut.pdf")
  
  #get args from command line
  try:
    startMonth = int(argv[1])
    startYear = int(argv[2])
    endMonth = int(handleInput(argv,3, 9))
    endYear = int(handleInput(argv,4, 2020))
  except:
    stopExecution("INPUT ERROR: Months and years must be expressed as integers")
  
  gender = handleInput(argv,5, "Both sexes")
  fileName = handleInput(argv,6, "chartOut.pdf")

  #check to see if the months and years fit an expected range
  for month in [startMonth, endMonth]:
    if month < 1 or month > 12:
      stopExecution("INPUT ERROR: Months cannot be less than 1 or greater than 12")

  for year in [startYear, endYear]:
    if year < 2001 or year > 2020:
      stopExecution("INPUT ERROR: Years cannot be less than 2001 or greater than 2020")

  #check if start date is a later than the end date
  if startYear > endYear or (startYear == endYear and startMonth > endMonth):
    stopExecution("INPUT ERROR: Start date cannot be greater than end date")
  
  #check if gender is one of the three choices
  if gender not in ["Male", "Female", "Both sexes"]:
    stopExecution("INPUT ERROR: Gender must either be: 'Male', 'Female', or 'Both sexes'")

  if fileName[-4:] != ".pdf":
    stopExecution("INPUT ERROR: File name must end with '.pdf'")
  
  #convert the months and years into proper date format
  startDate = date(startYear, startMonth, 1)
  endDate = date(endYear, endMonth, 1)

  #open files for the two datasets and read them in csv format
  unemploymentFile = openFile("Q1 datasets/unemployment.csv")
  unemploymentData = csv.reader(unemploymentFile)
  casesFile = openFile("Q1 datasets/cases_by_status_and_phu.csv")
  casesData = csv.reader(casesFile)

  #skip header line of unemployment data
  next(unemploymentData)

  #array that holds strings for sections of the data that are to either be used or ommited
  relevantInfo = ["Total, Ontario regions", "Average weeks unemployed (no top-code)", "Total, 15 years and over", " 15-64 years"]
  
  #string that holds the generated data initialized with the header
  outputString = "DATE,AGE,UNEMPLOYMENT_DURATION,CASES\n"
  
  for row in unemploymentData:
    #seek to the start of the cases file and skip the header line
    casesFile.seek(0)
    next(casesData)
    currentCases = 0
    #get current date from the unemployment data row
    currentDate = date(int(row[0][-4:]), getUnMonth(row[0]), 1)
    
    #check if date is within the start and end date and that the row has the relevent fields
    if currentDate >= startDate and currentDate <= endDate:
      if row[UN_MAP["GEOGRAPHY"]] in relevantInfo and row[UN_MAP["DURATION"]] in relevantInfo and row[UN_MAP["AGE GROUP"]] not in relevantInfo:
        
        for report in casesData:
          #split the date so it can be converted into a date object
          caseDate = report[CASE_MAP["FILE_DATE"]].split("-")
          #check if the case date matches the current unemployment date
          if date(int(caseDate[0]),int(caseDate[1]),int(caseDate[2])) == currentDate:
            #get the covid case count by adding the active cases, resolved cases, and deaths
            currentCases += int(report[CASE_MAP["ACTIVE_CASES"]]) + int(report[CASE_MAP["RESOLVED_CASES"]]) + int(report[CASE_MAP["DEATHS"]])

        #set the fields of the output data to the correct values
        outputString += str(currentDate)         + ","
        outputString += row[UN_MAP["AGE GROUP"]] + ","
        outputString += row[UN_MAP[gender]]      + ","
        outputString += str(currentCases) + "\n"

  #print generated date
  print(outputString)
  #send data to createChart to generate a visualization
  createChart1v2.createChart(StringIO(outputString), fileName)


main(sys.argv)