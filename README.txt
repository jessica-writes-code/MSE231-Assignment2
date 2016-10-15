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
    Output
        Tab-separated records which include both trip and fare information for 
        all matching records (i.e., those appearing in both files).
    Notes:
        The reduce step performs filtering for obviously erroneous data. 
        See the corresponding report for additional details.

