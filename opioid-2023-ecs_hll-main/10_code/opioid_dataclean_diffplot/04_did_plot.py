import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("mode.copy_on_write", True)

df = pd.read_csv('Merged_data_with_policy_info.csv')

policy_change_years = {
    'FL': 2010,
    'CA': 2010,
    'WA': 2012,
    'NC': 2012,
    'TX': 2007,
    'NY': 2007
}

def calculate_summed_per_capita(df, policy_change_years):

    
    
    df['MME_per_capita'] = df['MME'] / df['population'] 
    
    df['Period'] = df.apply(
        lambda row: 'Pre-Policy' if row['YEAR'] < policy_change_years[row['BUYER_STATE']] else 'Post-Policy',
        axis=1
    )

    df['Years_from_Policy_Change'] = df.apply(
        lambda row: row['YEAR'] - policy_change_years[row['BUYER_STATE']],
        axis=1
    )
    
    return df


df = calculate_summed_per_capita(df, policy_change_years)

def create_diff_in_diff_plot(df,state_with_policy,state_without_policy):
    ca_data = df[df['BUYER_STATE'] == state_without_policy]
    fl_data = df[df['BUYER_STATE'] == state_with_policy]
    ca_data['MME_per_capita'] = ca_data['MME_per_capita']/1000
    fl_data['MME_per_capita'] = fl_data['MME_per_capita']/1000
    # Define a function to calculate the confidence interval
    def calculate_confidence_interval(data, confidence=0.95):
        ci_data = data.groupby('Years_from_Policy_Change')['MME_per_capita'].agg(['mean', 'count', 'std'])
        ci_data['se'] = ci_data['std'] / np.sqrt(ci_data['count'])  # Standard error
        ci_data['h'] = ci_data['se'] * 1.96  # 95% CI multiplier for normal distribution
        ci_data['ci_lower'] = ci_data['mean'] - ci_data['h']
        ci_data['ci_upper'] = ci_data['mean'] + ci_data['h']
        return ci_data.reset_index()

    ca_pre_policy = ca_data[ca_data['Years_from_Policy_Change'] < 0]
    ca_post_policy = ca_data[ca_data['Years_from_Policy_Change'] >= 0]
    fl_pre_policy = fl_data[fl_data['Years_from_Policy_Change'] < 0]
    fl_post_policy = fl_data[fl_data['Years_from_Policy_Change'] >= 0]

    ca_pre_policy_ci = calculate_confidence_interval(ca_pre_policy)
    ca_post_policy_ci = calculate_confidence_interval(ca_post_policy)
    fl_pre_policy_ci = calculate_confidence_interval(fl_pre_policy)
    fl_post_policy_ci = calculate_confidence_interval(fl_post_policy)

    plt.figure(figsize=(14, 8))

    plt.plot(ca_pre_policy_ci['Years_from_Policy_Change'], ca_pre_policy_ci['mean'], label=f'{state_without_policy} Pre-Policy', color='blue')
    plt.fill_between(ca_pre_policy_ci['Years_from_Policy_Change'], ca_pre_policy_ci['ci_lower'], ca_pre_policy_ci['ci_upper'], color='blue', alpha=0.2)

    plt.plot(ca_post_policy_ci['Years_from_Policy_Change'], ca_post_policy_ci['mean'], label=f'{state_without_policy} Post-Policy', color='blue', linestyle='--')
    plt.fill_between(ca_post_policy_ci['Years_from_Policy_Change'], ca_post_policy_ci['ci_lower'], ca_post_policy_ci['ci_upper'], color='blue', alpha=0.2)

    plt.plot(fl_pre_policy_ci['Years_from_Policy_Change'], fl_pre_policy_ci['mean'], label=f'{state_with_policy} Pre-Policy', color='red')
    plt.fill_between(fl_pre_policy_ci['Years_from_Policy_Change'], fl_pre_policy_ci['ci_lower'], fl_pre_policy_ci['ci_upper'], color='red', alpha=0.2)

    plt.plot(fl_post_policy_ci['Years_from_Policy_Change'], fl_post_policy_ci['mean'], label=f'{state_with_policy} Post-Policy', color='red', linestyle='--')
    plt.fill_between(fl_post_policy_ci['Years_from_Policy_Change'], fl_post_policy_ci['ci_lower'], fl_post_policy_ci['ci_upper'], color='red', alpha=0.2)

    plt.axvline(x=0, color='grey', linestyle='--', label='Policy Change')

    plt.title('Difference-in-Difference Model with Confidence Intervals and Policy Change Break')
    plt.xlabel('Years from Policy Change')
    plt.ylabel('MME per Capita')

    plt.legend()

    file_path = f'diff_in_diff_{state_with_policy}_vs_{state_without_policy}.png'
    plt.tight_layout()
    plt.savefig(file_path)
    plt.show()

    plt.close()
    
    return file_path


policy_change_states = ['FL','WA']
states_without_policy_change = ['CA','NC']

for state_with_policy in policy_change_states:
    state_without_policy = states_without_policy_change.pop(0)
    file_path = create_diff_in_diff_plot(df,state_with_policy, state_without_policy)
    print(f'saved: {file_path}')