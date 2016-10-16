#! /usr/bin/env python2.7

import sys
import datetime

keep_cols = set([2, 4, 5, 9, 11, 18, 19, 21])

for line in sys.stdin:
    tokens = line.strip().split('\t')
    tokens = [token.strip() for i, token in enumerate(tokens) if i in keep_cols]

    year = tokens[1][:4]
    mapline = []
    mapline.append(tokens[0] + year)
    mapline.extend(tokens)

    print "\t".join(mapline)
