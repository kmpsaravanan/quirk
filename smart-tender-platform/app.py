import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import time

# Page Configuration
st.set_page_config(
    page_title="Smart Tender Management Platform",
    page_icon="✓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide ALL Streamlit UI elements
hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important; display: none !important;}
    header {visibility: hidden !important; display: none !important;}
    .stDeployButton {display: none !important;}
    div[data-testid="stToolbar"] {visibility: hidden !important; display: none !important;}
    .stApp > header {display: none !important;}
    .stApp [data-testid="stHeader"] {display: none !important;}
    .stApp [data-testid="stToolbar"] {display: none !important;}
    .stApp [data-testid="stDecoration"] {display: none !important;}
    pre, code, .stCodeBlock {display: none !important; visibility: hidden !important;}
    .stApp {overflow-x: hidden !important; padding: 0 !important; margin: 0 !important; background: #ffffff !important;}
    main {padding: 0 !important; margin: 0 !important; background: #ffffff !important;}
    .block-container {padding: 0 !important; max-width: 100% !important; background: #ffffff !important;}
    [data-testid="stAppViewContainer"] {background: #ffffff !important;}
</style>
<script>
    setTimeout(function() {
        document.querySelectorAll('pre, code, .stCodeBlock').forEach(el => {
            el.style.display = 'none';
            el.style.visibility = 'hidden';
        });
    }, 100);
</script>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# JioSign EXACT CSS Match - White background, Blue header
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    html, body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background: #ffffff !important;
        color: #1a1a1a;
        overflow-x: hidden;
    }
    
    .stApp { 
        background: #ffffff !important; 
        padding: 0 !important; 
        margin: 0 !important;
    }
    
    /* Header - EXACT JioSign Blue */
    .main-header {
        background: #0066CC !important;
        padding: 0;
        position: sticky;
        top: 0;
        z-index: 1000;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        width: 100%;
    }
    
    .header-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 16px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 12px;
        text-decoration: none;
    }
    
    .logo-circle {
        width: 40px;
        height: 40px;
        background: #00A651;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 20px;
        font-weight: 700;
        flex-shrink: 0;
    }
    
    .logo-text {
        font-size: 24px;
        font-weight: 700;
        color: white !important;
        letter-spacing: -0.5px;
    }
    
    .nav-menu {
        display: flex;
        align-items: center;
        gap: 32px;
        list-style: none;
        margin: 0;
        padding: 0;
    }
    
    .nav-link {
        color: white !important;
        text-decoration: none;
        font-size: 15px;
        font-weight: 500;
        padding: 8px 0;
        transition: opacity 0.2s;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    
    .nav-link:hover { opacity: 0.8; }
    
    .header-actions {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .btn-signup {
        background: #00A651;
        color: white;
        padding: 10px 24px;
        border-radius: 6px;
        font-size: 15px;
        font-weight: 600;
        text-decoration: none;
        display: inline-block;
        border: none;
        cursor: pointer;
    }
    
    .btn-signin {
        background: #0066CC;
        color: white;
        padding: 10px 24px;
        border-radius: 6px;
        font-size: 15px;
        font-weight: 600;
        text-decoration: none;
        display: inline-block;
        border: none;
        cursor: pointer;
    }
    
    .btn-signin:hover {
        background: #0052A3;
    }
    
    /* Hero Section - White Background */
    .hero-section {
        max-width: 1400px;
        margin: 0 auto;
        padding: 80px 24px 100px;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 80px;
        align-items: center;
        background: #ffffff !important;
    }
    
    .hero-title {
        font-size: 56px;
        font-weight: 800;
        line-height: 1.1;
        color: #1a1a1a;
        margin-bottom: 24px;
        letter-spacing: -1.5px;
    }
    
    .hero-subtitle {
        font-size: 20px;
        font-weight: 400;
        color: #666666;
        line-height: 1.6;
        max-width: 540px;
        margin-bottom: 32px;
    }
    
    /* Partners - Light Gray Background */
    .partners-section {
        background: #f8f9fa;
        padding: 60px 24px;
        width: 100%;
    }
    
    .partners-container {
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .partners-title {
        text-align: center;
        font-size: 14px;
        font-weight: 600;
        color: #666666;
        margin-bottom: 40px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .partners-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 40px;
        align-items: center;
        justify-items: center;
    }
    
    .partner-logo {
        font-size: 18px;
        font-weight: 600;
        color: #666;
        opacity: 0.6;
        transition: opacity 0.3s;
    }
    
    .partner-logo:hover { opacity: 1; color: #1a1a1a; }
    
    /* Dashboard - White Background */
    .dashboard-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 80px 24px;
        background: #ffffff !important;
    }
    
    .section-title {
        font-size: 36px;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 48px;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 24px;
        margin-bottom: 64px;
    }
    
    .stat-card {
        background: white;
        border: 1px solid #e5e5e5;
        border-radius: 12px;
        padding: 32px;
        text-align: center;
        transition: all 0.3s;
    }
    
    .stat-card:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        transform: translateY(-4px);
        border-color: #0066CC;
    }
    
    .stat-number {
        font-size: 48px;
        font-weight: 800;
        color: #0066CC;
        margin-bottom: 8px;
    }
    
    .stat-label {
        font-size: 16px;
        color: #666666;
        font-weight: 500;
    }
    
    .tender-card {
        background: white;
        border: 1px solid #e5e5e5;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 16px;
        transition: all 0.3s;
    }
    
    .tender-card:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        border-color: #0066CC;
        transform: translateY(-2px);
    }
    
    .tender-title {
        font-size: 20px;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 8px;
    }
    
    .tender-id {
        font-size: 14px;
        color: #666666;
        margin-bottom: 16px;
    }
    
    .match-score {
        background: #00A651;
        color: white;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 16px;
    }
    
    .tender-details {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin-bottom: 16px;
    }
    
    .detail-label {
        font-size: 12px;
        color: #999999;
        text-transform: uppercase;
        margin-bottom: 4px;
        font-weight: 600;
    }
    
    .detail-value {
        font-size: 16px;
        color: #1a1a1a;
        font-weight: 500;
    }
    
    .content-card {
        background: white;
        border: 1px solid #e5e5e5;
        border-radius: 12px;
        padding: 32px;
        margin-bottom: 24px;
    }
    
    .card-title {
        font-size: 24px;
        font-weight: 600;
        color: #1a1a1a !important;
        margin-bottom: 16px;
    }
    
    /* Professional Text Styling */
    p, li, span, div {
        color: #333333 !important;
        font-size: 16px;
        line-height: 1.6;
    }
    
    strong {
        color: #1a1a1a !important;
        font-weight: 600;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #1a1a1a !important;
        font-weight: 700;
    }
    
    /* Tabs Styling - Professional */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8f9fa;
        padding: 8px;
        border-radius: 8px;
        margin-bottom: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: #666666 !important;
        font-weight: 500;
        font-size: 15px;
        padding: 12px 24px;
        border-radius: 6px;
        transition: all 0.3s;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #0066CC !important;
        color: white !important;
        font-weight: 600;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e5e5e5 !important;
        color: #1a1a1a !important;
    }
    
    .stTabs [aria-selected="true"]:hover {
        background-color: #0052A3 !important;
        color: white !important;
    }
    
    /* Streamlit Info/Success/Warning/Error Boxes - Professional */
    .stAlert {
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 16px;
        border-left: 4px solid;
    }
    
    .element-container [data-testid="stAlert"] {
        border-radius: 8px;
    }
    
    div[data-testid="stAlert"] {
        border-radius: 8px !important;
        padding: 16px 20px !important;
    }
    
    /* Info Box */
    div[data-testid="stAlert"]:has(> div > div[class*="alert-info"]) {
        background-color: #E3F2FD !important;
        border-left-color: #2196F3 !important;
        color: #1565C0 !important;
    }
    
    /* Success Box */
    div[data-testid="stAlert"]:has(> div > div[class*="alert-success"]) {
        background-color: #E8F5E9 !important;
        border-left-color: #4CAF50 !important;
        color: #2E7D32 !important;
    }
    
    /* Warning Box */
    div[data-testid="stAlert"]:has(> div > div[class*="alert-warning"]) {
        background-color: #FFF3E0 !important;
        border-left-color: #FF9800 !important;
        color: #E65100 !important;
    }
    
    /* Error Box */
    div[data-testid="stAlert"]:has(> div > div[class*="alert-error"]) {
        background-color: #FFEBEE !important;
        border-left-color: #F44336 !important;
        color: #C62828 !important;
    }
    
    /* Markdown Text Colors */
    .stMarkdown {
        color: #333333 !important;
    }
    
    .stMarkdown p {
        color: #333333 !important;
        margin-bottom: 12px;
    }
    
    .stMarkdown strong {
        color: #1a1a1a !important;
        font-weight: 600;
    }
    
    .stMarkdown ul, .stMarkdown ol {
        color: #333333 !important;
    }
    
    .stMarkdown li {
        color: #333333 !important;
        margin-bottom: 8px;
    }
    
    /* Button Styling - JioSign Exact Match */
    .stButton > button {
        background-color: #0066CC !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        width: 100%;
        transition: all 0.3s;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        background-color: #0052A3 !important;
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
        transform: translateY(-1px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Primary Button (Green for Sign Up) */
    button[kind="primary"] {
        background-color: #00A651 !important;
    }
    
    button[kind="primary"]:hover {
        background-color: #008F45 !important;
    }
    
    /* Selectbox Styling - Make Visible and Professional */
    .stSelectbox {
        visibility: visible !important;
        display: block !important;
        margin-bottom: 20px;
    }
    
    .stSelectbox > label {
        color: #1a1a1a !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        margin-bottom: 8px !important;
        display: block !important;
        visibility: visible !important;
    }
    
    /* Selectbox Input Field */
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        border: 2px solid #e5e5e5 !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
        color: #1a1a1a !important;
        font-size: 15px !important;
        font-weight: 500 !important;
        visibility: visible !important;
        display: block !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #0066CC !important;
    }
    
    .stSelectbox > div > div:focus {
        border-color: #0066CC !important;
        box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1) !important;
    }
    
    /* Selectbox Selected Value Text */
    .stSelectbox [data-baseweb="select"] > div {
        color: #1a1a1a !important;
        background-color: #ffffff !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div > div {
        color: #1a1a1a !important;
        background-color: #ffffff !important;
    }
    
    /* Selectbox Dropdown Menu - White Background */
    [data-baseweb="popover"] {
        background-color: #ffffff !important;
        border: 1px solid #e5e5e5 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        z-index: 10000 !important;
    }
    
    /* Dropdown Options */
    [data-baseweb="popover"] ul {
        background-color: #ffffff !important;
    }
    
    [data-baseweb="popover"] li {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
        font-weight: 500 !important;
    }
    
    [data-baseweb="popover"] li:hover {
        background-color: #f8f9fa !important;
        color: #0066CC !important;
    }
    
    [data-baseweb="popover"] li[aria-selected="true"] {
        background-color: #E3F2FD !important;
        color: #0066CC !important;
        font-weight: 600 !important;
    }
    
    /* Selectbox Arrow Icon */
    .stSelectbox svg {
        color: #666666 !important;
    }
    
    /* Ensure all selectbox text is visible */
    [data-baseweb="select"] {
        visibility: visible !important;
        z-index: 1000 !important;
        background-color: #ffffff !important;
    }
    
    [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
    }
    
    [data-baseweb="select"] > div > div {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background-color: #0066CC !important;
    }
    
    /* Ensure all text is readable */
    .element-container {
        color: #333333 !important;
    }
    
    /* Content Card Text */
    .content-card p {
        color: #333333 !important;
        margin-bottom: 12px;
    }
    
    .content-card ul {
        color: #333333 !important;
    }
    
    .content-card li {
        color: #333333 !important;
        margin-bottom: 8px;
    }
    
    /* Mobile Responsive - Comprehensive */
    @media (max-width: 968px) {
        .hero-section { 
            grid-template-columns: 1fr !important; 
            padding: 40px 16px !important; 
            gap: 40px !important;
        }
        .hero-title { 
            font-size: 36px !important; 
            line-height: 1.2 !important;
        }
        .hero-subtitle {
            font-size: 18px !important;
        }
        .nav-menu { 
            display: none !important; 
        }
        .header-container {
            padding: 12px 16px !important;
        }
        .logo-text {
            font-size: 20px !important;
        }
        .btn-signup, .btn-signin {
            padding: 8px 16px !important;
            font-size: 14px !important;
        }
        .dashboard-container {
            padding: 40px 16px !important;
        }
        .section-title {
            font-size: 28px !important;
        }
        .stats-grid {
            grid-template-columns: 1fr !important;
            gap: 16px !important;
        }
        .stat-card {
            padding: 24px !important;
        }
        .stat-number {
            font-size: 36px !important;
        }
        .tender-card {
            padding: 16px !important;
        }
        .tender-details {
            grid-template-columns: 1fr !important;
            gap: 12px !important;
        }
        .content-card {
            padding: 20px !important;
        }
        .card-title {
            font-size: 20px !important;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 10px 16px !important;
            font-size: 13px !important;
        }
        .partners-grid {
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 24px !important;
        }
    }
    
    @media (max-width: 640px) {
        .hero-title { 
            font-size: 28px !important; 
        }
        .hero-subtitle {
            font-size: 16px !important;
        }
        .section-title {
            font-size: 24px !important;
        }
        .stat-number {
            font-size: 32px !important;
        }
        .tender-title {
            font-size: 18px !important;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 8px 12px !important;
            font-size: 12px !important;
        }
        .partners-grid {
            grid-template-columns: 1fr !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_tender' not in st.session_state:
    st.session_state.selected_tender = None
if 'bid_documents' not in st.session_state:
    st.session_state.bid_documents = []
if 'compliance_score' not in st.session_state:
    st.session_state.compliance_score = 87
if 'signature_complete' not in st.session_state:
    st.session_state.signature_complete = False
if 'documents_generated' not in st.session_state:
    st.session_state.documents_generated = False
if 'dsc_connected' not in st.session_state:
    st.session_state.dsc_connected = False

# Sample Data
def get_sample_tenders():
    return [
        {
            'id': 'GEM/2025/B/3856789',
            'title': 'Supply of Desktop Computers',
            'authority': 'Ministry of Education',
            'value': '₹2.5 Crore',
            'emd': '₹5 Lakh',
            'deadline': datetime.now() + timedelta(days=10),
            'category': 'IT Hardware',
            'location': 'New Delhi',
            'match_score': 95,
        },
        {
            'id': 'ET/2025/C/4521234',
            'title': 'Annual Maintenance Contract for Office Equipment',
            'authority': 'Department of Health',
            'value': '₹1.2 Crore',
            'emd': '₹2.4 Lakh',
            'deadline': datetime.now() + timedelta(days=7),
            'category': 'Services',
            'location': 'Mumbai',
            'match_score': 88,
        },
        {
            'id': 'GEM/2025/B/3890123',
            'title': 'Construction of Office Building',
            'authority': 'Public Works Department',
            'value': '₹15 Crore',
            'emd': '₹30 Lakh',
            'deadline': datetime.now() + timedelta(days=15),
            'category': 'Construction',
            'location': 'Bangalore',
            'match_score': 72,
        }
    ]

# Header - EXACT JioSign Match
def render_header():
    st.markdown("""
    <div class="main-header">
        <div class="header-container">
            <div class="logo-section">
                <div class="logo-circle">✓</div>
                <div class="logo-text">Smart Tender</div>
            </div>
            <ul class="nav-menu">
                <li><a href="#" class="nav-link">Features <span style="font-size:10px; margin-left:4px;">▼</span></a></li>
                <li><a href="#" class="nav-link">Solutions</a></li>
                <li><a href="#" class="nav-link">Help & resources <span style="font-size:10px; margin-left:4px;">▼</span></a></li>
                <li><a href="#" class="nav-link">Pricing</a></li>
            </ul>
            <div class="header-actions">
                <a href="#" class="btn-signup">Sign up</a>
                <a href="#" class="btn-signin">Sign in</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Hero Section
def render_hero():
    st.markdown("""
    <div class="hero-section">
        <div class="hero-content">
            <h1 class="hero-title">
                Go paperless:<br>
                Convenient & secure<br>
                tender management<br>
                with Smart Tender
            </h1>
            <p class="hero-subtitle">
                Say goodbye to the physical signatures and embrace the convenience of sending and signing 
                documents at any time, anywhere using legally binding digital signatures.
            </p>
        </div>
        <div style="display: flex; align-items: center; justify-content: center;">
            <div style="width: 100%; max-width: 500px; height: 600px; background: linear-gradient(135deg, #0066CC 0%, #00A651 100%); border-radius: 30px; display: flex; align-items: center; justify-content: center; box-shadow: 0 20px 60px rgba(0,0,0,0.2); position: relative;">
                <div style="color: white; text-align: center; padding: 40px;">
                    <div style="font-size: 120px; margin-bottom: 20px;">📋</div>
                    <div style="font-size: 32px; font-weight: 700; margin-bottom: 16px;">Smart Tender</div>
                    <div style="font-size: 18px; opacity: 0.9;">AI-Powered Platform</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Button with unique key
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Try Smart Tender now", key="hero_cta_button_home", use_container_width=True):
            st.session_state.page = 'dashboard_view'
            st.rerun()

# Partners
def render_partners():
    st.markdown("""
    <div class="partners-section">
        <div class="partners-container">
            <div class="partners-title">Trusted by leading organizations</div>
            <div class="partners-grid">
                <div class="partner-logo">C-SQUARE</div>
                <div class="partner-logo">Fynd</div>
                <div class="partner-logo">Jio</div>
                <div class="partner-logo">Haptik</div>
                <div class="partner-logo">Reliance</div>
                <div class="partner-logo">Asteria</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Dashboard
def render_dashboard():
    st.markdown("""
    <div class="dashboard-container">
        <h2 class="section-title">Dashboard</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">12</div>
                <div class="stat-label">Active Tenders</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">8</div>
                <div class="stat-label">Bids in Progress</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">₹45Cr</div>
                <div class="stat-label">Total Opportunity Value</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">92%</div>
                <div class="stat-label">Avg Compliance Score</div>
            </div>
        </div>
        <h3 style="font-size: 28px; font-weight: 600; color: #1a1a1a; margin-bottom: 24px; margin-top: 48px;">
            🎯 Matched Tenders (AI-Powered Recommendations)
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    tenders = get_sample_tenders()
    
    for idx, tender in enumerate(tenders):
        days_left = (tender['deadline'] - datetime.now()).days
        
        st.markdown(f"""
        <div class="tender-card">
            <div class="tender-title">{tender['title']}</div>
            <div class="tender-id">{tender['id']}</div>
            <div class="match-score">{tender['match_score']}% Match</div>
            <div class="tender-details">
                <div><div class="detail-label">Authority</div><div class="detail-value">{tender['authority']}</div></div>
                <div><div class="detail-label">Value</div><div class="detail-value">{tender['value']}</div></div>
                <div><div class="detail-label">EMD</div><div class="detail-value">{tender['emd']}</div></div>
                <div><div class="detail-label">Category</div><div class="detail-value">{tender['category']}</div></div>
                <div><div class="detail-label">Location</div><div class="detail-value">{tender['location']}</div></div>
                <div><div class="detail-label">Deadline</div><div class="detail-value">{tender['deadline'].strftime('%d %b %Y')}</div></div>
                <div><div class="detail-label">Days Left</div><div class="detail-value">{days_left} days</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # UNIQUE KEY for each button
        button_key = f"view_tender_btn_{idx}_{tender['id'].replace('/', '_')}"
        if st.button(f"View Details & Prepare Bid", key=button_key, use_container_width=True):
            st.session_state.selected_tender = tender
            st.session_state.page = 'tender_details'
            st.rerun()

# Tender Details Page
def render_tender_details():
    render_header()
    
    if not st.session_state.selected_tender:
        st.error("❌ No tender selected. Please go back to dashboard.")
        if st.button("← Back to Dashboard", key="back_no_tender_btn_details"):
            st.session_state.page = 'home'
            st.rerun()
        return
    
    tender = st.session_state.selected_tender
    
    st.markdown(f"""
    <div class="dashboard-container">
        <h2 class="section-title">{tender['title']}</h2>
        <p style="font-size: 16px; color: #666; margin-bottom: 32px;">
            <strong>Tender ID:</strong> {tender['id']} | <strong>Authority:</strong> {tender['authority']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs with unique keys
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📄 Tender Analysis", 
        "📝 Bid Preparation", 
        "🆔 Identity & Documents",
        "✅ Compliance Check", 
        "✍️ Digital Signature", 
        "📤 Submission"
    ])
    
    with tab1:
        st.markdown("""
        <div class="content-card" style="background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); border: 2px solid #e5e5e5;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
                <div style="width: 48px; height: 48px; background: #0066CC; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px;">🤖</div>
                <h3 class="card-title" style="margin: 0;">AI-Powered Tender Analysis</h3>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 24px;">
                <div style="background: white; padding: 20px; border-radius: 8px; border-left: 4px solid #0066CC;">
                    <div style="font-size: 14px; color: #666; font-weight: 600; margin-bottom: 8px; text-transform: uppercase;">📋 Tender Requirements</div>
                    <ul style="margin-left: 20px; color: #333; line-height: 1.8;">
                        <li><strong style="color: #1a1a1a;">Turnover:</strong> ₹10 Crore in last 3 years</li>
                        <li><strong style="color: #1a1a1a;">Experience:</strong> 3 similar orders in last 5 years</li>
                        <li><strong style="color: #1a1a1a;">Certifications:</strong> ISO 9001, ISO 27001</li>
                        <li><strong style="color: #1a1a1a;">Registration:</strong> GeM registered vendor</li>
                        <li><strong style="color: #1a1a1a;">Class:</strong> Class I or above</li>
                    </ul>
                </div>
                
                <div style="background: white; padding: 20px; border-radius: 8px; border-left: 4px solid #00A651;">
                    <div style="font-size: 14px; color: #666; font-weight: 600; margin-bottom: 8px; text-transform: uppercase;">💼 Technical Requirements</div>
                    <ul style="margin-left: 20px; color: #333; line-height: 1.8;">
                        <li>Intel Core i5 11th Gen or higher</li>
                        <li>8GB DDR4 RAM minimum</li>
                        <li>512GB SSD storage</li>
                        <li>3 years on-site warranty</li>
                    </ul>
                </div>
                
                <div style="background: white; padding: 20px; border-radius: 8px; border-left: 4px solid #FF9800;">
                    <div style="font-size: 14px; color: #666; font-weight: 600; margin-bottom: 8px; text-transform: uppercase;">📄 Documents Required</div>
                    <ul style="margin-left: 20px; color: #333; line-height: 1.8;">
                        <li>EMD (DD/BG) - ₹5 Lakh</li>
                        <li>Audited Financials (3 years)</li>
                        <li>Experience Certificates (3 nos.)</li>
                        <li>OEM Authorization</li>
                        <li>BIS Certificate</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="content-card" style="background: #E3F2FD; border-left: 4px solid #2196F3;">
            <h3 style="color: #1565C0; margin-bottom: 12px;">💡 AI Insights</h3>
            <ul style="color: #1565C0; margin-left: 20px;">
                <li style="margin-bottom: 8px;"><strong style="color: #1565C0;">High Match Score (95%):</strong> This tender aligns perfectly with your company profile</li>
                <li style="margin-bottom: 8px;"><strong style="color: #1565C0;">Eligibility Status:</strong> You meet all criteria except need 1 more experience certificate</li>
                <li style="margin-bottom: 8px;"><strong style="color: #1565C0;">Pricing Recommendation:</strong> Competitive price range is ₹2.3-2.6 Crore</li>
                <li style="margin-bottom: 8px;"><strong style="color: #1565C0;">Timeline:</strong> You have 10 days. Estimated time to prepare bid: 5-7 days with our platform</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div style="margin-bottom: 24px;">
            <h2 style="font-size: 28px; font-weight: 700; color: #1a1a1a; margin-bottom: 8px;">📝 Automated Bid Document Generation</h2>
            <p style="color: #666; font-size: 16px;">AI-powered document creation saves 40-80 hours of manual work</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="content-card" style="background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); border: 2px solid #e5e5e5;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
                <div style="width: 48px; height: 48px; background: #00A651; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px;">📄</div>
                <h3 class="card-title" style="margin: 0;">Document Components</h3>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 16px;">
                <div style="background: white; padding: 20px; border-radius: 8px; border: 1px solid #e5e5e5;">
                    <div style="font-size: 18px; font-weight: 600; color: #0066CC; margin-bottom: 8px;">📋 Technical Bid</div>
                    <p style="color: #666; font-size: 14px; margin: 0;">Company Profile, Experience, Compliance Matrix, Delivery Plan</p>
                </div>
                
                <div style="background: white; padding: 20px; border-radius: 8px; border: 1px solid #e5e5e5;">
                    <div style="font-size: 18px; font-weight: 600; color: #00A651; margin-bottom: 8px;">💰 Financial Bid</div>
                    <p style="color: #666; font-size: 14px; margin: 0;">Price Schedule (BOQ), Payment Terms, Delivery Schedule</p>
                </div>
                
                <div style="background: white; padding: 20px; border-radius: 8px; border: 1px solid #e5e5e5;">
                    <div style="font-size: 18px; font-weight: 600; color: #FF9800; margin-bottom: 8px;">📎 Supporting Documents</div>
                    <p style="color: #666; font-size: 14px; margin: 0;">Certificates, Undertakings, Declarations</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Generate Bid Documents (AI-Powered)", type="primary", use_container_width=True, key=f"generate_docs_btn_{tender['id'].replace('/', '_')}"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 30:
                    status_text.text("📄 Extracting tender requirements...")
                elif i < 60:
                    status_text.text("📝 Generating technical bid documents...")
                elif i < 90:
                    status_text.text("💰 Creating financial bid...")
                else:
                    status_text.text("✅ Finalizing documents...")
                time.sleep(0.02)
            
            progress_bar.empty()
            status_text.empty()
            
            st.markdown("""
            <div class="content-card" style="background: #E8F5E9; border-left: 4px solid #4CAF50;">
                <h3 style="color: #2E7D32; margin-bottom: 12px;">✅ Bid Documents Generated Successfully!</h3>
                <p style="color: #2E7D32;"><strong>💡 Time Saved:</strong> Documents generated in 2 minutes vs 40-80 hours manually!</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.session_state.documents_generated = True
            st.session_state.bid_documents = [
                {"name": "Cover Letter", "pages": 2, "status": "✅ Generated"},
                {"name": "Company Profile", "pages": 5, "status": "✅ Generated"},
                {"name": "Technical Compliance Matrix", "pages": 8, "status": "✅ Generated"},
                {"name": "Experience Certificates", "pages": 6, "status": "✅ Generated"},
                {"name": "Financial Bid (BOQ)", "pages": 12, "status": "✅ Generated"},
                {"name": "Delivery Schedule", "pages": 3, "status": "✅ Generated"},
                {"name": "Quality Assurance Plan", "pages": 7, "status": "✅ Generated"},
                {"name": "Undertakings & Declarations", "pages": 4, "status": "✅ Generated"},
            ]
        
        if st.session_state.bid_documents:
            st.markdown("### 📚 Generated Documents")
            for doc_idx, doc in enumerate(st.session_state.bid_documents):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{doc['name']}** ({doc['pages']} pages)")
                with col2:
                    st.write(doc['status'])
                with col3:
                    # Unique key with tender ID and index
                    tender_id_part = st.session_state.selected_tender['id'].replace('/', '_') if st.session_state.selected_tender else 'default'
                    st.button("📥 Download", key=f"download_tab2_{tender_id_part}_{doc_idx}_{doc['name'].replace(' ', '_').replace('(', '').replace(')', '')}")
    
    with tab3:
        st.markdown("### 🆔 Identity & Document Verification")
        st.markdown("""
        <p style="color: #666; font-size: 16px; margin-bottom: 32px;">
            Streamline vendor verification with integrated identity and document management solutions
        </p>
        """, unsafe_allow_html=True)
        
        # VKYC Section
        st.markdown("""
        <div class="content-card" style="background: linear-gradient(135deg, #E3F2FD 0%, #ffffff 100%); border-left: 4px solid #2196F3;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                <div style="width: 48px; height: 48px; background: #2196F3; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px;">🎥</div>
                <h3 class="card-title" style="margin: 0;">Video KYC (VKYC)</h3>
            </div>
            <p style="color: #333; margin-bottom: 16px;">Complete vendor verification through secure video calling with authorized personnel.</p>
            <ul style="color: #333; margin-left: 20px; line-height: 1.8;">
                <li><strong>Real-time Verification:</strong> Live video call with authorized signatory</li>
                <li><strong>Document Authentication:</strong> Real-time document verification during call</li>
                <li><strong>Geo-tagging:</strong> Location verification for compliance</li>
                <li><strong>Recording:</strong> Secure recording for audit trail</li>
                <li><strong>Status:</strong> <span style="color: #00A651; font-weight: 600;">✅ Verified on 2025-11-10</span></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎥 Initiate VKYC Session", key=f"vkyc_btn_{tender['id'].replace('/', '_')}", use_container_width=True):
            st.success("✅ VKYC session scheduled for tomorrow at 10:00 AM. Meeting link sent to registered email.")
        
        # EKYC Section
        st.markdown("""
        <div class="content-card" style="background: linear-gradient(135deg, #E0F7FA 0%, #ffffff 100%); border-left: 4px solid #00BCD4;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                <div style="width: 48px; height: 48px; background: #00BCD4; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px;">🆔</div>
                <h3 class="card-title" style="margin: 0;">Electronic KYC (EKYC)</h3>
            </div>
            <p style="color: #333; margin-bottom: 16px;">Instant verification using Aadhaar and PAN with UIDAI integration.</p>
            <ul style="color: #333; margin-left: 20px; line-height: 1.8;">
                <li><strong>Aadhaar Verification:</strong> OTP-based authentication</li>
                <li><strong>PAN Verification:</strong> Direct NSDL/Income Tax integration</li>
                <li><strong>GST Verification:</strong> GSTIN validation</li>
                <li><strong>Bank Account:</strong> Penny drop verification</li>
                <li><strong>Processing Time:</strong> <span style="color: #00A651; font-weight: 600;">< 2 minutes</span></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🆔 Verify Aadhaar", key=f"aadhaar_btn_{tender['id'].replace('/', '_')}", use_container_width=True):
                st.success("✅ Aadhaar verified successfully! Name: Rajesh Kumar, DOB: 15-Aug-1985")
        with col2:
            if st.button("💳 Verify PAN", key=f"pan_btn_{tender['id'].replace('/', '_')}", use_container_width=True):
                st.success("✅ PAN verified successfully! PAN: ABCDE1234F, Status: Active")
        
        # DigiLocker Section
        st.markdown("""
        <div class="content-card" style="background: linear-gradient(135deg, #FFE0B2 0%, #ffffff 100%); border-left: 4px solid #FF5722;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                <div style="width: 48px; height: 48px; background: #FF5722; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px;">🗂️</div>
                <h3 class="card-title" style="margin: 0;">DigiLocker Integration</h3>
            </div>
            <p style="color: #333; margin-bottom: 16px;">Fetch government-issued verified documents directly from DigiLocker.</p>
            <ul style="color: #333; margin-left: 20px; line-height: 1.8;">
                <li><strong>Aadhaar Card:</strong> Digitally signed by UIDAI</li>
                <li><strong>PAN Card:</strong> Issued by Income Tax Department</li>
                <li><strong>GST Certificate:</strong> GSTN verified</li>
                <li><strong>Incorporation Certificate:</strong> MCA verified</li>
                <li><strong>Authenticity:</strong> <span style="color: #00A651; font-weight: 600;">Government verified</span></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🗂️ Connect DigiLocker", key=f"digilocker_btn_{tender['id'].replace('/', '_')}", type="primary", use_container_width=True):
            st.markdown("""
            <div class="content-card" style="background: #E8F5E9; border-left: 4px solid #4CAF50; margin-top: 20px;">
                <h3 style="color: #2E7D32; margin-bottom: 12px;">✅ DigiLocker Connected!</h3>
                <p style="color: #2E7D32; margin-bottom: 16px;"><strong>Documents Available:</strong></p>
                <ul style="color: #2E7D32; margin-left: 20px;">
                    <li>✅ Aadhaar Card (Issued: 2018-05-20)</li>
                    <li>✅ PAN Card (Issued: 2015-03-12)</li>
                    <li>✅ GST Certificate (Valid till: 2026-12-31)</li>
                    <li>✅ Driving License (Valid till: 2028-08-15)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Cloud Storage Section
        st.markdown("""
        <div class="content-card" style="background: linear-gradient(135deg, #E8EAF6 0%, #ffffff 100%); border-left: 4px solid #3F51B5;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                <div style="width: 48px; height: 48px; background: #3F51B5; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px;">☁️</div>
                <h3 class="card-title" style="margin: 0;">Cloud Storage Integration</h3>
            </div>
            <p style="color: #333; margin-bottom: 16px;">Secure document storage and synchronization across platforms.</p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-top: 16px;">
                <div style="background: white; padding: 16px; border-radius: 8px; border: 1px solid #e5e5e5; text-align: center;">
                    <div style="font-size: 32px; margin-bottom: 8px;">☁️</div>
                    <div style="font-weight: 600; color: #1a1a1a;">Google Drive</div>
                    <div style="color: #666; font-size: 14px;">15 GB Free</div>
                </div>
                <div style="background: white; padding: 16px; border-radius: 8px; border: 1px solid #e5e5e5; text-align: center;">
                    <div style="font-size: 32px; margin-bottom: 8px;">📦</div>
                    <div style="font-weight: 600; color: #1a1a1a;">Dropbox</div>
                    <div style="color: #666; font-size: 14px;">2 GB Free</div>
                </div>
                <div style="background: white; padding: 16px; border-radius: 8px; border: 1px solid #e5e5e5; text-align: center;">
                    <div style="font-size: 32px; margin-bottom: 8px;">📁</div>
                    <div style="font-weight: 600; color: #1a1a1a;">OneDrive</div>
                    <div style="color: #666; font-size: 14px;">5 GB Free</div>
                </div>
                <div style="background: white; padding: 16px; border-radius: 8px; border: 1px solid #e5e5e5; text-align: center;">
                    <div style="font-size: 32px; margin-bottom: 8px;">🗄️</div>
                    <div style="font-weight: 600; color: #1a1a1a;">AWS S3</div>
                    <div style="color: #666; font-size: 14px;">Enterprise</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("☁️ Sync to Cloud", key=f"cloud_sync_btn_{tender['id'].replace('/', '_')}", use_container_width=True):
                st.success("✅ All documents synced to cloud storage successfully!")
        with col2:
            if st.button("📥 Download All", key=f"download_all_btn_{tender['id'].replace('/', '_')}", use_container_width=True):
                st.success("✅ Downloading all documents... (8 files, 12.5 MB)")
        with col3:
            if st.button("🔄 Backup Now", key=f"backup_btn_{tender['id'].replace('/', '_')}", use_container_width=True):
                st.success("✅ Backup completed! Last backup: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    with tab4:
        st.markdown(f"### ✅ AI-Powered Compliance Verification")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"""
            <div class="content-card" style="text-align: center;">
                <div style="font-size: 64px; font-weight: 800; color: #00A651; margin-bottom: 16px;">
                    {st.session_state.compliance_score}%
                </div>
                <div style="font-size: 18px; color: #666;">Compliance Score</div>
            </div>
            """, unsafe_allow_html=True)
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = st.session_state.compliance_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#00A651"},
                    'steps': [
                        {'range': [0, 70], 'color': "lightgray"},
                        {'range': [70, 90], 'color': "yellow"},
                        {'range': [90, 100], 'color': "#00A651"}
                    ],
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True, key=f"compliance_gauge_{tender['id'].replace('/', '_')}")
        
        with col2:
            st.markdown("### 🔍 Verification Results")
            
            st.markdown("**📋 Eligibility Criteria**")
            st.markdown("""
            <div style="background: #E8F5E9; padding: 12px; border-radius: 6px; margin-bottom: 8px; border-left: 3px solid #4CAF50;">
                <span style="color: #2E7D32;">✅ GeM Registration: Active</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div style="background: #E8F5E9; padding: 12px; border-radius: 6px; margin-bottom: 8px; border-left: 3px solid #4CAF50;">
                <span style="color: #2E7D32;">✅ Turnover: ₹15 Cr (Required: ₹10 Cr)</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div style="background: #E8F5E9; padding: 12px; border-radius: 6px; margin-bottom: 8px; border-left: 3px solid #4CAF50;">
                <span style="color: #2E7D32;">✅ ISO 9001: Valid till 2026-03-15</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div style="background: #FFF3E0; padding: 12px; border-radius: 6px; margin-bottom: 8px; border-left: 3px solid #FF9800;">
                <span style="color: #E65100;">⚠️ ISO 27001: Expired (2025-06-15) - <strong>CRITICAL</strong></span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div style="background: #E8F5E9; padding: 12px; border-radius: 6px; margin-bottom: 8px; border-left: 3px solid #4CAF50;">
                <span style="color: #2E7D32;">✅ PAN & GST: Verified</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div style="background: #E8F5E9; padding: 12px; border-radius: 6px; margin-bottom: 16px; border-left: 3px solid #4CAF50;">
                <span style="color: #2E7D32;">✅ Class of Contractor: Class I</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("**📄 Documents**")
            doc_count = len(st.session_state.bid_documents) if st.session_state.bid_documents else 0
            if doc_count >= 8:
                st.markdown(f"""
                <div style="background: #E8F5E9; padding: 12px; border-radius: 6px; margin-bottom: 8px; border-left: 3px solid #4CAF50;">
                    <span style="color: #2E7D32;">✅ {doc_count}/18 Documents Ready</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: #FFF3E0; padding: 12px; border-radius: 6px; margin-bottom: 8px; border-left: 3px solid #FF9800;">
                    <span style="color: #E65100;">⚠️ {doc_count}/18 Documents Ready - Generate documents first</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background: #FFF3E0; padding: 12px; border-radius: 6px; margin-bottom: 16px; border-left: 3px solid #FF9800;">
                <span style="color: #E65100;">⚠️ Missing: OEM Authorization, BIS Certificate, EMD</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("**📝 Technical Bid**")
            st.markdown("""
            <div style="background: #E8F5E9; padding: 12px; border-radius: 6px; margin-bottom: 8px; border-left: 3px solid #4CAF50;">
                <span style="color: #2E7D32;">✅ All 24 specifications compliant</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div style="background: #FFF3E0; padding: 12px; border-radius: 6px; margin-bottom: 16px; border-left: 3px solid #FF9800;">
                <span style="color: #E65100;">⚠️ Warranty: 2 years offered (Required: 3 years)</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("**💰 Financial Bid**")
            st.markdown("""
            <div style="background: #E8F5E9; padding: 12px; border-radius: 6px; margin-bottom: 8px; border-left: 3px solid #4CAF50;">
                <span style="color: #2E7D32;">✅ BOQ complete, formulas correct</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div style="background: #E8F5E9; padding: 12px; border-radius: 6px; margin-bottom: 16px; border-left: 3px solid #4CAF50;">
                <span style="color: #2E7D32;">✅ GST properly calculated</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="content-card" style="background: #FFEBEE; border-left: 4px solid #F44336;">
            <h3 style="color: #C62828; margin-bottom: 16px;">🔴 CRITICAL ISSUES (Must Fix Before Submission)</h3>
            <ol style="color: #C62828; margin-left: 20px;">
                <li style="margin-bottom: 12px;"><strong style="color: #C62828;">ISO 27001 Certificate EXPIRED</strong> - Will cause bid rejection<br>
                   <span style="color: #666;">→ Solution: Upload renewed certificate</span></li>
                <li style="margin-bottom: 12px;"><strong style="color: #C62828;">Warranty Period: 2 years vs 3 years required</strong> - Non-responsive bid<br>
                   <span style="color: #666;">→ Solution: Revise warranty terms to 3 years</span></li>
                <li style="margin-bottom: 12px;"><strong style="color: #C62828;">Missing OEM Authorization</strong> - Technical bid rejection risk<br>
                   <span style="color: #666;">→ Solution: Contact OEM for authorization certificate</span></li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with tab5:
        st.markdown("### ✍️ Digital Signature Workflow (JioSign Integration)")
        
        st.markdown("""
        <div style="display: flex; gap: 16px; margin-bottom: 32px;">
            <div style="flex: 1; padding: 16px; background: #E8F5E9; border-radius: 8px; text-align: center;">
                <div style="font-size: 24px; margin-bottom: 8px;">✅</div>
                <div style="font-weight: 600;">Upload Document</div>
            </div>
            <div style="flex: 1; padding: 16px; background: #E8F5E9; border-radius: 8px; text-align: center;">
                <div style="font-size: 24px; margin-bottom: 8px;">✅</div>
                <div style="font-weight: 600;">Add Participants</div>
            </div>
            <div style="flex: 1; padding: 16px; background: #FFF3E0; border-radius: 8px; text-align: center;">
                <div style="font-size: 24px; margin-bottom: 8px;">⏳</div>
                <div style="font-weight: 600;">Manage Signature</div>
            </div>
            <div style="flex: 1; padding: 16px; background: #F5F5F5; border-radius: 8px; text-align: center;">
                <div style="font-size: 24px; margin-bottom: 8px;">⏸️</div>
                <div style="font-weight: 600;">Review & Send</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="content-card">
            <h3 class="card-title">📋 Signature Fields Placement</h3>
            <p>Click on a card to select it, then click where you want to place it on the document.</p>
            <div style="display: flex; gap: 10px; margin-top: 16px; flex-wrap: wrap;">
                <button style="background: #FF6B9D; color: white; border: none; padding: 10px 20px; border-radius: 5px;">Signature</button>
                <button style="background: #FF6B9D; color: white; border: none; padding: 10px 20px; border-radius: 5px;">Initials</button>
                <button style="background: #FF6B9D; color: white; border: none; padding: 10px 20px; border-radius: 5px;">Signatory Name</button>
                <button style="background: #FF6B9D; color: white; border: none; padding: 10px 20px; border-radius: 5px;">Signing Date</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔐 Digital Signature Certificate (DSC)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background: white; padding: 24px; border-radius: 12px; border: 2px solid #e5e5e5; margin-bottom: 20px;">
                <h3 style="color: #1a1a1a; font-size: 20px; font-weight: 600; margin-bottom: 20px;">🔐 Digital Signature Certificate</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div style="margin-bottom: 8px;"><label style="color: #1a1a1a; font-weight: 600; font-size: 15px; display: block;">DSC Type</label></div>', unsafe_allow_html=True)
            dsc_type = st.selectbox("", ["Class 3 (Organization)", "Class 2 (Individual)", "Aadhaar eSign"], key=f"dsc_type_select_{tender['id'].replace('/', '_')}", label_visibility="collapsed")
            
            st.markdown('<div style="margin-bottom: 8px; margin-top: 20px;"><label style="color: #1a1a1a; font-weight: 600; font-size: 15px; display: block;">DSC Provider</label></div>', unsafe_allow_html=True)
            dsc_provider = st.selectbox("", ["eMudhra", "nCode", "Sify", "Capricorn"], key=f"dsc_provider_select_{tender['id'].replace('/', '_')}", label_visibility="collapsed")
            
            if st.button("🔌 Connect DSC Token", key=f"connect_dsc_btn_{tender['id'].replace('/', '_')}", use_container_width=True):
                st.markdown("""
                <div class="content-card" style="background: #E8F5E9; border-left: 4px solid #4CAF50; margin-top: 20px;">
                    <h3 style="color: #2E7D32; margin-bottom: 12px;">✅ DSC Token Connected!</h3>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("""
                <div style="background: #E3F2FD; padding: 16px; border-radius: 8px; margin-top: 12px; border-left: 3px solid #2196F3;">
                    <p style="color: #1565C0; margin-bottom: 8px; font-weight: 600;">Certificate Details:</p>
                    <ul style="color: #1565C0; margin-left: 20px;">
                        <li>Serial: 7A3B9F2E1D4C8560</li>
                        <li>Issuer: eMudhra CA</li>
                        <li>Valid Until: 2026-08-15</li>
                        <li>Class: 3 (Organization)</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                st.session_state.dsc_connected = True
        
        with col2:
            st.markdown("""
            <div class="content-card">
                <h3 class="card-title">🔒 Security Features</h3>
                <ul style="margin-left: 20px;">
                    <li>✅ ISO 27001 Certified</li>
                    <li>✅ SOC 2 Audited</li>
                    <li>✅ Tamper-evident documents</li>
                    <li>✅ Complete audit trail</li>
                    <li>✅ Timestamped signatures</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("✍️ Sign All Documents with DSC", type="primary", use_container_width=True, key=f"sign_documents_btn_{tender['id'].replace('/', '_')}"):
            if not st.session_state.documents_generated:
                st.markdown("""
                <div class="content-card" style="background: #FFF3E0; border-left: 4px solid #FF9800;">
                    <p style="color: #E65100;"><strong>⚠️ Please generate documents first in the Bid Preparation tab.</strong></p>
                </div>
                """, unsafe_allow_html=True)
            elif not st.session_state.dsc_connected:
                st.markdown("""
                <div class="content-card" style="background: #FFF3E0; border-left: 4px solid #FF9800;">
                    <p style="color: #E65100;"><strong>⚠️ Please connect DSC token first.</strong></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i in range(100):
                    progress_bar.progress(i + 1)
                    if i < 50:
                        status_text.text(f"📄 Signing document {i//10 + 1}...")
                    else:
                        status_text.text("🔐 Applying digital signatures...")
                    time.sleep(0.02)
                
                progress_bar.empty()
                status_text.empty()
                
                st.markdown("""
                <div class="content-card" style="background: #E8F5E9; border-left: 4px solid #4CAF50;">
                    <h3 style="color: #2E7D32; margin-bottom: 12px;">✅ All Documents Signed Successfully!</h3>
                    <p style="color: #2E7D32; margin-bottom: 8px;"><strong>Signature Applied:</strong></p>
                    <ul style="color: #2E7D32; margin-left: 20px;">
                        <li>8 documents signed</li>
                        <li>12 signature fields completed</li>
                        <li>Timestamp: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</li>
                        <li>Certificate: eMudhra Class 3 (Organization)</li>
                        <li>Audit trail generated</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                st.session_state.signature_complete = True
    
    with tab6:
        st.markdown("### 📤 Portal Submission")
        
        st.markdown("### ✅ Pre-Submission Verification")
        
        checklist = [
            ("All documents generated", st.session_state.documents_generated),
            ("Compliance score > 85%", st.session_state.compliance_score >= 85),
            ("All signatures applied", st.session_state.signature_complete),
            ("EMD uploaded", False),
            ("File sizes within limits", True),
            ("DSC valid and not expired", st.session_state.dsc_connected),
        ]
        
        all_ready = all(item[1] for item in checklist)
        
        for item, status in checklist:
            if status:
                st.success(f"✅ {item}")
            else:
                st.error(f"❌ {item}")
        
        st.markdown("---")
        
        st.markdown("### 🌐 Select Submission Portal")
        portal = st.selectbox("Portal", ["GeM (gem.gov.in)", "eTenders (etenders.gov.in)", "CPPP (eprocure.gov.in)"], key=f"portal_select_box_{tender['id'].replace('/', '_')}")
        
        if portal == "GeM (gem.gov.in)":
            st.info("**GeM Integration:** Direct API submission available. Auto-fill GeM catalog items.")
        elif portal == "eTenders (etenders.gov.in)":
            st.info("**eTenders Integration:** Automated login and document upload.")
        else:
            st.info("**CPPP Integration:** Multi-department tender tracking.")
        
        st.markdown("---")
        
        st.markdown("### 📋 Submission Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="content-card">
                <h3 class="card-title">Documents Ready</h3>
                <p>Technical Bid: 45 pages</p>
                <p>Financial Bid: 12 pages</p>
                <p>Supporting Documents: 18 files</p>
                <p>Total Size: 8.2 MB</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            days_left = (tender['deadline'] - datetime.now()).days
            st.markdown(f"""
            <div class="content-card">
                <h3 class="card-title">Submission Details</h3>
                <p><strong>Tender:</strong> {tender['id']}</p>
                <p><strong>Deadline:</strong> {tender['deadline'].strftime('%d %b %Y, %I:%M %p')}</p>
                <p><strong>Time Remaining:</strong> {days_left} days</p>
                <p><strong>Compliance Score:</strong> {st.session_state.compliance_score}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button("🚀 Submit Bid to Portal", type="primary", use_container_width=True, key="submit_bid_btn", disabled=not all_ready):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 30:
                    status_text.text("📤 Uploading documents to portal...")
                elif i < 60:
                    status_text.text("✍️ Applying digital signatures...")
                elif i < 90:
                    status_text.text("✅ Validating submission...")
                else:
                    status_text.text("🎉 Finalizing submission...")
                time.sleep(0.03)
            
            progress_bar.empty()
            status_text.empty()
            
            st.success("🎉 **Bid Submitted Successfully!**")
            
            st.markdown("""
            <div class="content-card" style="background: #E8F5E9; border-left: 4px solid #4CAF50;">
                <h3 class="card-title">✅ Submission Confirmed</h3>
                <ul style="margin-left: 20px;">
                    <li><strong>Acknowledgment No:</strong> ACK/GEM/2025/3856789/12345</li>
                    <li><strong>Submission Time:</strong> """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S IST") + """</li>
                    <li><strong>Documents Uploaded:</strong> 18/18</li>
                    <li><strong>Digital Signatures:</strong> 12/12 applied</li>
                    <li><strong>Time Before Deadline:</strong> """ + str(days_left) + """ days</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="content-card" style="background: #E3F2FD; border-left: 4px solid #2196F3;">
                <p style="color: #1565C0;"><strong>📧 Confirmation email sent.</strong> You can track bid status in the dashboard.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 📊 Post-Submission Tracking")
            st.markdown("""
            **Upcoming Milestones:**
            - ✅ Bid Submission: Completed
            - ⏰ Technical Bid Opening: """ + (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d 11:00 AM") + """
            - ⏰ Technical Evaluation: """ + (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d") + """ to """ + (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d") + """
            - ⏰ Financial Bid Opening: """ + (datetime.now() + timedelta(days=8)).strftime("%Y-%m-%d") + """ (if technically qualified)
            - ⏰ Award of Contract: """ + (datetime.now() + timedelta(days=18)).strftime("%Y-%m-%d") + """ (estimated)
            """)
        elif not all_ready:
            st.markdown("""
            <div class="content-card" style="background: #FFF3E0; border-left: 4px solid #FF9800;">
                <p style="color: #E65100;"><strong>⚠️ Please complete all checklist items before submission.</strong></p>
            </div>
            """, unsafe_allow_html=True)
    
    # Back Button with unique key
    st.markdown("---")
    if st.button("← Back to Dashboard", key="back_to_dashboard_btn", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()

# Main App
def main():
    if st.session_state.page == 'home':
        render_header()
        render_hero()
        render_partners()
        render_dashboard()
    elif st.session_state.page == 'dashboard_view':
        render_header()
        render_dashboard()
    elif st.session_state.page == 'tender_details':
        render_tender_details()
    else:
        st.session_state.page = 'home'
        st.rerun()

if __name__ == "__main__":
    main()
