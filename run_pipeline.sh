#!/bin/bash
#SBATCH --job-name=fitbit_analysis
#SBATCH --account=project_2010726
#SBATCH --partition=small
#SBATCH --time=02:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G

# Initialize Lmod
if [ -f /usr/share/lmod/lmod/init/bash ]; then
    source /usr/share/lmod/lmod/init/bash
elif [ -f /appl/lmod/lmod/init/bash ]; then
    source /appl/lmod/lmod/init/bash
fi

# Set MODULEPATH if not set
if [ -z "$MODULEPATH" ]; then
    if [ -d /appl/modulefiles ]; then
        export MODULEPATH=/appl/modulefiles
    fi
fi

# Load required modules
echo "Loading modules..."
if command -v module &> /dev/null; then
    module purge
    module load python-data/3.10-22.09 2>&1 || module load python-data 2>&1
    echo "✅ python-data module loaded"
else
    echo "❌ Module command not available"
    exit 1
fi
echo ""

# Find Python
if [ -f /appl/soft/ai/python-data/3.10-22.09/bin/python3 ]; then
    PYTHON_CMD=/appl/soft/ai/python-data/3.10-22.09/bin/python3
else
    PYTHON_CMD=$(which python3)
fi

echo "Using Python: $PYTHON_CMD"
$PYTHON_CMD --version
echo ""

# Set matplotlib backend
export MPLBACKEND=Agg

# Change to project directory
cd /scratch/project_2010726/senior_data_scientis_Oura/oura_fitbit_analysis

# Install packages if needed
echo "Checking/installing packages..."
$PYTHON_CMD -m pip install --user --quiet shap 2>&1 | grep -v "already satisfied" || true
# Note: pandas, numpy, matplotlib, seaborn, sklearn, xgboost should be in python-data module
echo ""

# Run pipeline
echo "=" * 60
echo "RUNNING FITBIT ANALYSIS PIPELINE"
echo "=" * 60
echo ""

echo "Step 1: EDA"
$PYTHON_CMD -u src/01_eda.py
echo ""

echo "Step 2: Feature Engineering"
$PYTHON_CMD -u src/02_feature_engineering.py
echo ""

echo "Step 3: Model Training"
$PYTHON_CMD -u src/03_train_models.py
echo ""

echo "Step 4: Visualizations"
$PYTHON_CMD -u src/04_create_visualizations.py
echo ""

echo "=" * 60
echo "✅ PIPELINE COMPLETE!"
echo "=" * 60
echo ""
echo "Results saved to:"
echo "  - Models: models/"
echo "  - Visualizations: outputs/"
echo "  - Processed data: data/processed/"

