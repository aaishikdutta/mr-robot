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

read -p "Please enter your OpenAI API Key: " OPENAI_API_KEY
export OPENAI_API_KEY

# Inform the user about the environment variable
info "The OpenAI API Key has been set as an environment variable."

# Disclaimer about the API key
info "Disclaimer: The OpenAI API Key is now set as an environment variable. Please note that this variable is ephemeral and attached to the current session. If you close this terminal or start a new session, you will need to set the API key again."

info "To persist the OpenAI API Key across sessions, add the following line to your shell configuration file (e.g., .bashrc, .bash_profile, or .zshrc):"
info "export OPENAI_API_KEY='your_api_key_here'"

# Source the copilot script for the current session
info "Adding the copilot widget for the current session..."

if [ -z "$ZSH_VERSION" ]
then
    error "The copilot widget requires Zsh and couldn't be installed." >&2
else
    zsh -c tools/copilot.zsh || error "Failed to load the copilot widget script."
    info "The copilot widget has been added to this Zsh session. Now you can use CTRL + K to convert natural language command queries into executable shell commands."
    
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

info "Setup complete!"
