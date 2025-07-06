#!/bin/bash

# Kill all tmux sessions
tmux kill-server

cd ~/pe-portfolio || exit 1

git fetch && git reset origin/main --hard

source python3-virtualenv/bin/activate

pip install -r requirements.txt

# Start a new detached tmux session running the Flask server
tmux new-session -d -s flask "cd ~/pe-portfolio && source python3-virtualenv/bin/activate && export FLASK_ENV=development && flask run --host=0.0.0.0"
