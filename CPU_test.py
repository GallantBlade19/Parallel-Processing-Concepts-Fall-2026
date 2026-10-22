import os
import pandas as pd
import time as t
import csv

execution_time_start = t.perf_counter_ns()
input_file = 'mimic_style_synthetic_30m.csv'
output_file = 'string_sorted_30m.csv'
sorttimeTakenfile = 'test_float_baseline_cpu_sort_30m.csv'
TotaltimeTakenfile = 'test_float_baseline_cpu__total_30m.csv'

sort_by = 'lab_value'

try:
    print("Starting full in-memory sort (No Chunks)...")
    
    # 1. Load the entire dataset into RAM at once
    df = pd.read_csv(input_file)
    
    start_sort = t.perf_counter_ns()
    
    # 2. Clean null entries and sort entirely in memory
    df[sort_by] = df[sort_by].fillna(-1)
    df_sorted = df.sort_values(by=sort_by, ascending=True)
    
    end_sort = t.perf_counter_ns()
    print("Ending sort\n")
    
    # Calculate pure sorting time
    total_time = (end_sort - start_sort) * 1e-9
    print(f"Sort time taken: {total_time:.8f}")

    df_sorted.to_csv(output_file,index=False,chunksize=100000)
    
    with open(sorttimeTakenfile, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([total_time])
        
except MemoryError:
    print("\n❌ CRITICAL: Your computer ran out of RAM (MemoryError) trying to load this dataset!")
except Exception as e:
    print(f"\n❌ An error occurred: {e}")

execution_time_end = t.perf_counter_ns()
total_execution = (execution_time_end - execution_time_start) * 1e-9
print(f"Total time taken: {total_execution:.8f}")

with open(TotaltimeTakenfile, 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([total_execution])
