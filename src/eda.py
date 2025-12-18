import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def run_eda():
    df = pd.read_csv("data/creditcard.csv")
    print("Shape:", df.shape)
    print(df.info())
    print(df.describe())

    # Fraud distribution
    sns.countplot(x="Class", data=df)
    plt.title("Fraud vs Non-Fraud")
    plt.show()

    # Transaction amount distribution
    sns.histplot(df["Amount"], bins=50, kde=True)
    plt.title("Transaction Amount Distribution")
    plt.show()

if __name__ == "__main__":
    run_eda()
