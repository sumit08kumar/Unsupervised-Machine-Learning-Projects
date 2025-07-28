import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the preprocessed data
data = pd.read_csv("/Users/sumitkumarsingh/Downloads/Anomaly Detection in High-Dimensional Data/data/Online Retail Preprocessed.csv")

# Convert InvoiceDate to datetime
data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"])

# --- RFM Analysis ---
# Calculate Recency, Frequency, Monetary (RFM) values
# Recency: Days since last purchase
# Frequency: Number of purchases
# Monetary: Total spending

# Get the most recent date in the dataset
max_date = data["InvoiceDate"].max()

rfm = data.groupby("CustomerID").agg({
    "InvoiceDate": lambda date: (max_date - date.max()).days, # Recency
    "InvoiceNo": lambda num: num.nunique(), # Frequency
    "TotalPrice": lambda price: price.sum() # Monetary
})

rfm.columns = ["Recency", "Frequency", "Monetary"]

print("\nRFM Data Head:")
print(rfm.head())

print("\nRFM Data Description:")
print(rfm.describe())

# --- Visualize RFM Distribution ---
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
sns.histplot(rfm["Recency"], bins=50, kde=True)
plt.title("Recency Distribution")

plt.subplot(1, 3, 2)
sns.histplot(rfm["Frequency"], bins=50, kde=True)
plt.title("Frequency Distribution")

plt.subplot(1, 3, 3)
sns.histplot(rfm["Monetary"], bins=50, kde=True)
plt.title("Monetary Distribution")

plt.tight_layout()
plt.savefig("rfm_distribution.png")

print("RFM distribution plots saved to rfm_distribution.png")

# --- Explore Top Countries by Sales ---
top_countries = data.groupby("Country")["TotalPrice"].sum().sort_values(ascending=False).head(10)
print("\nTop 10 Countries by Total Sales:")
print(top_countries)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_countries.index, y=top_countries.values)
plt.title("Top 10 Countries by Total Sales")
plt.xlabel("Country")
plt.ylabel("Total Sales")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("top_countries_sales.png")
print("Top countries by sales plot saved to top_countries_sales.png")

# --- Explore Top Products by Quantity ---
top_products = data.groupby("Description")["Quantity"].sum().sort_values(ascending=False).head(10)
print("\nTop 10 Products by Quantity:")
print(top_products)

plt.figure(figsize=(12, 6))
sns.barplot(x=top_products.index, y=top_products.values)
plt.title("Top 10 Products by Quantity")
plt.xlabel("Product Description")
plt.ylabel("Total Quantity Sold")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("top_products_quantity.png")
print("Top products by quantity plot saved to top_products_quantity.png")

# --- Explore Sales Over Time ---
data["InvoiceMonth"] = data["InvoiceDate"].dt.to_period("M")
monthly_sales = data.groupby("InvoiceMonth")["TotalPrice"].sum()

plt.figure(figsize=(12, 6))
monthly_sales.plot(kind="line")
plt.title("Monthly Sales Over Time")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.grid(True)
plt.tight_layout()
plt.savefig("monthly_sales_over_time.png")
print("Monthly sales over time plot saved to monthly_sales_over_time.png")


