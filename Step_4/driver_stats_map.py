#! /usr/bin/env python2.7

import sys
import datetime

# Data fields to be outputted
keep_cols = set([2, 4, 5, 9, 11, 18, 19, 21])

for line in sys.stdin:
    tokens = line.strip().split('\t')
    tokens = [token.strip() for i, token in enumerate(tokens) if i in keep_cols]

    # Hack IDs change every year
    # Concatenate year and hack ID to make year/hack ID a unique field
    year = tokens[1][:4]
    mapline = []
    mapline.append(tokens[0] + year)
    mapline.extend(tokens)

    print "\t".join(mapline)
