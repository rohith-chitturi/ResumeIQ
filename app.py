import streamlit as st
import time

# Set page configuration must be the first Streamlit command
st.set_page_config(
    page_title="ResumeIQ - AI Resume Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

def load_css():
    """Injects custom CSS for a premium Glassmorphism dark-mode UI."""
    st.markdown("""
        <style>
        /* Base Dark Mode & Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            background-color: #0d1117;
            color: #c9d1d9;
        }

        /* Glassmorphism Cards */
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 2rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .glass-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #58a6ff !important;
            font-weight: 700 !important;
        }

        /* Gradient Text for Main Title */
        .gradient-text {
            background: linear-gradient(90deg, #58a6ff, #8a2be2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }

        /* Subtitle */
        .subtitle {
            font-size: 1.2rem;
            color: #8b949e;
            margin-bottom: 2rem;
        }
        
        /* Custom Button */
        .stButton>button {
            background: linear-gradient(90deg, #58a6ff, #8a2be2) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.5rem 2rem !important;
            font-weight: 600 !important;
            transition: opacity 0.3s ease !important;
        }
        
        .stButton>button:hover {
            opacity: 0.8 !important;
            color: white !important;
        }
        
        </style>
    """, unsafe_allow_html=True)

def main():
    """Main function to render the Streamlit app."""
    load_css()

    # Sidebar Navigation
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        st.radio(
            "Go to",
            ["Dashboard", "Upload Resume", "Analytics", "Settings"],
            label_visibility="collapsed"
        )
        st.markdown("---")
        st.markdown("<div style='text-align: center; color: #8b949e;'>ResumeIQ v1.0</div>", unsafe_allow_html=True)

    # Main Content Area
    st.markdown('<div class="gradient-text">ResumeIQ 🚀</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">AI-Powered Resume Analysis & Optimization</div>', unsafe_allow_html=True)

    # Dashboard Cards using Columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3>📄 Smart Parsing</h3>
            <p>Accurately extract text, skills, and experience from your PDFs using advanced NLP techniques.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3>🧠 Semantic Matching</h3>
            <p>Compare your profile against job descriptions using state-of-the-art vector embeddings.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="glass-card">
            <h3>✨ AI Optimization</h3>
            <p>Get actionable ATS feedback and intelligently rewrite bullet points with the Antigravity LLM.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📤 Upload Your Resume")
    st.info("The upload and analysis pipeline will be implemented in the next phase!")

    # A simple demo button with loading animation
    if st.button("Start Analysis (Demo)"):
        with st.spinner("Initializing AI Engines..."):
            time.sleep(1.5)
            st.success("ResumeIQ is ready for development!")

if __name__ == "__main__":
    main()
