#!/bin/sh
cat venv/pyvenv.cfg
# Activate the virtual environment
. venv/bin/activate

pip install --no-cache-dir -r requirements.txt

# Initialize the database
python init_db.py

# Start the Flask application
python app.py
