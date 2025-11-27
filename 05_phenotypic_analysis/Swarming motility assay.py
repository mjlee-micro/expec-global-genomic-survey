import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import f_oneway

file_path = r"Swarming motility assay.xlsx"
xls = pd.ExcelFile(file_path)
df = xls.parse('Sheet1')

timepoints = {
    '4h': ['4h', 'Unnamed: 3', 'Unnamed: 4'],
    '8h': ['8h', 'Unnamed: 6', 'Unnamed: 7'],
    '24h': ['24h', 'Unnamed: 9', 'Unnamed: 10']
}

long_records = []
raw_records = []
for _, row in df.iterrows():
    serotype = row['serotype']
    for time, cols in timepoints.items():
        values = row[cols].dropna().values.astype(float)
        mean_val = np.mean(values)
        std_val = np.std(values)
        long_records.append({'serotype': serotype, 'time': time, 'mean': mean_val, 'std': std_val})
        for v in values:
            raw_records.append({'serotype': serotype, 'time': time, 'value': v})

long_df = pd.DataFrame(long_records)
raw_df = pd.DataFrame(raw_records)

desired_order = ['O1', 'O2', 'O4', 'O6', 'O8', 'O15', 'O16', 'O18',
                 'O25', 'O75', 'O77', 'O86', 'O153', 'O162']
long_df['serotype'] = pd.Categorical(long_df['serotype'], categories=desired_order, ordered=True)
raw_df['serotype'] = pd.Categorical(raw_df['serotype'], categories=desired_order, ordered=True)

anova_results = {}
for tp in ['4h', '8h', '24h']:
    tp_data = raw_df[raw_df['time'] == tp]
    grouped = [group['value'].values for _, group in tp_data.groupby('serotype') if len(group) > 1]
    if len(grouped) >= 2:
        res = f_oneway(*grouped)
        k = len(grouped)                 
        N = sum(len(g) for g in grouped) 
        df1 = k - 1
        df2 = N - k
        anova_results[tp] = {
            "F": res.statistic,
            "p": res.pvalue,
            "df1": df1,
            "df2": df2
        }

print("ANOVA test")
for tp, res in anova_results.items():
    Fval, pval, df1, df2 = res["F"], res["p"], res["df1"], res["df2"]
    if pval < 0.001:
        stars = '***'
    elif pval < 0.01:
        stars = '**'
    elif pval < 0.05:
        stars = '*'
    else:
        stars = 'ns'
    print(f"{tp}: F({df1},{df2}) = {Fval}, p = {pval} ({stars})")

plt.figure(figsize=(12, 6))
pastel_palette = sns.color_palette(["#d2e3fc", "#a5dbe5", "#3b8fc2"])  
ax = sns.barplot(data=long_df, x='serotype', y='mean', hue='time',
                 errorbar=None, palette=pastel_palette, hue_order=['4h', '8h', '24h'])

for bar, (_, row) in zip(ax.patches, long_df.iterrows()):
    x = bar.get_x() + bar.get_width() / 2
    y = bar.get_height()
    if pd.notna(row['std']) and row['std'] > 0:
        ax.errorbar(x=x, y=y, yerr=row['std'], fmt='none', c='black', capsize=5)

def sig_symbol(p):
    if p < 0.001:
        return "***"
    elif p < 0.01:
        return "**"
    elif p < 0.05:
        return "*"
    else:
        return "ns"

title_lines = ["Swarming Assay by Serotype"]
for tp, res in anova_results.items():
    p = res["p"]
    stars = sig_symbol(p)
    title_lines.append(f"{tp}: p = {p:.3g} ({stars})")

plt.title("\n".join(title_lines), fontsize=14)

ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=20)
plt.ylabel('Swarming Diameter (mean ± std)')
plt.xlabel('Serotype')
plt.legend(title='Time Point')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
