from ab_utilities import *
import sys, os

#get parameters
try:
	input_file = sys.argv[1]
	output_file = sys.argv[2]
except IndexError:
	print("This script needs two arguments to run: input filename and output filename")

input_path = os.path.join('input',input_file)
output_path = os.path.join('output',output_file)

#open the data
with open(input_path, 'r') as f:
    #Read in labels
    line_in = f.readline()
    labels = line_in.strip().split(",")
    
    #Store the data as lists in a dictionary
    data_dict = {}
    for label in labels:
        data_dict[label] = []
    
    
    #Load in line by line
    #For checking, count number of labels
    label_count = len(data_dict.keys())
    
    while True:
        line_in = f.readline()
        #break at EOF
        if line_in == "":
            break
            
        vals =  line_in.strip().split(",")
        
        #Make sure each line contains the same number of values as labels before adding it
        if len(vals) == label_count:
            for i, label in enumerate(labels):
                data_dict[label].append(vals[i])
        else:
            #put in warning logging here maybe?
            pass

#process the data

#Here the date (year, month) gets converted into a month integer
#The data will structured essentially as a table with each list being a column of the table
#Each row in the table corresponds to an index of the list. This index is the months since
#the earliest entry loaded in the data

YrMo = [MakeYearDate(i) for i in data_dict["Date"]]

MonthList = list(map(ToMonthCount,YrMo))
StartMonth = min(MonthList)
EndMonth = max(MonthList)
MonthCount = EndMonth - StartMonth + 1

#establish borders (probably can or mex)
borders = list(set(data_dict["Border"]))
#For consistent ordering that matches provided sample
borders.sort(reverse=True)

#establish measure (types of transit)
measures = list(set(data_dict["Measure"]))
measures.sort(reverse=True)

#first pass:
#Set up dictionary that represents labels to easily access lists
# Border -> Measure
counts = {}
for border in borders:
    measure_dict = {}
    for measure in measures:
        measure_dict[measure] = [None,]*MonthCount
    counts[border]  = measure_dict

#bin data
#for each YrMo combo
indices = map(lambda l: YearToMonthIndex(l, StartMonth),data_dict["Date"])

for i, month_index in enumerate(indices):
    border = data_dict["Border"][i]
    measure= data_dict["Measure"][i]
    if counts[border][measure][month_index] == None:
        counts[border][measure][month_index] = int(data_dict["Value"][i])
    else:
        counts[border][measure][month_index] += int(data_dict["Value"][i])

#Second pass
#calculated value average, sum of that month and previous months over total number of months for each measure
cum_avg = {}
for border in borders:
    measure_dict = {}
    for measure in measures:
        measure_dict[measure] = CumulativeAverage(counts[border][measure])
    cum_avg[border] =  measure_dict

#Save the data in the appropriate order: most recent first
with open(output_path, 'w') as f:
    f.write(",".join(["Border","Date","Measure","Value","Average"]))
    f.write("\n")
    for i in range(MonthCount - 1, -1, -1):
        for border in borders:
            for measure in measures:
                Value = counts[border][measure][i]
                if not Value == None:
                    Date = YearFromMonthIndex(i,StartMonth=StartMonth)            
                    Average = cum_avg[border][measure][i]
                    f.write(",".join([
                                        border,
                                        Date,
                                        measure,
                                        str(Value),
                                        str(kludgeround(Average))
                                     ])
                           )
                    f.write("\n")
