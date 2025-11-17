import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

mantel_df = pd.read_csv(r"D:\研究生\1.大肠埃希菌\论文\散点图数据\mantel_result_by_Otype_填补缺失.csv")
meta_df = pd.read_csv(r"D:\研究生\1.大肠埃希菌\论文\散点图数据\附表1_with_sharing_prop.csv")


mantel_df.columns = mantel_df.columns.str.strip()
meta_df.columns = meta_df.columns.str.strip()


sharing_df = meta_df.groupby("O_type", as_index=False).agg({
    "sharing_prop": "mean",
    "continent": lambda x: x.mode()[0] if not x.mode().empty else "Unknown"
})
merged_df = pd.merge(mantel_df, sharing_df, on="O_type", how="left")
merged_df = merged_df[merged_df["n_samples"] >= 0].copy()


sns.set(style="whitegrid")
fig, ax = plt.subplots(figsize=(12, 7))


sns.scatterplot(
    data=merged_df,
    x="sharing_prop",
    y="Mantel_r",
    hue="continent",
    palette="Set2",
    s=60,
    alpha=0.8,
    edgecolor="gray",
    ax=ax
)


sns.regplot(
    data=merged_df,
    x="sharing_prop",
    y="Mantel_r",
    scatter=False,
    color="blue",
    line_kws={'linewidth': 2},
    ci=95,
    ax=ax
)


highlighted_Otypes = ["O25", "O101", "O6", "O2", "O16", "O1", "O8", "O75"]

xlim = ax.get_xlim()
ylim = ax.get_ylim()
xrange = xlim[1] - xlim[0]
yrange = ylim[1] - ylim[0]

padding_x = 0.03 * xrange
padding_y = 0.03 * yrange

for _, row in merged_df.iterrows():
    if row["O_type"] in highlighted_Otypes:
        x, y = row["sharing_prop"], row["Mantel_r"]

       
        dx = padding_x
        dy = padding_y

        
        new_x = x + dx
        new_y = y + dy

      
        if new_x > xlim[1] - padding_x:
            new_x = x - dx
            ha = 'right'
        elif new_x < xlim[0] + padding_x:
            new_x = x + dx
            ha = 'left'
        else:
            ha = 'left'

    
        if new_y > ylim[1] - padding_y:
            new_y = y - dy
            va = 'top'
        elif new_y < ylim[0] + padding_y:
            new_y = y + dy
            va = 'bottom'
        else:
            va = 'bottom'

        ax.annotate(
            row["O_type"],
            xy=(x, y),
            xytext=(new_x, new_y),
            textcoords='data',
            arrowprops=dict(arrowstyle="-", color='black', lw=0.8),
            fontsize=9,
            weight='bold',
            color='black',
            ha=ha,
            va=va,
            clip_on=True
        )


plt.xlabel("Strain sharing proportion between regions")
plt.ylabel("Geographic effect (Mantel r)")
plt.title("Geographic Effect vs Strain Sharing across O types (with Labels)")
plt.legend(title="Continent", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(r"C:\Users\93966\Desktop\code\geography_vs_sharing_labeled_safe.png", dpi=600)
plt.show()
