import os
import heapq
import pandas as pd
import time as t
import csv

execution_time_start = t.perf_counter_ns()
input_file = 'mimic_style_synthetic_30m.csv'
timeTakenfile = 'float_baseline_cpu_sorted_30m.csv'
TotaltimeTakenfile = 'float_baseline_cpu__total_30m.csv'
sort_by = 'lab_value'
SIZE = 10000
temp_files = []
total_chunk_time = 0
merge_total_time = 0

try:
    print("Starting sort\n")
    for i, chunk in enumerate(pd.read_csv(input_file,chunksize=SIZE)):
        chunk_start = t.perf_counter_ns()
        chunk[sort_by] = pd.to_numeric(chunk[sort_by], errors='coerce').fillna(float('inf'))
        sorted_chunk = chunk.sort_values(by=sort_by, ascending=True)
        chunk_end = t.perf_counter_ns()


        total_chunk_time += (chunk_end - chunk_start)

        temp_file_name = f"temp_chunk_file{i}.csv"
        sorted_chunk.to_csv(temp_file_name, index=False)
        temp_files.append(temp_file_name)


    def make_row(file_path):
        with open(file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)

            for row in reader:
                yield row

    rows = [make_row(s) for s in temp_files]

    start_merge = t.perf_counter_ns()

    merged_rows = heapq.merge(
        *rows,
        key=lambda x: float(x[sort_by]) if x[sort_by] else float('inf')
    )

    for row in merged_rows:
        pass

    merge_end = t.perf_counter_ns()
    print("Ending sort\n")
    merge_total_time = merge_end - start_merge
    total_time = (total_chunk_time + merge_total_time) *1e-9 
    print(f"Total time taken: {total_time:.4f}")
    with open(timeTakenfile, 'a', newline='') as file: 
        writer = csv.writer(file) 
        writer.writerow([total_time])
    

finally:
    for f in temp_files:
        if os.path.exists(f):
            os.remove(f)

execution_time_end = t.perf_counter_ns()
total_execution = (execution_time_end- execution_time_start)*1e-9
print(f"Total time taken: {total_execution:.8f}")
with open(TotaltimeTakenfile, 'a', newline='') as file: 
    writer = csv.writer(file) 
    writer.writerow([total_execution])