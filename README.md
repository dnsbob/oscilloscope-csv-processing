/# oscilloscope-csv-processing

Input: A CSV file of data from an oscilloscope, possibly millions of lines long.

Actions:
- Split into separate files for each signal (channel)
- Summarize data into less samples

Status:    split columns 2 to N to separate files works
See sample data.csv file in samplefiles    

Sample command line usage:    
./splitcol.py samplefiles/outfile csv header < samplefiles/data.csv    

Creates output files:    
outfile_CH1.csv    
outfile_CH2.csv    

Format of data file:    
Header lines of one or two columns are copied directly to each output file.    
Header lines with three or more columns are assumed to be a label in the first column and values for each signal in the remaining columns.  The first column and the respective signal column are copied to the output files.    
The line with the first column containing "TIME" is the last header line.  The remaining fields in that line name the various signals.  Each signal is written to a separate file with the basename, an underscore, the signal name, a dot, and the extension, like "outfile_CH1.csv".
The lines after the header lines are data.  The first column (TIME) and the respective signal column are written to the output files.    

'processcsv.py' will split columns (if more than one) and do some processing on the file
avg - take average of every N readings, effectively a wider sample time, causing some smoothing, redices number of readings by factor of N
sample - take first of every N readings, which retains the high frequency noise, redices number of readings by factor of N
smooth - add 'reading'/N to 'running average'/(N+1), effectively a low-pass filter, does not change the number of readings

If you have oversampled, use "avg" first to reduce the number of readings, then "smooth" on the output file for a low-pass filter if needed.

sample commands:
./splitcol.py samplefiles/out csv < samplefiles/tek0028short.csv
./processcsv.py samplefiles/out2 csv < samplefiles/tek0028short.csv
./processcsv.py samplefiles/avg2 csv -p avg -n 2 < samplefiles/tek0028short.csv
./processcsv.py samplefiles/sample2 csv -p sample -n 2 < samplefiles/tek0028short.csv
./processcsv.py samplefiles/smooth2 csv -p smooth -n 2 < samplefiles/tek0028short.csv

Apparently the Python 'csv' module defaults to outputing <cr><lf> even on Linux.

Future:    
A data line that does not contain a valid "TIME" value is considered the start of a new set of header lines, and treated as if it were a new file.  Some new designator (a,b,c?) is added to the file name.  
