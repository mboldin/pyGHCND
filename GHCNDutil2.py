## GHCN Daily Weather data utilities
##  M Boldin April 2016 || modified  Dec 2017 / Jan 2018
##  Supports updates to Boldin-Wright Weather calculations
##   set up for Python 3.4

##    ID = 11 character station identification code
##    YEAR/MONTH/DAY = 8 character date in YYYYMMDD format (e.g. 19860529 = May 29, 1986)
##    ELEMENT = 4 character indicator of element type 
##    DATA VALUE = 5 character data value for ELEMENT 
##    M-FLAG = 1 character Measurement Flag 
##    Q-FLAG = 1 character Quality Flag 
##    S-FLAG = 1 character Source Flag 
##    OBS-TIME = 4-character time of observation in hour-minute format (i.e. 0700 =7:00 am)

###############################

import os
import datetime as dt
import time
from math import floor

from pprint import pprint
import urllib

import gzip
import csv
import io
import pickle
import sqlite3 as sql
import shutil

import numpy as np
import pandas as pd
from pandas import HDFStore, DataFrame
import h5py

########################################################################

def UncompressGz(file1,file2):
    #Uncompress CSV.GZ -> .CSV 
    file2 = os.path.join(fdir ,'GHCND' + str(year) + '.csv')
    outfh = open(file2, 'wb')
    with gzip.open(file1, 'rb') as infh:
        shutil.copyfileobj(infh, outfh)
    outfh.close()
    fh = open(file2)
    fstats = os.fstat( fh.fileno()  )
    fsize = fstats.st_size / (1000**2)
    print ("  created: %s" % time.ctime(os.path.getctime(file2)) )
    print ("  size: %s MB" % fsize)
    fh.close()

def ChunkGenerator(reader, chunksize= 1000):
    """ 
    Chunk Generator. Take a iterable reader (such as fh.readlines, or CSV reader)
    and yield  chunksize slices. 
    """
    chunksize = int(chunksize)
    chunk = []
    for i, line in enumerate(reader):
        if (i % chunksize == 0 and i > 0):
            yield chunk
            del chunk[:]
        chunk.append(line)
    yield chunk


def ReadCSV(file):
    fh = open(file,'r')
    chunk_size = int(1E6)
    wdat=[]
    #CSV module read with Chunk Generator
    for k, chunk in enumerate(ChunkGenerator(fh,chunk_size)):
        reader = csv.reader(chunk, delimiter=',')
        chunk2 = list(reader)   
        wdat.extend(chunk2)
        if k % 10 == 0:
            pass
            #print(k, len(chunk2), len(wdat))
    fh.close()
    return wdat


def PdReadCSV(file):
    ## Read CSV using Pandas
    from pandas import read_csv
    cnames= [ 'GHCNDid', 'Date', 'Element', 'Value', 'Mflag', 'Qflag', 'Sflag', 'Otime']
    fh = read_csv(file, chunksize = 10000, 
                        header=None, names= cnames,
                        converters = { 'Value' : float },
                        parse_dates= ['Date',], infer_datetime_format= True )
    a = fh.read()
    fh.close()
    return a

def saveSQLdb(db, data, table= None):  
    from sqlite3 import connect
    # save as SQLite database, need chunksize
    if isinstance(db,str):
        dbcon = connect(file2b)
    else:
        dbcon = db
    chunksize = int(10**6) 
    data.to_sql(table, dbcon, chunksize= chunksize)
    dbcon.close()

def readSQLdb(db, table= None):  
    from sqlite3 import connect
    from pandas import read_sql
    # Read as SQLite database, need chunksize
    if isinstance(db,str):
        dbcon = connect(file2b)
    else:
        dbcon = db
    #chunksize = int(10**6) 
    data = read_sql('select * from %s' % table, dbcon)
    dbcon.close()
    return data

#######################################################################

if __name__== '__main__':

    dt0 = dt.datetime.now()
    wdir = r'/home/michael/Desktop/PyProg/GitHub/PyWeather'
    os.chdir(wdir)
    
    ## File output directory
    fdir = os.path.join(wdir,'outx')

    year = 2018
    print('Extract GHCND %s csv.gz file to: %s' % (year, fdir))

    file1 = os.path.join(fdir ,'GHCND' + str(year) + '.csv.gz')
    fh = open(file1)
    fstats = os.fstat( fh.fileno()  )
    fsize = fstats.st_size / (1000**2)
    print(file1)
    print ("  last modified: %s" % time.ctime(os.path.getmtime(file1)) )
    print ("  created: %s" % time.ctime(os.path.getctime(file1)) )
    print ("  size: %s MB" % fsize)
    fh.close()

    #Uncompress CSV.GZ -> .CSV
    file2 = os.path.join(fdir ,'GHCND' + str(year) + '.csv')
    #UncompressGz(file1,file2)
    
    ## Read CSV
    #wdat = ReadCSV(file2)
    print( file2, len(wdat) )
    
    ## Read CSV using Pandas
    #b = PdReadCSV(file2)
    print( len(b) )
    print( b.iloc[:5,:])

    #Save as SQLite database, need chunksize    
    file2b = os.path.join(fdir, 'bGHCND' + str(year) + '.db')
    table = 'GHCND' + str(year) + 'a'
    #saveSQLdb(file2b, b, table= table)  

    #b2 = readSQLdb(file2b, table= table)  

    ## Check
    cnames= [ 'GHCNDid', 'Date', 'Element', 'Value', 'Mflag', 'Qflag', 'Sflag', 'Otime']
    k = 1
    x= b2.loc[:,cnames[k]]==b2.loc[:,cnames[k]]
    print( x.all() )
    
