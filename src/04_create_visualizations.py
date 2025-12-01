"""
Create Visualizations for Model Results
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for Puhti
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import json
from pathlib import Path

# Try to import shap (optional)
try:
    import shap
    HAS_SHAP = True
except ImportError:
    HAS_SHAP = False
    print("⚠️  SHAP not available, skipping SHAP visualizations")

from sklearn.metrics import mean_absolute_error, r2_score

# Directories
DATA_DIR = Path(__file__).parent.parent / 'data'
PROCESSED_DIR = DATA_DIR / 'processed'
MODEL_DIR = Path(__file__).parent.parent / 'models'
OUTPUT_DIR = Path(__file__).parent.parent / 'outputs'

def main():
    """Main visualization pipeline"""
    print("=" * 60)
    print("CREATING VISUALIZATIONS")
    print("=" * 60)
    
    # Load everything
    print("\nLoading data and models...")
    df = pd.read_csv(PROCESSED_DIR / 'features_complete.csv')
    
    with open(MODEL_DIR / 'best_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    with open(MODEL_DIR / 'scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    
    with open(MODEL_DIR / 'feature_names.json', 'r') as f:
        feature_names = json.load(f)
    
    # Prepare test data
    users = df['Id'].unique()
    np.random.seed(42)
    test_users = np.random.choice(users, size=int(0.2*len(users)), replace=False)
    test_mask = df['Id'].isin(test_users)
    
    X_test = df[test_mask][feature_names]
    y_test = df[test_mask]['SleepEfficiency']
    X_test_scaled = scaler.transform(X_test)
    
    y_pred = model.predict(X_test_scaled)
    
    # 1. Feature Importance
    print("\n1. Creating feature importance plot...")
    if hasattr(model, 'feature_importances_'):
        importance = model.feature_importances_
        indices = np.argsort(importance)[-20:]  # Top 20
        
        plt.figure(figsize=(10, 8))
        plt.barh(range(20), importance[indices])
        plt.yticks(range(20), [feature_names[i] for i in indices])
        plt.xlabel('Feature Importance')
        plt.title('Top 20 Most Important Features for Sleep Efficiency Prediction')
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / 'feature_importance.png', dpi=300)
        plt.close()
        print("✅ Saved: feature_importance.png")
    
    # 2. Predictions vs Actual
    print("\n2. Creating predictions vs actual plot...")
    plt.figure(figsize=(8, 8))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 
             'r--', lw=2, label='Perfect Prediction')
    plt.xlabel('Actual Sleep Efficiency')
    plt.ylabel('Predicted Sleep Efficiency')
    plt.title(f'Sleep Efficiency Prediction\nR² = {r2_score(y_test, y_pred):.3f}, MAE = {mean_absolute_error(y_test, y_pred):.3f}')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'predictions_vs_actual.png', dpi=300)
    plt.close()
    print("✅ Saved: predictions_vs_actual.png")
    
    # 3. Error distribution
    print("\n3. Creating error distribution plot...")
    errors = y_test - y_pred
    plt.figure(figsize=(10, 6))
    plt.hist(errors, bins=30, edgecolor='black', alpha=0.7)
    plt.axvline(0, color='red', linestyle='--', linewidth=2)
    plt.xlabel('Prediction Error')
    plt.ylabel('Frequency')
    plt.title(f'Prediction Error Distribution\nMean Error: {errors.mean():.4f}')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'error_distribution.png', dpi=300)
    plt.close()
    print("✅ Saved: error_distribution.png")
    
    # 4. SHAP analysis (if available)
    if HAS_SHAP:
        print("\n4. Computing SHAP values...")
        try:
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_test_scaled[:100])  # Sample for speed
            
            plt.figure(figsize=(10, 8))
            shap.summary_plot(shap_values, X_test_scaled[:100], feature_names=feature_names, show=False)
            plt.tight_layout()
            plt.savefig(OUTPUT_DIR / 'shap_summary.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("✅ Saved: shap_summary.png")
        except Exception as e:
            print(f"⚠️  SHAP visualization failed: {e}")
    else:
        print("\n4. Skipping SHAP analysis (not available)")
    
    # 5. Time series predictions for sample users
    print("\n5. Creating user time series predictions...")
    sample_users = test_users[:3]
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    
    for idx, user in enumerate(sample_users):
        user_data = df[df['Id'] == user].sort_values('ActivityDate')
        
        X_user = user_data[feature_names]
        X_user_scaled = scaler.transform(X_user)
        y_user_true = user_data['SleepEfficiency']
        y_user_pred = model.predict(X_user_scaled)
        
        ax = axes[idx]
        ax.plot(range(len(y_user_true)), y_user_true, 'o-', label='Actual', alpha=0.7)
        ax.plot(range(len(y_user_pred)), y_user_pred, 's-', label='Predicted', alpha=0.7)
        ax.fill_between(range(len(y_user_true)), y_user_true, y_user_pred, alpha=0.2)
        
        ax.set_xlabel('Day')
        ax.set_ylabel('Sleep Efficiency')
        ax.set_title(f'User {user}: Actual vs Predicted Sleep Efficiency')
        ax.legend()
        ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'user_predictions.png', dpi=300)
    plt.close()
    print("✅ Saved: user_predictions.png")
    
    print("\n" + "=" * 60)
    print("✅ All visualizations created!")
    print(f"Saved to: {OUTPUT_DIR}")
    print("=" * 60)

if __name__ == '__main__':
    main()

