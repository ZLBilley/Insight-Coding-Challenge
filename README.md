# Insight data engineering coding challenge submission
## Zach Billey

### Running the analysis script
The analysis script analyze_borders.py and the resource module ab_utilities.py are located in the src/ folder.

The run.sh script is set up so as to take a file named "Border_Crossing_Entry_Data.csv" in the input folder and output to a file named "report.csv" in the output folder.

### Testing
I wanted to do some slgihtly different tests that weren't just matching an input file to expected output. These tests are located in the folder zach_testsuite in the root directory. Running the runtests.sh script does the following:

1. Runs the unit tests in ab_utilities.py
2. Runs the analyze_borders script on the both the smaller sample set (testdata.csv) and the larger data file (Border_Crossing_Entry_Data.csv)
3. Checks to make sure that the output produced from Border_Crossing_Entry_Data.csv is plausible. Basically, it checks that the averages don't somehow produce numbers higher than any of the input values and that the sum of all border crossings remains the same before and after.
4. Checks that the testdata.csv produced the expected output provided in the problem definition. This should do the same thing as test_1 in the insight test suite

### Notes
This code is written assuming a pretty temporally dense set of mostly filled in data. This is with the idea that it might be good to make a table at some point which can show which entries (specified by date/time/border/measure) that there aren't any data for, in case that becomes important.

Because of this it constructs a full set of lists for each combination of border and measure over the full range of times included in the data set, using None as a placeholder for entries where there is no data.

If the data is such that large numbers of these are empty entries, this will result in unnecessarily large data structures and a different approach should be used. For example, using the dates as a dictionary, too, and just not including keys for the missing data would be the most straightforward.

I chose to correspond months to integer indexing because working with datetime objects can be a pain and introduce subtle bugs and eat up unnecessary memory/processing time - especially when the exact day and times in these data sets are just placeholder values.

For a more production level project, it might be a good idea to check for major outlier dates so a single malformed date doesn't cause it to choke.
