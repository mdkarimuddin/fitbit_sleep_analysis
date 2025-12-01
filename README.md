# Sleep Efficiency Prediction from FitBit Data

Predicting sleep efficiency from daily activity patterns using real wearable device data - demonstrating ML capabilities for health technology applications like Oura Ring.

## 🎯 Project Overview

This project analyzes FitBit fitness tracker data to predict sleep efficiency from daytime activity patterns. Built to showcase capabilities relevant to **wearable health technology companies** like Oura, Whoop, and Fitbit.

### Key Features

- ✅ **Real wearable data** from FitBit users
- ✅ **Comprehensive feature engineering** (50+ features including lags, rolling averages, baselines)
- ✅ **User-based train/test split** (prevents data leakage)
- ✅ **Explainable AI** (SHAP analysis)
- ✅ **Production-ready** code structure

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Download FitBit dataset from Kaggle
kaggle datasets download -d arashnic/fitbit
unzip fitbit.zip -d data/raw/

# Run EDA
jupyter notebook notebooks/01_EDA.ipynb

# Create features
python src/feature_engineering.py

# Train models
python src/train_models.py

# Generate visualizations
python src/create_visualizations.py
```

## 🗂️ Project Structure

```
oura_fitbit_analysis/
├── data/
│   ├── raw/                    # FitBit CSV files
│   └── processed/              # Cleaned & feature-engineered data
├── notebooks/
│   └── 01_EDA.ipynb           # Exploratory analysis
├── src/
│   ├── feature_engineering.py  # Feature creation
│   ├── train_models.py        # Model training
│   └── create_visualizations.py # Results visualization
├── models/                     # Trained models
├── outputs/                    # Plots and results
├── requirements.txt
└── README.md
```

## 📊 Results

(Will be updated after training)

## 🔬 Methodology

### Data
- **Source:** FitBit Fitness Tracker Data (Kaggle)
- **Metrics:** Steps, distance, calories, active minutes, sleep duration, sleep efficiency

### Feature Engineering
1. **Lagged features** (1, 2, 3 days prior)
2. **Rolling averages** (3-day and 7-day windows)
3. **User baselines** (personalization)
4. **Deviations from baseline** (activity/rest indicators)
5. **Training load** (acute vs chronic workload)
6. **Temporal features** (day of week, weekend)
7. **Sleep debt** (cumulative sleep deviation)

### Model
- **Algorithm:** XGBoost Regressor
- **Validation:** 5-fold cross-validation
- **Train/Test:** User-based split (80/20) to prevent leakage
- **Metrics:** R², MAE, RMSE

## 💡 Relevance to Oura Ring

This project demonstrates:

✅ **Real wearable data processing** (FitBit → generalizable to Oura)  
✅ **Time-series feature engineering** (multi-day patterns, trends)  
✅ **Personalization** (user baselines and adaptations)  
✅ **Predictive modeling** (forecasting sleep from activity)  
✅ **Explainable AI** (SHAP for interpretability)  
✅ **Production mindset** (proper validation, no data leakage)

## 🛠️ Technologies

- Python 3.8+
- pandas, numpy (data processing)
- scikit-learn (ML, preprocessing)
- XGBoost (modeling)
- SHAP (explainability)
- matplotlib, seaborn (visualization)
- Jupyter (analysis)

## 👤 Author

**Karim Uddin**  
PhD Veterinary Medicine | MEng Big Data Analytics  
Postdoctoral Researcher, University of Helsinki

## 📜 License

MIT License

## 🙏 Acknowledgments

- Data: FitBit Fitness Tracker Data via Kaggle
- Inspired by Oura Ring's approach to sleep tracking
- Built on Puhti supercomputer (CSC Finland)

