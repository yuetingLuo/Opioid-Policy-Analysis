# %%
from pathlib import Path
import pandas as pd
import numpy as np
import os

pd.set_option("mode.copy_on_write", True)

repo_root = Path("../..")
# source files
src_folder = repo_root / "00_source_data" / "mortality_data"

# output file
out_file = repo_root / "20_intermediate_file" / "overdose_03-15.tsv"

# %%
df_list = [pd.read_csv(p, sep="\t") for p in src_folder.glob("*")]
df = pd.concat(df_list)

# %%
clean_df = df[df["Notes"].isna()]

clean_df.drop(
    inplace=True, columns=["Notes", "Year Code", "Drug/Alcohol Induced Cause"]
)

overdoses = ["D1", "D2", "D3", "D4"]
clean_df = clean_df[clean_df["Drug/Alcohol Induced Cause Code"].isin(overdoses)]
clean_df["County Code"] = clean_df["County Code"].astype(int)
clean_df["Year"] = clean_df["Year"].astype(int)

clean_df = clean_df[clean_df["Deaths"] != "Missing"]
clean_df["Deaths"] = clean_df["Deaths"].astype(int)
clean_df.drop(inplace=True, columns="Drug/Alcohol Induced Cause Code")

# %%
# Group by county-year and sum all the different overdose categories
clean_df.rename(inplace=True, columns={"County Code": "FIPS"})
# Remove Alaska
clean_df = clean_df[clean_df["FIPS"] // 1000 != 2]
clean_df = clean_df.groupby(["FIPS", "County", "Year"], as_index=False).sum()

# %%
clean_df.to_csv(out_file, index=False, sep="\t")
