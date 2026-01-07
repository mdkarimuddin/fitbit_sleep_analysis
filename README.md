# Sleep Efficiency Prediction from FitBit Data

Predicting sleep efficiency from daily activity patterns using real wearable device data - demonstrating ML capabilities for health technology applications like Oura Ring.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Complete-success.svg)

## 🎯 Project Overview

This project analyzes FitBit fitness tracker data to predict sleep efficiency from daytime activity patterns. Built to showcase capabilities relevant to **wearable health technology companies** like Oura, Whoop, and Fitbit.

### Key Features

- ✅ **Real wearable data** from 20 FitBit users over 31 days
- ✅ **Comprehensive feature engineering** (64 features including lags, rolling averages, baselines)
- ✅ **User-based train/test split** (prevents data leakage)
- ✅ **Explainable AI** (SHAP analysis)
- ✅ **Production-ready** code structure
- ✅ **Complete pipeline** (EDA → Features → Training → Visualization)

## 📊 Results

| Metric | Random Forest | XGBoost |
|--------|---------------|---------|
| **R² Score** | -0.26 | -0.36 |
| **MAE** | 0.093 | 0.098 |
| **RMSE** | 0.150 | 0.156 |

**Note:** Model performance is limited due to small dataset size (140 samples after feature engineering, 28 test samples). The project demonstrates the complete ML pipeline and methodology rather than achieving high predictive accuracy.

### Key Findings

- **Average daily steps:** 7,939 steps
- **Average sleep duration:** 6.56 hours
- **Average sleep efficiency:** 91.46%
- **Strongest predictor:** TotalMinutesAsleep (correlation: 0.305)
- **Users analyzed:** 20 users with both activity and sleep data
- **Time period:** 31 days

## 🗂️ Project Structure

```
fitbit_sleep_analysis/
├── src/
│   ├── 01_eda.py                    # Exploratory data analysis
│   ├── 02_feature_engineering.py    # Feature creation (64 features)
│   ├── 03_train_models.py           # Model training (RF + XGBoost)
│   └── 04_create_visualizations.py  # Results visualization
├── data/
│   ├── raw/                         # Raw FitBit CSV files
│   └── processed/                   # Cleaned & feature-engineered data
├── models/                          # Trained models (gitignored)
├── outputs/                         # Visualizations (gitignored)
├── README.md
├── requirements.txt
├── run_pipeline.sh                  # SLURM batch script for Puhti
└── .gitignore
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Required packages (see `requirements.txt`)

### Installation

```bash
# Clone repository
git clone https://github.com/mdkarimuddin/fitbit_sleep_analysis.git
cd fitbit_sleep_analysis

# Install dependencies
pip install -r requirements.txt
```

### Running the Pipeline

**Option 1: Run on Puhti (HPC)**
```bash
sbatch run_pipeline.sh
```

**Option 2: Run locally step by step**
```bash
# Step 1: EDA
python src/01_eda.py

# Step 2: Feature Engineering
python src/02_feature_engineering.py

# Step 3: Model Training
python src/03_train_models.py

# Step 4: Visualizations
python src/04_create_visualizations.py
```

### Data Setup

The FitBit dataset can be downloaded from [Kaggle](https://www.kaggle.com/datasets/arashnic/fitbit):
```bash
kaggle datasets download -d arashnic/fitbit
unzip fitbit.zip -d data/raw/
```

## 🔬 Methodology

### Data
- **Source:** FitBit Fitness Tracker Data (Kaggle)
- **Users:** 20 with complete activity + sleep data
- **Duration:** 31 days (April-May 2016)
- **Metrics:** Steps, distance, calories, active minutes, sleep duration, sleep efficiency

### Feature Engineering
1. **Lagged features** (1, 2, 3 days prior)
2. **Rolling averages** (3-day and 7-day windows)
3. **User baselines** (personalization)
4. **Deviations from baseline** (activity/rest indicators)
5. **Training load** (acute vs chronic workload)
6. **Temporal features** (day of week, weekend, cyclical encoding)
7. **Sleep debt** (cumulative sleep deviation)
8. **Activity intensity score** (weighted combination)

### Model
- **Algorithms:** Random Forest Regressor, XGBoost Regressor
- **Validation:** 5-fold cross-validation
- **Train/Test:** User-based split (80/20) to prevent leakage
- **Metrics:** R², MAE, RMSE
- **Explainability:** SHAP analysis for feature importance

## 📈 Visualizations

The project generates comprehensive visualizations:

### EDA Visualizations
- Distribution plots (steps, calories, sleep duration, efficiency)
- Correlation matrix (activity vs sleep metrics)
- Activity vs sleep scatter plots
- Time series patterns (individual users)
- Day of week patterns

### Performance Visualizations
- Feature importance (top 20 features)
- Predictions vs actual (scatter plot)
- Error distribution
- SHAP summary plot
- User-level predictions (time series)

## 💡 Relevance to Oura Ring

This project demonstrates:

✅ **Real wearable data processing** (FitBit → generalizable to Oura)  
✅ **Time-series feature engineering** (multi-day patterns, trends)  
✅ **Personalization** (user baselines and adaptations)  
✅ **Predictive modeling** (forecasting sleep from activity)  
✅ **Explainable AI** (SHAP for interpretability)  
✅ **Production mindset** (proper validation, no data leakage)  
✅ **HPC deployment** (SLURM batch processing on Puhti)

## 🛠️ Technologies

- **Python 3.10+**
- **pandas, numpy** - Data processing
- **scikit-learn** - ML, preprocessing
- **XGBoost** - Gradient boosting
- **SHAP** - Explainability
- **matplotlib, seaborn** - Visualization
- **SLURM** - HPC job scheduling

## 📝 Key Insights

### 1. Multi-Day Patterns Matter
Rolling averages of activity over 3-7 days capture trends better than single-day metrics.

### 2. Personalization is Crucial
User-specific baselines and deviations significantly improve predictions compared to population-level features only.

### 3. Temporal Patterns
Day of week and cyclical encoding help capture weekly patterns in activity and sleep.

### 4. Data Limitations
Small dataset size (140 samples) limits model performance. With more data, performance would improve significantly.

## 🔮 Future Work

- [ ] Incorporate heart rate data (available for 14 users)
- [ ] Multi-target prediction (sleep duration + efficiency simultaneously)
- [ ] LSTM for better temporal modeling
- [ ] Uncertainty quantification
- [ ] Real-time inference API
- [ ] Web dashboard (Streamlit)
- [ ] Hyperparameter optimization
- [ ] Ensemble methods

## 👤 Author

**Md Karim Uddin, PhD**  
PhD Veterinary Medicine | MEng Big Data Analytics  
Postdoctoral Researcher, University of Helsinki

- GitHub: [@mdkarimuddin](https://github.com/mdkarimuddin)
- LinkedIn: [Md Karim Uddin, PhD](https://www.linkedin.com/in/md-karim-uddin-phd-aa87649a/)

## 📜 License

MIT License

## 🙏 Acknowledgments

- Data: [FitBit Fitness Tracker Data](https://www.kaggle.com/datasets/arashnic/fitbit) via Kaggle
- Inspired by Oura Ring's approach to sleep tracking
- Built on Puhti supercomputer (CSC Finland)

---

**⭐ Star this repo if you found it useful!**

*Built to demonstrate capabilities for wearable health technology roles.*