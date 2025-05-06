#!/bin/bash

# Start Redis
echo "Starting Redis Server..."
redis-server &

# Start FastAPI Server
echo "Starting FastAPI..."
uvicorn app:app --reload &

# Start Celery Worker
echo "Starting Celery Worker..."
celery -A tasks worker --loglevel=info &

# Start Streamlit Dashboard
echo "Starting Streamlit Dashboard..."
streamlit run dashboard.py &
