import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import os

dir = 'C:/Users/lyt13/Documents/GitHub/opioid-2023-ecs_hll/'  
os.chdir(dir)

#load three parts of parquet file
all_data = pd.read_csv("00_source_data/opioid_data/results.csv")
all_data = all_data.drop(columns = ["Unnamed: 0", "FIPS","MME","Population"])

WA_df = all_data[all_data["STNAME"] == 'WA']
# spilt data into two groups
before_2012 = WA_df[(WA_df['YEAR'] < 2012) & (WA_df['YEAR'] > 2007)]
after_2012 = WA_df[(WA_df['YEAR'] >= 2012) & (WA_df['YEAR'] < 2017)]

# Group data by state and year, calculating the mean of 'mme_per_cap'
state_level = all_data.groupby(["STNAME", "YEAR"])["mme_per_cap"].mean().reset_index()
state_level_before_2012 = state_level[(state_level["YEAR"] < 2012) & (state_level["YEAR"] > 2007)]
state_level_after_2012 = state_level[(state_level["YEAR"] >= 2012) & (state_level["YEAR"] < 2017)] 
all_states = state_level["STNAME"].unique() 

#Choose control states for WA state
all_slope_before_2012 = {}

# Calculate the slope of 'mme_per_cap' over years for each state
for s in all_states:
    tmp_data = state_level_before_2012[state_level_before_2012["STNAME"]==s]
    X = sm.add_constant(tmp_data['YEAR'])
    model = sm.OLS(tmp_data['mme_per_cap'], X).fit()
    all_slope_before_2012[s] = model.params["YEAR"]

#subtract WA slope and sort
wa_slope = all_slope_before_2012["WA"]
for i in all_slope_before_2012:
    all_slope_before_2012[i] = abs(all_slope_before_2012[i] - wa_slope)

all_slope_before_2012 = sorted(all_slope_before_2012.items(),key=lambda x : x[1])

# Extract slopes for Washington (WA) for comparison
control_states_before_2012 = state_level_before_2012[(state_level_before_2012["STNAME"] == all_slope_before_2012[1][0]) | 
(state_level_before_2012["STNAME"] == all_slope_before_2012[2][0]) | (state_level_before_2012["STNAME"] == all_slope_before_2012[3][0])]

control_states_after_2012 = state_level_after_2012[(state_level_after_2012["STNAME"] == all_slope_before_2012[1][0]) | 
(state_level_after_2012["STNAME"] == all_slope_before_2012[2][0]) | (state_level_after_2012["STNAME"] == all_slope_before_2012[3][0])]

# plot data before 2012 in WA state
sns.regplot(x='YEAR', y='mme_per_cap', data=before_2012, scatter=False, ci=95, color='green', label='Washington')
# plot data after 2012 in WA state
sns.regplot(x='YEAR', y='mme_per_cap', data=after_2012, scatter=False, ci=95, color='green')
plt.axvline(x=2012, color='green', linestyle='--', label='Policy Change')

# plot data before 2012 in compared state
sns.regplot(x='YEAR', y='mme_per_cap', data=control_states_before_2012, scatter=False, ci=68, color='red', label='Control states')
# plot data after 2012 in compared state
sns.regplot(x='YEAR', y='mme_per_cap', data=control_states_after_2012, scatter=False, ci=68, color= 'red')

plt.xlabel('YEAR')
plt.ylabel('mme_per_cap')
plt.title("WA and Control States Comparsion before and after 2012")
plt.legend()
plt.tight_layout()
plt.savefig('30_results/opioid/wa_comparsion.png')
plt.show()
