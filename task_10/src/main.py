import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Ensure absolute path resolution so imports work regardless of the execution directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import custom modules (No scikit-learn allowed)
import data_utils
import metrics
import baselines
from linear_regression_gd import LinearRegressionGD
from logistic_regression_gd import LogisticRegressionGD
from kmeans import KMeans

def generate_markdown_templates(output_dir: str):
    """Generates the required markdown files with the exact rubric questions as templates."""
    model_comp_path = os.path.join(output_dir, "model_comparison.md")
    if not os.path.exists(model_comp_path):
        with open(model_comp_path, "w") as f:
            f.write("# Model Comparison\n\n")
            f.write("1. State the regression target and explain why it is a valid continuous prediction task.\n\n")
            f.write("2. Compare regression model performance against the regression baseline.\n\n")
            f.write("3. State the classification target and explain how the class label was created.\n\n")
            f.write("4. Compare classification model performance against the majority-class baseline.\n\n")
            f.write("5. Explain which classification errors are more serious and why.\n\n")
            f.write("6. State the clustering features used and explain why labels were not used during clustering.\n\n")
            f.write("7. Explain whether the clusters appear meaningful or artificial.\n\n")
            f.write("8. Identify possible data leakage risks in the implementation.\n\n")
            f.write("9. State whether the dataset is ready for stronger ML models and justify the answer.\n")

    error_analysis_path = os.path.join(output_dir, "error_analysis.md")
    if not os.path.exists(error_analysis_path):
        with open(error_analysis_path, "w") as f:
            f.write("# Error Analysis\n\n")
            f.write("1. List examples where the regression model made large errors and explain possible reasons.\n\n")
            f.write("2. List examples where the classifier made wrong predictions and explain possible reasons.\n\n")
            f.write("3. Explain whether the classification task appears balanced or imbalanced.\n\n")
            f.write("4. Explain whether the clustering result aligns with any meaningful pattern in the data.\n\n")
            f.write("5. Mention at least three limitations of the current baseline models.\n")

