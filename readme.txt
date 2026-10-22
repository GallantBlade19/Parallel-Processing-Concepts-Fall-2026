# MIMIC-IV-Style Data Sorting Benchmarks
## CPU Baseline and GPU Implementations

### 1. Project Overview

This project contains Python programs designed to benchmark sorting performance on synthetic, MIMIC-IV-style clinical datasets. The programs compare a serial CPU implementation using pandas with a GPU implementation using NVIDIA RAPIDS cuDF.

The purpose of these benchmarks is to measure the time required to sort datasets of different sizes by selected columns and to examine the performance differences between CPU-based and GPU-based sorting.

The project contains seven sorting programs. Each program follows the same general structure, but the programs may sort by different columns, use different data types, or process different dataset sizes.

### 2. Included Files

The ZIP archive should contain this README, all seven Python sorting programs, and all CSV datasets required by those programs.

The files fall into three categories:

- **CPU sorting programs:** Use pandas to sort data on the CPU in chunks, write intermediate sorted chunks to temporary CSV files, and merge the chunks using Python's `heapq.merge`.
- **GPU sorting programs:** Use NVIDIA RAPIDS cuDF to sort data on the GPU.
- **Input datasets:** Synthetic CSV files containing MIMIC-IV-style clinical data used for benchmarking.

The programs may also generate timing CSV files, sorted output files, and temporary chunk files during execution.

Before running a program, check its input filename and sorting column to ensure that they match the intended dataset and benchmark.

### 3. System Requirements

#### CPU implementations

The CPU programs require:

- Python 3
- pandas
- A compatible operating system
- Sufficient disk space for the input dataset and temporary files

The CPU programs use standard Python libraries, including `os`, `heapq`, `time`, and `csv`, in addition to pandas.

Install pandas if it is not already available:

```bash
python -m pip install pandas
```

#### GPU implementations

The GPU programs require:

- An NVIDIA GPU supported by the installed RAPIDS release
- Compatible NVIDIA drivers and CUDA support
- Python 3
- NVIDIA RAPIDS cuDF
- CuPy
- Sufficient GPU memory for the dataset being processed

The GPU programs use cuDF for GPU-based data processing and CuPy to synchronize GPU operations when measuring execution time.

**Windows users must run the GPU programs through WSL (Windows Subsystem for Linux), preferably using Visual Studio Code with its WSL extension.** Running the scripts directly in a standard Windows Python environment is not the intended configuration.

GPU software versions must be compatible with one another and with the installed NVIDIA drivers. Follow the official RAPIDS installation instructions to select a supported environment:

https://docs.rapids.ai/install/

### 4. Setting Up the Environment

#### A. Windows users: CPU benchmarks

CPU benchmarks can be run from Windows using a compatible Python installation and terminal, including the VS Code terminal.

1. Extract the ZIP archive into a folder.
2. Open that folder in Visual Studio Code.
3. Install Python if necessary and ensure that the Python extension is available.
4. Open a terminal in the project folder.
5. Install pandas if necessary.
6. Run the desired CPU program.

#### B. Windows users: GPU benchmarks through WSL

GPU benchmarks must be run inside a Linux environment using WSL.

1. Install and configure WSL with a supported Linux distribution, such as Ubuntu.
2. Install the appropriate NVIDIA Windows driver with WSL GPU support. Follow NVIDIA's official instructions: https://docs.nvidia.com/cuda/wsl-user-guide/
3. Install Visual Studio Code and its **WSL extension**.
4. Open the project folder from the WSL environment. The extracted files must be accessible from Linux.
5. Set up a compatible Python environment with RAPIDS cuDF and CuPy.
6. Open a VS Code terminal connected to WSL.
7. Verify that the environment can import `cudf` and `cupy` and that GPU access is working.
8. Run the desired GPU program from the WSL terminal.

Do not assume that packages installed in Windows Python are automatically available in WSL. The Linux environment needs its own compatible packages.

#### C. Linux users

Linux users can run the CPU programs using Python and pandas. GPU programs additionally require a supported NVIDIA GPU, compatible drivers, and a correctly configured RAPIDS/CuPy environment.

### 5. Preparing the Programs

Before executing a program, inspect the configuration variables near the beginning of the script.

| Variable | Purpose |
|---|---|
| `input_file` | Name or path of the input CSV dataset |
| `output_file` | Output filename for the GPU-sorted dataset |
| `sort_by` | Column used as the sorting key |
| `SIZE` | Number of rows read per chunk in the CPU implementation |
| `timeTakenfile` | CPU timing output file for the measured sorting operation |
| `TotaltimeTakenfile` | CPU timing output file for the complete program execution |

Not every variable appears in every program. GPU programs and CPU programs have different output and timing configurations.

#### Input file paths

The CPU example uses a relative path:

```python
input_file = 'mimic_style_synthetic_30m.csv'
```

