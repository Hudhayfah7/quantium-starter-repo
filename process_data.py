import pandas as pd

# Load CSV files
df1 = pd.read_csv("data/daily_sales_data_0.csv")
df2 = pd.read_csv("data/daily_sales_data_1.csv")
df3 = pd.read_csv("data/daily_sales_data_2.csv")

# Combine into one dataframe
df = pd.concat([df1, df2, df3], ignore_index=True)
# Keep only Pink Morsel sales
df = df[df["product"] == "pink morsel"]
# Clean price field and convert price/quantity to numbers
df["price"] = df["price"].str.replace("$", "").astype(float)
df["quantity"] = df["quantity"].astype(int)

# Compute total sales value
df["sales"] = df["price"] * df["quantity"]
# Keep required output columns
output = df[["sales", "date", "region"]]
# Export formatted CSV
output.to_csv("processed/pink_morsel_sales.csv", index=False)
