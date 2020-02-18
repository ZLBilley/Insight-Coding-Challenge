#contains all the utility functions used for the border analysis code in analyze_borders.py

#Used for converting the month and year of the date entry to integer representations
def MakeYearDate(x):
    #returns a tuple of (year,date) provided format is exactly "MM/DD/YYYY [...]""
    return (int(x[6:10]),int(x[0:2]))

def ToMonthCount(x):
    #Converts the (year, month) tuple to an absolute month count
    return 12*x[0]+x[1]-1 #The -1 makes it easier to use modulo when converting back

def FromMonthCount(x, StartMonth = 0):
    #converts from a month count back to a (year,month) tuple
    return ((x+StartMonth)//12,(x+StartMonth)%12+1)

def YearToMonthIndex(x, StartMonth = 0):
    #combines above functions
    return ToMonthCount(MakeYearDate(x)) - StartMonth

def YearFromMonthIndex(x,StartMonth = 0):
    #Need to invoke datetime to rewrite month index as a date
    YrMo = FromMonthCount(x,StartMonth = StartMonth)
    return "{1:0>2}/01/{0:0>4} 12:00:00 AM".format(YrMo[0],YrMo[1])


#because python's native round() function doesn't necessarily round 0.5 up
def kludgeround(x):
    #Will probably be weird with -0.5 or large numbers or something
    return int(x+0.5)


#For calculating the Average column
def CumulativeAverage(x):
    """Takes a list of number and returns a new list containing running average of all previous numbers on the list.
    The running average does not include the value at the cell being averaged
    The initial list element that is not None will always be zero as there are no previous numbers to average
    Entries containing None will not be counted for the size of the average and recorded as None in the output list
    """
    running_sum = 0
    running_count = 0
    averages = []
    for i, element in enumerate(x):
        if element == None:
            averages.append(None)
        elif running_count == 0:
            averages.append(0)
            running_sum += element
            running_count += 1
        else:
            averages.append(running_sum/running_count)
            running_sum += element
            running_count += 1            
    return averages

#Run unit tests if calling the module as a script
if __name__ == "__main__":
    print("Running unit tests for ab_utilities.py...")

    #Cumulative average test
    test_input = [0,1,None,2,3]
    expected_output = [0,0,None,0.5,1]
    assert CumulativeAverage(test_input) == expected_output

    #kludgeround testing
    max_exponent = 13
    for i in range(0,max_exponent):
        test_input = 10**i + 0.5
        expected_output = 10**i+1
        errstr = "Rounding failed at {}".format(expected_output)
        assert kludgeround(test_input) == expected_output, errstr
 
    for i in range(0,max_exponent):
        test_input = 10**i + 0.499
        expected_output = 10**i
        errstr = "Rounding failed at {}".format(expected_output)
        assert kludgeround(test_input) == expected_output, errstr

    for i in range(0,max_exponent):
        test_input = 10**i - 0.0001
        expected_output = 10**i
        errstr = "Rounding failed at {}".format(expected_output)
        assert kludgeround(test_input) == expected_output, errstr    
    
    #FromMonthCount testing
    test_input = 24000
    expected_output = (2000,1)
    actual_output = FromMonthCount(test_input) 
    assert actual_output == expected_output,"Got {0}. Expected {1}".format(actual_output, expected_output)

    #YearFromMonthIndex testing
    test_input =  17
    month = 24000 #index starts at 0 = jan 1, "0" AD/1 BC, so 24000 should be jan 1, 2000 AD
    #(pretending calender changes never existed)
    expected_output = "06/01/2001 12:00:00 AM"
    actual_output = YearFromMonthIndex(test_input, StartMonth=month)
    assert actual_output == expected_output, "Chose {0} date. Expected {1}".format(actual_output, expected_output)

    #month index chain testing
    test_input = "06/01/2000 12:00:00 AM"
    start_input = "01/01/2000 12:00:00 AM"
    test_date = ToMonthCount(MakeYearDate(test_input))
    start_date = ToMonthCount(MakeYearDate(start_input))
    test_index = test_date - start_date
    assert YearFromMonthIndex(test_index, StartMonth = start_date) == test_input

    print("Passed!")