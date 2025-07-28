import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA

# Load the dataset with anomaly predictions
data = pd.read_csv("KDD2014_donors_10feat_nomissing_normalised_with_anomalies.csv")

# Separate features and anomaly labels
X = data.iloc[:, :-2]  # All columns except the last two (class and anomaly)
y_anomaly = data["anomaly"]

# Perform PCA for dimensionality reduction to 2 components for visualization
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

# Create a DataFrame for the PCA results
pca_df = pd.DataFrame(data=X_pca, columns=["PC1", "PC2"])
pca_df["anomaly"] = y_anomaly

# Plot the data points, highlighting anomalies
plt.figure(figsize=(10, 8))
sns.scatterplot(x="PC1", y="PC2", hue="anomaly", data=pca_df, palette=["blue", "red"], alpha=0.6)
plt.title("Anomaly Detection using Isolation Forest (PCA Reduced)")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend(title="Anomaly", labels=["Inlier", "Outlier"])
plt.grid(True)
plt.savefig("anomaly_detection_pca_plot.png")


print("Anomaly visualization saved to anomaly_detection_pca_plot.png")

