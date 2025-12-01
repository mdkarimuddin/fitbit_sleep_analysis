#!/bin/bash
# Download FitBit dataset - handles multiple methods

cd /scratch/project_2010726/senior_data_scientis_Oura/oura_fitbit_analysis
mkdir -p data/raw

echo "=== Downloading FitBit Dataset ==="
echo ""

# Method 1: Try Kaggle CLI (if credentials are set)
if [ -f ~/.kaggle/kaggle.json ] || ([ -n "$KAGGLE_USERNAME" ] && [ -n "$KAGGLE_KEY" ]); then
    echo "Attempting download via Kaggle CLI..."
    module load python-data/3.12-25.09 2>&1
    
    if /appl/soft/ai/tykky/python-data-2025-09/bin/kaggle datasets download -d arashnic/fitbit -p data/raw/ 2>&1; then
        echo "✅ Download successful via Kaggle!"
        if [ -f data/raw/fitbit.zip ]; then
            echo "Extracting..."
            unzip -q data/raw/fitbit.zip -d data/raw/
            rm data/raw/fitbit.zip
            echo "✅ Extraction complete!"
            exit 0
        fi
    else
        echo "⚠️  Kaggle download failed, trying alternative..."
    fi
fi

# Method 2: Direct download (if dataset is publicly accessible)
echo "Attempting direct download..."
if wget -q --show-progress -O data/raw/fitbit.zip "https://www.kaggle.com/datasets/arashnic/fitbit/download" 2>&1; then
    echo "✅ Download successful!"
    unzip -q data/raw/fitbit.zip -d data/raw/
    rm data/raw/fitbit.zip
    echo "✅ Extraction complete!"
    exit 0
fi

# Method 3: Instructions
echo ""
echo "❌ Automatic download failed."
echo ""
echo "Please download manually:"
echo "  1. Go to: https://www.kaggle.com/datasets/arashnic/fitbit"
echo "  2. Click 'Download' (requires Kaggle account)"
echo "  3. Upload fitbit.zip to: data/raw/"
echo "  4. Run: unzip data/raw/fitbit.zip -d data/raw/"
echo ""
echo "OR set up Kaggle credentials:"
echo "  - Upload kaggle.json to ~/.kaggle/"
echo "  - Or set: export KAGGLE_USERNAME='...' and export KAGGLE_KEY='...'"
echo "  - Then re-run this script"

