#!/usr/bin/env python2.7

import sys

#Assume input is sorted by key
if __name__ == "__main__":
    currKey = ""
    lastKey = ""
    line_to_write = {} #dictionary going from tableID to table contents
   
    for line in sys.stdin:
        tokens = line.strip().split('\t')
        tokens = [token.strip() for token in tokens]
        currKey = tokens[0]
        currTable = tokens[1]
        if currKey != lastKey: #if the key changed (regardless of whether the table is full or not
            line_to_write = {} #flush the dictionary, make space for (new) current key
        lastKey = currKey
        if len(line_to_write) == 2: #if three consecutive keys are the same
            continue        
        if len(line_to_write) == 1:
            storedTable = line_to_write.keys()[0]
            if storedTable == currTable:
                continue
            else:
                line_to_write[currTable] = [token for token in tokens\
                                            if token!=currTable and token!=currKey]
                line1 = '\t'.join(line_to_write['1'])
                line2 = '\t'.join(line_to_write['2'])
                lineToPrint = '\t'.join([currKey, line1, line2])
                print lineToPrint
        elif len(line_to_write) == 0:
            line_to_write[currTable] = [token for token in tokens\
                                        if token!=currTable and token!=currKey]
