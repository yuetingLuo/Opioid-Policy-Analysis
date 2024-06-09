import pandas as pd
import dask.dataframe as dd

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
 'DOSAGE_UNIT',
] 

ddf = dd.read_csv('zip://arcos_all_washpost.zip', compression='zip', sep='\t', blocksize=None, assume_missing=True)



ddf = ddf.drop(columns=columns_to_drop)

def add_date_columns(df):
    df['YEAR'] = pd.to_datetime(df['TRANSACTION_DATE']).dt.year
    df['MONTH'] = pd.to_datetime(df['TRANSACTION_DATE']).dt.month
    return df

ddf = ddf.map_partitions(add_date_columns)

ddf.to_parquet('output_directory/', write_index=False)