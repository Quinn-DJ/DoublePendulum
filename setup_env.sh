#!/bin/bash
# The script for setting up the environment for the double pendulum project

# Getting the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONDA_ENV="${SCRIPT_DIR}/.conda"

echo "Environment Setup"
echo "=================="

# Searching for conda installation
CONDA_BASE=""
echo "Searching for conda installation..."

# Common conda installation paths
CONDA_PATHS=(
    "$HOME/miniconda3/bin/conda"
    "$HOME/anaconda3/bin/conda"
    "/opt/miniconda3/bin/conda"
    "/opt/anaconda3/bin/conda"
    "/usr/local/miniconda3/bin/conda"
    "/usr/local/anaconda3/bin/conda"
)

# Check if conda is in PATH
if command -v conda &> /dev/null; then
    CONDA_BASE=$(dirname $(dirname $(which conda)))
    echo "Found conda in PATH: $CONDA_BASE"
else
    # Search in common paths
    for conda_path in "${CONDA_PATHS[@]}"; do
        if [ -f "$conda_path" ]; then
            CONDA_BASE=$(dirname $(dirname "$conda_path"))
            echo "Found conda installation: $CONDA_BASE"
            break
        fi
    done
    
    if [ -z "$CONDA_BASE" ]; then
        echo "Error: Conda installation not found."
        echo "Please install Miniconda or Anaconda."
        exit 1
    fi
fi

# Check and create environment
if [ ! -d "$CONDA_ENV" ]; then
    echo "Local conda environment not found, creating..."
    echo "Environment path: $CONDA_ENV"

    # Initialize conda
    source "$CONDA_BASE/etc/profile.d/conda.sh"

    # Create a new conda environment
    conda create --prefix "$CONDA_ENV" python=3.9 -y
    
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create conda environment"
        exit 1
    fi

    echo "Environment created successfully"
else
    echo "Found existing environment: $CONDA_ENV"
    # Initialize conda for later use
    source "$CONDA_BASE/etc/profile.d/conda.sh"
fi

# Check and install dependencies
echo "Checking Python dependencies..."
# Use conda run to execute commands in the specified environment
conda run --prefix "$CONDA_ENV" python -c "import matplotlib, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing necessary Python packages..."
    conda install --prefix "$CONDA_ENV" matplotlib numpy -y
    
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
    echo "Dependencies installed successfully"
else
    echo "All dependencies are already installed"
fi

# Display environment information
echo ""
echo "Environment Information"
echo "========"
echo "Conda Location: $CONDA_BASE"
echo "Environment Path: $CONDA_ENV"
echo "Python Path: $(conda run --prefix "$CONDA_ENV" which python)"
echo "Python Version: $(conda run --prefix "$CONDA_ENV" python --version)"
echo "Available Packages:"
conda run --prefix "$CONDA_ENV" python -c "
try:
    import matplotlib
    import numpy
    print(f'  matplotlib: {matplotlib.__version__}')
    print(f'  numpy: {numpy.__version__}')
except ImportError as e:
    print(f'  Error importing packages: {e}')
"

echo ""
echo "Environment setup complete!"
