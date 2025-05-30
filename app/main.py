"""
Main entry point for running the HSK Chatbot application.

This module provides a direct way to run the application from the app directory.
"""

import uvicorn
from app import create_app

# Create the app instance for direct import
app = create_app()

def run_app():
    """Run the FastAPI application with uvicorn."""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    run_app() 