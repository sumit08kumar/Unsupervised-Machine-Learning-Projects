import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the RFM data with clusters
rfm = pd.read_csv("/Users/sumitkumarsingh/Downloads/Anomaly Detection in High-Dimensional Data/data/Online Retail RFM Clusters.csv", index_col='CustomerID')
# --- Analyze Cluster Characteristics ---
cluster_means = rfm.groupby('Cluster').mean()
print("\nCluster Means (Original Scale):\n", cluster_means)

cluster_medians = rfm.groupby('Cluster').median()
print("\nCluster Medians (Original Scale):\n", cluster_medians)

cluster_sizes = rfm['Cluster'].value_counts().sort_index()
print("\nCluster Sizes:\n", cluster_sizes)

# --- Generate Customer Persona Profiles ---
def generate_persona(cluster_id, cluster_data):
    print(f"\n--- Persona for Cluster {cluster_id} ---")
    print(f"Number of customers: {len(cluster_data)}")
    print(f"Average Recency: {cluster_data['Recency'].mean():.2f} days")
    print(f"Average Frequency: {cluster_data['Frequency'].mean():.2f} purchases")
    print(f"Average Monetary: ${cluster_data['Monetary'].mean():.2f}")
    
    if cluster_id == 0:
        print("Description: This segment represents recent, frequent, and high-spending customers. They are likely your most valuable customers.")
        print("Recommendations: Implement loyalty programs, offer exclusive previews of new products, personalized recommendations, and excellent customer service to retain them.")
    elif cluster_id == 1:
        print("Description: This segment consists of customers who purchased long ago, with low frequency and monetary value. They might be at risk of churning.")
        print("Recommendations: Send re-engagement campaigns, special discounts to encourage repeat purchases, and surveys to understand their needs.")
    elif cluster_id == 2:
        print("Description: This segment includes highly frequent and high-spending customers, but their recency might vary. These are your 'Whales' or 'VIPs'.")
        print("Recommendations: Provide dedicated account managers, exclusive high-value offers, and solicit feedback for product development. Ensure they feel valued.")
    else:
        print("Description: General customer segment. Further analysis might be needed to refine this segment.")
        print("Recommendations: Standard marketing campaigns, focus on increasing frequency and monetary value through promotions.")

for cluster_id in sorted(rfm['Cluster'].unique()):
    cluster_data = rfm[rfm["Cluster"] == cluster_id]
    generate_persona(cluster_id, cluster_data)

# --- Visualize Cluster Characteristics (Box Plots) ---
plt.figure(figsize=(18, 6))

plt.subplot(1, 3, 1)
sns.boxplot(x='Cluster', y='Recency', data=rfm)
plt.title('Recency by Cluster')

plt.subplot(1, 3, 2)
sns.boxplot(x='Cluster', y='Frequency', data=rfm)
plt.title('Frequency by Cluster')

plt.subplot(1, 3, 3)
sns.boxplot(x='Cluster', y='Monetary', data=rfm)
plt.title('Monetary by Cluster')

plt.tight_layout()
plt.savefig('cluster_characteristics_boxplot.png')
print("\nCluster characteristics box plots saved to cluster_characteristics_boxplot.png")

# --- Statistical Significance Testing (Example: ANOVA for Monetary value across clusters) ---
from scipy.stats import f_oneway

# Extract monetary values for each cluster
monetary_by_cluster = [rfm[rfm['Cluster'] == i]["Monetary"] for i in sorted(rfm['Cluster'].unique())]

# Perform ANOVA test
f_statistic, p_value = f_oneway(*monetary_by_cluster)

print(f"\nANOVA Test for Monetary Value Across Clusters:")
print(f"F-statistic: {f_statistic:.2f}")
print(f"P-value: {p_value:.4f}")

if p_value < 0.05:
    print("Conclusion: There is a statistically significant difference in Monetary value across the clusters.")
else:
    print("Conclusion: There is no statistically significant difference in Monetary value across the clusters.")


