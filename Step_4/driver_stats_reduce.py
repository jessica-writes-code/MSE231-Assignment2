#! /usr/bin/env python2.7

import sys
from itertools import groupby
from operator import itemgetter
from datetime import datetime
from datetime import timedelta

def read_mapper_output(lines):
    for line in lines:
        yield line.rstrip().split('\t')

def end_hour(current_hour, hack, dict_features):
    list_to_print = []
    out_date = current_hour.strftime("%Y-%m-%d")
    out_hour = current_hour.strftime("%H")
    list_to_print.append(out_date)
    list_to_print.append(out_hour)
    list_to_print.append(hack)
    
    for key in ['t_onduty', 't_occupied', 'n_pass', 'n_trip', 'n_mile', 'earnings']:
        list_to_print.append(str(dict_features[key]))
        dict_features[key] = 0.0
    
    list_to_print.extend([str(x) for x in dict_features['money_list']])
    dict_features['money_list'] = [0.0]*6

    print '\t'.join(list_to_print)

    return dict_features
   

data = read_mapper_output(sys.stdin)
# Data become grouped by HackID/Year
money_list_lookup = {'CSH': 0, 'CRD': 2, 'Other': 4}
for hack, group in groupby(data, itemgetter(0)):
    # Sort records with same HackID by trip start date/time
    group = sorted(group, key=itemgetter(2)) 
    
    # Initialize variables/dictionary
    previous_trip_end_time = None
    current_hour = None
    dict_features = {'t_onduty': 0.0, #fraction of hour
                     't_occupied': 0.0, # fraction of hour
                     'n_pass': 0.0, # number of passengers
                     'n_trip': 0.0, # number of trips started
                     'n_mile': 0.0, # number of miles driven
                     'earnings': 0.0, # money earned
                     'money_list': [0.0]*6} #cash (earnings, tip), credit (earnings, tip), other (earnings, tip)
    
    for record in group:
        # Convert string date/time to unix datetime
        try:
            current_start_time = datetime.strptime(record[2], "%Y-%m-%d %H:%M:%S")
            current_end_time = datetime.strptime(record[6], "%Y-%m-%d %H:%M:%S")
        except:
            print >> sys.stderr, "error"
            continue

        # Find hour of current trip
        current_hour_of_trip = current_start_time - timedelta(minutes=current_start_time.minute,
                                                              seconds=current_start_time.second)

        t_onduty_extra_time = 0.0
        # First trip for a HackID/year
        if previous_trip_end_time is None:
            current_hour = current_hour_of_trip
            previous_trip_end_time = current_start_time
        # New trip does not start w/in current hour
        elif current_hour != current_hour_of_trip:
            # Calculate on-duty time for unoccupied time containing hour break
            if current_start_time - previous_trip_end_time < timedelta(minutes=30):
                dict_features['t_onduty'] += (current_hour + timedelta(hours=1) - previous_trip_end_time).seconds / 3600.0
                t_onduty_extra_time = (current_start_time - current_hour_of_trip).seconds / 3600.0 

            # Finish hour
            dict_features = end_hour(current_hour, hack, dict_features)
            # Update current hour
            current_hour = current_hour_of_trip

        # New trip's information to dictionary
        dict_features['n_pass'] += int(record[7])
        dict_features['n_trip'] += 1
        trip_time = current_end_time - current_start_time
        dict_features['t_onduty'] += t_onduty_extra_time
        # find our index to add earnings to the correct column of 'money_list'
        # default is 'Other' unless 'CSH' or 'CRD' is found
        money_list_index = money_list_lookup['Other']
        if record[3] in money_list_lookup:
            money_list_index = money_list_lookup[record[3]]

        # If trip ends in the same hour it begins
        if current_end_time.hour == current_start_time.hour:
            # Add all trip miles/earning/time occupied to current hour
            dict_features['n_mile'] += float(record[8])
            dict_features['earnings'] += float(record[5])
            dict_features['money_list'][money_list_index] += float(record[5])
            dict_features['money_list'][money_list_index + 1] += float(record[4])
            dict_features['t_occupied'] += trip_time.seconds / 3600.0 

            # Add pre-trip time to time occupied, if necessary
            if current_start_time - previous_trip_end_time < timedelta(minutes=30) and previous_trip_end_time >= current_hour:
                dict_features['t_onduty'] += (current_end_time - previous_trip_end_time).seconds / 3600.0
            else:
                dict_features['t_onduty'] += trip_time.seconds / 3600.0

        # If trip crosses hour break
        else:
            # Add relevant proportion of trip miles/earnings/time occupied to current hour
            trip_time_within_hour = (current_hour + timedelta(hours=1) - current_start_time)
            proportion_in_hour = float(trip_time_within_hour.seconds) / trip_time.seconds
            dict_features['n_mile'] += proportion_in_hour * float(record[8])
            dict_features['earnings'] += proportion_in_hour * float(record[5])
            dict_features['money_list'][money_list_index] += proportion_in_hour * float(record[5])
            dict_features['money_list'][money_list_index + 1] += proportion_in_hour * float(record[4])
            dict_features['t_occupied'] += trip_time_within_hour.seconds / 3600.0

            # Add pre-trip time to time occupied, if necessary
            if current_start_time - previous_trip_end_time < timedelta(minutes=30) and previous_trip_end_time >= current_hour:
                dict_features['t_onduty'] += (current_hour + timedelta(hours=1) - previous_trip_end_time).seconds / 3600.0
            else:
                dict_features['t_onduty'] += trip_time_within_hour.seconds / 3600.0

            # Finish hour
            dict_features = end_hour(current_hour, hack, dict_features)
            current_hour += timedelta(hours=1)

            # Add records for trips crossing multiple hour breaks
            while current_hour.hour != current_end_time.hour:
                dict_features['n_mile'] += 3600.0 / trip_time.seconds * float(record[8])
                dict_features['earnings'] += 3600.0 / trip_time.seconds * float(record[5])
                dict_features['money_list'][money_list_index] += 3600.0 / trip_time.seconds * float(record[5])
                dict_features['money_list'][money_list_index + 1] += 3600.0 / trip_time.seconds * float(record[4])
                dict_features['t_occupied'] = 1.0
                dict_features['t_onduty'] = 1.0
                dict_features = end_hour(current_hour, hack, dict_features)
                current_hour += timedelta(hours=1)

            # Add record for hour in which trip ends
            trip_time_within_hour = (current_end_time - current_hour)
            proportion_in_hour = float(trip_time_within_hour.seconds) / trip_time.seconds
            dict_features['n_mile'] += proportion_in_hour * float(record[8])
            dict_features['earnings'] += proportion_in_hour * float(record[5])
            dict_features['money_list'][money_list_index] += proportion_in_hour * float(record[5])
            dict_features['money_list'][money_list_index + 1] += proportion_in_hour * float(record[4])
            dict_features['t_occupied'] += trip_time_within_hour.seconds / 3600.0
            dict_features['t_onduty'] += trip_time_within_hour.seconds / 3600.0

        previous_trip_end_time = current_end_time
    dict_features = end_hour(current_hour, hack, dict_features)
