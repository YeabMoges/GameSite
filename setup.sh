#!/bin/bash

# Define project metadata (optional)
PROJECT_NAME="GameSite"
PROJECT_DESCRIPTION="A Flask-based game site project."
PROJECT_VERSION="1.0"

echo "Starting $PROJECT_NAME Setup - Version $PROJECT_VERSION"
echo "$PROJECT_DESCRIPTION"
echo "--------------------------------------"

# Step 1: Check and Install Python
echo "Checking if Python is installed..."
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Installing..."
    sudo apt update
    sudo apt install -y python3 python3-venv python3-pip
    echo "Python3 installed successfully."
else
    echo "Python3 is already installed."
fi

# Step 2: Create a virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists. Skipping creation."
fi

# Step 3: Activate the virtual environment and install dependencies
echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "Dependencies installed successfully."
else
    echo "Failed to install dependencies. Please check your requirements.txt."
    exit 1
fi

# Step 4: Run the Flask application
echo "Running the Flask application..."
python app.py
