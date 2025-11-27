import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['axes.unicode_minus'] = False
sns.set(style="whitegrid")

file_path = r"Growth performance.xlsx"  
df = pd.read_excel(file_path)

df[['sample', 'serotype']] = df[['sample', 'serotype']].ffill()
df['serotype'] = df['serotype'].replace('DEFULT', 'Negative Control')

raw_time_cols = df.columns[3:]


try:
    time_in_hours = [t.total_seconds() / 3600 for t in raw_time_cols]  
except AttributeError:
    time_in_hours = []
    for t in raw_time_cols:
        if isinstance(t, str):  
            h, m, s = map(int, t.split(":"))
            time_in_hours.append(h + m/60 + s/3600)
        elif isinstance(t, datetime.time):  
            time_in_hours.append(t.hour + t.minute / 60 + t.second / 3600)
        else:
            raise ValueError(f"unable to identify: {t}")


unique_serotypes = df['serotype'].unique()
palette = sns.color_palette("tab10", len(unique_serotypes))
serotype_colors = dict(zip(unique_serotypes, palette))
serotype_colors['DEFULT'] = 'gray'


plt.figure(figsize=(12, 6))

for sample_name, group in df.groupby('sample'):
    serotype = group['serotype'].iloc[0]
    color = serotype_colors[serotype]
    
    data = group[raw_time_cols].astype(float)
    mean_vals = data.mean(axis=0)
    std_vals = data.std(axis=0)
    
    plt.plot(time_in_hours, mean_vals, label=sample_name, color=color, linewidth=2)
    plt.fill_between(time_in_hours, mean_vals - std_vals, mean_vals + std_vals, alpha=0.2, color=color)

handles = []
labels_seen = set()
for sample_name, group in df.groupby('sample'):
    serotype = group['serotype'].iloc[0]
    if serotype not in labels_seen:
        handles.append(plt.Line2D([], [], color=serotype_colors[serotype], label=serotype))
        labels_seen.add(serotype)

plt.legend(handles=handles, title="Serotype", bbox_to_anchor=(1.05, 1), loc='upper left')

plt.xlabel("Time (hours)", fontsize=12)
plt.ylabel("OD600", fontsize=12)
plt.title("Bacterial Growth Curves by Serotype", fontsize=14)
plt.tight_layout()
plt.grid(True, linestyle='--', alpha=0.3)

plt.show()