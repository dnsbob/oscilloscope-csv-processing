#!/usr/bin/python3
# splitcol.py outfile ext header-pattern

import csv
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='split to separate files baseNNN.ext')
    parser.add_argument('outfile',help='base name of output files')
    parser.add_argument('ext',help='extension of output files')
    args=parser.parse_args()
    print(f'files {args.outfile}_COL.{args.ext}')
    
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

    # see how many signals
    numchans=len(row) - 1
    print(f'numchans {numchans}')

    # use list of dictionaries for the rest of the info on each signal, ordered by column number
    # signals = [
    #          { 'column': 1, 'signalname': 'CH1', 'filename': 'outfile_CH1.csv", 'filehandle': <object>, 'writer': <object> },
    #          { 'column': 2, 'signalname': 'CH2', ... }
    #        ]
    signals=[]
    for column in range(1,numchans + 1):    # columns 1 to end, not column 0
        signalname=row[column]
        print(f'signalname {signalname}')
        
        # open the output files
        filename=f'{args.outfile}_{signalname}.{args.ext}'
        print(filename)
        filehandle = open(filename,"w",newline='')
        writer=csv.writer(filehandle)
        signals.append({ 'column': column, 'signalname': signalname, 'filename': filename, 
                            'filehandle': filehandle, 'writer': writer })

    # write header lines to files
    for row in headers:
        print(f'row is {row}')
        if len(row) == numchans + 1:
            for signal in signals:
                column=signal['column']
                signal['writer'].writerow([row[0],row[column]])
                print(signal['filename'],row[0],row[column])
        else:
            for signal in signals:
                print(f'signal {signal}')
                writer=signal['writer']
                print(f'row is {row}')
                writer.writerow(row)
                print(signal['filename'],row)

if __name__ == "__main__":
    main()
