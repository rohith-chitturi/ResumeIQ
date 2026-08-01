import streamlit as st
import requests
import json
from fpdf import FPDF
import time

st.set_page_config(
    page_title="ResumeIQ - AI Platform",
    page_icon="🚀",
    layout="wide",
)

def create_pdf_report(result):
    """Creates a downloadable PDF report."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="ResumeIQ - AI Analysis Report", ln=1, align="C")
    pdf.ln(10)
    
    pdf.cell(200, 10, txt=f"Overall ATS Score: {result['ats_scores'].get('overall', 0)}/100", ln=1)
    
    if result.get("feedback"):
        pdf.ln(5)
        pdf.cell(200, 10, txt="Summary:", ln=1)
        pdf.multi_cell(0, 10, txt=result["feedback"].get("summary", ""))
        
        pdf.ln(5)
        pdf.cell(200, 10, txt="Missing Skills:", ln=1)
        for skill in result["feedback"].get("missing_skills", []):
            pdf.cell(200, 10, txt=f"- {skill}", ln=1)
            
    return pdf.output(dest='S').encode('latin1')

st.title("ResumeIQ 🚀 - Explainable AI Dashboard")
st.markdown("Upload a resume and job description to see a breakdown of the ATS score and AI feedback.")

col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])
with col2:
    jd = st.text_area("Job Description")

if st.button("Analyze with AI Pipeline"):
    if uploaded_file and jd:
        with st.spinner("Executing AI Orchestrator Pipeline..."):
            # Call backend API
            files = {"resume": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            data = {"job_description": jd}
            
            try:
                # In docker, it's http://backend:8000. Locally, it's localhost.
                # Assuming localhost for demo purposes if not overridden by env
                api_url = "http://localhost:8000/api/v1/analyze" 
                
                start_time = time.time()
                response = requests.post(api_url, files=files, data=data)
                response.raise_for_status()
                
                frontend_latency = (time.time() - start_time) * 1000
                
                result = response.json()
                
                st.success("Analysis Complete!")
                
                st.markdown("---")
                st.subheader("📊 Explainable ATS Scoring")
                
                scores = result.get("ats_scores", {})
                
                c1, c2, c3, c4, c5 = st.columns(5)
                c1.metric("Overall Score", f"{scores.get('overall', 0)}/100")
                c2.metric("Education", f"{scores.get('education', 0)}/100")
                c3.metric("Experience", f"{scores.get('experience', 0)}/100")
                c4.metric("Skills", f"{scores.get('skills', 0)}/100")
                c5.metric("Projects", f"{scores.get('projects', 0)}/100")
                
                st.markdown("---")
                st.subheader("⚡ AI Metrics (Observability)")
                m1, m2 = st.columns(2)
                backend_latency = result.get("metrics", {}).get("total_latency_ms", 0)
                m1.metric("Backend Inference Time", f"{backend_latency:.2f} ms")
                m2.metric("Total Roundtrip Time", f"{frontend_latency:.2f} ms")
                
                st.markdown("---")
                st.subheader("📝 AI Feedback (JSON Structure)")
                if result.get("feedback"):
                    st.json(result["feedback"])
                
                st.markdown("---")
                pdf_bytes = create_pdf_report(result)
                st.download_button(
                    label="📥 Export Report as PDF",
                    data=pdf_bytes,
                    file_name="resumeiq_report.pdf",
                    mime="application/pdf"
                )
                    
            except Exception as e:
                st.error(f"Error communicating with backend: {e}")
