#!/bin/bash

export OPENAI_API_KEY=$1
export chat_history_count=$2
echo "The server will start in a few minutes. Stay relaxed."

# Start virtual-environment
alias venv="python3 -m venv .venv && source $PWD/.venv/bin/activate"
venv

# Install dependency
pip install -r requirements.txt -q

# Start Chat Application
chmod +x ./app.py
./app.py
