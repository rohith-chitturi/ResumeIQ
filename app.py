import streamlit as st
import time
from parser.pdf_parser import PDFParser
from embedding.vectorizer import EmbeddingService
from similarity.matcher import SemanticMatcher

@st.cache_resource
def get_embedding_service():
    """Caches the EmbeddingService so the model is only loaded once per session."""
    return EmbeddingService()
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
    st.markdown("### 📤 Upload Your Resume & Job Description")
    
    col_upload, col_jd = st.columns(2)
    
    with col_upload:
        uploaded_file = st.file_uploader("Upload your PDF resume", type=["pdf"], help="Limit 5MB. Only PDF files are supported.")
    
    with col_jd:
        job_description = st.text_area("Paste the Job Description (Optional)", height=100, placeholder="Paste the target job description here to see semantic matching...")
        
    if uploaded_file is not None:
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        
        with st.spinner("Extracting text from PDF..."):
            # Read the file bytes directly (no saving to disk!)
            pdf_bytes = uploaded_file.read()
            
            # Extract text using our single-responsibility parser
            extracted_text = PDFParser.extract_text_from_bytes(pdf_bytes)
            
            if extracted_text:
                st.session_state['resume_text'] = extracted_text
                
                with st.expander("📄 View Extracted Text (For Debugging)"):
                    st.text_area("Parsed Text", extracted_text, height=300, disabled=True)
                
                # We trigger the actual analysis
                if st.button("🚀 Analyze Resume with AI", use_container_width=True):
                    if not job_description.strip():
                        st.warning("⚠️ Please paste a Job Description to see the match percentage.")
                    else:
                        with st.spinner("🧠 Generating Semantic Embeddings..."):
                            embedder = get_embedding_service()
                            resume_emb = embedder.generate_embedding(extracted_text)
                            jd_emb = embedder.generate_embedding(job_description)
                            
                            score = SemanticMatcher.calculate_similarity(resume_emb, jd_emb)
                            match_percent = int(score * 100)
                            
                            st.markdown("---")
                            st.markdown("### 📊 Analysis Results")
                            
                            # Beautiful animated metric
                            col_metric, col_dummy = st.columns([1, 3])
                            with col_metric:
                                st.metric(label="Semantic Match Score", value=f"{match_percent}%", delta="vs Job Description")
                            
                            st.progress(score, text="Match Percentage")
                            
                            st.info("✨ In Phase 4, we will use Gemini LLM to rewrite your bullet points and provide ATS feedback!")
            else:
                st.error("Failed to extract text from the PDF. The file might be corrupted or scanned as an image.")

if __name__ == "__main__":
    main()
