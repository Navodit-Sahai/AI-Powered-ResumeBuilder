import streamlit as st
from src.agent.ResumeAgent import ResumeAgent
import tempfile
import os
import shutil

st.set_page_config(page_title="AI Resume Assistant", page_icon="📄", layout="wide")

@st.cache_resource
def load_agent():
    return ResumeAgent()

agent = load_agent()

st.title("📄 AI Resume Builder (Groq-Powered)")
st.write("Upload your resume, let AI enhance it, and download a polished version!")

with st.sidebar:
    st.header("🎨 Resume Template Style")
    template_style = st.selectbox(
        "Choose your preferred template",
        options=["professional", "modern", "academic"],
        index=0,
        help="Select the style that best fits your career field"
    )
    
    # Template descriptions
    template_info = {
        "professional": "📋 Classic and formal - ideal for corporate roles",
        "modern": "✨ Contemporary design - great for tech and creative fields",
        "academic": "🎓 Research-focused - perfect for academic positions"
    }
    st.info(template_info[template_style])

uploaded_file = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])

if st.button("🚀 Enhance My Resume"):
    if not uploaded_file:
        st.warning("Please upload a resume file first.")
    else:
        # Create a temporary folder for uploaded file
        temp_dir = tempfile.mkdtemp()
        file_ext = os.path.splitext(uploaded_file.name)[-1]
        file_path = os.path.join(temp_dir, f"uploaded_resume{file_ext}")

        try:
            # Save file to temp path
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

            st.info("⏳ Processing your resume... Please wait.")

            # Process through AI agent with template style
            result = agent.process_resume({
                "file_path": file_path,
                "template_style": template_style
            })

            # Display ATS Scores in three columns
            st.subheader("📊 ATS Score Comparison")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Initial ATS Score", 
                    f"{result['initial_score']['score']}/{result['initial_score']['max_score']}",
                    help="Score before AI enhancement"
                )
            
            with col2:
                st.metric(
                    "Enhanced ATS Score", 
                    f"{result['final_score']['score']}/{result['final_score']['max_score']}",
                    delta=f"+{result['final_score']['score'] - result['initial_score']['score']}",
                    help="Score after AI enhancement"
                )
            
            with col3:
                improvement = ((result['final_score']['score'] - result['initial_score']['score']) / 
                              result['initial_score']['score'] * 100)
                st.metric(
                    "Improvement", 
                    f"{improvement:.1f}%",
                    help="Percentage improvement in ATS score"
                )

            # Show enhanced text
            st.subheader("✨ Enhanced Resume Text")
            st.text_area("AI-Enhanced Resume", result['enhanced_text'], height=400)

            # Download Buttons
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

            st.success(f"✅ Resume successfully enhanced using **{template_style}** template!")

        except Exception as e:
            st.error(f"❌ Error while processing file: {e}")

        finally:
            # ✅ Clean up temporary files and directory
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                print(f"🧹 Deleted temporary directory: {temp_dir}")

st.markdown("---")
st.subheader("💬 Ask the AI for Resume Advice")
user_query = st.text_input("Ask something like 'How can I improve my skills section?'")

if user_query:
    with st.spinner("Thinking..."):
        response = agent.chat(user_query)
    st.write("🤖 **AI:**", response)