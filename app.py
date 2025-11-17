import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import requests
import base64
from io import BytesIO

# Page Configuration
st.set_page_config(
    page_title="Smart Tender Management Platform",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit default UI
hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    div[data-testid="stToolbar"] {visibility: hidden;}
    .stApp > header {display: none;}
    .stApp [data-testid="stHeader"] {display: none;}
    .stApp [data-testid="stToolbar"] {display: none;}
    .stApp [data-testid="stDecoration"] {display: none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Professional JioSign-Style CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body, html {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background-color: #ffffff;
        color: #1a1a1a;
        line-height: 1.6;
    }
    
    .stApp {
        background: #ffffff;
        padding: 0;
        margin: 0;
    }
    
    /* Header Styles */
    .main-header {
        background: #ffffff;
        border-bottom: 1px solid #e5e5e5;
        padding: 0;
        position: sticky;
        top: 0;
        z-index: 1000;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
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
        background: linear-gradient(135deg, #00A651 0%, #00C853 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 20px;
        font-weight: 700;
        box-shadow: 0 2px 8px rgba(0, 166, 81, 0.3);
    }
    
    .logo-text {
        font-size: 24px;
        font-weight: 700;
        color: #1a1a1a;
        letter-spacing: -0.5px;
    }
    
    .nav-menu {
        display: flex;
        align-items: center;
        gap: 32px;
        list-style: none;
    }
    
    .nav-item {
        position: relative;
    }
    
    .nav-link {
        color: #1a1a1a;
        text-decoration: none;
        font-size: 15px;
        font-weight: 500;
        padding: 8px 0;
        transition: color 0.2s;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    
    .nav-link:hover {
        color: #0066CC;
    }
    
    .nav-link .dropdown-icon {
        font-size: 10px;
        margin-left: 4px;
    }
    
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
        border: none;
        font-size: 15px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        text-decoration: none;
        display: inline-block;
    }
    
    .btn-signup:hover {
        background: #008F45;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 166, 81, 0.3);
    }
    
    .btn-signin {
        background: #0066CC;
        color: white;
        padding: 10px 24px;
        border-radius: 6px;
        border: none;
        font-size: 15px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        text-decoration: none;
        display: inline-block;
    }
    
    .btn-signin:hover {
        background: #0052A3;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
    }
    
    .search-icon {
        width: 20px;
        height: 20px;
        cursor: pointer;
        opacity: 0.7;
        transition: opacity 0.2s;
    }
    
    .search-icon:hover {
        opacity: 1;
    }
    
    /* Hero Section */
    .hero-section {
        max-width: 1400px;
        margin: 0 auto;
        padding: 80px 24px;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 60px;
        align-items: center;
    }
    
    .hero-content {
        display: flex;
        flex-direction: column;
        gap: 24px;
    }
    
    .hero-title {
        font-size: 56px;
        font-weight: 800;
        line-height: 1.1;
        color: #1a1a1a;
        letter-spacing: -1.5px;
    }
    
    .hero-subtitle {
        font-size: 20px;
        font-weight: 400;
        color: #666666;
        line-height: 1.6;
        max-width: 540px;
    }
    
    .btn-primary {
        background: #0066CC;
        color: white;
        padding: 16px 32px;
        border-radius: 8px;
        border: none;
        font-size: 18px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        width: fit-content;
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
    }
    
    .btn-primary:hover {
        background: #0052A3;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 102, 204, 0.4);
    }
    
    .hero-image {
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
    }
    
    .phone-illustration {
        width: 100%;
        max-width: 500px;
        height: auto;
    }
    
    /* Partner Logos Section */
    .partners-section {
        background: #f8f9fa;
        padding: 60px 24px;
        margin-top: 80px;
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
        opacity: 0.6;
        transition: opacity 0.2s;
        filter: grayscale(100%);
        max-width: 120px;
        height: auto;
    }
    
    .partner-logo:hover {
        opacity: 1;
        filter: grayscale(0%);
    }
    
    /* Dashboard Content */
    .dashboard-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 40px 24px;
    }
    
    .section-title {
        font-size: 36px;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 32px;
        letter-spacing: -0.5px;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 24px;
        margin-bottom: 48px;
    }
    
    .stat-card {
        background: white;
        border: 1px solid #e5e5e5;
        border-radius: 12px;
        padding: 32px;
        text-align: center;
        transition: all 0.2s;
    }
    
    .stat-card:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        transform: translateY(-2px);
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
        transition: all 0.2s;
        cursor: pointer;
    }
    
    .tender-card:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        border-color: #0066CC;
    }
    
    .tender-header {
        display: flex;
        justify-content: space-between;
        align-items: start;
        margin-bottom: 16px;
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
        font-weight: 500;
    }
    
    .match-score {
        background: #00A651;
        color: white;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
    }
    
    .tender-details {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin-top: 16px;
    }
    
    .detail-item {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    
    .detail-label {
        font-size: 12px;
        color: #999999;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    
    .detail-value {
        font-size: 16px;
        color: #1a1a1a;
        font-weight: 500;
    }
    
    .btn-view-details {
        background: #0066CC;
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        border: none;
        font-size: 15px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        margin-top: 16px;
        width: 100%;
    }
    
    .btn-view-details:hover {
        background: #0052A3;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
    }
    
    /* Tabs Styling */
    .tabs-container {
        border-bottom: 2px solid #e5e5e5;
        margin-bottom: 32px;
    }
    
    .tabs-list {
        display: flex;
        gap: 8px;
        list-style: none;
    }
    
    .tab-item {
        padding: 16px 24px;
        font-size: 16px;
        font-weight: 500;
        color: #666666;
        cursor: pointer;
        border-bottom: 3px solid transparent;
        transition: all 0.2s;
    }
    
    .tab-item:hover {
        color: #0066CC;
    }
    
    .tab-item.active {
        color: #0066CC;
        border-bottom-color: #0066CC;
    }
    
    /* Content Cards */
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
        color: #1a1a1a;
        margin-bottom: 16px;
    }
    
    .card-content {
        font-size: 16px;
        color: #666666;
        line-height: 1.6;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-section {
            grid-template-columns: 1fr;
            padding: 40px 24px;
        }
        
        .hero-title {
            font-size: 36px;
        }
        
        .nav-menu {
            display: none;
        }
        
        .stats-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_tender' not in st.session_state:
    st.session_state.selected_tender = None

# Sample Tender Data
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
            'status': 'active'
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
            'status': 'active'
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
            'status': 'active'
        }
    ]

