import pandas as pd

# Load the dataset
data = pd.read_excel('/Users/sumitkumarsingh/Downloads/Anomaly Detection in High-Dimensional Data/data/Online Retail.xlsx')

# Display basic information about the dataset
print('Dataset Info:')
data.info()

print('\nFirst 5 rows of the dataset:')
print(data.head())

print('\nMissing values before preprocessing:')
print(data.isnull().sum())

# Handle missing values
# Drop rows where CustomerID is NaN, as it's crucial for customer segmentation
data.dropna(subset=['CustomerID'], inplace=True)

# Fill missing Description with 'Unknown'
data['Description'].fillna('Unknown', inplace=True)

# Convert CustomerID to integer
data['CustomerID'] = data['CustomerID'].astype(int)

# Remove rows with negative Quantity (returns)
data = data[data['Quantity'] > 0]

# Calculate TotalPrice for each transaction
data['TotalPrice'] = data['Quantity'] * data['UnitPrice']

print('\nMissing values after preprocessing:')
print(data.isnull().sum())

print('\nDataset Info after preprocessing:')
data.info()

print('\nFirst 5 rows after preprocessing:')
print(data.head())


