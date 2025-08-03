#!/bin/bash
# Script to set up virtual environment and run tests for the Flask application

# Exit on error
set -e

# Define colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up test environment for Flask Demo Application...${NC}"

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

# Run the tests
echo -e "${GREEN}Running tests...${NC}"
python -m pytest tests.py -v

# Deactivate virtual environment
deactivate
echo -e "${GREEN}Tests completed. Virtual environment deactivated.${NC}"
