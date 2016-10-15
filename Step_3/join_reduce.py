#!/usr/bin/env python2.7

import sys

## Function to filter erroneous data
def passesIntegrityCheck(line_to_write):
    try:
        # Fare total is less than $2.50
        totalFare = float(line_to_write['1'][10])
        if totalFare < 2.50:
            return False
        # Total passengers is less than or equal to 0
        totalPassengers = int(line_to_write['2'][7])
        if totalPassengers <= 0:
            return False
        # Trip time is less than or equal to 0
        tripTime = int(line_to_write['2'][8])
        if tripTime <= 0:
            return False
        # Trip distance is less than or equal to 0
        tripDistance = float(line_to_write['2'][9])
        if tripDistance <= 0:
            return False
        return True
    except ValueError:
        # One of the above features is unreadable
        return False
    
## Assume input is sorted by key
if __name__ == "__main__":
    currKey = ""
    lastKey = ""
    line_to_write = {} # dictionary going from tableID to table contents
   
    for line in sys.stdin:
        tokens = line.strip().split('\t')
        tokens = [token.strip() for token in tokens]
        currKey = tokens[0]
        currTable = tokens[1]
        if currKey != lastKey: # if the key changed (regardless of whether the table is full or not
            line_to_write = {} # flush the dictionary, make space for (new) current key
        lastKey = currKey
        if len(line_to_write) == 2: # if three consecutive keys are the same
            continue        
        if len(line_to_write) == 1: # if one table's info has been collected, but not the other
            storedTable = line_to_write.keys()[0]
            if storedTable == currTable:
                continue
            else:
                line_to_write[currTable] = tokens[2:]
                if passesIntegrityCheck(line_to_write):
                    line1 = '\t'.join(line_to_write['1'])
                    line2 = '\t'.join(line_to_write['2'])
                    lineToPrint = '\t'.join([currKey, line1, line2])
                    print lineToPrint
        elif len(line_to_write) == 0: # if neither table's info has been collected 
            line_to_write[currTable] = tokens[2:]
