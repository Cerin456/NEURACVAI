#!/bin/bash

# NEURACV Setup Script

echo "Setting up NEURACV..."

# Create necessary directories
mkdir -p templates static/css static/images data utils tests

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Set up environment variables
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOL
OPENAI_API_KEY=your_openai_api_key_here
DEBUG=True
EOL
    echo "Please update .env with your actual API keys"
fi

echo "Setup complete! Run with: streamlit run app.py"