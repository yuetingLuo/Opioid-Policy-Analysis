import pandas as pd
import dask.dataframe as dd
import os

ddf = dd.read_parquet('output_directory/')

states = ['CA', 'FL', 'NC', 'NY', 'TX', 'WA']

for state in states:
    ddf_state = ddf[ddf['BUYER_STATE'] == state]

    grouped = ddf_state.groupby(['BUYER_COUNTY', 'YEAR'])['MME'].sum()

    df_final = grouped.compute().reset_index()

    df_final['BUYER_STATE'] = state

    STATE_NAME = state.lower()
    file_path = f'arcos-{STATE_NAME}-statewide-itemized.csv.gz'
    clean_file_path = 'CLEAN_' + file_path

    df_final.to_csv(clean_file_path, compression='gzip', index=False)

    print(f'File saved: {clean_file_path}')
    print(df_final.head())

    print('-' * 40)