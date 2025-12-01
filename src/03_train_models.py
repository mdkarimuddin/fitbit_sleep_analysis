"""
Model Training for Sleep Efficiency Prediction
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
import pickle
import json
from pathlib import Path

# Directories
DATA_DIR = Path(__file__).parent.parent / 'data'
PROCESSED_DIR = DATA_DIR / 'processed'
MODEL_DIR = Path(__file__).parent.parent / 'models'
OUTPUT_DIR = Path(__file__).parent.parent / 'outputs'

MODEL_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    """Main training pipeline"""
    print("=" * 60)
    print("MODEL TRAINING")
    print("=" * 60)
    
    # Load data
    print("\nLoading features...")
    df = pd.read_csv(PROCESSED_DIR / 'features_complete.csv')
    
    # Define features (exclude targets and IDs)
    exclude_cols = ['Id', 'ActivityDate', 'SleepDay', 'TotalMinutesAsleep', 
                   'TotalTimeInBed', 'TotalSleepRecords', 'SleepEfficiency']
    
    feature_cols = [col for col in df.columns if col not in exclude_cols]
    
    X = df[feature_cols]
    y = df['SleepEfficiency']  # Primary target
    
    print(f"\nFeatures: {len(feature_cols)}")
    print(f"Samples: {len(X)}")
    
    # Split by user (prevent leakage)
    users = df['Id'].unique()
    train_users, test_users = train_test_split(users, test_size=0.2, random_state=42)
    
    train_mask = df['Id'].isin(train_users)
    test_mask = df['Id'].isin(test_users)
    
    X_train, X_test = X[train_mask], X[test_mask]
    y_train, y_test = y[train_mask], y[test_mask]
    
    print(f"\nTrain users: {len(train_users)}")
    print(f"Test users: {len(test_users)}")
    print(f"Train samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    
    # Scale features
    print("\nScaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train models
    models = {
        'Random Forest': RandomForestRegressor(
            n_estimators=200,
            max_depth=12,
            min_samples_split=10,
            random_state=42,
            n_jobs=-1
        ),
        'XGBoost': xgb.XGBRegressor(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.05,
            random_state=42,
            n_jobs=-1
        )
    }
    
    results = {}
    best_model = None
    best_score = -np.inf
    best_name = None
    
    for name, model in models.items():
        print(f"\n{'='*60}")
        print(f"Training {name}")
        print(f"{'='*60}")
        
        # Cross-validation
        print("Running cross-validation...")
        cv_scores = cross_val_score(model, X_train_scaled, y_train, 
                                     cv=5, scoring='r2', n_jobs=-1)
        print(f"CV R² = {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")
        
        # Train on full training set
        print("Training on full training set...")
        model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test_scaled)
        
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        print(f"\nTest Results:")
        print(f"  MAE:  {mae:.4f}")
        print(f"  RMSE: {rmse:.4f}")
        print(f"  R²:   {r2:.4f}")
        
        results[name] = {
            'cv_r2_mean': float(cv_scores.mean()),
            'cv_r2_std': float(cv_scores.std()),
            'test_mae': float(mae),
            'test_rmse': float(rmse),
            'test_r2': float(r2)
        }
        
        if r2 > best_score:
            best_score = r2
            best_model = model
            best_name = name
    
    print(f"\n{'='*60}")
    print(f"✅ Best Model: {best_name} (R² = {best_score:.4f})")
    print(f"{'='*60}")
    
    # Save best model
    print("\nSaving models...")
    with open(MODEL_DIR / 'best_model.pkl', 'wb') as f:
        pickle.dump(best_model, f)
    
    with open(MODEL_DIR / 'scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    with open(MODEL_DIR / 'feature_names.json', 'w') as f:
        json.dump(feature_cols, f)
    
    with open(OUTPUT_DIR / 'model_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n✅ Models saved!")
    print(f"  - Best model: {MODEL_DIR / 'best_model.pkl'}")
    print(f"  - Scaler: {MODEL_DIR / 'scaler.pkl'}")
    print(f"  - Feature names: {MODEL_DIR / 'feature_names.json'}")
    print(f"  - Results: {OUTPUT_DIR / 'model_results.json'}")

if __name__ == '__main__':
    main()

