import pandas as pd

giftsFile = "./GiftDatabase.csv"
giftsData = pd.read_csv(giftsFile)

print(giftsData.head(10))