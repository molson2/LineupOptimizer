library(dplyr)
library(stringr)

# Load DBS
my_db <- src_sqlite(path="fantasyFootball2015.db")
src_tbls(my_db)
offensive <- collect(tbl(my_db, 'offensive'))
dst <- collect(tbl(my_db, 'dst'))
kicker <- collect(tbl(my_db, 'kicker'))
matchups <- collect(tbl(my_db, 'matchups'))
fan_duel <- collect(tbl(my_db, 'fan_duel'))
RSQLite::dbDisconnect(my_db$con)
rm(my_db)

# Merge matchup data
matchup_long <- with(matchups,data.frame(team=c(away, home),
                                         opp=c(home, away),
                                         home = rep(c(F,T), each=length(away)),
                                         team_score=c(away_score, home_score),
                                         opp_score=c(home_score, away_score),
                                         week=c(week,week)))
matchup_long <- matchup_long %>% arrange(week)

offensive <- merge(matchup_long, offensive, by=c("team", "week")) %>%
    select(-team, -opp, -team_score, -opp_score, everything())

dst <- merge(matchup_long, dst, by=c("team", "week")) %>%
    select(-team, -opp, -team_score, -opp_score, everything())

kicker <- merge(matchup_long, kicker, by=c("team", "week")) %>%
    select(-team, -opp, -team_score, -opp_score, everything())

matchups <- matchup_long
rm(matchup_long)

# re-write name in fan_duel data to flip from "last, first" to "first last"
# still a little frustrating that first names get abbreviated, so maybe can
# do a reg-exp to match on these
fdNames <- fan_duel$name
commaIx <- grepl(",", fdNames)
fdNames <- fdNames[commaIx]
newNames <- sapply(strsplit(fdNames, split=","), function(x) paste(x[2], x[1]))
newNames <- str_trim(newNames)
fan_duel$name[commaIx] <- newNames
rm(fdNames, newNames, commaIx)

# Function for calculating fantasy points
ffpoints <- function(row, pos){
    # Calculate fantasy football points for player x, which is a row of a data
    # frame
    if(pos %in% c("QB", "RB", "WR", "TE")){
        points <- with(row,{
            rush_yd*(.1) + 
            rush_td*(6) + 
            pass_yd*(0.04) + 
            pass_td*(4) + 
            pass_int*(-1) + 
            rec_yd*(0.1) +
            rec_td*(6) + 
            rec_reception*(0.5) +
            fumble_lost*(-2)})
    } else if(pos == "K"){
        points <- with(row,{
            xp*(1) +
            fg*(3.5)}) # not perfect, but I don't have distance data
    } else if(pos == "DST"){
        points <- with(row, {
            sacks*(1) +
            dfr*(2) +
            dtd*(6) +
            int*(2) +
            10*(pa <= 10) +
            7*(pa >=1 & pa <= 6) +
            4*(pa >=7 & pa <= 13) +
            1*(pa >=14 & pa <= 20) +
            (-1)*(pa >=28 & pa <= 34) +
            (-4)*(pa >=35)})
    } else{
        stop("Position must be one of: QB, RB, WR, TE, K, DST")
    }
       points
   
}

# Calculate "historical fantasy points for each team (rough)
offensive$fp <- rep(NA, nrow(offensive))
for(i in 1:nrow(offensive)){
    val <- ffpoints(offensive[i,], offensive[i, "pos"])
    offensive$fp[i] <- val
}

kicker$fp <- rep(NA, nrow(kicker))
for(i in 1:nrow(kicker)){
    val <- ffpoints(kicker[i,], "K")
    kicker$fp[i] <- val
}

dst$fp <- rep(NA, nrow(dst))
for(i in 1:nrow(dst)){
    val <- ffpoints(dst[i,], "DST")
    dst$fp[i] <- val
}

rm(i, val)
