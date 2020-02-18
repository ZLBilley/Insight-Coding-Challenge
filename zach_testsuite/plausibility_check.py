#Loads input and output data and checks the plausibility of results

import sys, os

#get parameters
try:
	input_file = sys.argv[1]
	output_file = sys.argv[2]
except IndexError:
	print("This script needs two arguments to run: input filename and output filename")

input_path = os.path.join('input',input_file)
output_path = os.path.join('output',output_file)


def GetColumnVals(target_file, column = "Value",val_type = int):
    """Loads the target column from a .csv file with the first row being column labels
    Defaults to 'Value' column
    Defaults to in, set val_type to a function that converts from str to appropriate type
    """
    with open(target_file, 'r') as f:
        #Read in labels
        line_in = f.readline()
        labels = line_in.strip().split(",")

        assert column in labels, "Error: No {} label found in output".format(column)
        i = labels.index(column)

        output_values = []


        while True:
            line_in = f.readline()
            #break at EOF
            if line_in == "":
                break

            vals =  line_in.strip().split(",")
            output_values.append(val_type(vals[i]))
    return output_values

input_folder = "input/"
output_folder = "output/"

in_vals = GetColumnVals(input_path)
out_vals = GetColumnVals(output_path)
out_avgs = GetColumnVals(output_path, column = "Average", val_type = float)

expected_output = sum(in_vals)
actual_output = sum(out_vals)

max_val = max(out_vals)
#min_val = min(out_vals)
max_avg = max(out_avgs)

#make sure no counts were missed!
#Binning and summing values should not affect the total
assert actual_output == expected_output, "Value counts were missed"

#make sure we didn't just copy the values for our running totals
assert not out_vals == out_avgs, "Average and Value columns are duplicates of each other" 

#Make sure averages are plausible
assert max_avg <= max_val, "Produced impossibly high averager"

print("Passed plausibility checks")
