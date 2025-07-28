import pandas as pd
from sklearn.ensemble import IsolationForest

# Load the dataset
data = pd.read_csv('KDD2014_donors_10feat_nomissing_normalised.csv')

# Assuming the last column is the 'class' label and should not be used for training
X = data.iloc[:, :-1]

# Initialize and train the Isolation Forest model
# contamination is the proportion of outliers in the dataset. Adjust as needed.
model = IsolationForest(random_state=42, contamination=0.01)
model.fit(X)

# Predict anomalies (-1 for outliers, 1 for inliers)
data['anomaly'] = model.predict(X)

# Filter out the anomalies
anomalies = data[data['anomaly'] == -1]

print(f"Total data points: {len(data)}")
print(f"Number of anomalies detected: {len(anomalies)}")
print("\nFirst 5 detected anomalies:\n", anomalies.head())

# Optionally, save the data with anomaly scores
data.to_csv('KDD2014_donors_10feat_nomissing_normalised_with_anomalies.csv', index=False)
print("\nData with anomaly predictions saved to KDD2014_donors_10feat_nomissing_normalised_with_anomalies.csv")

