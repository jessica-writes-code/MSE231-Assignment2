#! /usr/bin/env python2.7

import sys

for line in sys.stdin:
    tokens = line.strip().split('\t')
    tokens = [token.strip() for i, token in enumerate(tokens)]

    # Make key (date/hour)
    mapline = [tokens[0]+tokens[1]]
    mapline.extend(tokens)

    print "\t".join(mapline)