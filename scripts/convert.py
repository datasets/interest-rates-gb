import csv
import datetime
inFilePath = 'archive/data.original.csv'
outFilePath = 'data/data.csv'

def convertMonthStringToInt(monthString):
    convertDict= { 'jan' : 1,
                   'feb' : 2,
                   'mar' : 3,
                   'apr' : 4,
                   'may' : 5,
                   'jun' : 6,
                   'jul' : 7,
                   'aug' : 8,
                   'sep': 9,
                   'oct' : 10,
                   'nov' : 11,
                   'dec' : 12,
                   'january' : 1,
                   'february' : 2,
                   'march' : 3,
                   'april' : 4,
                   'june': 6,
                   'july': 7,
                   'august' : 8,
                   'sept' : 9,
                   'september' : 9,
                   'october': 10,
                   'november' : 11,
                   'december' : 12
                   }
    return convertDict[monthString.lower()]

import unittest

class TestStuff(unittest.TestCase):
    def testConvertMonthStringToInt(self):
        in1 = [ 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sept',
                'oct', 'nov', 'dec' ]
        expected = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        in2 = [ xx.upper() for xx in in1 ]
        for index in range(len(in1)):
            self.assertEquals(convertMonthStringToInt(in1[index]),
                expected[index])
            self.assertEquals(convertMonthStringToInt(in2[index]),
                expected[index])

def processCsvFile(inFilePath, outFilePath):
    latest_date = None

    # Read the latest processed date from the existing output file
    try:
        with open(outFilePath, 'r', newline='') as outFile:
            existing_data = list(csv.reader(outFile))
            if len(existing_data) > 1:  # Ensure data exists
                latest_date = datetime.date.fromisoformat(existing_data[-1][0])
    except FileNotFoundError:
        pass  # If output file doesn't exist, start from the beginning

    with open(inFilePath, 'r', newline='') as inFile, open(outFilePath, 'a', newline='') as outFile:
        reader = csv.reader(inFile)
        writer = csv.writer(outFile)

        lastYear = None
        lastMonth = 1
        lastDay = 1
        yearCol = 0
        monthCol = 2
        dayCol = 1
        valueCol = 3
        rowNum = -1

        for row in reader:
            rowNum += 1
            if rowNum == 0:
                continue  # Skip header

            if row[yearCol] != '':
                lastYear = int(row[yearCol])
                lastMonth = 1
                lastDay = 1
            if row[monthCol] != '':
                lastMonth = convertMonthStringToInt(row[monthCol])
                lastDay = 1
            if row[dayCol] != '':
                lastDay = int(row[dayCol])

            date = datetime.date(lastYear, lastMonth, lastDay)

            # Append only if the date is newer than the last recorded date
            if latest_date is None or date > latest_date:
                writer.writerow([date.isoformat(), row[valueCol]])

if __name__ == '__main__':
    # unittest.main()
    processCsvFile(inFilePath, outFilePath)
