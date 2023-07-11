#!/usr/bin/python3
# process.py outfile ext header-pattern [-p method -n number]

import csv
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='split to separate files baseNNN.ext')
    parser.add_argument('outfile',help='base name of output files')
    parser.add_argument('ext',help='extension of output files')
    parser.add_argument('--process','-p',default='',help='processing type - avg, sample, smooth\n'
                        + 'avg = average every N readings\n'
                        + 'sample = only use every Nth reading\n'
                        + 'smooth = adjust ongoing average by reading/N')
    parser.add_argument('--number','-n',help='number argument for process type', default=0)
    args=parser.parse_args()
    process=args.process
    n=int(args.number)
    if process != '' and n == 0:
        print(f'process requires a number')
        sys.exit(1)
    #print(f'files {args.outfile}_COL.{args.ext}')
    
    # read headers
    headers=[]
    reader=csv.reader(sys.stdin)
    for row in reader:
        # remove any blank entries at end of row?
        while len(row) and row[-1] == '':
            row.pop(-1)
        headers.append(row)
        #print(row)
        if len(row) > 0:
            if row[0] == 'TIME':
                #print(f'found TIME')
                break

    # see how many signals
    numchans=len(row) - 1
    #print(f'numchans {numchans}')

    # use list of dictionaries for the rest of the info on each signal, ordered by column number
    # signals = [
    #          { 'column': 1, 'signalname': 'CH1', 'filename': 'outfile_CH1.csv", 'filehandle': <object>, 'writer': <object> },
    #          { 'column': 2, 'signalname': 'CH2', ... }
    #        ]
    signals=[]
    for column in range(1,numchans + 1):    # columns 1 to end, not column 0
        signalname=row[column]
        #print(f'signalname {signalname}')
        
        # open the output files
        filename=f'{args.outfile}_{signalname}.{args.ext}'
        print(filename)
        filehandle = open(filename,"w",newline='')
        writer=csv.writer(filehandle)
        signals.append({ 'column': column, 'signalname': signalname, 'filename': filename, 
                            'filehandle': filehandle, 'writer': writer })

    # write header lines to files
    for row in headers:
        #print(f'row is {row}')
        if len(row) == numchans + 1:
            for signal in signals:
                column=signal['column']
                signal['writer'].writerow([row[0],row[column]])
                #print(signal['filename'],row[0],row[column])
        else:
            for signal in signals:
                #print(f'signal {signal}')
                writer=signal['writer']
                #print(f'row is {row}')
                writer.writerow(row)
                #print(signal['filename'],row)

    # read and write data lines
    cnt=0
    avg=[0]
    for signal in signals:
        avg.append(0)
    for row in reader:
        # remove any blank entries at end of row?
        while len(row) and row[-1] == '':
            row.pop(-1)
        cnt += 1
        for signal in signals:
            column=signal['column']
            value=float(row[column])
            #print(f'value {value}, cnt {cnt}, n {n}')
            if process =='':
                signal['writer'].writerow([row[0],value])
            elif process == 'avg':
                avg[column]+=value
                if cnt == n:
                    signal['writer'].writerow([row[0],avg[column]/n])
                    avg[column]=0
            elif process == 'sample':
                if cnt==1:
                    signal['writer'].writerow([row[0],value])
            elif process == 'smooth':
                value= ((n-1)*avg[column] + value) / n
                avg[column]=value
                signal['writer'].writerow([row[0],value])
            else:
                print(f'error - process type {process} not recognized')
                sys.exit(2)
        if cnt == n:
            cnt=0

if __name__ == "__main__":
    main()
