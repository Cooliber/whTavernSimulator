#!/usr/bin/env python3
"""
Startup script for Warhammer Fantasy Tavern Simulator FastAPI Server
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'websockets',
        'crewai',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing required packages: {missing_packages}")
        logger.info("Install them with: pip install -r requirements_crewai.txt")
        return False
    
    return True

def check_environment():
    """Check environment variables"""
    required_env_vars = ['groq_api_key', 'Cerebras_api']
    missing_vars = []
    
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {missing_vars}")
        logger.info("The server will use mock LLMs for missing API keys")
    
    return True

def start_server():
    """Start the FastAPI server"""
    try:
        logger.info("🏰 Starting Warhammer Fantasy Tavern Simulator API Server...")
        
        # Check dependencies
        if not check_dependencies():
            return False
        
        # Check environment
        check_environment()
        
        # Start server
        cmd = [
            sys.executable, "-m", "uvicorn",
            "api.fastapi_server:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload",
            "--log-level", "info"
        ]
        
        logger.info("Starting server with command: " + " ".join(cmd))
        logger.info("Server will be available at: http://localhost:8000")
        logger.info("API documentation at: http://localhost:8000/docs")
        logger.info("WebSocket endpoint at: ws://localhost:8000/ws")
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = start_server()
    sys.exit(0 if success else 1)
