import matplotlib.pyplot as plt
import pandas as pd
import os

csvs = ["innovation_bump.csv", "prosection.csv",
        "prosecution_normalization.csv", ]
for csv in csvs:
    df = pd.read_csv(os.path.join(os.curdir, csv))
    varying_parameter = df.iloc[:, 0]
    xlabel = df.columns[0]

    for i in [2, 3, 4]:
        y = df.iloc[:, i]
        ylabel = df.columns[i]

        plt.plot(varying_parameter, y)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig(f"./plots/{xlabel}-{ylabel}.png")
        plt.close()
