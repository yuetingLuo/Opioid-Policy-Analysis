import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

dir = 'C:/Users/lyt13/Documents/GitHub/opioid-2023-ecs_hll/'  
os.chdir(dir)

#Plot all counties in WA state
all_data = pd.read_csv("00_source_data/opioid_data/results.csv")
all_data = all_data.drop(columns = ["Unnamed: 0", "FIPS","MME","Population"])

WA_df = all_data[all_data["STNAME"] == 'WA']

# spilt data into two groups
before_2012 = WA_df[(WA_df['YEAR'] < 2012) & (WA_df['YEAR'] > 2007)]
after_2012 = WA_df[(WA_df['YEAR'] >= 2012) & (WA_df['YEAR'] < 2017)]

plt.figure(figsize=(10, 6))

# plot data before 2010 in FL state
sns.regplot(x='YEAR', y='mme_per_cap', data=before_2012, scatter=False, ci=68, scatter_kws={'facecolor': 'none', 'edgecolor': 'green'}, label='Before 2012')

# plot data after 2010 in FL state
sns.regplot(x='YEAR', y='mme_per_cap', data=after_2012, scatter=False, ci=68, scatter_kws={'facecolor': 'none', 'edgecolor': 'red'}, label='After 2012')
plt.axvline(x=2012, color='green', linestyle='--', label='Policy Change')

plt.xlabel('YEAR')
plt.ylabel('mme_per_cap')
plt.title('mme_per_cap Trend in Washington Counties before/after 2012')
plt.legend()
plt.tight_layout()
plt.savefig('30_results/opioid/wa_prepost.png')
plt.show()


