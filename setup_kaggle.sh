#!/bin/bash
# Setup script for Kaggle credentials

echo "=== Kaggle Credentials Setup ==="
echo ""

# Check if credentials already exist
if [ -f ~/.kaggle/kaggle.json ]; then
    echo "✅ Kaggle credentials already exist at ~/.kaggle/kaggle.json"
    chmod 600 ~/.kaggle/kaggle.json
    exit 0
fi

# Check environment variables
if [ -n "$KAGGLE_USERNAME" ] && [ -n "$KAGGLE_KEY" ]; then
    echo "✅ Kaggle credentials found in environment variables"
    exit 0
fi

echo "❌ No Kaggle credentials found."
echo ""
echo "To set up Kaggle:"
echo ""
echo "OPTION 1: Upload kaggle.json file"
echo "  1. Go to https://www.kaggle.com/settings"
echo "  2. Click 'Create New API Token'"
echo "  3. Download kaggle.json"
echo "  4. Upload to Puhti:"
echo "     scp kaggle.json username@puhti.csc.fi:~/.kaggle/"
echo "  5. Then run: chmod 600 ~/.kaggle/kaggle.json"
echo ""
echo "OPTION 2: Set environment variables"
echo "  export KAGGLE_USERNAME='your_username'"
echo "  export KAGGLE_KEY='your_api_key'"
echo ""
echo "After setup, you can download the dataset with:"
echo "  kaggle datasets download -d arashnic/fitbit -p data/raw/"

