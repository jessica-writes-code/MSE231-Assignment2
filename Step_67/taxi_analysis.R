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
precip_df$DATE <- as.POSIXct(precip_df$DATE, format="%Y%m%d %H:%M") - 3600
precip_df$DATE <- as.character(precip_df$DATE)

precip_df$hour <- as.integer(substr(precip_df$DATE, 12, 13))
precip_df$date <- substr(precip_df$DATE, 1, 10)

taxi_df$date <- as.character(taxi_df$date)

# Join data
combined_data <- taxi_df %>% left_join(precip_df, by = c("date","hour"))

# Write-out Table
combined_data_out <- combined_data[,c("date","hour","HPCP","n_onduty","n_occupied", "t_onduty", "t_occupied", "n_pass", "n_trips", "n_miles", "earnings")]
names(combined_data_out) <- c("date","hour","precip","drivers_onduty","drivers_occupied", "t_onduty", "t_occupied", "n_pass", "n_trip", "n_mile", "earnings")
write.table(combined_data_out, file="taxi_precip_data.tsv", sep="\t")

# Supply & Demand Analysis
## Remove NAs in precipitation data
combined_data$HPCP <- ifelse(is.na(combined_data$HPCP), -1, combined_data$HPCP)
combined_data$precip_level <- ifelse(combined_data$HPCP >= 1, "> 1in", 
                                     ifelse(combined_data$HPCP >= 0, "0in to 1in", 
                                            "No rain"))
combined_data$precip_level <- factor(combined_data$precip_level, levels=c("No rain","0in to 1in","> 1in"), ordered = TRUE)


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
                             ratio_occupied_onduty = total_t_occupied/total_t_onduty,
                             disp_hour = hour + 0.5)

## Earnings/Hour On Duty
ggplot(taxi_rain_df, aes(x=disp_hour, y=earnings_per_t_onduty, group=precip_level, colour=precip_level)) +
  geom_line() +
  scale_x_continuous(breaks=seq(0,25,by=3)) +
  labs(x="Hour of Day", y="$ per Driver-Hours Onduty") +
  theme(legend.position="bottom") +
  theme(legend.title=element_blank())
ggsave("Earnings_Per_TOnduty.png", width=6, height=4)

## Average Trip Length
ggplot(taxi_rain_df, aes(x=hour, y=avg_trip_length, group=precip_level, colour=precip_level)) +
  geom_line() +
  scale_x_continuous(breaks=seq(0,25,by=3)) +
  labs(x="Hour of Day", y="Avg. Trip Length (Prop. of Hour)") +
  theme(legend.position="bottom") +
  theme(legend.title=element_blank())
ggsave("Avg_Trip_Length.png", width=6, height=4)

## Average Driver-Hours On-Duty
ggplot(taxi_rain_df, aes(x=hour, y=avg_t_onduty, group=precip_level, colour=precip_level)) +
  geom_line() +
  scale_x_continuous(breaks=seq(0,25,by=3)) +
  labs(x="Hour of Day", y="Avg. Driver-Hours On-Duty") +
  theme(legend.position="bottom") +
  theme(legend.title=element_blank())
ggsave("Avg_Driver_Hours_OnDuty.png", width=6, height=4)

## Average Driver-Hours Occupied
ggplot(taxi_rain_df, aes(x=hour, y=avg_t_occupied, group=precip_level, colour=precip_level)) +
  geom_line() +
  scale_x_continuous(breaks=seq(0,25,by=3)) +
  labs(x="Hour of Day", y="Avg. Driver-Hours Occupied") +
  theme(legend.position="bottom") +
  theme(legend.title=element_blank())
ggsave("Avg_Driver_Hours_Occupied.png", width=6, height=4)

## Ratio of Occupied to Onduty
ggplot(taxi_rain_df, aes(x=hour, y=ratio_occupied_onduty, group=precip_level, colour=precip_level)) +
  geom_line()+
  scale_x_continuous(breaks=seq(0,25,by=3)) +
  labs(x="Hour of Day", y="Occupied/Onduty Ratio") +
  theme(legend.position="bottom") +
  theme(legend.title=element_blank())
ggsave("Occupied_Onduty_Ratio.png", width=6, height=4)
      
      