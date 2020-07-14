data_cleaning <- function(data, factors){
  data <- data%>% filter(!(Zone.Beat=="" & Longitude==0))
    data[factors] <- lapply(data[factors], function(x) as.factor(x))
 
  names(data)[names(data)=="Occurred.Date.or.Date.Range.Start"]<-"EventStart"
  names(data)[names(data)=="Date.Reported"]<- "EventReported"
  names(data)[names(data)=="Occurred.Date.Range.End"] <- "EventEnd"
  names(data)[names(data)=="Summarized.Offense.Description"] <- "Offense"
  names(data)[names(data)=="District.Sector"] <- "District"
  names(data)[names(data)=="Zone.Beat"] <- "Zone"
  
  data$EventStart <- mdy_hms(data$EventStart)
  data$EventEnd <- mdy_hms(data$EventEnd)
  data$EventReported <- mdy_hms(data$EventReported)
  
  data$DateStart <- format(as.POSIXct(data$EventStart,format="%Y-%m-%d %H:%M:%S"),"%m-%d")
  data$WeekStart <- format(as.POSIXct(data$EventStart,format="%Y-%m-%d %H:%M:%S"),"%W")
  data$DateEnd <- format(as.POSIXct(data$EventEnd,format="%Y-%m-%d %H:%M:%S"),"%m-%d")
  data$WeekEnd <- format(as.POSIXct(data$EventEnd,format="%Y-%m-%d %H:%M:%S"),"%W")
  data$DateReported <- format(as.POSIXct(data$EventReported,format="%Y-%m-%d %H:%M:%S"),"%m-%d")
  data$WeekReported <- format(as.POSIXct(data$EventReported,format="%Y-%m-%d %H:%M:%S"),"%W")
  
  data$TimeStart <- format(as.POSIXct(data$EventStart,format="%Y-%m-%d %H:%M:%S"),"%H")
  data$TimeEnd <- format(as.POSIXct(data$EventEnd,format="%Y-%m-%d %H:%M:%S"),"%H")
  data$TimeReported <- format(as.POSIXct(data$EventReported,format="%Y-%m-%d %H:%M:%S"),"%H")
  
  
  
  drop <- c("EventStart", "EventEnd", "EventReported", 'Year')
  data <- data[, !(names(data) %in% drop)]
  
  return(data)
}
allocate_maps <- function(){
  register_google(key="AIzaSyChqgC6g-pMlpbZxR4yxIIVzAlAiijSHmY")
  Seattle = qmap("Seattle", zoom = 11,
                 source="stamen", maptype="toner", darken = c(.3,"#BBBBBB"))
  UDistrict = qmap("University District, Seattle", zoom = 14, 
                   source="stamen", maptype="toner",darken = c(.3,"#BBBBBB"))
  
  E2District = qmap("Pike/Pine District, Seattle", zoom = 14, 
                    source="stamen", maptype="toner",darken = c(.3,"#BBBBBB"))
  
  return(list("Seattle"=Seattle, "UDistrict"=UDistrict, "E2District"=E2District))
}


library(dplyr)
library(ggplot2)
library(class)
library(ggmap)
library(lubridate)


seattle <- read.csv("seattle_incidents_summer_2014.csv")
factors <- c('District.Sector', 'Zone.Beat', 'Month', 'Summarized.Offense.Description', 'Summary.Offense.Code', 'Offense.Code.Extension')
seattle_clean <- data_cleaning(seattle, factors)

### Conto dei crimini riportati per distretto
#numero dei distretti
Theme = theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)) 

##Tabella con conto di specifici reati per zona
zone_offense_count<-seattle_clean%>%
  group_by(Zone, Offense)%>%
  summarise(N_Offense_Per_Zone=n())
names(zone_offense_count)<-c('Zone', 'Offense', 'N_Offense_Per_Zone')

factors <- c('District', 'Zone', 'Month', 'Offense', 'Summary.Offense.Code', 'Offense.Code.Extension')
seattle_district <- seattle_clean[factors]



total_per_district<-seattle_district%>%
  group_by(District, Zone)%>%summarise(Total_per_Zone=n())

