import streamlit as st


def apply_custom_css(css_path='src/styles/custom_css.css'):
    """Apply custom CSS styling"""
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def display_title():
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h1 style='font-size: 2.5rem; font-weight: 800; color: #1e293b; 
                      letter-spacing: -0.025em;'>
                MaTOS 2024
            </h1>
            <h2 style='color: #64748b; font-size: 1.1rem;'>
                Social Media Analytics Dashboard
            </h2>
        </div>
    """, unsafe_allow_html=True)

def create_tabs():
    return st.tabs(["📈 Engagement", "🔄 Time Series", "📊 Analysis"]) 