import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns

# Load the preprocessed data
data = pd.read_csv("/Users/sumitkumarsingh/Downloads/Anomaly Detection in High-Dimensional Data/data/Online Retail Preprocessed.csv")

# Convert InvoiceDate to datetime
data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"])

# --- RFM Analysis ---
# Calculate Recency, Frequency, Monetary (RFM) values
max_date = data["InvoiceDate"].max()

rfm = data.groupby("CustomerID").agg({
    "InvoiceDate": lambda date: (max_date - date.max()).days, # Recency
    "InvoiceNo": lambda num: num.nunique(), # Frequency
    "TotalPrice": lambda price: price.sum() # Monetary
})

rfm.columns = ["Recency", "Frequency", "Monetary"]

# Handle outliers in RFM data (e.g., capping)
# For now, let's focus on the core clustering, but this is a point for refinement.

# Scale the RFM data
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm)
rfm_scaled_df = pd.DataFrame(rfm_scaled, columns=rfm.columns, index=rfm.index)

# --- Determine Optimal Number of Clusters (Elbow Method and Silhouette Score) ---
ssd = [] # Sum of squared distances
silhouette_scores = []
range_n_clusters = range(2, 11) # Test 2 to 10 clusters

for num_clusters in range_n_clusters:
    kmeans = KMeans(n_clusters=num_clusters, max_iter=300, random_state=42, n_init=10)
    kmeans.fit(rfm_scaled_df)
    ssd.append(kmeans.inertia_)
    
    cluster_labels = kmeans.labels_
    silhouette_avg = silhouette_score(rfm_scaled_df, cluster_labels)
    silhouette_scores.append(silhouette_avg)

# Plot Elbow Method
plt.figure(figsize=(10, 5))
plt.plot(range_n_clusters, ssd, marker='o')
plt.title("Elbow Method for Optimal K")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Sum of Squared Distances")
plt.grid(True)
plt.savefig("elbow_method.png")

# Plot Silhouette Scores
plt.figure(figsize=(10, 5))
plt.plot(range_n_clusters, silhouette_scores, marker='o')
plt.title("Silhouette Score for Optimal K")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Silhouette Score")
plt.grid(True)
plt.savefig("silhouette_score.png")

print("Elbow method plot saved to elbow_method.png")
print("Silhouette score plot saved to silhouette_score.png")

# --- K-Means Clustering with chosen K (e.g., K=3 or K=4 based on typical elbow/silhouette analysis) ---
# For demonstration, let's choose K=3 (a common choice for RFM segmentation)
optimal_k = 3 
kmeans = KMeans(n_clusters=optimal_k, max_iter=300, random_state=42, n_init=10)
rfm_scaled_df["Cluster"] = kmeans.fit_predict(rfm_scaled_df)

# Add cluster labels back to the original RFM dataframe
rfm["Cluster"] = rfm_scaled_df["Cluster"]

print(f"\nK-Means Clustering with K={optimal_k} completed.")
print("\nCluster Sizes:")
print(rfm["Cluster"].value_counts())

print("\nCluster Means (Original Scale):")
print(rfm.groupby("Cluster").mean())

# Visualize clusters (e.g., pairplot of RFM with hue=Cluster)
sns.pairplot(rfm, vars=["Recency", "Frequency", "Monetary"], hue="Cluster", palette="viridis")
plt.suptitle(f"RFM Clusters (K={optimal_k})", y=1.02) # Adjust suptitle position
plt.savefig("rfm_clusters_pairplot.png")
print("RFM clusters pairplot saved to rfm_clusters_pairplot.png")


