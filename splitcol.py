#!/usr/bin/python3
# splitcol.py outfile ext header-pattern

import csv
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='split to separate files baseNNN.ext')
    parser.add_argument('outfile',help='base name of output files')
    parser.add_argument('ext',help='extension of output files')
    parser.add_argument('header_pattern',help='pattern to determine if row is a header')
    #parser.add_argument('numcols',help='number of columns to split as separate file, can be repeated')
    args=parser.parse_args()
    print(f'files {args.outfile}_COL.{args.ext}')
    #print(f'splitting {args.numcols} columns')
    
    # read headers
    headers=[]
    reader=csv.reader(sys.stdin)
    for row in reader:
        headers.append(row)
        print(row)
        if len(row) > 0:
            if row[0] == 'TIME':
                print(f'found TIME')
                break
            #print(f'row[0] {row[0]}')

    # see how many channels
    numchans=len(row) - 1
    print(f'numchans {numchans}')

    channels=[]
    for channel in row[1:]:	# col 1 to end, not col 0
        print(f'channel {channel}')
        channels.append(channel)
        
    # open all the output files
    filehandles=[]
    for channel in channels:
        filename=f'{args.outfile}_{channel}.{args.ext}'
        print(filename)
        filehandle=open(filename,"w")
        filehandles.append(filehandle)
    # print headers for each file
    for i in range(0,numchans):
        filehandle = filehandles[i]
        for row in headers:
            if len(row) == numchans + 1:
                print(row[0],row[i+1])

if __name__ == "__main__":
    main()
