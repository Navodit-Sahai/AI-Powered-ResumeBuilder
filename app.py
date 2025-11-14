import streamlit as st
from src.agent.ResumeAgent import ResumeAgent
import tempfile
import os
import shutil

# Initialize Streamlit page
st.set_page_config(
    page_title="AI Resume Builder", 
    page_icon="📄", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load external or fallback CSS
def load_css():
    css_file = "style.css"
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.markdown("""<style>body{background:#000;color:#fff}</style>""", unsafe_allow_html=True)

load_css()

# Load AI resume agent once
@st.cache_resource
def load_agent():
    return ResumeAgent()

agent = load_agent()

# Header section
st.markdown("""
<div class="app-header">
    <h1>📄 AI Resume Builder</h1>
    <p>Powered by Groq AI - Transform your resume into a professional masterpiece</p>
</div>
""", unsafe_allow_html=True)

# Sidebar (template selection & instructions)
with st.sidebar:
    st.markdown('<div class="sidebar-info">', unsafe_allow_html=True)
    st.header("🎨 Resume Template Style")

    template_style = st.selectbox(
        "Choose your preferred template",
        options=["professional", "modern", "academic"],
        index=0,
        help="Select the style that best fits your career field"
    )

    template_info = {
        "professional": "📋 Classic and formal - ideal for corporate roles",
        "modern": "✨ Contemporary design - great for tech and creative fields",
        "academic": "🎓 Research-focused - perfect for academic positions"
    }
    st.info(template_info[template_style])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="sidebar-info">
        <h3>ℹ️ How It Works</h3>
        <ol>
            <li>Upload your resume</li>
            <li>Select template style</li>
            <li>Click Enhance</li>
            <li>Download resume</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# Resume upload section
st.markdown('<div class="info-card">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("📤 Upload Your Resume (PDF or DOCX)", type=["pdf", "docx"])
st.markdown('</div>', unsafe_allow_html=True)

# Process resume when user clicks enhance
if st.button("🚀 Enhance My Resume"):
    if not uploaded_file:
        st.warning("⚠️ Please upload a resume file first.")
    else:
        # Create temporary workspace
        temp_dir = tempfile.mkdtemp()
        file_ext = os.path.splitext(uploaded_file.name)[-1]
        file_path = os.path.join(temp_dir, f"uploaded_resume{file_ext}")

        try:
            # Save uploaded file locally
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

            # Run AI resume enhancement
            with st.spinner("⏳ Processing your resume..."):
                result = agent.process_resume({
                    "file_path": file_path,
                    "template_style": template_style
                })

            # Show ATS scores
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.subheader("📊 ATS Score Comparison")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric("Initial ATS Score",
                          f"{result['initial_score']['score']}/{result['initial_score']['max_score']}")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric("Enhanced Score",
                          f"{result['final_score']['score']}/{result['final_score']['max_score']}",
                          delta=f"+{result['final_score']['score'] - result['initial_score']['score']}")
                st.markdown('</div>', unsafe_allow_html=True)

            with col3:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                improvement = (
                    (result['final_score']['score'] - result['initial_score']['score'])
                    / result['initial_score']['score'] * 100
                )
                st.metric("Improvement", f"{improvement:.1f}%")
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

            # Show enhanced resume text
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.subheader("✨ Enhanced Resume Text")
            st.text_area("AI-Enhanced Resume",
                         result['enhanced_text'],
                         height=400,
                         key="enhanced_resume")
            st.markdown('</div>', unsafe_allow_html=True)

            # Download section
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.subheader("📥 Download Your Resume")
            col1, col2 = st.columns(2)

            with col1:
                with open(result['docx_path'], "rb") as docx_file:
                    st.download_button(
                        label="📄 Download Word Resume (.docx)",
                        data=docx_file,
                        file_name=f"Enhanced_Resume_{template_style}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

            with col2:
                with open(result['pdf_path'], "rb") as pdf_file:
                    st.download_button(
                        label="📑 Download PDF Resume (.pdf)",
                        data=pdf_file,
                        file_name=f"Enhanced_Resume_{template_style}.pdf",
                        mime="application/pdf"
                    )

            st.markdown('</div>', unsafe_allow_html=True)
            st.success(f"✅ Resume enhanced using **{template_style}** template!")

        except Exception as e:
            st.error(f"❌ Error while processing: {e}")

        finally:
            # Cleanup temporary files
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

# Chat section for resume advice
st.markdown("---")
st.markdown('<div class="info-card">', unsafe_allow_html=True)
st.subheader("💬 Ask the AI for Resume Advice")

user_query = st.text_input("Ask something like 'How can I improve my skills section?'")

if user_query:
    with st.spinner("🤔 Thinking..."):
        response = agent.chat(user_query)

    st.markdown(f"""
    <div style="background: linear-gradient(135deg,#f5f7fa,#c3cfe2);
                padding:1.5rem;
                border-radius:10px;
                margin-top:1rem;
                border-left:4px solid #667eea;">
        <p><strong>🤖 AI:</strong> {response}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center;padding:2rem;color:#666;">
    <p>© 2024 AI Resume Builder | Powered by Groq AI</p>
    <p style="font-size:0.9rem;">Built with ❤️ using Streamlit & LangChain</p>
</div>
""", unsafe_allow_html=True)
