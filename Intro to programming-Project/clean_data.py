# Step 1: load and clean the Posidonia dataset (Marbà et al. 2013)
import pandas as pd

# the column names are on row 6 of the sheet, so skip the first 5 rows
data = pd.read_excel("data/Posidonia_oceanica_changes_Mediterranean.xls", header=5)

# remove empty rows and extra spaces in the column names
data = data.dropna(how="all")
data.columns = data.columns.str.strip()

# give two long column names a shorter name
data = data.rename(columns={"end of observation period (year)": "end_year",
  "relative  shoot  pop growth rate (yr-1)": "growth_rate"})

# some numbers are saved as text, so convert them to numbers
data["end_year"] = pd.to_numeric(data["end_year"], errors="coerce")
data["growth_rate"] = pd.to_numeric(data["growth_rate"], errors="coerce")

# status of each meadow: one column instead of three
data["status"] = "unknown"
data.loc[data["decline"] == 1, "status"] = "decline"
data.loc[data["no change"] == 1, "status"] = "stable"
data.loc[data["expansion"] == 1, "status"] = "expansion"

# 4 meadows are marked as two things at once (e.g. decline AND expansion)
number_of_marks = data[["decline", "no change", "expansion"]].sum(axis=1)
data.loc[number_of_marks > 1, "status"] = "mixed" # some meadows are classified as both expanding and declining 

# time period, based on the last year of observation
data["period"] = "unknown"
data.loc[data["end_year"] < 1990, "period"] = "before 1990"
data.loc[(data["end_year"] >= 1990) & (data["end_year"] < 2000), "period"] = "1990s"
data.loc[data["end_year"] >= 2000, "period"] = "2000s"

# pressure: True if at least one human pressure was reported
pressures = ["coastal works", "organic and nutrient sewage outfall",
             "Industrial sewage pollution", "Desalination sewage outfall",
             "Thermic sewage outfall", "bottom trawling", "fish farming",
             "anchor & other boat damages", "beach refilling",
             "invasive species", "turbidity", "erosion", "siltation"]
data["any_pressure"] = data[pressures].sum(axis=1) > 0

# save the clean data
data.to_csv("data/posidonia_clean.csv", index=False)

print(data.shape)
print(pd.crosstab(data["period"], data["status"]))