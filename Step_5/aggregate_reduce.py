#! /usr/bin/env python2.7

import sys
from itertools import groupby

def read_mapper_output(lines):
    for line in lines:
        yield line.rstrip().split('\t')

data = read_mapper_output(sys.stdin)
for day_hour, group in groupby(data, itemgetter(0)):
    for record in group:
        