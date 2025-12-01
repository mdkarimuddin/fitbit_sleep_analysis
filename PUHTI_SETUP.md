# Puhti Setup Guide for FitBit Analysis

## ✅ Available Resources

### Python Modules
- **python-data/3.10-22.09** (recommended)
- **python-data/3.10-24.04** (newer)
- **python-data/3.12-25.09** (latest, default)

### ML Modules (if needed)
- **pytorch/2.4** through **pytorch/2.7** (default)
- **tensorflow/2.8** through **tensorflow/2.18** (default)

### SLURM Partitions
- **small**: 3 days time limit, suitable for this project
- **large**: 3 days time limit, for larger jobs

### Tools Available
- ✅ **Kaggle CLI**: `/appl/soft/ai/tykky/python-data-2025-09/bin/kaggle`
- ✅ **Internet access**: Available for downloading datasets
- ✅ **wget/curl**: Available for downloads
- ✅ **Disk space**: 17TB available on `/scratch`

## 📋 Setup Steps

### 1. Load Python Module
```bash
module load python-data/3.10-22.09
# or
module load python-data/3.12-25.09  # Latest
```

### 2. Check Available Packages
```bash
python3 -c "import pandas, numpy, matplotlib, seaborn, sklearn; print('Core packages OK')"
```

### 3. Install Missing Packages (if needed)
```bash
# Install to user directory
pip install --user xgboost shap
```

### 4. Setup Kaggle API (for dataset download)

**Option A: If you have kaggle.json file**
```bash
mkdir -p ~/.kaggle
# Upload your kaggle.json to ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

**Option B: Set environment variables**
```bash
export KAGGLE_USERNAME="your_username"
export KAGGLE_KEY="your_api_key"
```

### 5. Download FitBit Dataset
```bash
cd /scratch/project_2010726/senior_data_scientis_Oura/oura_fitbit_analysis

# Using Kaggle CLI
kaggle datasets download -d arashnic/fitbit

# Or if kaggle command not found, use full path
/appl/soft/ai/tykky/python-data-2025-09/bin/kaggle datasets download -d arashnic/fitbit

# Extract
unzip fitbit.zip -d data/raw/
```

### 6. Run Pipeline
```bash
# Submit job
sbatch run_pipeline.sh

# Or run interactively (for testing)
module load python-data/3.10-22.09
python src/01_eda.py
```

## 🔍 Verify Setup

```bash
# Check Python
which python3
python3 --version

# Check packages
python3 -c "import pandas; print(pandas.__version__)"
python3 -c "import xgboost; print(xgboost.__version__)"  # May need installation

# Check Kaggle
which kaggle
kaggle datasets list  # Should work if credentials are set
```

## ⚠️ Troubleshooting

### Kaggle Not Found
- Use full path: `/appl/soft/ai/tykky/python-data-2025-09/bin/kaggle`
- Or install: `pip install --user kaggle`

### Missing Packages
- Install to user: `pip install --user package_name`
- Check module: `module spider python-data`

### Internet Issues
- Download dataset manually on local machine
- Upload to Puhti via `scp` or Puhti web interface

## 📊 Recommended Configuration

For this project:
- **Module**: `python-data/3.10-22.09` or `3.12-25.09`
- **Partition**: `small` (sufficient for this project)
- **Time**: 2 hours should be enough
- **Memory**: 8GB (default in script)
- **CPUs**: 4 (default in script)

## 🚀 Quick Start

```bash
cd /scratch/project_2010726/senior_data_scientis_Oura/oura_fitbit_analysis

# Load module
module load python-data/3.12-25.09

# Install missing packages
pip install --user xgboost shap

# Download data (if Kaggle credentials set)
kaggle datasets download -d arashnic/fitbit
unzip fitbit.zip -d data/raw/

# Run pipeline
sbatch run_pipeline.sh
```

