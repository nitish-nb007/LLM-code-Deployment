@echo off
echo 🚀 Starting LLM Deployment API in production mode...
gunicorn -c gunicorn_config.py app:app
pause