# Next Steps - Download FitBit Dataset

## Current Status
- ✅ Project structure created
- ✅ All Python scripts ready
- ✅ Pipeline script ready
- ⚠️  Kaggle credentials need to be set up
- ⏳ Dataset download pending

## Option 1: Set Up Kaggle Credentials (Recommended)

### Step 1: Get Kaggle API Token
1. Go to https://www.kaggle.com/settings
2. Scroll to "API" section
3. Click "Create New API Token"
4. This downloads `kaggle.json` to your local machine

### Step 2: Upload to Puhti
```bash
# From your local machine
scp ~/Downloads/kaggle.json username@puhti.csc.fi:~/.kaggle/
```

### Step 3: Set Permissions
```bash
# On Puhti
chmod 600 ~/.kaggle/kaggle.json
```

### Step 4: Download Dataset
```bash
cd /scratch/project_2010726/senior_data_scientis_Oura/oura_fitbit_analysis
module load python-data/3.12-25.09
kaggle datasets download -d arashnic/fitbit -p data/raw/
unzip data/raw/fitbit.zip -d data/raw/
```

## Option 2: Use Environment Variables

If you prefer not to upload files:

```bash
export KAGGLE_USERNAME="your_kaggle_username"
export KAGGLE_KEY="your_kaggle_api_key"
```

Then run:
```bash
./download_data.sh
```

## Option 3: Manual Download

1. Visit: https://www.kaggle.com/datasets/arashnic/fitbit
2. Click "Download" (requires Kaggle account login)
3. Upload `fitbit.zip` to Puhti:
   ```bash
   scp fitbit.zip username@puhti.csc.fi:/scratch/project_2010726/senior_data_scientis_Oura/oura_fitbit_analysis/data/raw/
   ```
4. Extract:
   ```bash
   cd /scratch/project_2010726/senior_data_scientis_Oura/oura_fitbit_analysis
   unzip data/raw/fitbit.zip -d data/raw/
   ```

## After Download

Once the dataset is downloaded, verify files:
```bash
ls -lh data/raw/*.csv
```

You should see files like:
- `dailyActivity_merged.csv`
- `sleepDay_merged.csv`
- `heartrate_seconds_merged.csv`
- etc.

Then run the pipeline:
```bash
sbatch run_pipeline.sh
```

## Quick Test

To test if credentials work:
```bash
module load python-data/3.12-25.09
kaggle datasets list --max-size 1000
```

If this works, credentials are set up correctly!

