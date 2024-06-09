import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

csv_file_path = 'arcos_all_washpost.zip'
batch_size = 100000  # row numbers of each batch

#read tsv file and convert to parquet format
csv_reader = pd.read_csv(csv_file_path, compression='zip', sep='\t', chunksize=batch_size)
columns_to_drop = ['REPORTER_DEA_NO',
 'REPORTER_BUS_ACT',
 'REPORTER_NAME',
 'REPORTER_ADDL_CO_INFO',
 'REPORTER_ADDRESS1',
 'REPORTER_ADDRESS2',
 'REPORTER_CITY',
 'REPORTER_STATE',
 'REPORTER_ZIP',
 'REPORTER_COUNTY',
 'BUYER_DEA_NO',
 'BUYER_BUS_ACT',
 'BUYER_NAME',
 'BUYER_ADDL_CO_INFO',
 'BUYER_ADDRESS1',
 'BUYER_ADDRESS2',
 'BUYER_CITY',
 'BUYER_ZIP',
 'TRANSACTION_CODE',
 'DRUG_CODE',
 'NDC_NO',
 'DRUG_NAME',
 'Measure',
 'MME_Conversion_Factor',
 'Dosage_Strength',
 'Combined_Labeler_Name',
 'Reporter_family',
 'DOSAGE_UNIT'] 

for i, chunk in enumerate(csv_reader):

    chunk = chunk.drop(columns=columns_to_drop)

    # generate new columns of year and month
    chunk['YEAR'] = chunk['TRANSACTION_DATE'].apply(lambda x: pd.to_datetime(x).year)
    chunk['MONTH'] = chunk['TRANSACTION_DATE'].apply(lambda x: pd.to_datetime(x).month)
    
    table = pa.Table.from_pandas(chunk)
    
    # create file name of parquet file
    parquet_file_name = f'batch_{i}.parquet'
    
    with pq.ParquetWriter(parquet_file_name, table.schema) as writer:
        writer.write_table(table)
    
    print(f'Batch {i} converted to Parquet: {parquet_file_name}')

