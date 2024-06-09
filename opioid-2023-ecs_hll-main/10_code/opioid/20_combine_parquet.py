import pandas as pd
import numpy as np
import os
import pyarrow as pa
import pyarrow.parquet as pq

dir = 'D:/Workbench/ids720/batch/'
output_file = 'D:/Workbench/ids720/combined_1000_2000.parquet'
combined_table = None

# 3298 parquet files in totle
# oObtain the merged parquet file through three times to avoid memory overflow
parquet_files = [os.path.join(dir, f'batch_{i}.parquet') for i in range(1000,2000,1)] #

for file_path in parquet_files:

    print(file_path)
    table = pq.read_table(file_path)

    if combined_table is None:
        combined_table = table
    else:
        combined_table = pa.concat_tables([combined_table, table])


pq.write_table(combined_table, output_file)