import streamlit as st


def apply_custom_css(css_path='src/styles/custom_css.css'):
    """Apply custom CSS styling"""
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def display_title():
    st.markdown("""
        <h1 style='text-align: center; font-size: clamp(1.5rem, 2.5vw, 2.5rem); margin-bottom: 2rem;'>
        MaTOS 2024 - Social Media Analytics Dashboard
        </h1>
    """, unsafe_allow_html=True)

def create_tabs():
    return st.tabs(["📈 Engagement", "🔄 Time Series", "📊 Analysis"]) 