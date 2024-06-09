import pandas as pd

pd.set_option("mode.copy_on_write", True)

file_paths = [
    'CLEAN_arcos-ca-statewide-itemized.csv.gz',
    'CLEAN_arcos-fl-statewide-itemized.csv.gz',
    'CLEAN_arcos-nc-statewide-itemized.csv.gz',
    'CLEAN_arcos-ny-statewide-itemized.csv.gz',
    'CLEAN_arcos-tx-statewide-itemized.csv.gz',
    'CLEAN_arcos-wa-statewide-itemized.csv.gz']

pop_file_path = 'population_00-19.csv'

cmbined_save_path = 'combined_opioid.csv'

policy_merged_save_path = 'Merged_data_with_policy_info.csv'

dataframes = []

for file in file_paths:
    df = pd.read_csv(file)
    dataframes.append(df)

combined_df = pd.concat(dataframes, axis=0)

# Reset the index
combined_df = combined_df.reset_index(drop=True)

combined_df["New_County"] = combined_df["BUYER_COUNTY"].apply(
    lambda x: (x + " County").title()
)

state_mapping = {
    'CA': 'California',
    'FL': 'Florida',
    'NC': 'North Carolina',
    'NY': 'New York',
    'TX': 'Texas',
    'WA': 'Washington'
}

combined_df['BUYER_STATE_FULL'] = combined_df['BUYER_STATE'].map(state_mapping)

combined_df.to_csv(cmbined_save_path, index=False)

try:
    # Try reading with utf-8 encoding
    df = pd.read_csv(pop_file_path, encoding='utf-8')
except UnicodeDecodeError:
    # If utf-8 encoding fails, try with ISO-8859-1
    df = pd.read_csv(pop_file_path, encoding='ISO-8859-1')

STATE_list = ['California','Florida','North Carolina','New York','Texas','Washington']
df = df[df['STNAME'].isin(STATE_list)]

county_names = combined_df['New_County'].unique()
population_data_filtered = df[df['CTYNAME'].isin(county_names)]


combined_data = combined_df.merge(population_data_filtered, 
                                          left_on=['New_County', 'YEAR','BUYER_STATE_FULL'], 
                                          right_on=['CTYNAME', 'Year','STNAME'], 
                                          how='inner')


combined_data.drop(columns=['CTYNAME', 'YEAR','STNAME','BUYER_STATE_FULL','FIPS','New_County'], inplace=True)


combined_data.rename(columns={'Population': 'population','Year':'YEAR'}, inplace=True)

combined_data.to_csv(policy_merged_save_path, index=False)