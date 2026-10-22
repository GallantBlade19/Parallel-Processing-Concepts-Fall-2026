import os
import cudf
import cupy as cp
import time

#set the input and output files
input_file = "/home/daigl/MIMIC-IV GPU Research/mimic_style_synthetic_500k.csv" 
output_file = "float_gpu_sorted_500k.csv"
#set the sort value
sort_by = "lab_value"
#check file size
file_size = os.path.getsize(input_file)
# start total timer
start_total = time.perf_counter()

df = cudf.read_csv(input_file)
df[sort_by] = df[sort_by].fillna(-1.0)

#wait for GPU to start timer for sorting
cp.cuda.runtime.deviceSynchronize()
start_sort = time.perf_counter()

# Sort using cuDF
sorted_df = df.sort_values(
    by=sort_by,
    ascending=True
)

# Wait for GPU work to finish before stopping the timer
cp.cuda.runtime.deviceSynchronize()
end_sort = time.perf_counter()

#print out the total sorting time
print(f"GPU sort time: {end_sort - start_sort:.6f} seconds")

#output the sorted file in chunks of 100,000
sorted_df.to_csv(output_file, index=False, chunksize=100000)

#end the total timer
cp.cuda.runtime.deviceSynchronize()
end_total = time.perf_counter()

#print the total time taken
print(f"GPU total time: {end_total - start_total:.6f} seconds")
