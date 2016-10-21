library(dplyr)
library(ggplot2)

# Load data
taxi_df <- data.frame()
for (i in 0:10) {
  df_curr <- read.csv(paste0("Aggregate Data/part-",sprintf("%05d",i)), sep="\t", header=FALSE)
  taxi_df <- rbind(taxi_df, df_curr)
}
names(taxi_df) <- c("date","hour", "n_onduty","n_occupied", "t_onduty", "t_occupied",
                    "n_pass","n_trips", "n_miles","earnings","cash_earnings","cash_tip",
                    "credit_earnings","credit_tip","other_earnings","other_tip")

precip_df <- read.csv("nyc_precipitation.csv", sep=",", header=TRUE, as.is=TRUE)

# Standardize and format data
precip_df$hour <- as.integer(substr(precip_df$DATE, 10, 11))
precip_df$date <- paste0(substr(precip_df$DATE, 1, 4),"-",substr(precip_df$DATE, 5, 6),"-",substr(precip_df$DATE, 7, 8))

taxi_df$date <- as.character(taxi_df$date)

# Join data
combined_data <- taxi_df %>% left_join(precip_df, by = c("date","hour"))
combined_data$HPCP <- ifelse(is.na(combined_data$HPCP), -1, combined_data$HPCP)
combined_data$precip_level <- ifelse(combined_data$HPCP >= 1, "> 1in", 
                                     ifelse(combined_data$HPCP >= 0, "0in to 1in", 
                                            "No rain"))
combined_data$precip_level <- factor(combined_data$precip_level, levels=c("No rain","0in to 1in","> 1in"), ordered = TRUE)

# Supply & Demand Analysis
## Data frame manipulation
taxi_rain_df <- combined_data %>% 
                  group_by(hour, precip_level) %>%
                    summarise(total_hours=n(),
                              total_earnings = sum(earnings),
                              total_t_onduty = sum(t_onduty),
                              total_t_occupied = sum(t_occupied),
                              total_n_trips = sum(n_trips)) %>%
                      mutate(earnings_per_t_onduty = total_earnings/total_t_onduty,
                             avg_trip_length = total_t_occupied/total_n_trips,
                             avg_t_onduty = total_t_onduty/total_hours,
                             avg_t_occupied = total_t_occupied/total_hours,
                             ratio_occupied_onduty = total_t_occupied/total_t_onduty)

## Earnings/Hour On Duty
ggplot(taxi_rain_df, aes(x=hour, y=earnings_per_t_onduty, group=precip_level, colour=precip_level)) +
  geom_line()

## Average Trip Length
ggplot(taxi_rain_df, aes(x=hour, y=avg_trip_length, group=precip_level, colour=precip_level)) +
  geom_line()

## Average Driver-Hours On-Duty
ggplot(taxi_rain_df, aes(x=hour, y=avg_t_onduty, group=precip_level, colour=precip_level)) +
  geom_line()

## Average Driver-Hours Occupied
ggplot(taxi_rain_df, aes(x=hour, y=avg_t_occupied, group=precip_level, colour=precip_level)) +
  geom_line()

## Ratio of Occupied to Onduty
ggplot(taxi_rain_df, aes(x=hour, y=ratio_occupied_onduty, group=precip_level, colour=precip_level)) +
  geom_line()


Argument:
  drivers make less money per hour b/c trips take longer
    - $/time on duty
    - avg. trip length
   --> drivers are not incentivized to drive more in the rain
      we agree w/ farber 
  
  supply: # time onduty
    - no substantive change in number of drivers working during rain/not rain
    - not in line w/ farber's conclusions that there are fewer cabs working when it rains
    
  demand: # time occupied
    - there is an increase in demand when it rains (in line w/ Farber's conclusions)
    
  ratio of supply to demand = more important
    - occupied/on-duty
      
      