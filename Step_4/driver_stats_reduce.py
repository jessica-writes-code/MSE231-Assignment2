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
for hack, group in groupby(data, itemgetter(0)):
    # print >> sys.stderr, group
    group = sorted(group, key=itemgetter(2)) 
    
    #2 and #6 needs to be unix time
    previous_trip_end_time = None
    current_hour = None #start of the hour
    dict_features = {'t_onduty': 0.0, #hours
                     't_occupied': 0.0, #hours
                     'n_pass': 0.0,
                     'n_trip': 0.0,
                     'n_mile': 0.0,
                     'earnings': 0.0,
                     'money_list': [0.0]*6} #cash (earnings, tip), credit (same), other (same)
    
    for record in group:

        # process
        try:
            current_start_time = datetime.strptime(record[2], "%Y-%m-%d %H:%M:%S")
            current_end_time = datetime.strptime(record[6], "%Y-%m-%d %H:%M:%S")
        except:
            print >> sys.stderr, "error"
            continue

    
        current_hour_of_trip = current_start_time - timedelta(minutes=current_start_time.minute,
                                                              seconds=current_start_time.second)

        t_onduty_extra_time = 0.0
        if previous_trip_end_time is None:
            current_hour = current_hour_of_trip
            previous_trip_end_time = current_start_time
        elif current_hour != current_hour_of_trip:
            # t_onduty
            if current_start_time - previous_trip_end_time < timedelta(minutes=30):
                dict_features['t_onduty'] += (current_hour + timedelta(hours=1) - previous_trip_end_time).seconds / 3600.0
                t_onduty_extra_time = (current_start_time - current_hour_of_trip).seconds / 3600.0 

            # dump and flush
            dict_features = end_hour(current_hour, hack, dict_features)
            # update the current
            current_hour = current_hour_of_trip

        dict_features['n_pass'] += int(record[7])
        dict_features['n_trip'] += 1
        trip_time = current_end_time - current_start_time
        dict_features['t_onduty'] += t_onduty_extra_time
        
        if current_end_time.hour == current_start_time.hour:
            dict_features['n_mile'] += float(record[8])
            dict_features['earnings'] += float(record[5])
            dict_features['t_occupied'] += trip_time.seconds / 3600.0 

            # t_onduty
            if current_start_time - previous_trip_end_time < timedelta(minutes=30) and previous_trip_end_time >= current_hour:
                dict_features['t_onduty'] += (current_end_time - previous_trip_end_time).seconds / 3600.0
            else:
                dict_features['t_onduty'] += trip_time.seconds / 3600.0

            # extra earnings
        else:
            trip_time_within_hour = (current_hour + timedelta(hours=1) - current_start_time)
            proportion_in_hour = float(trip_time_within_hour.seconds) / trip_time.seconds
            dict_features['n_mile'] += proportion_in_hour * float(record[8])
            dict_features['earnings'] += proportion_in_hour * float(record[5])
            dict_features['t_occupied'] += trip_time_within_hour.seconds / 3600.0

            #t_onduty
            if current_start_time - previous_trip_end_time < timedelta(minutes=30) and previous_trip_end_time >= current_hour:
                dict_features['t_onduty'] += (current_hour + timedelta(hours=1) - previous_trip_end_time).seconds / 3600.0
            else:
                dict_features['t_onduty'] += trip_time_within_hour.seconds / 3600.0

            # t_onduty
            # flush this hour:
            dict_features = end_hour(current_hour, hack, dict_features)
            current_hour += timedelta(hours=1)
            while current_hour.hour != current_end_time.hour:
                dict_features['n_mile'] += 3600.0 / trip_time.seconds * float(record[8])
                dict_features['earnings'] += 3600.0 / trip_time.seconds * float(record[5])
                dict_features['t_occupied'] = 1.0
                dict_features['t_onduty'] = 1.0
                #extra earnings
                dict_features = end_hour(current_hour, hack, dict_features)
                current_hour += timedelta(hours=1)

            # rest of the part of trip
            trip_time_within_hour = (current_end_time - current_hour)
            proportion_in_hour = float(trip_time_within_hour.seconds) / trip_time.seconds
            dict_features['n_mile'] += proportion_in_hour * float(record[8])
            dict_features['earnings'] += proportion_in_hour * float(record[5])
            dict_features['t_occupied'] += trip_time_within_hour.seconds / 3600.0
            dict_features['t_onduty'] += trip_time_within_hour.seconds / 3600.0

        #print current_start_time,':', dict_features['t_onduty']
        previous_trip_end_time = current_end_time
    dict_features = end_hour(current_hour, hack, dict_features)
