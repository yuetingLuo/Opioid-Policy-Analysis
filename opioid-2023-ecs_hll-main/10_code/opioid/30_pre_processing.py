import pandas as pd

#load three parts of parquet file
opioid1 = pd.read_parquet("D:/arcos_all_washpost/combined_999.parquet")
opioid1.drop(columns=["CALC_BASE_WT_IN_GM", "TRANSACTION_DATE"])
opioid1 = opioid1[opioid1["BUYER_STATE"] != "AK"]
opioid1 = opioid1.groupby(["BUYER_STATE", "BUYER_COUNTY","YEAR"])["MME"].sum().reset_index()

opioid2 = pd.read_parquet("D:/arcos_all_washpost/combined_1000_1999.parquet")
opioid2.drop(columns=["CALC_BASE_WT_IN_GM", "TRANSACTION_DATE"])
opioid2 = opioid2[opioid2["BUYER_STATE"] != "AK"]
opioid2 = opioid2.groupby(["BUYER_STATE", "BUYER_COUNTY","YEAR"])["MME"].sum().reset_index()

opioid3 = pd.read_parquet("D:/arcos_all_washpost/combined_2000_3298.parquet")
opioid3.drop(columns=["CALC_BASE_WT_IN_GM", "TRANSACTION_DATE"])
opioid3 = opioid3[opioid3["BUYER_STATE"] != "AK"]
opioid3 = opioid3.groupby(["BUYER_STATE", "BUYER_COUNTY","YEAR"])["MME"].sum().reset_index()

#Combine and group by state-county-year
combine_all = pd.concat([opioid1, opioid2, opioid3], axis=0)
combine_all = combine_all.groupby(["BUYER_STATE", "BUYER_COUNTY","YEAR"])["MME"].sum().reset_index()

combine_all.to_parquet("opioid_cleaned_data.parquet")
