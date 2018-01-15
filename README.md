# pyGHCND

Utilities to Download, Read, Convert and Use GHCN Daily data
 see NOAA-NCDC website 
 Datafiles for a year ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/by_year

dloadGHCND(year='current', outfile=None, outpath=None):
    Downloads GHCN Daily Weather station data in compressed (.gz) form
    Current year is the default.
    Renames local file using GHCND prefix  2017.csv.gz --> GHCND2017.csv.gz

