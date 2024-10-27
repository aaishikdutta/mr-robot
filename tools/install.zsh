#!/bin/zsh

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

# Source the copilot script for the current session
info "Adding the copilot widget for the current session..."

if [ -z "$ZSH_VERSION" ]
then
    error "The copilot widget requires Zsh and couldn't be installed." >&2
else
    zsh -c tools/copilot.zsh || error "Failed to load the copilot widget script."
    
    # Add the Zsh widget to .zshrc if not already present
    ZSHRC="$HOME/.zshrc"
    WIDGET_CODE="source $(pwd)/tools/copilot.zsh"

    if ! grep -q "$WIDGET_CODE" "$ZSHRC"; then
        echo "$WIDGET_CODE" >> "$ZSHRC"
        info "The copilot widget has been added to your .zshrc. Restart your terminal or run 'source ~/.zshrc' to use it across sessions."
    else
        info "Zsh widget is already set up in .zshrc."
    fi
fi
info "The copilot widget has been added to this Zsh session. Now you can use CTRL + K to convert natural language command queries into executable shell commands."
info "Please add the OPENAI API key by setting the 'OPENAI_API_KEY' environment variable"


info "Setup complete!"
