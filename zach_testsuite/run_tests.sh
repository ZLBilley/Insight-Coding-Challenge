#!/bin/bash
#
# Runs the coding challenge code
python3.7 ../src/ab_utilities.py
python3.7 ../src/analyze_borders.py Border_Crossing_Entry_Data.csv report.csv
python3.7 ../src/analyze_borders.py testdata.csv test_report.csv
python3.7 plausibility_check.py Border_Crossing_Entry_Data.csv report.csv
python3.7 output_is_same.py