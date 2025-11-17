import pandas as pd
import numpy as np

meta = pd.read_excel(r"Supplementary Table 1.xlsx", dtype=str)
samples = meta["sample"].tolist()
conts = meta["continent"].tolist()

centroids = {
    "Africa":       (-0.0236,   9.1021),
    "Asia":         (100.6197,  34.0479),
    "Europe":       (10.4515,   51.1657),
    "North America":(-100.4459, 40.1267),
    "South America":(-58.4438, -14.2350),
    "Oceania":      (134.4890, -25.7340)
}
valid_conts = list(centroids.keys())

unknowns = sorted({c for c in conts if c not in valid_conts})
if unknowns:
    print("Warning：", unknowns)

lon = np.array([centroids[c][0] for c in valid_conts])
lat = np.array([centroids[c][1] for c in valid_conts])
lon_r = np.radians(lon)
lat_r = np.radians(lat)
dlon = lon_r[:, None] - lon_r[None, :]
dlat = lat_r[:, None] - lat_r[None, :]
a = np.sin(dlat/2)**2 + np.cos(lat_r)[:, None] * np.cos(lat_r)[None, :] * np.sin(dlon/2)**2
c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
R = 6371.0
cent_dist = R * c  # valid_conts x valid_conts

cont_idx = np.array([valid_conts.index(c) if c in valid_conts else -1 for c in conts])

geo_mat = cent_dist[cont_idx[:, None] % len(valid_conts),
                    cont_idx[None, :]  % len(valid_conts)]

mask = (cont_idx[:, None] == -1) | (cont_idx[None, :] == -1)
geo_mat[mask] = np.nan

geo_df = pd.DataFrame(geo_mat, index=samples, columns=samples)
geo_df.to_csv(r"geo_dist.csv", float_format="%.3f")
