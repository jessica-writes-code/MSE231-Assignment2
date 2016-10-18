subset_january.py
    Subsets input data to data set containing only entries from January 15.
    Input:
        CSV file with one column named "pickup_datetime"; date must be formatted
        as "YEAR-MONTH-DATE".
    Output:
        CSV file with the same header & format as the input
        file, but subsetted to include only records where the "pickup_datetime"
        is January 15 (i.e., pickup_datetime includes "2013-01-15")
    Use:
        input.csv | python subset_january.py > output.csv
    Notes:
        In order to obtain both subsetted trip data and subsetted fare data,
        we ran this script separately on each of the provided January data sets

join_map.py and join_reduce.py
    Perform the map and and reduce steps (respectively) to join trip and fare data.
    Input:
        At least two CSV files with the same form as those located at 
        https://5harad.com/data/nyctaxi/2013_trip_data_1.csv.gz and 
        https://5harad.com/data/nyctaxi/2013_trip_fare_1.csv.gz
        There should be at least one CSV file of the "trip_data" format
        and one CSV file of the "trip_fare" format. Ideally, these should have 
        records which match on medallion, hack license, and pickup_datetime.
    Output:
        Tab-separated records which include both trip and fare information for 
        all matching records (i.e., those appearing in both files).
    Notes:
        The reduce step performs filtering for obviously erroneous data.
        Specifically, the reduce step eliminates records for which:
        - no data exists about either the trip or the fare
        - total fare was less than $2.50
        - total passengers was either not an integer, less than 0 or equal to 0
        - trip time was less than or equal to 0
        - trip distance is less than or equal to 0

driver_stats_map.py and driver_stats_reduce.py
    Perform the map and reduce steps (respectively) to aggregate trip-level data
    to driver-hour-level data.
    Input:
        Tab-separated data of the form outputted by join_reduce.py
    Output:
        Tab-separated records at the driver-hour level (i.e., each record identifies
        one driver in one hour). Output records contain the following fields, in order:
            date
            hour
            hackID
            t_onduty - fraction of hour the driver was on-duty
            t_occupied - fraction of hour the driver was occupied with rides
            n_pass - number of passengers whose rides started in the hour
            n_trip - number of trips started in the hour
            n_mile - number of miles driven in the hour
            earnings - amount earned in the hour
            cash earnings - amount earned via cash in the hour
            cash tip - amount tipped via cash in the hour
            credit earnings - amount earned via credit card in the hour
            cash fare - amount tippped via credit card in the hour
            other earnings - amount earned via non-cash, non-credit in the hour
            other tip - amount earned via non-cash, non-credit in the hour
    Notes:
        1) t_occupied is calculated assuming a driver is "on-duty" between the 
        beginning of his/her frist trip after a (at least) half-hour break and 
        his/her next half-hour break
        2) When trips begin in one hour and end in another, n_mile and earnings
        allocate miles and earnings in accordance with the proportion of the trip
        that occurred in each hour 
        3) Cash tip is not systematically recorded in the data; it is almost 
        always zero. The last six columns record the fare & tip for distinct
        types of transactions so that cash tips can be estimated later.