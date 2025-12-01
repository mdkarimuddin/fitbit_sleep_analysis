"""
Feature Engineering for Sleep Efficiency Prediction
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Directories
DATA_DIR = Path(__file__).parent.parent / 'data'
PROCESSED_DIR = DATA_DIR / 'processed'

def create_features(df):
    """
    Engineer features for sleep prediction
    """
    df = df.copy()
    df = df.sort_values(['Id', 'ActivityDate'])
    
    print("Creating features...")
    
    # 1. Basic calculations
    df['ActiveMinutesTotal'] = (df['VeryActiveMinutes'] + 
                                 df['FairlyActiveMinutes'] + 
                                 df['LightlyActiveMinutes'])
    
    df['IntenseActivityRatio'] = df['VeryActiveMinutes'] / (df['ActiveMinutesTotal'] + 1)
    df['SedentaryHours'] = df['SedentaryMinutes'] / 60
    df['StepsPerKm'] = df['TotalSteps'] / (df['TotalDistance'] + 0.1)
    
    # 2. Lagged features (previous days)
    lag_features = ['TotalSteps', 'Calories', 'ActiveMinutesTotal', 
                   'SleepEfficiency', 'TotalMinutesAsleep']
    
    for feature in lag_features:
        for lag in [1, 2, 3]:
            df[f'{feature}_lag{lag}'] = df.groupby('Id')[feature].shift(lag)
    
    # 3. Rolling averages (trends)
    rolling_features = ['TotalSteps', 'Calories', 'ActiveMinutesTotal']
    
    for feature in rolling_features:
        for window in [3, 7]:
            df[f'{feature}_rolling{window}d'] = df.groupby('Id')[feature].transform(
                lambda x: x.rolling(window, min_periods=1).mean()
            )
    
    # 4. User baselines (personalization)
    user_baselines = df.groupby('Id').agg({
        'TotalSteps': 'mean',
        'Calories': 'mean',
        'ActiveMinutesTotal': 'mean',
        'SleepEfficiency': 'mean'
    }).add_suffix('_user_avg')
    
    df = df.merge(user_baselines, left_on='Id', right_index=True)
    
    # 5. Deviations from baseline
    df['Steps_deviation'] = (df['TotalSteps'] - df['TotalSteps_user_avg']) / (df['TotalSteps_user_avg'] + 1)
    df['Calories_deviation'] = (df['Calories'] - df['Calories_user_avg']) / (df['Calories_user_avg'] + 1)
    df['Activity_deviation'] = (df['ActiveMinutesTotal'] - df['ActiveMinutesTotal_user_avg']) / (df['ActiveMinutesTotal_user_avg'] + 1)
    
    # 6. Sleep debt (cumulative)
    df['SleepDebt'] = df.groupby('Id')['TotalMinutesAsleep'].transform(
        lambda x: (x - x.mean()).cumsum()
    )
    
    # 7. Activity intensity score
    df['ActivityIntensityScore'] = (
        df['VeryActiveMinutes'] * 3 + 
        df['FairlyActiveMinutes'] * 2 + 
        df['LightlyActiveMinutes'] * 1
    )
    
    # 8. Temporal features
    df['DayOfWeek'] = df['ActivityDate'].dt.dayofweek
    df['IsWeekend'] = (df['DayOfWeek'] >= 5).astype(int)
    df['DayOfMonth'] = df['ActivityDate'].dt.day
    
    # Cyclical encoding
    df['DayOfWeek_sin'] = np.sin(2 * np.pi * df['DayOfWeek'] / 7)
    df['DayOfWeek_cos'] = np.cos(2 * np.pi * df['DayOfWeek'] / 7)
    
    # 9. Training load (acute vs chronic)
    df['AcuteLoad'] = df['ActiveMinutesTotal_rolling3d']
    df['ChronicLoad'] = df['ActiveMinutesTotal_rolling7d']
    df['TrainingStrain'] = df['AcuteLoad'] / (df['ChronicLoad'] + 1)
    
    # 10. Recovery indicators
    df['DaysSinceRest'] = df.groupby('Id').apply(
        lambda x: (x['ActiveMinutesTotal'] < 30).cumsum() - 
                  (x['ActiveMinutesTotal'] < 30).cumsum().where(x['ActiveMinutesTotal'] >= 30).ffill().fillna(0)
    ).reset_index(level=0, drop=True)
    
    print(f"Created {df.shape[1]} features")
    
    return df

def main():
    """Main feature engineering pipeline"""
    print("=" * 60)
    print("FEATURE ENGINEERING")
    print("=" * 60)
    
    # Load data
    print("\nLoading merged data...")
    df = pd.read_csv(PROCESSED_DIR / 'merged_activity_sleep.csv')
    df['ActivityDate'] = pd.to_datetime(df['ActivityDate'])
    print(f"Loaded {len(df)} records")
    
    # Create features
    df_features = create_features(df)
    
    # Remove rows with NaN (from lagging)
    initial_len = len(df_features)
    df_features = df_features.dropna()
    print(f"\nRemoved {initial_len - len(df_features)} rows with NaN (from lagging)")
    
    print(f"\nFinal dataset shape: {df_features.shape}")
    print(f"Samples: {len(df_features)}")
    print(f"Features: {df_features.shape[1]}")
    
    # Save
    df_features.to_csv(PROCESSED_DIR / 'features_complete.csv', index=False)
    print(f"\n✅ Features saved to: {PROCESSED_DIR / 'features_complete.csv'}")

if __name__ == '__main__':
    main()

