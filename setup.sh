#!/bin/bash

# Define project metadata
PROJECT_NAME="GameSite"
PROJECT_DESCRIPTION="A Flask-based game site project."
PROJECT_VERSION="1.0"

echo "Starting $PROJECT_NAME Setup - Version $PROJECT_VERSION"
echo "$PROJECT_DESCRIPTION"
echo "--------------------------------------"

# Step 1: Install Python 3.11 and required modules
echo "Installing Python 3.11 and required modules..."
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-distutils
echo "Python 3.11 and required modules installed successfully."

# Step 2: Create a virtual environment using Python 3.11
if [ -d "venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf venv
fi

echo "Creating virtual environment with Python 3.11..."
python3.11 -m venv venv
if [ $? -eq 0 ]; then
    echo "Virtual environment created successfully."
else
    echo "Failed to create virtual environment. Exiting."
    exit 1
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
