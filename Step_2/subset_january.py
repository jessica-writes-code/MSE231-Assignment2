import sys
import csv

doc = csv.writer(sys.stdout, lineterminator='\n')

header = sys.stdin.readline().strip().split(",")
header = [x.strip() for x in header]
date_index = header.index("pickup_datetime") 
doc.writerow(header)

for line in sys.stdin:
    line = line.strip().split(",")
    line = [x.strip() for x in line]
    if line[date_index][0:10] == "2013-01-15":
        doc.writerow(line)
