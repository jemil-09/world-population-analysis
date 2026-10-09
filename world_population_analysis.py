"""World Population Analysis
Put world_population.csv inside the data/ folder, then run:  python world_population_analysis.py
Charts are saved in the images/ folder."""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
pd.options.display.float_format = "{:,.2f}".format

# find the data file whether the notebook is run from notebooks/ or the repo root
candidates = [Path("../data/world_population.csv"), Path("data/world_population.csv"), Path("world_population.csv")]
DATA = next((p for p in candidates if p.exists()), None)
if DATA is None:
    raise FileNotFoundError("Put world_population.csv inside the data/ folder (see README).")

IMG = Path("../images") if Path("../data").exists() else Path("images")
IMG.mkdir(exist_ok=True)

def save(name):
    plt.savefig(IMG / name, dpi=150, bbox_inches="tight")

raw = pd.read_csv(DATA)
print("Rows and columns:", raw.shape)
print(raw.head())

raw.info()

print("Missing values per column:")
print(raw.isna().sum())
print()
print("Duplicate rows:", raw.duplicated().sum())
print("Duplicate country names:", raw["Country/Territory"].duplicated().sum())

df = raw.rename(columns={
    "Country/Territory": "country",
    "Continent": "continent",
    "Capital": "capital",
    "CCA3": "code",
    "Rank": "rank",
    "Area (km²)": "area_km2",
    "Density (per km²)": "density",
    "Growth Rate": "growth_rate",
    "World Population Percentage": "world_pct",
    **{f"{y} Population": f"pop_{y}" for y in [2022, 2020, 2015, 2010, 2000, 1990, 1980, 1970]},
})

df = df.drop_duplicates()
df["country"] = df["country"].str.strip()
df["continent"] = df["continent"].str.strip()

# 1.0156 means the population grew 1.56% in a year
df["growth_pct"] = (df["growth_rate"] - 1) * 100

pop_cols = sorted([c for c in df.columns if c.startswith("pop_")])   # pop_1970 ... pop_2022
years = [int(c.split("_")[1]) for c in pop_cols]
print(df.head())

print(df[["pop_2022", "area_km2", "density", "growth_pct", "world_pct"]].describe())

print(df.groupby("continent").agg(
    countries=("country", "count"),
    population_2022=("pop_2022", "sum"),
    avg_density=("density", "mean"),
    avg_growth_pct=("growth_pct", "mean"),
).sort_values("population_2022", ascending=False))

top10 = df.nlargest(10, "pop_2022").sort_values("pop_2022")

plt.figure(figsize=(8, 5))
plt.barh(top10["country"], top10["pop_2022"] / 1e6, color=sns.color_palette("Blues", 10))
plt.xlabel("Population in 2022 (millions)")
plt.title("Top 10 most populated countries, 2022")
save("01_top10_population.png")
plt.show()

share = df.groupby("continent")["pop_2022"].sum().sort_values(ascending=False)

plt.figure(figsize=(7, 7))
plt.pie(share, labels=share.index, autopct="%1.1f%%", startangle=90,
        wedgeprops=dict(width=0.45), colors=sns.color_palette("Set2", len(share)))
plt.title("Share of world population by continent, 2022")
save("02_continent_share.png")
plt.show()

cont_year = df.groupby("continent")[pop_cols].sum()

plt.figure(figsize=(9, 5))
for cont in cont_year.index:
    plt.plot(years, cont_year.loc[cont] / 1e6, marker="o", label=cont)
plt.xlabel("Year")
plt.ylabel("Population (millions)")
plt.title("Population by continent, 1970 to 2022")
plt.legend()
save("03_continent_trend.png")
plt.show()

change = ((cont_year["pop_2022"] / cont_year["pop_1970"] - 1) * 100).sort_values()

plt.figure(figsize=(8, 4.5))
plt.barh(change.index, change.values, color=sns.color_palette("Greens", len(change)))
plt.xlabel("Population change from 1970 to 2022 (%)")
plt.title("Growth since 1970 by continent")
save("04_growth_since_1970.png")
plt.show()

plt.figure(figsize=(8, 5))
sns.histplot(df["pop_2022"], log_scale=True, bins=30, color="steelblue")
plt.xlabel("Population in 2022 (log scale)")
plt.ylabel("Number of countries")
plt.title("Distribution of country populations")
save("05_population_histogram.png")
plt.show()

plt.figure(figsize=(9, 5))
sns.boxplot(data=df, x="continent", y="density", palette="Set3", hue="continent", legend=False)
plt.yscale("log")
plt.xlabel("")
plt.ylabel("Density (people per km², log scale)")
plt.title("Population density by continent")
plt.xticks(rotation=20)
save("06_density_boxplot.png")
plt.show()

fast = df.nlargest(10, "growth_pct").sort_values("growth_pct")

plt.figure(figsize=(8, 5))
plt.barh(fast["country"], fast["growth_pct"], color=sns.color_palette("Oranges", 10))
plt.xlabel("Yearly growth rate (%)")
plt.title("Top 10 fastest growing countries")
save("07_fastest_growing.png")
plt.show()

shrinking = df[df["growth_pct"] < 0][["country", "continent", "growth_pct"]].sort_values("growth_pct")
print(f"Countries with a falling population: {len(shrinking)}")
print(shrinking.head(10))

plt.figure(figsize=(9, 6))
sns.scatterplot(data=df, x="area_km2", y="pop_2022", hue="continent", alpha=0.8)
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Area (km², log scale)")
plt.ylabel("Population in 2022 (log scale)")
plt.title("Area vs population")
save("08_area_vs_population.png")
plt.show()

corr_cols = ["pop_2022", "pop_1970", "area_km2", "density", "growth_pct", "world_pct"]

plt.figure(figsize=(7, 5.5))
sns.heatmap(df[corr_cols].corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0)
plt.title("Correlation between numeric columns")
save("09_correlation_heatmap.png")
plt.show()

# Needs plotly (pip install plotly). Skipped automatically if it is not installed.
try:
    import plotly.express as px
    fig = px.choropleth(df, locations="code", color="density", hover_name="country",
                        color_continuous_scale="Viridis", range_color=(0, 500),
                        title="Population density (people per km²)")
    fig.show()
except ImportError:
    print("plotly not installed, skipping the map.")

largest = df.loc[df["pop_2022"].idxmax()]
fastest = df.loc[df["growth_pct"].idxmax()]
densest = df.loc[df["density"].idxmax()]
densest_big = df[df["area_km2"] >= 1000].nlargest(1, "density").iloc[0]
top_cont = share.index[0]
fast_cont = change.index[-1]

print(f"Most populated country: {largest['country']} ({largest['pop_2022']:,.0f} people)")
print(f"{top_cont} holds {share.iloc[0] / share.sum() * 100:.1f}% of the population in this dataset")
print(f"Fastest growing continent since 1970: {fast_cont} ({change.iloc[-1]:.0f}% increase)")
print(f"Fastest growing country: {fastest['country']} ({fastest['growth_pct']:.2f}% per year)")
print(f"Densest place: {densest['country']} ({densest['density']:,.0f} per km²)")
print(f"Densest country with area of 1,000 km² or more: {densest_big['country']} ({densest_big['density']:,.0f} per km²)")
print(f"Countries with a shrinking population: {len(shrinking)}")

