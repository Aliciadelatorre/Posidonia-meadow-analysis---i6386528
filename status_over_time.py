# Step 2 (part 1): has the share of declining meadows changed over time?
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv("data/posidonia_clean.csv")

# keep only meadows with a known period and a clear status
data = data[data["period"] != "unknown"]
data = data[data["status"].isin(["decline", "stable", "expansion"])]

# count meadows per period and status
periods = ["before 1990", "1990s", "2000s"]
counts = pd.crosstab(data["period"], data["status"])
counts = counts.loc[periods, ["decline", "stable", "expansion"]]
print(counts)

# percentage of each status per period
n = counts.sum(axis=1)
percent = counts.div(n, axis=0) * 100
print(percent.round(1))

# uncertainty from subsampling: split each period into 5 random subsamples
np.random.seed(1)
number_of_subsamples = 5
error = {}
for period in periods:
    in_decline = (data[data["period"] == period]["status"] == "decline") * 100   # 100 if declining, 0 if not
    shuffled = np.random.permutation(in_decline)
    subsamples = np.array_split(shuffled, number_of_subsamples)
    subsample_percent = [np.mean(sub) for sub in subsamples]
    error[period] = np.std(subsample_percent, ddof=1)
    print(period, ": decline =", round(percent["decline"][period], 1), "+/-", round(error[period], 1), "% (n =", n[period], ")")
error = pd.Series(error)[periods]

# difference between the 1990s and the 2000s, and its uncertainty
difference = percent["decline"]["1990s"] - percent["decline"]["2000s"]
difference_error = np.sqrt(error["1990s"]**2 + error["2000s"]**2)
print("Drop in decline from 1990s to 2000s =", round(difference, 1), "+/-", round(difference_error, 1), "percentage points")

# significant if the difference is more than 3 times its uncertainty (3 sigma)
significance = abs(difference) / difference_error
print("This is", round(significance, 1), "sigma")
if significance > 3:
    print("Significant (more than 3 sigma)")
else:
    print("Not significant (less than 3 sigma)")

# stacked bar chart
plt.figure()
plt.bar(periods, percent["decline"], color="cornflowerblue", label="decline")
plt.bar(periods, percent["stable"], bottom=percent["decline"], color="lightsteelblue", label="stable")
plt.bar(periods, percent["expansion"], bottom=percent["decline"] + percent["stable"],
        color="slategrey", label="expansion")
plt.errorbar(periods, percent["decline"], yerr=error, fmt="none", color="black", capsize=5)

for i, period in enumerate(periods):
    plt.text(i, 102, "n = " + str(n[period]), ha="center")

plt.ylabel("Meadows (%)")
plt.xlabel("End of observation period")
plt.ylim(0, 110)
plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
plt.title("Status of Posidonia oceanica meadows over time")
plt.savefig("figure1_status_over_time.png", dpi=300, bbox_inches="tight")
