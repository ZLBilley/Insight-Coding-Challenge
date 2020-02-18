#A brief test to confirm the output hasn't changed
max_size = 10**8

output_file = 'output/test_report.csv'

with open(output_file,'r') as f:
    new_file_data = f.read(max_size)

with open("prototype_test_report.csv",'r') as f:
    old_file_data = f.read(max_size)

assert new_file_data == old_file_data,"You broke it!"
print("Passed output check: Output matches sample output")
