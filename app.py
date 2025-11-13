import streamlit as st
from src.agent.ResumeAgent import ResumeAgent
import tempfile
import json
import os

st.set_page_config(page_title="AI Resume Assistant", page_icon="📄", layout="wide")

# Initialize the agent
@st.cache_resource
def load_agent():
    return ResumeAgent()

agent = load_agent()

# App title
st.title("📄 AI Resume Builder (Groq-Powered)")
st.write("Upload your resume, let AI enhance it, and download a polished version!")

# Sidebar for job description
with st.sidebar:
    st.header("🧠 Job Description (Optional)")
    job_desc = st.text_area("Paste a job description to optimize your resume", height=200)

# File uploader
uploaded_file = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])

# Run button
if st.button("🚀 Enhance My Resume"):
    if not uploaded_file:
        st.warning("Please upload a resume file first.")
    else:
        # Save temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as tmp_file:
            tmp_file.write(uploaded_file.read())
            file_path = tmp_file.name

        st.info("⏳ Processing your resume... Please wait.")
        try:
            # Process resume
            result = agent.process_resume({
                "file_path": file_path,
                "job_description": job_desc
            })

            # Display ATS scores
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Initial ATS Score", f"{result['initial_score']['score']}/{result['initial_score']['max_score']}")
            with col2:
                st.metric("Final ATS Score", f"{result['final_score']['score']}/{result['final_score']['max_score']}")

            # Show enhanced resume text
            st.subheader("✨ Enhanced Resume Text")
            st.text_area("AI-Enhanced Resume", result['enhanced_text'], height=400)

            # Download buttons
            st.download_button(
                label="📄 Download Word Resume (.docx)",
                data=open(result['docx_path'], "rb").read(),
                file_name="Enhanced_Resume.docx"
            )
            st.download_button(
                label="📑 Download PDF Resume (.pdf)",
                data=open(result['pdf_path'], "rb").read(),
                file_name="Enhanced_Resume.pdf"
            )

        except Exception as e:
            st.error(f"❌ Error: {e}")

# Optional chat section
st.markdown("---")
st.subheader("💬 Ask the AI for Resume Advice")
user_query = st.text_input("Ask something like 'How can I improve my skills section?'")

if user_query:
    with st.spinner("Thinking..."):
        response = agent.chat(user_query)
    st.write("🤖 **AI:**", response)
