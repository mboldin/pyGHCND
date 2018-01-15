## Download GHCN Daily data
##   M Boldin (mdboldin@gmail.com)
##    version 1:  2105 updates/mods:  2016, 2017
##    latest: Jan 2018

##    Pulls NOAA-NCDC website file for a year
##      ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/by_year
##    Note-- will overwrite a existing local file

#############################################################################

def dloadGHCND(year='current', outfile=None, outpath=None):
    """
    Downloads GHCN Daily Weather station data in compressed (.gz) form
    from NOAA-NCDC ftp location
      ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/by_year
    The file is either a full year or the current year to date.
    Current year is the default.
    Renames local file using GHCND prefix  2017.csv.gz --> GHCND2017.csv.gz
    """

    import  os.path
    import datetime as dt
    from urllib import request

    dt0= dt.datetime.now()
    if year == 'current':
         year = dt0.year       

    rootURL = "ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/by_year"   # base URL for all files
    filesuffix = ".csv.gz" # suffix for all of the raw files 
    saveVersion= '' 
    
    # Start by constructing filenames with paths
    filename = str(year) + filesuffix
    fullURL = rootURL + "/" + str(year) + filesuffix
    if outfile == None or not outfile:
        outfile = r'GHCND' + str(year) + saveVersion + filesuffix
    if outpath:
        outfile = os.path.join(outpath,outfile)
    else:
        pass
        
    # TRY Download of file with basic error handling
    try:
        print('Trying to download NOAA-NCDC GHCN Daily file for year: %s' % year) 
        print('  Root URL: %s ' % rootURL) 
        print('  Filename: %s ' % filename) 
        print('  Outfile: %s ' % outfile) 
        a = request.urlretrieve(url=fullURL, filename = outfile)
    except OSError as e:
        print(e)
    except:
        print('Error retrieving and/or saving', fullURL, filename, a, end='\n')
    else: # if no errors, then
        msg= "   ... retrieved  ... wrote output to: %s "  % outfile
        print ( msg )        
        dt1= dt.datetime.now()
        print ('Finished in %s seconds' % (dt1-dt0).seconds )
        print ('Date/time:', dt1)
        

####################################################
if __name__ == '__main__':

    ## Current Year download
    dloadGHCND()

    # Multiyear with outpath
    #out = r' .... '
    #for year in range(2012,2018+1):
    #    dloadGHCND(year,outpath = out)
    
