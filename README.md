# oscilloscope-csv-processing

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

