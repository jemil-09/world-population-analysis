# World Population Analysis

A data analysis project on population, growth and density for 234 countries and territories between 1970 and 2022.

**Team:** [Member 1 name] and [Member 2 name]

## About the project

Population numbers are easier to understand when they are plotted. In this project we clean the World Population dataset, compare countries and continents, and use charts to answer a few simple questions:

- Which countries and continents hold most of the world's people?
- How did population change from 1970 to 2022?
- Which countries are growing fastest, and which are shrinking?
- Is a country's size related to how crowded it is?

## Dataset

[World Population Dataset on Kaggle](https://www.kaggle.com/datasets/iamsouravbanerjee/world-population-dataset)

Each row is one country or territory. Columns include continent, population for 2022, 2020, 2015, 2010, 2000, 1990, 1980 and 1970, area, density, growth rate and share of world population.

## Tools used

Python, pandas, numpy, matplotlib, seaborn, plotly (optional, for the map), Jupyter Notebook, Git and GitHub.

## How to run

```bash
git clone https://github.com/[username]/world-population-analysis.git
cd world-population-analysis
pip install -r requirements.txt
```

1. Download the CSV from Kaggle and put it in the `data/` folder as `world_population.csv`.
2. Open `notebooks/world_population_analysis.ipynb` and run all cells.
3. The charts are saved automatically in the `images/` folder.

## Project structure

```
world-population-analysis/
├── data/                  (put the CSV here)
├── notebooks/
│   └── world_population_analysis.ipynb
├── images/                (charts are saved here)
├── requirements.txt
└── README.md
```

## Charts in the notebook

| File | What it shows |
|---|---|
| 01_top10_population.png | Top 10 most populated countries |
| 02_continent_share.png | Share of world population by continent |
| 03_continent_trend.png | Population by continent, 1970 to 2022 |
| 04_growth_since_1970.png | Percentage growth since 1970 by continent |
| 05_population_histogram.png | Distribution of country populations |
| 06_density_boxplot.png | Population density by continent |
| 07_fastest_growing.png | Top 10 fastest growing countries |
| 08_area_vs_population.png | Area vs population |
| 09_correlation_heatmap.png | Correlation between numeric columns |

## Findings

_Fill this in after running the notebook. Copy the key numbers from section 6 of the notebook and add your own short conclusions._

## Contributors

| Member | Work done |
|---|---|
| [Member 1] | Data cleaning, summary statistics, bar and line charts |
| [Member 2] | Box plot, scatter plot, heatmap, README |
