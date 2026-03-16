import streamlit as st
from app.pages.planning_studio import show_page as show_planning_studio
from app.pages.receipt_generator import show_page as show_receipt_generator
from app.pages.financial_dashboard import show_page as show_financial_dashboard
import os

# Page configuration
st.set_page_config(
    page_title="Stone Bar Studio",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "static", "styles.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load CSS
load_css()

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = "Planning Studio"

# Sidebar with logo
st.sidebar.markdown("""
<div class="logo-container">
    <div class="logo-text">STONE BAR STUDIO</div>
    <div class="logo-subtitle">Custom Outdoor Stone Bars</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select a feature:",
    ["Planning Studio", "Invoice Generator", "Financial Dashboard"],
    index=["Planning Studio", "Invoice Generator", "Financial Dashboard"].index(st.session_state.page)
)
st.session_state.page = page

# Page routing
if page == "Planning Studio":
    show_planning_studio()
elif page == "Invoice Generator":
    show_receipt_generator()
elif page == "Financial Dashboard":
    show_financial_dashboard()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Stone Bar Studio v1.2**")
st.sidebar.markdown("Custom outdoor stone bars built by Stone Bar Studio, San Antonio, TX")