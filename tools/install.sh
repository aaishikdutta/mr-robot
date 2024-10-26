#!/bin/sh

set -e

# Function to display messages
info() {
    echo "\033[1;34m$1\033[0m"  # Display messages in blue
}

# Function to handle errors
error() {
    echo "\033[1;31mError: $1\033[0m"  # Display error messages in red
    exit 1
}

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null 
then
    error "Python 3 is not installed. Please install Python 3 and try again."
fi

# Clone the repository
info "Cloning the repository..."
git clone https://github.com/aaishikdutta/mr-robot.git || error "Failed to clone the repository."

cd mr-robot || error "Failed to change directory to mr-robot."

# Create and activate a virtual environment
info "Creating a virtual environment..."
python3 -m venv venv || error "Failed to create virtual environment."

source venv/bin/activate || error "Failed to activate the virtual environment."

# Install the required libraries
info "Installing required libraries..."
pip install -e . || error "Failed to install required libraries."

read -p "Please enter your OpenAI API Key: " OPENAI_API_KEY

mr-robot
