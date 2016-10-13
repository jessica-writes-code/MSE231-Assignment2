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

