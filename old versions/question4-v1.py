#!/usr/bin/env python
'''
question4.py
  Author(s): Anthony Perez-Carey (1137637), 
             Ben Turner-Theijsmeijer (1152536), 
             Connor Schulz (1103003) Matthew Biggins (1136122)

  Project: CIS2250 group project (Kolkata)
  Question: How does age and gender affect the mortality 
          and survivability rates in the different public health units  
          (Iteration 1)
  Date of Last Update: March 16, 2021.

  Functional Summary
      question4-v1.py takes in the specified gender and PHU ID and
      sorts data found in the Confirmed positive cases of COVID-19
      in Ontario data set to find the total people in each age group
      for the specified gender that have died due to complications
      related to COVID-19 and those that have survived the infection.
      This data is then outputed into a stacked column chart for 
      visulizating the effects of COVID-19 on each age group in 
      the specified gender. 
     Commandline Parameters: 2
        argv[1] = gender
        argv[2] = PHU ID number
'''


import sys
import csv


INDEX_MAP = {
        "Row_ID" :  0,
        "Accurate_Episode_Date" :  1,
        "Case_Reported_Date" :  2,
        "Test_Reported_Date" :  3,
        "Specimen_Date" :  4,
        "Age_Group" :  5,
        "Client_Gender" :  6,
        "Case_AcquisitionInfo" :  7,
        "Outcome1" :  8,
        "Outbreak_Related" :  9,
        "Reporting_PHU_ID" : 10,
        "Reporting_PHU" : 11,
        "Reporting_PHU_Address" : 12,
        "Reporting_PHU_City" : 13,
        "Reporting_PHU_Postal_Code" : 14,
        "Reporting_PHU_Website" : 15,
        "Reporting_PHU_Latitude" : 16,
        "Reporting_PHU_Longitude" : 17 }

AGES = {
        "<20" : 0,
        "20s" : 1,
        "30s" : 2,
        "40s" : 3,
        "50s" : 4,
        "60s" : 5,
        "70s" : 6,
        "80s" : 7,
        "90+" : 8}


def main(argv):
  
  filename = "conposcovidloc.csv"
  # check to make sure there are the correct number of parameters
  if len(argv) != 3:
    print("Usage: extract_PHU_data_by_gender.py <gender> <PHU ID>")
    sys.exit(1)
  
  # assign args to a variable
  gender = argv[1]
  PHUID = argv[2]
  gender = gender.upper()
  if gender not in ["MALE","FEMALE","UNSPECIFIED","GENDER DIVERSE"]:
    print("Usage: extract_PHU_data_by_gender.py <gender> <PHU ID>")
    print("Options for gender are 'MALE' 'FEMALE' 'UNSPECIFIED' 'GENDER DIVERSE'")
    sys.exit(1)
  
  # open the file
  try:
    fh = open(filename, encoding="utf-8-sig")
    
  except IOError as err:
    print("Unable to open file '{}' : {}".format(
            filename, err), file=sys.stderr)
    sys.exit(1)

  data_reader = csv.reader(fh)

  resolved_array = [0, 0, 0, 0, 0, 0, 0, 0, 0]
  fatal_array = [0, 0, 0, 0, 0, 0, 0, 0, 0]

  
  # read all rows of the file
  for row in data_reader:
    
    # check if the PHU ID matches the one in the row
    if row[INDEX_MAP["Reporting_PHU_ID"]] == PHUID:
      # check if the specified ClientGender matches the one in the row
      if row[INDEX_MAP["Client_Gender"]] == gender:
        # check if the outcome is Fatal and matches the one in the row
        if row[INDEX_MAP["Outcome1"]] == "Fatal":
          fatal_array[AGES[row[INDEX_MAP["Age_Group"]]]] += 1

        # check if the outcome is Resolved and matches the one in the row
        elif row[INDEX_MAP["Outcome1"]] == "Resolved":
          resolved_array[AGES[row[INDEX_MAP["Age_Group"]]]] += 1
  '''
          if row[INDEX_MAP["Age_Group"]] == "<20":
            fatal_array[AGES["<20"]] += 1
          elif row[INDEX_MAP["Age_Group"]] == "20s":
            fatal_array[AGES["20s"]] += 1
          elif row[INDEX_MAP["Age_Group"]] == "30s":
            fatal_array[AGES["30s"]] += 1
          elif row[INDEX_MAP["Age_Group"]] == "40s":
            fatal_array[AGES["40s"]] += 1
          elif row[INDEX_MAP["Age_Group"]] == "50s":
            fatal_array[AGES["50s"]] += 1
          elif row[INDEX_MAP["Age_Group"]] == "60s":
            fatal_array[AGES["60s"]] += 1
          elif row[INDEX_MAP["Age_Group"]] == "70s":
            fatal_array[AGES["70s"]] += 1
          elif row[INDEX_MAP["Age_Group"]] == "80s":
            fatal_array[AGES["80s"]] += 1
          elif row[INDEX_MAP["Age_Group"]] == "90+":
            fatal_array[AGES["90+"]] += 1
  '''
        
  '''
          if row[INDEX_MAP["Age_Group"]] == "<20":
            resolved_array[AGES["<20"]] += 1
          elif row[INDEX_MAP["Age_Group"]] == "20s":
            resolved_array[AGES["20s"]] += 1
          elif row[INDEX_MAP["Age_Group"]] == "30s":
            resolved_array[AGES["30s"]] += 1
          elif row[INDEX_MAP["Age_Group"]] == "40s":
            resolved_array[AGES["40s"]] += 1
          elif row[INDEX_MAP["Age_Group"]] == "50s":
            resolved_array[AGES["50s"]] += 1
          elif row[INDEX_MAP["Age_Group"]] == "60s":
            resolved_array[AGES["60s"]] += 1
          elif row[INDEX_MAP["Age_Group"]] == "70s":
            resolved_array[AGES["70s"]] += 1
          elif row[INDEX_MAP["Age_Group"]] == "80s":
            resolved_array[AGES["80s"]] += 1
          elif row[INDEX_MAP["Age_Group"]] == "90+":
            resolved_array[AGES["90+"]] += 1
  '''
  print(resolved_array)
  print(fatal_array)

main(sys.argv)

  

