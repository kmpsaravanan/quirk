# Setup Instructions - Smart Tender Management Platform

## Quick Fix for Running the App

### Option 1: Install Dependencies (Recommended)

Open Terminal and run:

```bash
cd /Users/psaravanan/Downloads/JSNewDesign/quirk
python3 -m pip install --user streamlit pandas plotly requests
```

Then run:
```bash
python3 -m streamlit run app.py
```

### Option 2: Use Python Virtual Environment

```bash
cd /Users/psaravanan/Downloads/JSNewDesign/quirk
python3 -m venv venv
source venv/bin/activate
pip install streamlit pandas plotly requests
streamlit run app.py
```

### Option 3: Check Python Path

If you get "No module named streamlit", try:

```bash
# Find where Python packages are installed
python3 -m pip show streamlit

# Add to PATH if needed
export PATH="$HOME/Library/Python/3.8/bin:$PATH"
python3 -m streamlit run app.py
```

## Troubleshooting

1. **If streamlit command not found:**
   - Use: `python3 -m streamlit run app.py` instead of just `streamlit run app.py`

2. **If port 8501 is busy:**
   - Use different port: `python3 -m streamlit run app.py --server.port 8502`

3. **If permission errors:**
   - Use `--user` flag: `pip install --user streamlit`

## Expected Output

When running successfully, you should see:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

Then open http://localhost:8501 in your browser.

