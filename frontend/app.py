import streamlit as st
import time
from parser.pdf_parser import PDFParser
from embedding.vectorizer import EmbeddingService
from similarity.matcher import SemanticMatcher
from llm.gemini_service import GeminiService

@st.cache_resource
def get_embedding_service():
    """Caches the EmbeddingService so the model is only loaded once per session."""
    return EmbeddingService()

@st.cache_resource
def get_gemini_service():
    """Caches the GeminiService."""
    return GeminiService()
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
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif !important;
            background-color: #131314 !important; /* Gemini dark background */
            color: #e3e3e3 !important;
        }

        /* Sidebar Override */
        [data-testid="stSidebar"] {
            background-color: #1e1e20 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        }

        /* Glassmorphism Cards */
        .glass-card {
            background: #1e1e20;
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 2rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .glass-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 28px rgba(0, 0, 0, 0.6), 0 0 15px rgba(155, 114, 203, 0.2);
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #ffffff !important;
            font-weight: 600 !important;
            letter-spacing: -0.5px;
        }

        /* Gemini Gradient Text */
        .gradient-text {
            background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570, #4285f4);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            animation: gradient-shimmer 4s linear infinite;
        }

        @keyframes gradient-shimmer {
            0% { background-position: 0% 50%; }
            100% { background-position: 200% 50%; }
        }

        /* Subtitle */
        .subtitle {
            font-size: 1.2rem;
            color: #a0aab4;
            margin-bottom: 2rem;
            font-weight: 400;
        }
        
        /* Custom Button (Pill shape with Gemini gradient) */
        .stButton>button {
            background: linear-gradient(90deg, #4285f4, #9b72cb, #d96570) !important;
            color: white !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 0.6rem 2.5rem !important;
            font-weight: 500 !important;
            font-size: 1.1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(155, 114, 203, 0.4) !important;
        }
        
        .stButton>button:hover {
            box-shadow: 0 6px 20px rgba(155, 114, 203, 0.6), 0 0 15px rgba(217, 101, 112, 0.4) !important;
            transform: scale(1.02) !important;
        }

        /* Inputs and Text Areas */
        .stTextArea>div>div>textarea, .stFileUploader>div {
            background-color: #1e1e20 !important;
            border-radius: 16px !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            color: #e3e3e3 !important;
            padding: 1rem !important;
        }
        .stTextArea>div>div>textarea:focus {
            border-color: #9b72cb !important;
            box-shadow: 0 0 10px rgba(155, 114, 203, 0.2) !important;
        }

        /* Progress bar */
        .stProgress > div > div > div > div {
            background-image: linear-gradient(90deg, #4285f4, #9b72cb, #d96570) !important;
        }

        /* Tags / Pills */
        .skill-pill {
            background: rgba(155, 114, 203, 0.15);
            border: 1px solid rgba(155, 114, 203, 0.3);
            color: #d8b4fe;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-right: 8px;
            display: inline-block;
            margin-bottom: 8px;
            backdrop-filter: blur(4px);
            transition: all 0.2s ease;
        }
        .skill-pill:hover {
            background: rgba(155, 114, 203, 0.25);
            border-color: rgba(155, 114, 203, 0.6);
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
                            
                        # Now call Gemini
                        with st.spinner("🤖 Analyzing resume with Gemini..."):
                            llm_service = get_gemini_service()
                            if llm_service.client is None:
                                st.error("Gemini API Key is missing. Please set it in your .env file.")
                            else:
                                feedback = llm_service.analyze_resume(extracted_text, job_description)
                                
                                if feedback:
                                    st.markdown("---")
                                    st.markdown("### 📝 ATS Feedback")
                                    st.info(feedback.match_summary)
                                    
                                    col_skills, col_bullets = st.columns(2)
                                    
                                    with col_skills:
                                        st.markdown("#### 🎯 Missing Skills")
                                        for skill in feedback.missing_skills:
                                            # Using a nice pill-like tag design
                                            st.markdown(f"<span class='skill-pill'>{skill}</span>", unsafe_allow_html=True)
                                            
                                    with col_bullets:
                                        st.markdown("#### ✨ Bullet Point Improvements")
                                        for i, bullet in enumerate(feedback.bullet_point_improvements):
                                            st.markdown(f"**{i+1}.** {bullet}")
                                            
                                else:
                                    st.error("Failed to generate feedback from Gemini. Check the logs.")
            else:
                st.error("Failed to extract text from the PDF. The file might be corrupted or scanned as an image.")

if __name__ == "__main__":
    main()
