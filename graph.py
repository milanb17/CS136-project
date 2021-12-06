import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

csvs = ["innovation_bump.csv", "prosection.csv",
        "prosecution_normalization.csv", ]
for csv in csvs:
    df = pd.read_csv(os.path.join(os.curdir, csv))
    varying_parameter = df.iloc[:, 0]

    for i in [2, 3, 4]:
        y = df.iloc[:, i]

        plt.plot(varying_parameter, y)
        plt.xlabel(df.columns[0])
        plt.ylabel(df.columns[i])
        plt.show()
