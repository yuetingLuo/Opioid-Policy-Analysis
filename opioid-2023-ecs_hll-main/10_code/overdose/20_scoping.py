# %%
from pathlib import Path
import pandas as pd
import numpy as np

pd.set_option("mode.copy_on_write", True)

repo_root = Path("../..")
int_dir = repo_root / '20_intermediate_file'
# source file
overdose = int_dir / "overdose_03-15.tsv"
pop = int_dir / "population_00-19.csv"

# output file
out_dir = int_dir

overdose = pd.read_csv(overdose, sep="\t")
pop = pd.read_csv(pop)

# %%
impute = overdose.loc[[6747, 6812, 6813]]
impute.Year -= 1
impute.Deaths = 8
imputed_overdose = pd.concat([overdose, impute], ignore_index=True)

pop = pop[["STNAME", "FIPS", "Year", "Population"]]
merged = imputed_overdose.merge(pop, how="left", on=["FIPS", "Year"], validate="1:1")

# %%
treated = ["Texas", "Florida", "Washington"]
exclude = {"New Jersey", "New York", *treated}
change_years = {"Texas": 2007, "Florida": 2010, "Washington": 2012}

def analysis_scope(overdose_pop, state, p_m=4):
    print("====", state, "====")
    change_year = change_years[state]
    state_df = overdose_pop[~overdose_pop.STNAME.isin(exclude - {state})]
    state_df = state_df[
        state_df.Year.between(change_year - p_m, change_year + p_m, "left")
    ]
    print(f"Year range: {state_df.Year.min()} to {state_df.Year.max()}")

    num_years = state_df.Year.nunique()
    thresh = (
        state_df.groupby("FIPS", as_index=False)
        .Population.filter(lambda g: len(g) < num_years)
        .max()
    )
    print(f"Population threshold: {thresh}")

    filtered = state_df.groupby("FIPS", as_index=False).filter(
        lambda g: g.Population.max() > thresh
    )
    print(f"Number of counties: {filtered.FIPS.nunique()}\n")
    filtered.to_parquet(out_dir / f"overdose_analysis_scope_{state}.parquet")

# %%
analysis_scope(merged, "Texas")
analysis_scope(merged, "Florida")
analysis_scope(merged, "Washington")
