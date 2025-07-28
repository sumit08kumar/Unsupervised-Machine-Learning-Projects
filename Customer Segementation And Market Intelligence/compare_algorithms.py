import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler

# Load the dataset
data = pd.read_csv("KDD2014_donors_10feat_nomissing_normalised.csv")

# Assuming the last column is the 'class' label and should not be used for training
X = data.iloc[:, :-1]
y_true = data.iloc[:, -1] # True labels for evaluation (if available)

# Standardize the data (important for distance-based methods like LOF)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --- Isolation Forest ---
print("\n--- Isolation Forest ---")
if_model = IsolationForest(random_state=42, contamination=0.01)
if_model.fit(X_scaled)
if_scores = if_model.decision_function(X_scaled)
if_predictions = if_model.predict(X_scaled)

# Convert predictions to 0 for inliers and 1 for outliers for ROC AUC
if_binary_predictions = [1 if p == -1 else 0 for p in if_predictions]

# Evaluate Isolation Forest (if true labels are available)
if len(y_true.unique()) > 1: # Check if y_true contains both normal and anomaly classes
    if_roc_auc = roc_auc_score(y_true, -if_scores) # -if_scores because higher scores are inliers
    print(f"Isolation Forest ROC AUC: {if_roc_auc:.4f}")
else:
    print("True anomaly labels not available for ROC AUC evaluation.")

# --- Local Outlier Factor (LOF) ---
print("\n--- Local Outlier Factor (LOF) ---")
# LOF does not have a 'fit' method like Isolation Forest for unsupervised learning
# It calculates anomaly scores for the training data itself
lof_model = LocalOutlierFactor(n_neighbors=20, contamination=0.01, novelty=False) # novelty=False for unsupervised
lof_predictions = lof_model.fit_predict(X_scaled)
lof_scores = -lof_model.negative_outlier_factor_ # LOF returns negative_outlier_factor, so negate for consistency

# Convert predictions to 0 for inliers and 1 for outliers for ROC AUC
lof_binary_predictions = [1 if p == -1 else 0 for p in lof_predictions]

# Evaluate LOF (if true labels are available)
if len(y_true.unique()) > 1:
    lof_roc_auc = roc_auc_score(y_true, lof_scores)
    print(f"Local Outlier Factor ROC AUC: {lof_roc_auc:.4f}")
else:
    print("True anomaly labels not available for ROC AUC evaluation.")

print("\nComparison Complete.")