This means Python looks for the CSV in the current working directory.

The GPU example uses an absolute Linux path:

```python
input_file = "/home/daigl/MIMIC-IV GPU Research/mimic_style_synthetic_500k.csv"
```

This path is specific to the original development environment. **It must be changed to the actual location of the dataset in the reader's WSL environment.**

For example, if the dataset is in the same directory from which the program is run, the path can be changed to:

```python
input_file = "mimic_style_synthetic_500k.csv"
```

The program must be run from the directory containing the dataset for this relative path to work.

#### Sorting column

The `sort_by` variable specifies which column will be sorted. For example:

```python
sort_by = 'lab_value'
```

Other programs may use different columns, such as `anchor_age` or `medication`.

The selected column must exist in the input CSV. When changing the dataset or sorting column, ensure that the program's missing-value handling is appropriate for that column's data type.

### 6. Running the CPU Benchmarks

The CPU implementation uses pandas to read a large CSV dataset in chunks rather than loading the entire dataset into memory at once.

For each chunk, the program:

1. Reads a portion of the input CSV.
2. Converts the selected sorting column to numeric values when configured to do so.
3. Handles missing values according to the program's configuration.
4. Sorts the chunk in ascending order.
5. Writes the sorted chunk to a temporary CSV file.
6. Records the time spent processing and sorting the chunk.

After all chunks have been processed, the program uses `heapq.merge` to merge the individually sorted chunks in ascending order.

In the supplied CPU implementation, the merged rows are iterated over but are **not written to a final sorted CSV file**. This is intentional in the current implementation because the benchmark is focused on timing the sorting and merge operations rather than producing a final output dataset.

To run a CPU benchmark, open a terminal in the project directory and execute the relevant script:

```bash
python float_baseline_cpu_sort.py
```

Replace `float_baseline_cpu_sort.py` with the actual filename of the desired program.

The CPU program reports timing information in the terminal and appends timing results to its configured CSV files.

#### CPU chunk size

The variable `SIZE` determines the number of rows read per chunk:

```python
SIZE = 10000
```

A smaller chunk size reduces the number of rows processed at once but creates more temporary files and increases merge overhead. A larger chunk size reduces the number of chunks but increases the memory required to process each chunk.

For consistent benchmarks, use the intended chunk size for each experiment and document any changes.

#### CPU temporary files

During execution, the CPU program creates temporary files named similarly to:

```text
temp_chunk_file0.csv
temp_chunk_file1.csv
temp_chunk_file2.csv
```

The program attempts to remove these temporary files in its cleanup section after processing finishes. If execution is interrupted, temporary files may remain and can be removed manually after confirming that they are no longer needed.

### 7. Running the GPU Benchmarks

The GPU implementation uses cuDF to load the CSV into a GPU-compatible DataFrame and sort it by the selected column.

To run a GPU benchmark from the WSL terminal in VS Code:

```bash
python float_gpu_sort.py
```

Replace the example filename with the actual name of the GPU program.

The GPU program performs the following operations:

1. Reads the input CSV using cuDF.
2. Handles missing values in the selected sorting column.
3. Synchronizes GPU operations before starting the sort timer.
4. Sorts the DataFrame in ascending order using `sort_values`.
5. Synchronizes GPU operations again to ensure the sorting work has completed before stopping the timer.
6. Writes the sorted DataFrame to an output CSV.
7. Reports the sort time and total measured execution time in the terminal.

#### GPU output

The GPU program writes the sorted dataset to the filename configured in `output_file`, for example:

```python
output_file = "float_gpu_sorted_500k.csv"
```

The output is written with `index=False`, so the pandas-style DataFrame index is not added as an extra column. The supplied code requests a CSV write chunk size of 100,000 rows.

The GPU timing results are printed in the terminal. In the supplied implementation, they are not automatically appended to a timing CSV file.

#### GPU memory requirements

The current GPU implementation reads the complete CSV into a cuDF DataFrame before sorting it. Writing the sorted output in chunks does not make the initial input loading or sorting operation out-of-core.

Consequently, the input data, intermediate sorting allocations, and other GPU operations must fit within the available GPU memory. A dataset that works with the CPU implementation may exceed GPU memory limits.

If a dataset fails because of insufficient GPU memory, use a smaller dataset or develop a separate out-of-core GPU implementation. The current GPU program should not be assumed to support datasets larger than GPU memory simply because it writes the output in chunks.

### 8. Understanding the Timing Results

The CPU and GPU programs measure different parts of their execution, so it is important to distinguish the reported timing values.

#### CPU timing values

The CPU implementation records two timing measurements.

- **Sorting and merge time:** The sum of the time spent processing and sorting individual chunks, plus the time spent merging the sorted chunks. The supplied program records this in `timeTakenfile`.
- **Total execution time:** The elapsed time for the overall script, including work outside the primary sorting and merge measurements. The supplied program records this in `TotaltimeTakenfile`.

