#! /usr/bin/env python2.7

import sys
from itertools import groupby
from operator import itemgetter

def read_mapper_output(lines):
    for line in lines:
        yield line.rstrip().split('\t')

data = read_mapper_output(sys.stdin)
# Initialize dictionary
agg_features = {"drivers_onduty": 0.0, "drivers_occupied": 0.0, "t_onduty": 0.0,
                "t_occupied": 0.0, "n_pass": 0.0, "n_trip": 0.0, "n_mile": 0.0,
                "earnings": 0.0, "money_list": [0.0]*6 }

# Group by day/hour
for day_hour, group in groupby(data, itemgetter(0)):

    # Initialize record for new day/hour
    day = day_hour[:-2]
    hour = day_hour[-2:]
    agg_features = {"drivers_onduty": 0.0, "drivers_occupied": 0.0, "t_onduty": 0.0,
                "t_occupied": 0.0, "n_pass": 0.0, "n_trip": 0.0, "n_mile": 0.0,
                "earnings": 0.0, "money_list": [0.0]*6 }    

    for record in group:
        # Add record info to day/hour
        agg_features["t_onduty"] += float(record[4])
        agg_features["t_occupied"] += float(record[5])
        agg_features["n_pass"] += float(record[6])
        agg_features["n_trip"] += float(record[7])
        agg_features["n_mile"] += float(record[8])
        agg_features["earnings"] += float(record[9])
        agg_features["money_list"] = [agg_features["money_list"][i] + float(l) \
                                      for i, l in enumerate(record[10:16])]

        # Only add drivers onduty if hackID has been created in current year
        # Avoids overcounting drivers with December 31-January 1 drives
        if record[0][0:4] == record[3][0:4]:
            agg_features["drivers_onduty"] += 1
            agg_features["drivers_occupied"] += 1
    
    # Print day/hour
    list_to_print = [day, hour]
    for key in ["drivers_onduty", "drivers_occupied", "t_onduty", "t_occupied", 
                "n_pass", "n_trip", "n_mile", "earnings"]:
        list_to_print.append(str(agg_features[key]))
    list_to_print.extend([str(l) for l in agg_features["money_list"]])

    print "\t".join(list_to_print)


