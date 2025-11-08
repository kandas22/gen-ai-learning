#!/bin/bash
# Run Streamlit with Twilio credentials
# Usage: ./run_streamlit.sh

# Change to script directory
cd "$(dirname "$0")"

# Load environment variables
if [ -f .env.sh ]; then
    source .env.sh
fi

# Activate virtual environment if it exists
if [ -d .venv ]; then
    source .venv/bin/activate
fi

# Run Streamlit
streamlit run src/kavihealthcare.py