def main():
    # ---------------------------------------------------------
    # System Setup & Data Loading
    # ---------------------------------------------------------
    if len(sys.argv) < 3:
        print("Error: Missing arguments.")
        print("Usage: python task_10/src/main.py <input_csv_path> <output_dir_path>")
        sys.exit(1)

    csv_path = sys.argv[1]
    output_dir = sys.argv[2]
    
    os.makedirs(output_dir, exist_ok=True)
    generate_markdown_templates(output_dir)

    print(f"[*] Output directory secured at: {output_dir}")
    print("[*] Loading and cleaning raw dataset...")
    
    raw_df = data_utils.load_data(csv_path)
    df = data_utils.clean_dataset(raw_df)

    # =========================================================
    # TASK 1: REGRESSION
    # =========================================================
    print("\n--- Starting Regression Pipeline ---")
    X_reg, y_reg = data_utils.prepare_regression_dataset(df)
    
    # Split
    (X_r_train, X_r_val, X_r_test, 
     y_r_train, y_r_val, y_r_test) = data_utils.train_validation_test_split(X_reg, y_reg)
    
    # Standardize (Strictly using train params to prevent Data Leakage)
    print("[*] Scaling regression features...")
    mean_r, std_r = data_utils.compute_standardization_parameters(X_r_train)
    X_r_train_scaled = data_utils.apply_standardization(X_r_train, mean_r, std_r)
    X_r_test_scaled = data_utils.apply_standardization(X_r_test, mean_r, std_r)
    
    # Train Predictors
    print("[*] Training Regression Baseline and Linear Regression (GD)...")
    reg_baseline = baselines.RegressionBaseline()
    reg_baseline.fit(y_r_train)
    y_r_base_pred = reg_baseline.predict(X_r_test_scaled)
    
    reg_model = LinearRegressionGD(learning_rate=0.01, iterations=1500)
    reg_model.fit(X_r_train_scaled, y_r_train)
    y_r_model_pred = reg_model.predict(X_r_test_scaled)
    
    # Save Metrics
    reg_metrics = {
        "Baseline": {
            "MAE": metrics.mae(y_r_test, y_r_base_pred),
            "MSE": metrics.mse(y_r_test, y_r_base_pred),
            "RMSE": metrics.rmse(y_r_test, y_r_base_pred),
            "R2": metrics.r2_score(y_r_test, y_r_base_pred)
        },
        "Model": {
            "MAE": metrics.mae(y_r_test, y_r_model_pred),
            "MSE": metrics.mse(y_r_test, y_r_model_pred),
            "RMSE": metrics.rmse(y_r_test, y_r_model_pred),
            "R2": metrics.r2_score(y_r_test, y_r_model_pred)
        }
    }
    with open(os.path.join(output_dir, "regression_metrics.json"), "w") as f:
        json.dump(reg_metrics, f, indent=4)
        
    pd.DataFrame({
        "Actual": y_r_test,
        "Baseline_Predicted": y_r_base_pred,
        "Model_Predicted": y_r_model_pred
    }).to_csv(os.path.join(output_dir, "regression_predictions.csv"), index=False)
    
    # Regression Plots
    plt.figure(figsize=(8, 5))
    plt.plot(reg_model.loss_history_, color='#1f77b4', linewidth=2)
    plt.title("Linear Regression: MSE Loss over Iterations", fontsize=14)
    plt.xlabel("Iterations", fontsize=12)
    plt.ylabel("Mean Squared Error (MSE)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "regression_loss_curve.png"), dpi=300)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.scatter(y_r_test, y_r_model_pred, alpha=0.5, color='#9467bd', edgecolor='k')
    min_val, max_val = min(y_r_test.min(), y_r_model_pred.min()), max(y_r_test.max(), y_r_model_pred.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label="Perfect Prediction")
    plt.title("Regression: Actual vs. Predicted Target", fontsize=14)
    plt.xlabel("Actual CO(GT)", fontsize=12)
    plt.ylabel("Predicted CO(GT)", fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "actual_vs_predicted.png"), dpi=300)
    plt.close()

    # =========================================================
    # TASK 2: CLASSIFICATION
    # =========================================================
    print("\n--- Starting Classification Pipeline ---")
    X_cls, y_cls = data_utils.prepare_classification_dataset(df)
    
    (X_c_train, X_c_val, X_c_test, 
     y_c_train, y_c_val, y_c_test) = data_utils.train_validation_test_split(X_cls, y_cls)
    
    print("[*] Scaling classification features...")
    mean_c, std_c = data_utils.compute_standardization_parameters(X_c_train)
    X_c_train_scaled = data_utils.apply_standardization(X_c_train, mean_c, std_c)
    X_c_test_scaled = data_utils.apply_standardization(X_c_test, mean_c, std_c)
    
    print("[*] Training Classification Baseline and Logistic Regression (GD)...")
    cls_baseline = baselines.ClassificationBaseline()
    cls_baseline.fit(y_c_train)
    y_c_base_pred = cls_baseline.predict(X_c_test_scaled)
    
    cls_model = LogisticRegressionGD(learning_rate=0.1, iterations=1500, threshold=0.5)
    cls_model.fit(X_c_train_scaled, y_c_train)
    y_c_model_pred = cls_model.predict(X_c_test_scaled)
    
    # Save Metrics
    cls_metrics = {
        "Baseline": {
            "Accuracy": metrics.accuracy(y_c_test, y_c_base_pred),
            "Precision": metrics.precision(y_c_test, y_c_base_pred),
            "Recall": metrics.recall(y_c_test, y_c_base_pred),
            "F1_Score": metrics.f1_score(y_c_test, y_c_base_pred),
            "Confusion_Matrix": metrics.confusion_matrix(y_c_test, y_c_base_pred).tolist()
        },
        "Model": {
            "Accuracy": metrics.accuracy(y_c_test, y_c_model_pred),
            "Precision": metrics.precision(y_c_test, y_c_model_pred),
            "Recall": metrics.recall(y_c_test, y_c_model_pred),
            "F1_Score": metrics.f1_score(y_c_test, y_c_model_pred),
            "Confusion_Matrix": metrics.confusion_matrix(y_c_test, y_c_model_pred).tolist()
        }
    }
    with open(os.path.join(output_dir, "classification_metrics.json"), "w") as f:
        json.dump(cls_metrics, f, indent=4)
        
    pd.DataFrame({
        "Actual": y_c_test,
        "Baseline_Predicted": y_c_base_pred,
        "Model_Predicted": y_c_model_pred
    }).to_csv(os.path.join(output_dir, "classification_predictions.csv"), index=False)
    
    # Classification Plots
    plt.figure(figsize=(8, 5))
    plt.plot(cls_model.loss_history_, color='#ff7f0e', linewidth=2)
    plt.title("Logistic Regression: Log Loss over Iterations", fontsize=14)
    plt.xlabel("Iterations", fontsize=12)
    plt.ylabel("Binary Cross-Entropy Loss", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "classification_loss_curve.png"), dpi=300)
    plt.close()

    cm = metrics.confusion_matrix(y_c_test, y_c_model_pred)
    fig, ax = plt.subplots(figsize=(6, 5))
    cax = ax.matshow(cm, cmap='Blues')
    plt.title("Confusion Matrix (Logistic Regression)", pad=20, fontsize=14)
    fig.colorbar(cax)
    ax.set_xticklabels([''] + ['Predicted 0', 'Predicted 1'])
    ax.set_yticklabels([''] + ['Actual 0', 'Actual 1'])
    for (i, j), val in np.ndenumerate(cm):
        ax.text(j, i, f'{val}', ha='center', va='center', color='red', fontsize=14, weight='bold')
    plt.savefig(os.path.join(output_dir, "confusion_matrix.png"), dpi=300)
    plt.close()

    # =========================================================
    # TASK 3: CLUSTERING
    # =========================================================
    print("\n--- Starting Unsupervised Clustering Pipeline ---")
    X_clu = data_utils.prepare_clustering_dataset(df)
    
    print("[*] Standardizing global dataset for distance-based KMeans...")
    mean_clu = np.mean(X_clu, axis=0)
    std_clu = np.std(X_clu, axis=0)
    std_clu = np.where(std_clu == 0, 1.0, std_clu)
    X_clu_scaled = (X_clu - mean_clu) / std_clu
    
    print("[*] Training KMeans model from scratch...")
    kmeans_model = KMeans(n_clusters=3, max_iterations=300, random_seed=42)
    kmeans_model.fit(X_clu_scaled)
    labels = kmeans_model.labels_
    centroids = kmeans_model.centroids_
    
    # Safe Subsampling for Silhouette Score to maintain fast performance
    rng = np.random.default_rng(42)
    if X_clu_scaled.shape[0] > 1000:
        subset_idx = rng.choice(X_clu_scaled.shape[0], 1000, replace=False)
        sil_score = metrics.silhouette_score(X_clu_scaled[subset_idx], labels[subset_idx])
    else:
        sil_score = metrics.silhouette_score(X_clu_scaled, labels)

    clu_metrics = {
        "Inertia": metrics.inertia(X_clu_scaled, labels, centroids),
        "Cluster_Counts": metrics.cluster_counts(labels),
        "Silhouette_Score_Subset": sil_score
    }
    with open(os.path.join(output_dir, "clustering_metrics.json"), "w") as f:
        json.dump(clu_metrics, f, indent=4)
        
    clu_df = pd.DataFrame(X_clu, columns=data_utils.CLUSTERING_FEATURES)
    clu_df["Cluster_Assignment"] = labels
    clu_df.to_csv(os.path.join(output_dir, "clustering_assignments.csv"), index=False)
    
    # Clustering Visualization (Features 1 and 2)
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(X_clu_scaled[:, 0], X_clu_scaled[:, 1], c=labels, cmap='viridis', alpha=0.6, edgecolor='k', s=25)
    plt.scatter(centroids[:, 0], centroids[:, 1], c='red', marker='X', s=250, edgecolor='black', linewidth=2, label='Centroids')
    plt.title("KMeans Clustering Plot (k=3)", fontsize=14)
    plt.xlabel(f"{data_utils.CLUSTERING_FEATURES[0]} (Scaled)", fontsize=12)
    plt.ylabel(f"{data_utils.CLUSTERING_FEATURES[1]} (Scaled)", fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "clustering_plot.png"), dpi=300)
    plt.close()

    print("\n[✔] Workflow Complete! All outputs generated seamlessly.")
    print(f"[✔] Check the '{output_dir}' directory for your JSON metrics, CSVs, and PNG plots.")

if __name__ == "__main__":
    main()