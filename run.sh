#!/bin/bash
# Script to set up virtual environment, install dependencies, and run the Flask application

# Exit on error
set -e

# Define colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up Flask Demo Application...${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    FRESH_INSTALL=true
else
    echo -e "${YELLOW}Virtual environment already exists.${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies if fresh install or if requested
if [ "$FRESH_INSTALL" = true ] || [ "$1" = "--reinstall" ]; then
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# Run the application
echo -e "${GREEN}Starting Flask application...${NC}"
echo -e "${GREEN}Access the application at http://localhost:5001${NC}"
python app.py

# Note: The virtual environment will be deactivated when the script exits
# but we don't explicitly deactivate it here because the script terminates
# when the Flask app is stopped with Ctrl+C
