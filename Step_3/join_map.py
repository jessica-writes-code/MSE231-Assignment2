#!/usr/bin/env python2.7
import sys

for line in sys.stdin:
    if line.startswith('medallion'):
        continue
    tokens = line.strip().split(',')
    tokens = [token.strip() for token in tokens]
    line_to_write = []
    #fare data: 11 fields
    if len(tokens) == 11:
        key = '_'.join([tokens[0], tokens[1], tokens[3]]).replace(' ', '_') #replace all spaces in the key with underscores
        tableID = '1'  
    #trip data: 14 fields       
    elif len(tokens) == 14:
        key = '_'.join([tokens[0], tokens[1], tokens[5]]).replace(' ', '_') #replace all spaces in the key with underscores
        tableID = '2'
    #unreadable data from either file
    else:
        print >> sys.stderr, line.strip()
        continue
    
    line_to_write.append(key)
    line_to_write.append(tableID)
    for token in tokens:
        line_to_write.append(token)
    line_to_write = '\t'.join(line_to_write)
    print line_to_write

    