# Header Component
def render_header():
    st.markdown("""
    <div class="main-header">
        <div class="header-container">
            <a href="#" class="logo-section">
                <div class="logo-circle">✓</div>
                <div class="logo-text">Smart Tender</div>
            </a>
            
            <ul class="nav-menu">
                <li class="nav-item">
                    <a href="#" class="nav-link">Features <span class="dropdown-icon">▼</span></a>
                </li>
                <li class="nav-item">
                    <a href="#" class="nav-link">Solutions</a>
                </li>
                <li class="nav-item">
                    <a href="#" class="nav-link">Help & resources <span class="dropdown-icon">▼</span></a>
                </li>
                <li class="nav-item">
                    <a href="#" class="nav-link">Pricing</a>
                </li>
            </ul>
            
            <div class="header-actions">
                <a href="#" class="btn-signup">Sign up</a>
                <a href="#" class="btn-signin">Sign in</a>
                <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="11" cy="11" r="8"></circle>
                    <path d="m21 21-4.35-4.35"></path>
                </svg>
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
                Smart & efficient<br>
                tender management<br>
                with AI
            </h1>
            <p class="hero-subtitle">
                Say goodbye to manual bid preparation and embrace the convenience of AI-powered 
                tender management. Create, verify, sign, and submit government tenders faster 
                with legally binding digital signatures.
            </p>
            <button class="btn-primary" onclick="window.location.href='#dashboard'">
                Try Smart Tender now
            </button>
        </div>
        <div class="hero-image">
            <div style="width: 100%; max-width: 500px; height: 600px; background: linear-gradient(135deg, #0066CC 0%, #00A651 100%); border-radius: 30px; display: flex; align-items: center; justify-content: center; box-shadow: 0 20px 60px rgba(0,0,0,0.2);">
                <div style="color: white; text-align: center; padding: 40px;">
                    <div style="font-size: 120px; margin-bottom: 20px;">📋</div>
                    <div style="font-size: 32px; font-weight: 700; margin-bottom: 16px;">Smart Tender</div>
                    <div style="font-size: 18px; opacity: 0.9;">AI-Powered Platform</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Partners Section
def render_partners():
    st.markdown("""
    <div class="partners-section">
        <div class="partners-container">
            <div class="partners-title">Trusted by leading organizations</div>
            <div class="partners-grid">
                <div style="font-size: 24px; font-weight: 700; color: #666;">C-SQUARE</div>
                <div style="font-size: 24px; font-weight: 700; color: #666;">Fynd</div>
                <div style="font-size: 24px; font-weight: 700; color: #666;">Jio</div>
                <div style="font-size: 24px; font-weight: 700; color: #666;">Haptik</div>
                <div style="font-size: 24px; font-weight: 700; color: #666;">Reliance</div>
                <div style="font-size: 24px; font-weight: 700; color: #666;">Asteria</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Dashboard Page
def render_dashboard():
    st.markdown('<div id="dashboard"></div>', unsafe_allow_html=True)
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
    
    for tender in tenders:
        days_left = (tender['deadline'] - datetime.now()).days
        
        st.markdown(f"""
        <div class="tender-card">
            <div class="tender-header">
                <div>
                    <div class="tender-title">{tender['title']}</div>
                    <div class="tender-id">{tender['id']}</div>
                </div>
                <div class="match-score">{tender['match_score']}% Match</div>
            </div>
            
            <div class="tender-details">
                <div class="detail-item">
                    <div class="detail-label">Issuing Authority</div>
                    <div class="detail-value">{tender['authority']}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Tender Value</div>
                    <div class="detail-value">{tender['value']}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">EMD Required</div>
                    <div class="detail-value">{tender['emd']}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Category</div>
                    <div class="detail-value">{tender['category']}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Location</div>
                    <div class="detail-value">{tender['location']}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Deadline</div>
                    <div class="detail-value">{tender['deadline'].strftime('%d %b %Y, %I:%M %p')}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Days Left</div>
                    <div class="detail-value">{days_left} days</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"View Details & Prepare Bid", key=f"view_{tender['id']}", use_container_width=True):
            st.session_state.selected_tender = tender
            st.session_state.page = 'tender_details'
            st.rerun()

# Home Page
def render_home():
    render_header()
    render_hero()
    render_partners()
    
    # Add scroll to dashboard button
    st.markdown("""
    <div style="text-align: center; padding: 60px 24px;">
        <a href="#dashboard" style="background: #0066CC; color: white; padding: 16px 32px; border-radius: 8px; text-decoration: none; font-size: 18px; font-weight: 600; display: inline-block;">
            Explore Dashboard →
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    render_dashboard()

# Tender Details Page
def render_tender_details():
    render_header()
    
    if not st.session_state.selected_tender:
        st.markdown("""
        <div class="dashboard-container">
            <h2 class="section-title">No Tender Selected</h2>
            <p>Please go back to dashboard and select a tender.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("← Back to Dashboard"):
            st.session_state.page = 'home'
            st.rerun()
        return
    
    tender = st.session_state.selected_tender
    
    st.markdown(f"""
    <div class="dashboard-container">
        <h2 class="section-title">{tender['title']}</h2>
        <p style="font-size: 16px; color: #666; margin-bottom: 32px;">
            Tender ID: {tender['id']} | Authority: {tender['authority']}
        </p>
        
        <div class="tabs-container">
            <ul class="tabs-list">
                <li class="tab-item active">📄 Tender Analysis</li>
                <li class="tab-item">📝 Bid Preparation</li>
                <li class="tab-item">✅ Compliance Check</li>
                <li class="tab-item">✍️ Digital Signature</li>
                <li class="tab-item">📤 Submission</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tab Content
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📄 Tender Analysis", 
        "📝 Bid Preparation", 
        "✅ Compliance Check", 
        "✍️ Digital Signature", 
        "📤 Submission"
    ])
    
    with tab1:
        st.markdown("""
        <div class="content-card">
            <h3 class="card-title">🤖 AI-Powered Tender Analysis</h3>
            <div class="card-content">
                <p><strong>Turnover Requirement:</strong> ₹10 Crore in last 3 years</p>
                <p><strong>Experience:</strong> 3 similar orders in last 5 years</p>
                <p><strong>Certifications:</strong> ISO 9001, ISO 27001</p>
                <p><strong>Registration:</strong> GeM registered vendor</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        if st.button("🚀 Generate Bid Documents (AI-Powered)", type="primary", use_container_width=True):
            st.success("✅ Bid documents generated successfully!")
            st.info("💡 **Time Saved**: Documents generated in 2 minutes vs 40-80 hours manually!")
    
    with tab3:
        st.markdown("""
        <div class="content-card">
            <h3 class="card-title">✅ Compliance Score: 87%</h3>
            <div class="card-content">
                <p>✅ 12/18 Documents Ready</p>
                <p>⚠️ Missing: OEM Authorization, BIS Certificate</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("""
        <div class="content-card">
            <h3 class="card-title">✍️ Digital Signature Workflow</h3>
            <div class="card-content">
                <p>1. Upload Document ✅</p>
                <p>2. Add Participants ✅</p>
                <p>3. Manage Signature ⏳</p>
                <p>4. Review & Send ⏸️</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab5:
        st.markdown("""
        <div class="content-card">
            <h3 class="card-title">📤 Portal Submission</h3>
            <div class="card-content">
                <p>Ready to submit to GeM/eTenders portal</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'home'
        st.rerun()

# Main App
def main():
    if st.session_state.page == 'home':
        render_home()
    elif st.session_state.page == 'tender_details':
        render_tender_details()
    else:
        render_home()

if __name__ == "__main__":
    main()
