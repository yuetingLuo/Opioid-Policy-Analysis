from pathlib import Path
import pandas as pd

pd.set_option("mode.copy_on_write", True)

import warnings
import seaborn as sns

warnings.simplefilter(action="ignore", category=FutureWarning)
sns.set(rc={"figure.dpi": 300, "savefig.dpi": 300})
sns.set_style("whitegrid")

repo_root = "../.."
# source files
scoped = repo_root + "/20_intermediate_file/overdose_analysis_scope_{}.parquet"

# output file
res_dir = Path(repo_root + "/30_results/overdose")
percap = "Deaths per 100k Population"

states = ["Texas", "Florida", "Washington"]
for state in states:
    file = scoped.format(state)
    state_df = pd.read_parquet(file)
    state_df[percap] = state_df.Deaths * 100000 / state_df.Population
    state_df.to_parquet(file)
