import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

dir = 'C:/Users/lyt13/Documents/GitHub/opioid-2023-ecs_hll/'  
os.chdir(dir)

# Load data and drop unnecessary columns
all_data = pd.read_csv("00_source_data/opioid_data/results.csv")
all_data = all_data.drop(columns = ["Unnamed: 0", "FIPS","MME","Population"])
WA_df = all_data[all_data["STNAME"] == 'WA']
WA_df = WA_df[(WA_df['YEAR'] < 2017) &(WA_df['YEAR'] > 2007)]
WA_county = WA_df["CTYNAME"].unique()

# Find the peak year of 'mme_per_cap' for each county in WA
wa_peak_years = []
for c in WA_county:
    tmp_data = WA_df[WA_df["CTYNAME"]==c]
    wa_peak_years.append(tmp_data[tmp_data["mme_per_cap"] == tmp_data["mme_per_cap"].max()]["YEAR"].iloc[0])

# Determine the year when the slope of 'mme_per_cap' becomes negative (indicating a decrease)
wa_slope_change_years = []
wa_slope_change_years = []
import statsmodels.api as sm
for c in WA_county:
    tmp_data = WA_df[WA_df["CTYNAME"]==c]
    year = tmp_data["YEAR"].unique()
    i = 0
    value = []

    # Calculate the slope for a 3-year moving window
    while i < len(year) and i+3 < len(year):
        tmp2_data = tmp_data[(tmp_data["YEAR"]>=year[i]) & (tmp_data["YEAR"] < year[i+3])]
        X = sm.add_constant(tmp2_data['YEAR'])
        model = sm.OLS(tmp2_data['mme_per_cap'], X).fit()
        value.append(model.params["YEAR"])
        i= i + 1

    # Find the first year where the slope becomes negative
    for i,v in enumerate(value):
        if v<0:
            wa_slope_change_years.append(year[i])
            break
        if i == len(value)-1 and v>=0:
            wa_slope_change_years.append(np.nan)

# Combine the collected data into a DataFrame
WA_info =pd.DataFrame(
    {"County":WA_county,
     "max_Year":wa_peak_years,
     "change_Year":wa_slope_change_years
     }
) 

# Visualizing the data
plt.figure(figsize=(10,7))
plt.scatter(range(len(WA_info)),WA_info["max_Year"],marker="o",color="blue",label = "The year of max mme")
plt.scatter(range(len(WA_info)),WA_info["change_Year"],marker="x",color="red",label = "The year k became decreasing")
plt.legend()
x_ticks = range(0,len(WA_info),2)
county_xticks = []
for i in x_ticks:
    county_xticks.append(WA_county[i])
plt.xticks(x_ticks,county_xticks,rotation = 45, fontsize=6)


plt.title('Maximum year and slope change year observation in Washington')
plt.savefig('30_results/opioid/wa_trend_analysis.png')
plt.show()