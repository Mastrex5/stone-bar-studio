import streamlit as st
from app.pages.planning_studio import show_page as show_planning_studio
from app.pages.receipt_generator import show_page as show_receipt_generator

# Page configuration
st.set_page_config(
    page_title="Stone Bar Studio",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = "Planning Studio"

# Sidebar navigation
st.sidebar.title("Stone Bar Studio")
page = st.sidebar.radio(
    "Select a feature:",
    ["Planning Studio", "Invoice Generator", "Dashboard"],
    index=["Planning Studio", "Invoice Generator", "Dashboard"].index(st.session_state.page)
)
st.session_state.page = page

# Page routing
if page == "Planning Studio":
    show_planning_studio()
elif page == "Invoice Generator":
    show_receipt_generator()
elif page == "Dashboard":
    st.title("Financial Dashboard")
    st.info("Coming soon: Real-time profit tracking and splits for the team.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Stone Bar Studio v1.0**")
st.sidebar.markdown("Custom outdoor stone bars built by Stone Bar Studio, San Antonio, TX")