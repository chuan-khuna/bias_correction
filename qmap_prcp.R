library(ggplot2)
library(tidyverse)
library(qmap)
library(hydroGOF)
library(EnvStats)

obs <- read_csv("./observed/CHIANG_RAI_TH_TH000048303_1951-2019.csv", 
                col_types = cols(
                                  TAVG = col_double(),
                                  TMIN = col_double(),
                                  TMAX = col_double(),
                                  PRCP = col_double()
                                )
                )
mod <- read_csv("./RCM/RCM_hist_TH.csv")

# convert kelvin to celcius
mod <- mod %>% mutate(tas=tas-273.15)
mod <- mod %>% mutate(tasmin=tasmin-273.15)
mod <- mod %>% mutate(tasmax=tasmax-273.15)
# convert prcp unit to mm/day
mod <- mod %>% mutate(pr=pr*86400)

# find RCM min grid center from station
obs_lat <- unique(obs$LATITUDE)
obs_lon <- unique(obs$LONGITUDE)
mod_lats <- unique(mod$lat)
mod_lons <- unique(mod$lon)
grid_lat <- mod_lats[which.min(abs(mod_lats-obs_lat))]
grid_lon <- mod_lons[which.min(abs(mod_lons-obs_lon))]


# cleansing RCM model and observed data
obs_clean <- na.omit(obs)
obs_clean <- obs_clean %>% filter(DATE >= "1970-01-01", DATE <= "2005-12-01")
# filter grid and date
mod_clean <- mod %>% filter(lat==grid_lat, lon==grid_lon)
mod_clean <- mod_clean %>% subset(date %in% obs_clean$DATE)

obs_train <- obs_clean %>% filter(DATE < "2000-01-01")
mod_train <- mod_clean %>% filter(date < "2000-01-01")
obs_test <- obs_clean %>% filter(DATE >= "2000-01-01")
mod_test <- mod_clean %>% filter(date >= "2000-01-01")

# Select index
mod_ind <- 'pr'
obs_ind <- 'PRCP'

# Qmap Empirical Quantile mapping
qm <- fitQmapSSPLIN(obs_train[, obs_ind], mod_train[, mod_ind], 
                  qstep=0.001)

mod_train_corrected <- doQmap(mod_train[, mod_ind], qm)
mod_test_corrected <- doQmap(mod_test[, mod_ind], qm)

print(sprintf("Train: %f", mae(mod_train[, mod_ind], obs_train[, obs_ind])))
print(sprintf("Train bias corrected: %f", mae(mod_train_corrected, obs_train[, obs_ind])))

print(sprintf("Test: %f", mae(mod_test[, mod_ind], obs_test[, obs_ind])))
print(sprintf("Test bias corrected: %f", mae(mod_test_corrected, obs_test[, obs_ind])))


summary(obs_test %>% dplyr::select(DATE:TMIN))
summary(mod_test %>% dplyr::select(tas:pr))