The primary CPU timing is calculated as:

`(total_chunk_time + merge_total_time) * 1e-9`

The conversion from nanoseconds to seconds is necessary because the CPU implementation uses `time.perf_counter_ns()`.

Note that the CPU timing excludes the time spent writing each sorted chunk to its temporary file, but the total execution time includes that work.

#### GPU timing values

The GPU implementation reports:

- **GPU sort time:** The measured interval surrounding the cuDF sorting operation, with GPU synchronization before and after the operation.
- **GPU total time:** The measured elapsed time from the beginning of the program's timed workflow through the output-writing stage and final synchronization.

Both values are reported in seconds. The total time includes loading and preparing the dataset, sorting, and writing the output, along with other operations inside the timed interval.

The total time is not simply the sort time because it includes additional work.

#### Important comparison limitation

The CPU and GPU timing measurements are not perfectly equivalent in their current form. The CPU's primary sorting measurement includes chunk sorting and merging, whereas the GPU's sort measurement covers one in-memory cuDF sort. The total execution measurements also reflect different workflows.

For a rigorous comparison, report both sorting time and total elapsed time, clearly define the operations included in each measurement, and avoid presenting unlike timing measurements as if they measure exactly the same work.

### 9. Missing Values and Data Types

The supplied programs handle missing values differently.

The example CPU program converts the sorting column to numeric values and replaces missing or invalid values with positive infinity:

```python
chunk[sort_by] = pd.to_numeric(
    chunk[sort_by], errors='coerce'
).fillna(float('inf'))
```

The example GPU program replaces missing values in its selected column with `-1.0`:

```python
df[sort_by] = df[sort_by].fillna(-1.0)
```

For ascending numeric sorting, these choices place missing values in different positions: positive infinity sorts after ordinary finite values, while `-1.0` sorts before values greater than `-1.0`.

This difference may affect the sorted output and can influence the interpretation of a benchmark comparison. To make a direct CPU-versus-GPU comparison fair, use equivalent missing-value handling in both implementations, taking care that the chosen replacement does not conflict with legitimate data values.

Different data types may also affect sorting performance. Sorting numeric values, strings, and integers can produce different results in terms of execution time and memory usage. Ensure that the corresponding CPU and GPU tests use equivalent datasets, sorting columns, and data-cleaning rules.

### 10. Benchmarking Recommendations

For reliable benchmark results:

1. Use the same input dataset for the CPU and GPU tests being compared.
2. Use the same sorting column and ascending/descending order.
3. Apply equivalent missing-value handling and data-type conversion.
4. Keep the dataset size consistent between the two implementations.
5. Run multiple trials and record each result.
6. Compare both sorting time and total elapsed time.
7. Document the CPU, GPU, memory capacity, software versions, and relevant configuration settings.
8. Avoid running other resource-intensive tasks during measurements.
9. Confirm that the GPU is performing the work and that GPU synchronization is included where necessary.
10. Keep the benchmark configuration consistent across repeated trials.

The current CPU example uses a 30-million-row input, while the GPU example uses a 500,000-row input. These are configuration examples, not directly comparable benchmark runs. Change the input paths and settings so that both implementations process the same dataset before comparing their performance.

### 11. Troubleshooting

| Problem | Possible solution |
|---|---|
| `FileNotFoundError` | Check the input filename, current working directory, and file path. |
| `ModuleNotFoundError: No module named 'pandas'` | Install pandas in the Python environment being used. |
| `ModuleNotFoundError: No module named 'cudf'` | Configure a supported RAPIDS environment in WSL or Linux. |
| `ModuleNotFoundError: No module named 'cupy'` | Install a compatible CuPy version in the GPU environment. |
| GPU not detected | Check NVIDIA driver compatibility, WSL GPU support, and the RAPIDS environment. |
| GPU out-of-memory error | Try a smaller dataset or implement a separate out-of-core GPU workflow. |
| Sorting-column error | Verify that the selected column exists in the input CSV and that the missing-value operation supports its data type. |
| Unexpected timing differences | Check the dataset size, data type, chunk size, missing-value handling, and measured code sections. |
| Temporary CPU files remain | Remove leftover temporary chunk files after confirming that no benchmark is still using them. |

### 12. Summary

These programs provide a foundation for evaluating CPU and GPU sorting performance on synthetic clinical-style datasets. The CPU implementation uses chunked pandas processing and a merge operation to handle larger datasets without loading the complete dataset into memory at once. The GPU implementation uses cuDF to perform an in-memory GPU sort.

The seven programs share a common benchmarking structure but may use different sorting columns, data types, and dataset sizes. Before running a test, verify the configuration and ensure that the CPU and GPU versions use comparable inputs and data-cleaning rules.

The results can then be used to investigate how dataset size, data type, and implementation strategy affect sorting performance.
