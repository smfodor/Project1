import os
import filecmp
from dateutil.relativedelta import *
from datetime import date
import csv
import datetime


def getData(file):
# get a list of dictionary objects from the file
#Input: file name
#Ouput: return a list of dictionary objects where
#the keys are from the first row in the data. and the values are each of the other rows
	file_dict = []
	infile = open(file, 'r')
	lines = infile.readlines()
	for line in lines:
		data_dict = {}
		values = line.split(",")
		first = values[0]
		last = values[1]
		email = values[2]
		year = values[3]
		dob = values[4]
		data_dict["First"] = first
		data_dict["Last"] = last
		data_dict["Email"] = email
		data_dict["Year"] = year
		data_dict["DOB"] = dob

		file_dict.append(data_dict)
	return file_dict


def mySort(data,col):
# Sort based on key/column
#Input: list of dictionaries and col (key) to sort on
#Output: Return the first item in the sorted list as a string of just: firstName lastName
	sorted_lst = sorted(data, key = lambda k: k[col])
	first = sorted_lst[0]["First"]
	last = sorted_lst[0]["Last"]
	return first + ' ' + last


def classSizes(data):
# Create a histogram
# Input: list of dictionaries
# Output: Return a list of tuples sorted by the number of students in that class in
# descending order
# [('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)]
	fresh = 0
	soph = 0
	jun = 0
	sen = 0

	for student in data:
		if student["Year"] == "Freshman":
			fresh += 1
		elif student["Year"] == "Sophomore":
			soph += 1
		elif student["Year"] == "Junior":
			jun += 1
		elif student["Year"] == 'Senior':
			sen += 1
	year_list = [("Freshman", fresh), ("Sophomore", soph), ("Junior", jun), ("Senior", sen)]
	return sorted(year_list, key = lambda k: k[-1], reverse= True)

def findMonth(a):
# Find the most common birth month form this data
# Input: list of dictionaries
# Output: Return the month (1-12) that had the most births in the data
	dict_month = {}
	for student in a:
		bday = student["DOB"].split("/")[0]
		if bday in dict_month:
			dict_month[bday] += 1
		else:
			dict_month[bday] = 1
	sorted_months = sorted(dict_month, key = lambda k: dict_month[k], reverse = True)
	return int(sorted_months[0])

def mySortPrint(a,col,fileName):
#Similar to mySort, but instead of returning single
#Student, the sorted data is saved to a csv file.
# as fist,last,email
#Input: list of dictionaries, col (key) to sort by and output file name
#Output: No return value, but the file is written
	sorted_list = sorted(a, key = lambda k: k[col])
	new_list = []
	for x in sorted_list:
		new_list.append((x["First"] + "," + x["Last"] + "," + x["Email"] + "\n"))
	outFile = open(fileName, "w")
	for x in new_list:
		outFile.write(x)

def findAge(a):
# def findAge(a):
# Input: list of dictionaries
# Output: Return the average age of the students and round that age to the nearest
# integer.  You will need to work with the DOB and the current date to find the current
# age in years.
	age_list = []
	year_today = (datetime.datetime.today().strftime("%m/%d/%Y"))

	for d in a[1:]:
		DOB = d["DOB"]
		date_today = year_today.split("/")
		bday = DOB.split("/")
		age = int(date_today[2]) - int(bday[2])
		if int(bday[0]) >= int(date_today[0]):
			age = int(date_today[2]) - int(bday[2]) - 1
		if int(bday[0]) == int(date_today[0]) and int(bday[1]) > int(date_today[1]):
			age = int(date_today[2]) - int(bday[2]) - 1
		age_list.append(age)

	total = 0
	for x in age_list:
		total += x

	avg = float(total/ len(age_list))
	return round(avg)

################################################################
## DO NOT MODIFY ANY CODE BELOW THIS
################################################################

## We have provided simple test() function used in main() to print what each function returns vs. what it's supposed to return.
def test(got, expected, pts):
  score = 0;
  if got == expected:
    score = pts
    print(" OK ", end=" ")
  else:
    print (" XX ", end=" ")
  print("Got: ",got, "Expected: ",expected)
  return score


# Provided main() calls the above functions with interesting inputs, using test() to check if each result is correct or not.
def main():
	total = 0
	print("Read in Test data and store as a list of dictionaries")
	data = getData('P1DataA.csv')
	data2 = getData('P1DataB.csv')
	total += test(type(data),type([]),50)

	print()
	print("First student sorted by First name:")
	total += test(mySort(data,'First'),'Abbot Le',25)
	total += test(mySort(data2,'First'),'Adam Rocha',25)

	print("First student sorted by Last name:")
	total += test(mySort(data,'Last'),'Elijah Adams',25)
	total += test(mySort(data2,'Last'),'Elijah Adams',25)

	print("First student sorted by Email:")
	total += test(mySort(data,'Email'),'Hope Craft',25)
	total += test(mySort(data2,'Email'),'Orli Humphrey',25)

	print("\nEach grade ordered by size:")
	total += test(classSizes(data),[('Junior', 28), ('Senior', 27), ('Freshman', 23), ('Sophomore', 22)],25)
	total += test(classSizes(data2),[('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)],25)

	print("\nThe most common month of the year to be born is:")
	total += test(findMonth(data),3,15)
	total += test(findMonth(data2),3,15)

	print("\nSuccessful sort and print to file:")
	mySortPrint(data,'Last','results.csv')
	if os.path.exists('results.csv'):
		total += test(filecmp.cmp('outfile.csv', 'results.csv'),True,20)

	print("\nTest of extra credit: Calcuate average age")
	total += test(findAge(data), 40, 5)
	total += test(findAge(data2), 42, 5)

	print("Your final score is " + str(total))

# Standard boilerplate to call the main() function that tests all your code
if __name__ == '__main__':
    main()
