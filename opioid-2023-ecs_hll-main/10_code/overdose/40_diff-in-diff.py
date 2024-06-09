# %%
from pathlib import Path
import pandas as pd

pd.set_option("mode.copy_on_write", True)
import matplotlib.pyplot as plt
import warnings
import seaborn as sns
warnings.simplefilter(action="ignore", category=FutureWarning)
sns.set(rc={"figure.dpi": 300, "savefig.dpi": 300})
sns.set_style("whitegrid")

repo_root = "../.."
# source files
scoped = repo_root + "/20_intermediate_file/overdose_analysis_scope_{}.parquet"

# output files
res_dir = Path(repo_root + "/30_results/overdose")


# %%
change_years = {"Texas": 2007, "Florida": 2010, "Washington": 2012}
percap = "Deaths per 100k Population"


# %%
def diff_in_diff(overdose, state, controls):
    state_df = overdose[overdose["STNAME"].isin(controls + [state])]
    state_df[state] = state_df["STNAME"] == state
    state_df["Year"] -= change_years[state]

    plt.figure(figsize=(9, 6))
    ax = sns.regplot(
        state_df[(state_df[state]) & (state_df.Year >= 0)],
        x="Year",
        y=percap,
        color=sns.color_palette()[0],
        scatter=False,
        ci=68,
    )
    ax.text(0, ax.get_ylim()[1] - 2, "Policy Change", ha="right")
    sns.regplot(
        state_df[(state_df[state]) & (state_df.Year < 0)],
        x="Year",
        y=percap,
        color=sns.color_palette()[0],
        scatter=False,
        ci=68,
        label=state,
    )
    sns.regplot(
        state_df[(~state_df[state]) & (state_df.Year >= 0)],
        x="Year",
        y=percap,
        color=sns.color_palette()[1],
        scatter=False,
        ci=68,
    )
    sns.regplot(
        state_df[(~state_df[state]) & (state_df.Year < 0)],
        x="Year",
        y=percap,
        color=sns.color_palette()[1],
        scatter=False,
        ci=68,
        label=", ".join(controls),
    )

    ax.set_title(f"{state} Overdose Deaths Diff-in-diff Model Graph")
    ax.set_xlabel("Years from Policy Change")
    ax.axvline(0, color="grey", linestyle="--")

    ax.legend()
    plt.tight_layout()
    plt.savefig(res_dir / f"{state}_Overdose_Diff-in-diff")

# %%
tx_df = pd.read_parquet(scoped.format("Texas"))
fl_df = pd.read_parquet(scoped.format("Florida"))
wa_df = pd.read_parquet(scoped.format("Washington"))
# %%
controls = ["Georgia", "Alabama", "Kansas"]
diff_in_diff(tx_df, "Texas", controls)

controls = ["South Carolina", "Alabama", "Tennessee"]
diff_in_diff(fl_df, "Florida", controls)

controls = ["Oregon", "Colorado", "Maryland"]
diff_in_diff(wa_df, "Washington", controls)