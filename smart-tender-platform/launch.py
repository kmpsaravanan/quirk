#!/usr/bin/env python3
"""
Simple launcher script for Smart Tender Management Platform
"""
import subprocess
import sys
import os

def main():
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Try to run streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"], check=True)
    except subprocess.CalledProcessError:
        print("Error: Streamlit not found. Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--user", "streamlit", "pandas", "plotly", "requests"], check=True)
        print("Dependencies installed. Please run again.")
    except KeyboardInterrupt:
        print("\nApp stopped.")

if __name__ == "__main__":
    main()

