import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

dir = 'C:/Users/lyt13/Documents/GitHub/opioid-2023-ecs_hll/'  
os.chdir(dir)

# Load data from a CSV file and drop columns that are not needed
all_data = pd.read_csv("00_source_data/opioid_data/results.csv")
all_data = all_data.drop(columns = ["Unnamed: 0", "FIPS","MME","Population"])

FL_df = all_data[all_data["STNAME"] == 'FL']

# spilt data into two groups
before_2010 = FL_df[FL_df['YEAR'] < 2010]
after_2010 = FL_df[(FL_df['YEAR'] >= 2010) & (FL_df['YEAR'] < 2015)]

plt.figure(figsize=(10, 6))

# plot data before 2010 in FL state
sns.regplot(x='YEAR', y='mme_per_cap', data=before_2010, scatter=False, ci=68, scatter_kws={'facecolor': 'none', 'edgecolor': 'green'}, label='Before 2010')

# plot data after 2010 in FL state
sns.regplot(x='YEAR', y='mme_per_cap', data=after_2010, scatter=False, ci=68, scatter_kws={'facecolor': 'none', 'edgecolor': 'red'}, label='After 2010')
plt.axvline(x=2010, color='green', linestyle='--', label='Policy Change')

plt.xlabel('YEAR')
plt.ylabel('mme_per_cap')
plt.title('mme_per_cap Trend in Florida Counties before/after 2010')
plt.legend()
plt.tight_layout()
plt.savefig('30_results/opioid/fl_prepost.png')
plt.show()
