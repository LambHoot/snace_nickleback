import csv

def checkIfCsvContainsId(id, idCol, csvPath):
    print("I'm looking bro")
    with open(csvPath, "r") as f:
        csvReader = csv.reader(f, delimiter=",")
        for row in csvReader:
            if len(row) > 1 and row[idCol] == id:
                return True