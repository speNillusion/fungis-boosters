#!/usr/bin/env python3
"""
Main script to run the plastic degradation prediction application
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Checks if dependencies are installed"""
    try:
        import streamlit
        import plotly
        import pandas
        import numpy
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def install_requirements():
    """Installs necessary dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies")
        return False

def run_streamlit_app():
    """Runs the Streamlit application"""
    print("🚀 Starting application...")
    
    # Streamlit configurations
    config_args = [
        "--server.port=8501",
        "--server.address=localhost",
        "--server.headless=false",
        "--browser.gatherUsageStats=false",
        "--theme.primaryColor=#1f77b4",
        "--theme.backgroundColor=#ffffff",
        "--theme.secondaryBackgroundColor=#f0f2f6"
    ]
    
    cmd = [sys.executable, "-m", "streamlit", "run", "dashboard_app.py"] + config_args
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 Application closed by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    """Main function"""
    print("🧪 Plastic Degradation Dashboard by Fungi")
    print("=" * 50)
    
    # Check if we're in the correct directory
    if not Path("dashboard_app.py").exists():
        print("❌ dashboard_app.py file not found in current directory")
        print("Make sure you're in the correct directory")
        return
    
    # Check dependencies
    if not check_requirements():
        print("\n📦 Installing necessary dependencies...")
        if not install_requirements():
            print("❌ Failed to install dependencies")
            return
    
    print("\n🌐 The application will open at: http://localhost:8501")
    print("💡 To stop the application, press Ctrl+C")
    print("-" * 50)
    
    # Executar aplicação
    run_streamlit_app()

if __name__ == "__main__":
    main()