ggplot(total_per_district, aes(Zone, Total_per_Zone, color=District))+
  geom_point()+Theme

ggplot(zone_offense_count, aes(Offense, N_Offense_Per_Zone, color=Zone))+
  geom_point()+Theme



### Andamento giornaliero e orario reati
offense_per_week<-seattle_clean %>% group_by(WeekStart) %>% summarise(N_Offense_Per_Week=n())

offense_per_time<-seattle_clean %>%
  group_by(TimeStart) %>% summarise(N_Offense_Per_Time=n())

ggplot(offense_per_week, aes(WeekStart, N_Offense_Per_Week))+
  geom_line(aes(group=1))+geom_point()+Theme

ggplot(offense_per_time, aes(TimeStart, N_Offense_Per_Time))+
  geom_line(aes(group=1))+geom_point()+Theme

## Variazione numero reati per mese
n_offense_per_month<-seattle_district %>% group_by(Month, Offense)%>%summarise(Offense_count=n())
tot_offense_per_month<-seattle_district %>% group_by(Month)%>% summarise(Offense_total=n())


## top 6 reati per mese
top_offense <- n_offense_per_month %>% group_by(Month)%>%top_n(6, Offense_count)
ggplot(top_offense, aes(x=Month, y=Offense_count, fill=Offense))+
  geom_col(position = 'dodge2')


##andamento top 5 reati 6 per settimana
top_offense_per_week <- seattle_clean %>% group_by(WeekStart, Offense)%>%
  summarise(Offense_count=n())%>%top_n(5, Offense_count)

ggplot(top_offense_per_week, aes(x=WeekStart, y=Offense_count, color=Offense))+
geom_point()+geom_line(aes(group=Offense))

## quali reati di notte
night <- c(23, 00, 01, 02, 03, 04, 05)
cols <- c('District', 'Zone', 'Offense', 'Month', 'WeekStart', 'TimeStart')

offense_at_night <- seattle_clean[seattle_clean$TimeStart %in% night, cols] %>%
  group_by(Offense) %>% summarise(Offense_total=n()) %> %top_n(5, Offense_total)

## Reato e numero di reati per ora del giorno (top 6 per ora)
a <- seattle_clean %>%
  group_by(TimeStart, Offense) %>% summarise(N_Offense_Per_Time=n())%>%
  top_n(5, N_Offense_Per_Time)


#Seleziono i 6 reati in maggior numero totale
top_off <- c('ASSAULT', 'BURGLARY', 'CAR PROWL', 'OTHER PROPERTY', 'PROPERTY DAMAGE', 'VEHICLE THEFT')

#andamento orario dei 6 reati più comuni
ggplot(a[a$Offense %in% top_off, ], aes(x=TimeStart, y=N_Offense_Per_Time, color=Offense))+
  geom_point()+geom_line(aes(group=Offense))


## Tabella con densità di reato di Car Prowl e Vehicle Theft per zona
zone_of_offense <- seattle_clean %>% 
  filter(Offense=='CAR PROWL' | Offense=='VEHICLE THEFT')%>% 
  select(District, Zone, Offense, Longitude, Latitude)

maps <- allocate_maps()
Seattle <- maps$Seattle
UDistrict <- maps$UDistrict
E2District <-maps$E2District
Seattle + geom_point(data=zone_of_offense[zone_of_offense$Offense=='CAR PROWL', ], aes(x=Longitude, y=Latitude),
                     color="dark green", alpha=.15, size=2)



UDistrict + geom_point(data=zone_of_offense[zone_of_offense$Offense=='VEHICLE THEFT', ], aes(x=Longitude, y=Latitude),
                     color="dark green", alpha=.15, size=2)

Seattle + stat_density2d(
  aes(x = Longitude, y = Latitude, fill = ..level.., alpha = ..level..),
  size = 2, bins = 4, data = seattle_clean[seattle_clean$Offense=='ASSAULT', ],
  geom = "polygon"
)

E2District + 
  geom_point(data=seattle_clean[seattle_clean$Offense %in% top_off, ], aes(x = Longitude, y = Latitude, color=Offense))
