#! /usr/bin/env python2.7

import sys

for line in sys.stdin:
    tokens = line.strip().split('\t')
    tokens = [token.strip() for i, token in enumerate(tokens) if i in keep_cols]

    # Make key (date/hour)
    

    print "\t".join(mapline)