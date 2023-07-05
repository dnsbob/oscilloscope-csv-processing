/# oscilloscope-csv-processing

Input: A CSV file of data from an oscilloscope, possibly millions of lines long.

Actions:
- Split into separate files for each signal (channel)
- Summarize data into less samples

Status: Just started, not working yet.    
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

Future:    
A data line that does not contain a valid "TIME" value is considered the start of a new set of header lines, and treated as if it were a new file.  Some new designator (a,b,c?) is added to the file name.    
