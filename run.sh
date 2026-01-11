#!/bin/bash

ENV_NAME="mario_bike"
REQ_FILE="requirements.txt"

if ! command -v conda &> /dev/null; then
    echo "Conda not found. Please install Miniconda or Anaconda first."
    exit 1
fi

if ! conda info --envs | grep -q "$ENV_NAME"; then
    echo "env '$ENV_NAME' not found. Creating it now..."
    conda create -n "$ENV_NAME" python=3.14 -y
fi

source $(conda info --base)/etc/profile.d/conda.sh
conda activate "$ENV_NAME"

pip install -r "$REQ_FILE"

echo "Starting MarioBike64"
python main.py
