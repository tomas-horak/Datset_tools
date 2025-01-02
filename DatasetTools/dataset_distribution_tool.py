import pandas as pd
import matplotlib.pyplot as plt


def show_distribution_from_csv(input_csv):
    df = pd.read_csv(input_csv, )
    class_sums = df.iloc[:, 1:].sum()
    print(df.info)
    print(df.shape)
    print(class_sums)
    plt.figure(figsize=(12, 6))
    class_sums.plot(kind='bar')
    plt.title("Class Distribution of Houseplants-25")
    plt.xlabel("Class", fontsize=12)
    plt.ylabel("Number of Samples")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
