library(dplyr)
library(ggplot2)

obs <- read_csv("./observed/CHIANG_RAI_TH_TH000048303_1951-2019.csv", 
                col_types = cols(TAVG = col_double(),
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
obs_lat <- as.numeric(unique(obs['LATITUDE']))
obs_lon <- as.numeric(unique(obs['LONGITUDE']))
mod_lats <- unique(mod['lat'])
mod_lons <- unique(mod['lon'])
grid_lat <- as.numeric(mod_lats[which(abs(mod_lats-obs_lat) == min(abs(mod_lats-obs_lat))), 1])
grid_lon <- as.numeric(mod_lons[which(abs(mod_lons-obs_lon) == min(abs(mod_lons-obs_lon))), 1])


# cleansing RCM model and observed data
obs_clean <- na.omit(obs)
obs_clean <- obs_clean %>% filter(DATE >= "1970-01-01", DATE <= "2005-12-01")
# filter grid and date
mod_clean <- mod %>% filter(lat==grid_lat, lon==grid_lon)
mod_clean <- mod_clean %>% subset(date %in% obs_clean$DATE)

obs.train <- obs_clean %>% filter(DATE < "2000-01-01")
mod.train <- mod_clean %>% filter(date < "2000-01-01")
obs.test <- obs_clean %>% filter(DATE >= "2000-01-01")
mod.test <- mod_clean %>% filter(date >= "2000-01-01")

qm <- fitQmap(obs.train$PRCP, mod.train$pr)
