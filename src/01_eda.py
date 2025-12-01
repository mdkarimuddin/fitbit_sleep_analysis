"""
Exploratory Data Analysis for FitBit Sleep Efficiency Prediction
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for Puhti
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Directories
DATA_DIR = Path(__file__).parent.parent / 'data'
RAW_DIR = DATA_DIR / 'raw'
PROCESSED_DIR = DATA_DIR / 'processed'
OUTPUT_DIR = Path(__file__).parent.parent / 'outputs'

# Create directories
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_data():
    """Load FitBit datasets"""
    print("=== Loading Data ===")
    
    # Load main datasets
    daily_activity = pd.read_csv(RAW_DIR / 'dailyActivity_merged.csv')
    
    # Try to load sleep data - check for different possible filenames
    sleep_data = None
    if (RAW_DIR / 'sleepDay_merged.csv').exists():
        sleep_data = pd.read_csv(RAW_DIR / 'sleepDay_merged.csv')
    elif (RAW_DIR / 'minuteSleep_merged.csv').exists():
        # If only minute-level sleep data, we'll aggregate it
        print("  Found minuteSleep_merged.csv - aggregating to daily level...")
        minute_sleep = pd.read_csv(RAW_DIR / 'minuteSleep_merged.csv')
        # Convert date column
        minute_sleep['date'] = pd.to_datetime(minute_sleep['date'])
        # Extract date (without time)
        minute_sleep['date_only'] = minute_sleep['date'].dt.date
        
        # Group by Id, date, and logId (each logId is a sleep session)
        # value=1 means asleep, value=2 means restless, value=3 means awake
        # Count total minutes in bed (all records) and asleep minutes (value=1)
        sleep_by_session = minute_sleep.groupby(['Id', 'date_only', 'logId']).agg({
            'value': [
                ('TotalTimeInBed', 'count'),  # Total minutes in bed (all records)
                ('TotalMinutesAsleep', lambda x: (x == 1).sum())  # Minutes actually asleep
            ]
        }).reset_index()
        sleep_by_session.columns = ['Id', 'date_only', 'logId', 'TotalTimeInBed', 'TotalMinutesAsleep']
        
        # For each day, sum all sleep sessions
        sleep_data = sleep_by_session.groupby(['Id', 'date_only']).agg({
            'TotalMinutesAsleep': 'sum',
            'TotalTimeInBed': 'sum',
            'logId': 'count'  # Number of sleep sessions
        }).reset_index()
        sleep_data.columns = ['Id', 'SleepDay', 'TotalMinutesAsleep', 'TotalTimeInBed', 'TotalSleepRecords']
        sleep_data['SleepDay'] = pd.to_datetime(sleep_data['SleepDay'])
    
    # Try to load heart rate if available
    heartrate = None
    if (RAW_DIR / 'heartrate_seconds_merged.csv').exists():
        heartrate = pd.read_csv(RAW_DIR / 'heartrate_seconds_merged.csv')
    
    print(f"Daily Activity: {daily_activity.shape}")
    if sleep_data is not None:
        print(f"Sleep Data: {sleep_data.shape}")
    else:
        print("⚠️  No sleep data found - will need to handle this")
    if heartrate is not None:
        print(f"Heart Rate: {heartrate.shape}")
    
    return daily_activity, sleep_data, heartrate

def clean_data(daily_activity, sleep_data):
    """Clean and merge datasets"""
    print("\n=== Cleaning Data ===")
    
    # Convert dates
    daily_activity['ActivityDate'] = pd.to_datetime(daily_activity['ActivityDate'])
    sleep_data['SleepDay'] = pd.to_datetime(sleep_data['SleepDay'])
    
    # Check for missing values
    print("\nMissing Values:")
    print("Daily Activity:", daily_activity.isnull().sum().sum())
    print("Sleep Data:", sleep_data.isnull().sum().sum())
    
    # Check unique users
    print(f"\nUnique users in activity: {daily_activity['Id'].nunique()}")
    print(f"Unique users in sleep: {sleep_data['Id'].nunique()}")
    
    # Merge sleep with activity
    merged_data = daily_activity.merge(
        sleep_data,
        left_on=['Id', 'ActivityDate'],
        right_on=['Id', 'SleepDay'],
        how='inner'
    )
    
    print(f"\nMerged data shape: {merged_data.shape}")
    print(f"Users with both activity and sleep data: {merged_data['Id'].nunique()}")
    
    # Calculate sleep efficiency
    merged_data['SleepEfficiency'] = merged_data['TotalMinutesAsleep'] / merged_data['TotalTimeInBed']
    
    return merged_data

def basic_statistics(merged_data):
    """Calculate basic statistics"""
    print("\n=== Basic Statistics ===")
    
    print("\nActivity Statistics:")
    print(merged_data[['TotalSteps', 'TotalDistance', 'Calories', 
                       'VeryActiveMinutes', 'FairlyActiveMinutes', 
                       'LightlyActiveMinutes', 'SedentaryMinutes']].describe())
    
    print("\nSleep Statistics:")
    print(merged_data[['TotalMinutesAsleep', 'TotalTimeInBed', 'SleepEfficiency']].describe())
    
    print(f"\nAverage Sleep Efficiency: {merged_data['SleepEfficiency'].mean():.2%}")

def plot_distributions(merged_data):
    """Create distribution plots"""
    print("\n=== Creating Distribution Plots ===")
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    
    # Steps distribution
    axes[0, 0].hist(merged_data['TotalSteps'], bins=30, edgecolor='black', alpha=0.7)
    axes[0, 0].set_title('Daily Steps Distribution')
    axes[0, 0].set_xlabel('Steps')
    axes[0, 0].axvline(merged_data['TotalSteps'].mean(), color='red', linestyle='--', 
                      label=f'Mean: {merged_data["TotalSteps"].mean():.0f}')
    axes[0, 0].legend()
    
    # Calories
    axes[0, 1].hist(merged_data['Calories'], bins=30, edgecolor='black', alpha=0.7, color='orange')
    axes[0, 1].set_title('Daily Calories Burned')
    axes[0, 1].set_xlabel('Calories')
    
    # Sleep duration
    axes[0, 2].hist(merged_data['TotalMinutesAsleep']/60, bins=30, edgecolor='black', alpha=0.7, color='purple')
    axes[0, 2].set_title('Sleep Duration (hours)')
    axes[0, 2].set_xlabel('Hours')
    axes[0, 2].axvline(merged_data['TotalMinutesAsleep'].mean()/60, color='red', linestyle='--',
                       label=f'Mean: {merged_data["TotalMinutesAsleep"].mean()/60:.1f}h')
    axes[0, 2].legend()
    
    # Sleep efficiency
    axes[1, 0].hist(merged_data['SleepEfficiency'], bins=30, edgecolor='black', alpha=0.7, color='green')
    axes[1, 0].set_title('Sleep Efficiency Distribution')
    axes[1, 0].set_xlabel('Efficiency')
    
    # Active minutes
    active_data = merged_data[['VeryActiveMinutes', 'FairlyActiveMinutes', 'LightlyActiveMinutes']].sum()
    axes[1, 1].bar(range(3), active_data.values, color=['red', 'orange', 'yellow'])
    axes[1, 1].set_xticks(range(3))
    axes[1, 1].set_xticklabels(['Very Active', 'Fairly Active', 'Lightly Active'], rotation=45)
    axes[1, 1].set_title('Total Active Minutes by Intensity')
    
    # Sedentary hours
    axes[1, 2].hist(merged_data['SedentaryMinutes']/60, bins=30, edgecolor='black', alpha=0.7, color='gray')
    axes[1, 2].set_title('Sedentary Time (hours/day)')
    axes[1, 2].set_xlabel('Hours')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'distributions.png', dpi=300)
    plt.close()
    print("✅ Saved: distributions.png")

def plot_correlations(merged_data):
    """Create correlation matrix"""
    print("\n=== Creating Correlation Matrix ===")
    
    # Select numerical columns
    numeric_cols = ['TotalSteps', 'TotalDistance', 'Calories', 
                    'VeryActiveMinutes', 'FairlyActiveMinutes', 'LightlyActiveMinutes',
                    'SedentaryMinutes', 'TotalMinutesAsleep', 'TotalTimeInBed', 'SleepEfficiency']
    
    corr_matrix = merged_data[numeric_cols].corr()
    
    # Heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title('Correlation Matrix: Activity vs Sleep', fontsize=16)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'correlation_matrix.png', dpi=300)
    plt.close()
    print("✅ Saved: correlation_matrix.png")
    
    print("\n=== Strongest Correlations with Sleep Efficiency ===")
    sleep_corrs = corr_matrix['SleepEfficiency'].sort_values(ascending=False)
    print(sleep_corrs)
    
    return sleep_corrs

def plot_activity_vs_sleep(merged_data):
    """Create scatter plots of activity vs sleep"""
    print("\n=== Creating Activity vs Sleep Plots ===")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Steps vs Sleep Efficiency
    axes[0, 0].scatter(merged_data['TotalSteps'], merged_data['SleepEfficiency'], alpha=0.5)
    axes[0, 0].set_xlabel('Total Steps')
    axes[0, 0].set_ylabel('Sleep Efficiency')
    axes[0, 0].set_title('Steps vs Sleep Efficiency')
    z = np.polyfit(merged_data['TotalSteps'], merged_data['SleepEfficiency'], 1)
    p = np.poly1d(z)
    axes[0, 0].plot(merged_data['TotalSteps'].sort_values(), 
                    p(merged_data['TotalSteps'].sort_values()), 
                    "r--", alpha=0.8, label='Trend')
    axes[0, 0].legend()
    
    # Calories vs Sleep Duration
    axes[0, 1].scatter(merged_data['Calories'], merged_data['TotalMinutesAsleep']/60, alpha=0.5, color='orange')
    axes[0, 1].set_xlabel('Calories Burned')
    axes[0, 1].set_ylabel('Sleep Duration (hours)')
    axes[0, 1].set_title('Calories vs Sleep Duration')
    
    # Active Minutes vs Sleep Efficiency
    merged_data['TotalActiveMinutes'] = (merged_data['VeryActiveMinutes'] + 
                                         merged_data['FairlyActiveMinutes'] + 
                                         merged_data['LightlyActiveMinutes'])
    axes[1, 0].scatter(merged_data['TotalActiveMinutes'], merged_data['SleepEfficiency'], 
                       alpha=0.5, color='purple')
    axes[1, 0].set_xlabel('Total Active Minutes')
    axes[1, 0].set_ylabel('Sleep Efficiency')
    axes[1, 0].set_title('Activity vs Sleep Efficiency')
    
    # Sedentary vs Sleep Efficiency
    axes[1, 1].scatter(merged_data['SedentaryMinutes']/60, merged_data['SleepEfficiency'], 
                       alpha=0.5, color='gray')
    axes[1, 1].set_xlabel('Sedentary Hours')
    axes[1, 1].set_ylabel('Sleep Efficiency')
    axes[1, 1].set_title('Sedentary Time vs Sleep Efficiency')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'activity_vs_sleep.png', dpi=300)
    plt.close()
    print("✅ Saved: activity_vs_sleep.png")
    
    return merged_data

def plot_timeseries(merged_data):
    """Create time series plots for individual users"""
    print("\n=== Creating Time Series Plots ===")
    
    # Get top 5 users by number of records
    top_users = merged_data['Id'].value_counts().head(5).index
    
    fig, axes = plt.subplots(5, 1, figsize=(14, 15))
    
    for idx, user_id in enumerate(top_users):
        user_data = merged_data[merged_data['Id'] == user_id].sort_values('ActivityDate')
        
        ax = axes[idx]
        ax2 = ax.twinx()
        
        # Plot steps
        ax.plot(user_data['ActivityDate'], user_data['TotalSteps'], 
                'o-', color='blue', label='Steps', alpha=0.7)
        
        # Plot sleep efficiency
        ax2.plot(user_data['ActivityDate'], user_data['SleepEfficiency'], 
                 's-', color='red', label='Sleep Efficiency', alpha=0.7)
        
        ax.set_xlabel('Date')
        ax.set_ylabel('Total Steps', color='blue')
        ax2.set_ylabel('Sleep Efficiency', color='red')
        ax.set_title(f'User {user_id}: Activity vs Sleep Over Time')
        ax.tick_params(axis='y', labelcolor='blue')
        ax2.tick_params(axis='y', labelcolor='red')
        ax.legend(loc='upper left')
        ax2.legend(loc='upper right')
        ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'user_timeseries.png', dpi=300)
    plt.close()
    print("✅ Saved: user_timeseries.png")

def plot_day_of_week_patterns(merged_data):
    """Create day of week pattern plots"""
    print("\n=== Creating Day of Week Patterns ===")
    
    # Add day of week
    merged_data['DayOfWeek'] = merged_data['ActivityDate'].dt.day_name()
    
    # Order days
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    merged_data['DayOfWeek'] = pd.Categorical(merged_data['DayOfWeek'], categories=day_order, ordered=True)
    
    # Group by day
    day_stats = merged_data.groupby('DayOfWeek').agg({
        'TotalSteps': 'mean',
        'Calories': 'mean',
        'TotalMinutesAsleep': 'mean',
        'SleepEfficiency': 'mean'
    }).reset_index()
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    axes[0, 0].bar(range(7), day_stats['TotalSteps'], color='blue', alpha=0.7)
    axes[0, 0].set_xticks(range(7))
    axes[0, 0].set_xticklabels(day_order, rotation=45)
    axes[0, 0].set_title('Average Steps by Day of Week')
    axes[0, 0].set_ylabel('Steps')
    
    axes[0, 1].bar(range(7), day_stats['Calories'], color='orange', alpha=0.7)
    axes[0, 1].set_xticks(range(7))
    axes[0, 1].set_xticklabels(day_order, rotation=45)
    axes[0, 1].set_title('Average Calories by Day of Week')
    
    axes[1, 0].bar(range(7), day_stats['TotalMinutesAsleep']/60, color='purple', alpha=0.7)
    axes[1, 0].set_xticks(range(7))
    axes[1, 0].set_xticklabels(day_order, rotation=45)
    axes[1, 0].set_title('Average Sleep Duration by Day of Week')
    axes[1, 0].set_ylabel('Hours')
    
    axes[1, 1].bar(range(7), day_stats['SleepEfficiency'], color='green', alpha=0.7)
    axes[1, 1].set_xticks(range(7))
    axes[1, 1].set_xticklabels(day_order, rotation=45)
    axes[1, 1].set_title('Average Sleep Efficiency by Day of Week')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'day_of_week_patterns.png', dpi=300)
    plt.close()
    print("✅ Saved: day_of_week_patterns.png")
    
    return merged_data

def main():
    """Main EDA pipeline"""
    print("=" * 60)
    print("FITBIT DATA EXPLORATORY DATA ANALYSIS")
    print("=" * 60)
    
    # Load data
    daily_activity, sleep_data, heartrate = load_data()
    
    # Clean and merge
    merged_data = clean_data(daily_activity, sleep_data)
    
    # Basic statistics
    basic_statistics(merged_data)
    
    # Visualizations
    plot_distributions(merged_data)
    sleep_corrs = plot_correlations(merged_data)
    merged_data = plot_activity_vs_sleep(merged_data)
    plot_timeseries(merged_data)
    merged_data = plot_day_of_week_patterns(merged_data)
    
    # Save cleaned data
    merged_data.to_csv(PROCESSED_DIR / 'merged_activity_sleep.csv', index=False)
    print(f"\n✅ Processed data saved to: {PROCESSED_DIR / 'merged_activity_sleep.csv'}")
    
    # Summary
    print("\n" + "=" * 60)
    print("=== KEY FINDINGS ===")
    print(f"1. Average daily steps: {merged_data['TotalSteps'].mean():.0f}")
    print(f"2. Average sleep duration: {merged_data['TotalMinutesAsleep'].mean()/60:.2f} hours")
    print(f"3. Average sleep efficiency: {merged_data['SleepEfficiency'].mean():.2%}")
    if len(sleep_corrs) > 1:
        print(f"4. Strongest predictor of sleep efficiency: {sleep_corrs.index[1]} ({sleep_corrs.values[1]:.3f})")
    print(f"5. Number of users analyzed: {merged_data['Id'].nunique()}")
    print(f"6. Number of days analyzed: {(merged_data['ActivityDate'].max() - merged_data['ActivityDate'].min()).days}")
    print("=" * 60)
    print("\n✅ EDA Complete!")
    print(f"Visualizations saved to: {OUTPUT_DIR}")

if __name__ == '__main__':
    main()

