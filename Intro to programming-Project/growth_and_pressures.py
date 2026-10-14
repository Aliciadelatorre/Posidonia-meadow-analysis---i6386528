# Step 3 (part 2): do meadows with human pressures lose shoots faster?
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skew

data = pd.read_csv("data/posidonia_clean.csv")

# keep only meadows with a measured growth rate
data = data[data["growth_rate"].notna()]

with_pressure = data[data["any_pressure"] == True]["growth_rate"]
without_pressure = data[data["any_pressure"] == False]["growth_rate"]

# subsampling: split each group into 5 random subsamples
# the uncertainty is the standard deviation of the 5 subsample values
np.random.seed(1)
number_of_subsamples = 5

results = {}
for name, group in [("with pressure", with_pressure), ("without pressure", without_pressure)]:
    shuffled = np.random.permutation(group)
    subsamples = np.array_split(shuffled, number_of_subsamples)

    subsample_means = [np.mean(sub) for sub in subsamples]
    subsample_skews = [skew(sub) for sub in subsamples]

    mean = group.mean()
    mean_error = np.std(subsample_means, ddof=1)
    skewness = skew(group)
    skewness_error = np.std(subsample_skews, ddof=1)
    median = group.median()
    loss = (1 - np.exp(median)) * 100

    print(name, ": n =", len(group))
    print("   mean =", round(mean, 3), "+/-", round(mean_error, 3), "per year")
    print("   skewness =", round(skewness, 2), "+/-", round(skewness_error, 2))
    print("   median =", round(median, 3), "per year (about", round(loss, 1), "% of shoots lost per year)")

    results[name] = (mean, mean_error)

# difference between the two means and its uncertainty
mean1, error1 = results["with pressure"]
mean2, error2 = results["without pressure"]
difference = mean1 - mean2
difference_error = np.sqrt(error1**2 + error2**2)
print("Difference in means =", round(difference, 3), "+/-", round(difference_error, 3), "per year")

# significant if the difference is more than 3 times its uncertainty (3 sigma)
significance = abs(difference) / difference_error
print("This is", round(significance, 1), "sigma")
if significance > 3:
    print("Significant (more than 3 sigma)")
else:
    print("Not significant (less than 3 sigma)")

# boxplot
plt.figure()
plt.boxplot([without_pressure, with_pressure])
plt.xticks([1, 2], ["No pressure reported\n(n = " + str(len(without_pressure)) + ")",
                    "At least one pressure\n(n = " + str(len(with_pressure)) + ")"])
plt.axhline(0, color="cornflowerblue", linestyle="--")
plt.ylabel("Relative shoot population growth rate (per year)")
plt.title("Shoot growth rate of Posidonia oceanica meadows")
plt.savefig("figure2_growth_and_pressures.png", dpi=300, bbox_inches="tight")