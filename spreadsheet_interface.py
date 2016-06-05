## \file spreadsheet_interface.py
#  \author Judge Lee (jblee@hmc.edu)
#  \date June 4, 2016
#  
#  Creates the interface between the schduler and an input CSV file.

from dance_scheduler import *
import csv

##
#  \brief Retrieve the data from the CSV.
#
#  \param[in] file  The input CSV filename as a string
#  \return          A list of lists of the data from the CSV
def readFile(filename):
	with open(filename, 'r') as f:
		reader = csv.reader(f)
		data = list(reader)
		return data

##
#  \brief Takes the data returned from reading in the file and stores it in a scheduler.
#
#  \param[in] data  A list of lists of the data from the CSV
#  \return          A list of performers, a list of routines, and a scheduler
#
#  \todo Figure out what the data will look like
#  \todo Store the data.
def extractData(data):