# %%
from pathlib import Path
import pandas as pd

pd.set_option("mode.copy_on_write", True)

repo_root = Path('../..')
# source files
src_folder = repo_root / "00_source_data/population_data"
src09 = src_folder / "co-est00int-tot.csv"
src19 = src_folder / "co-est2020.csv"

# read into pandas dataframe
# 09 and 19 as we only need 00-09 from the first, 10-19 from the second
pop09 = pd.read_csv(src09, encoding="latin-1")
pop19 = pd.read_csv(src19, encoding="latin-1")

# output file
out_file = repo_root / "20_intermediate_file/population_00-19.csv"

# %%
def clean_pop(pop):
    # clean rows: drop state and Alaska rows
    pop = pop[(pop["SUMLEV"] == 50) & (pop["STNAME"] != "Alaska")]
    pop = pop.reset_index(drop=True)

    # create FIPS column (int values)
    pop["FIPS"] = pop["STATE"] * 1000 + pop["COUNTY"]
    return pop

# %%
# clean pop09
pop09 = clean_pop(pop09)

# drop columns no longer needed
pop09.drop(
    inplace=True,
    columns=[
        "SUMLEV",
        "REGION",
        "DIVISION",
        "STATE",
        "COUNTY",
        "ESTIMATESBASE2000",
        "CENSUS2010POP",
        "POPESTIMATE2010",
    ],
)
pop09.rename(inplace=True, columns=lambda c: c[-4:] if "POP" in c else c)

# %%
# clean pop19
pop19 = clean_pop(pop19)

# drop columns no longer needed
pop19.drop(
    inplace=True,
    columns=[
        "SUMLEV",
        "REGION",
        "DIVISION",
        "STATE",
        "COUNTY",
        "ESTIMATESBASE2010",
        "CENSUS2010POP",
        "POPESTIMATE042020",
        "POPESTIMATE2020",
    ],
)
pop19.rename(inplace=True, columns=lambda c: c[-4:] if "POP" in c else c)
# Decided to just use the old name in accordance with mortality data
# Note: opioid shipment data may use `Oglala Lakota County`, be sure to change to Shannon County
pop19.loc[pop19["FIPS"] == 46102, ["CTYNAME", "FIPS"]] = ["Shannon County", 46113]

# %%
id_vars = ["STNAME", "CTYNAME", "FIPS"]
pop09 = pop09.melt(id_vars=id_vars, var_name="Year", value_name="Population")
pop19 = pop19.melt(id_vars=id_vars, var_name="Year", value_name="Population")

# %%
pop_all = pd.concat([pop09, pop19])
pop_all.to_csv(out_file, index=False)