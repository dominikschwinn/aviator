#load csv airport file
airport_file = "C:/_aviation/aviation/data/iata_airport_list.csv"
airports <- read.csv(airport_file)
print(airports)
# number of rows in airports
nrow(airports)
# number of columns in airports
ncol(airports)
# print airports with cell == True (='is na') or False (='is not na')
is.na(airports)
