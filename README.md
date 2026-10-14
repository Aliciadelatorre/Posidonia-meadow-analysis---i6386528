# Posidonia oceanica decline in the Mediterranean Sea

Data analysis project for MAT2007.

This project asks two questions:

1. Has decline of *Posidonia oceanica* meadows become less common over time?
2. Do meadows exposed to human pressures lose shoots faster than meadows without them?

The full results and discussion are in the report (`report/report.pdf`).

## Repository contents

| File | What it does |
|---|---|
| `clean_data.py` | Loads the raw Excel file, cleans it and saves `data/posidonia_clean.csv` |
| `status_over_time.py` | Percentage of declining meadows per period, uncertainties from subsampling, 3σ significance test, Figure 1 |
| `growth_and_pressures.py` | Shoot growth rates with vs without human pressures (mean, skewness, median), uncertainties from subsampling, 3σ significance test, Figure 2 |
| `data/` | Raw dataset (`.xls`) and the cleaned dataset (`.csv`) |
| `report/` | LaTeX source and PDF of the report |

## Dataset

Marbà, N., Díaz-Almela, E., & Duarte, C. M. (2013). *Posidonia oceanica changes in the Mediterranean Sea* [Dataset]. Digital.CSIC. https://doi.org/10.20350/digitalCSIC/3861

The raw file is already included in `data/` as `Posidonia_oceanica_changes_Mediterranean.xls`, so you do not need to download it. The dataset is licensed under CC BY-NC-SA 4.0.

The data needs cleaning before analysis. `clean_data.py` does this automatically:

- skips the 5 empty rows above the column names in the Excel sheet
- removes empty rows and extra spaces in column names
- converts numbers stored as text to numeric values (invalid entries become missing values)
- combines the three status columns (decline / no change / expansion) into one `status` column; 5 meadows marked with two contradictory statuses are labelled `mixed` and excluded from the analysis
- groups meadows by the end year of their observation period: before 1990, 1990s, 2000s
- marks a meadow as pressured if at least one of 13 human pressures was reported

## Requirements

- Python 3 (tested with Python 3.14)
- Packages: `pandas`, `numpy`, `scipy`, `matplotlib`, `xlrd`

`xlrd` is needed because the raw data is an old Excel `.xls` file.

## Installation

Clone the repository and install the packages:

```
git clone https://github.com/USERNAME/posidonia-meadow-analysis.git
cd posidonia-meadow-analysis
pip3 install pandas numpy scipy matplotlib xlrd
```

## How to run

Run the three scripts one after the other, in this order, from the main folder of the repository:

```
python3 clean_data.py
python3 status_over_time.py
python3 growth_and_pressures.py
```

1. `clean_data.py` must be run first: it creates `data/posidonia_clean.csv`, which the other two scripts read.
2. `status_over_time.py` prints the percentages, the difference between the 1990s and the 2000s and its significance, and saves `figure1_status_over_time.png`.
3. 'growth_and_pressures.py` prints the mean, skewness and median per group, the difference of means and its significance, and saves `figure2_growth_and_pressures.png`.

The scripts must be run from the main folder, because they look for the data in `data/`.

## Reproducibility

The subsampling uses a fixed random seed (`np.random.seed(1)`), so every run gives exactly the same numbers. Expected key results:

- Decline 1990s → 2000s: 72.8 ± 5.4 % → 43.5 ± 4.7 %, a drop of 29.2 ± 7.1 percentage points (4.1σ, significant)
- Difference in mean growth rate (pressure − no pressure): −0.437 ± 0.264 per year (1.7σ, not significant)
