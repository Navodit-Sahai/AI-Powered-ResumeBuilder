# 📄 AI Resume Builder

An intelligent resume enhancement tool powered by Groq AI and LangChain that transforms your resume into a professional, ATS-optimized masterpiece.

🔗 **Live Demo**: [https://ai-powered-resumebuilder-ksjbmzztuyi2hmknprndd8.streamlit.app](https://ai-powered-resumebuilder-ksjbmzztuyi2hmknprndd8.streamlit.app)

📦 **GitHub Repository**: [https://github.com/Navodit-Sahai/AI-Powered-ResumeBuilder](https://github.com/Navodit-Sahai/AI-Powered-ResumeBuilder)

## ✨ Features

- **🤖 AI-Powered Enhancement**: Leverages Groq's Llama 3.3 70B model to optimize resume content
- **📊 ATS Scoring**: Comprehensive scoring system to evaluate resume compatibility with Applicant Tracking Systems
- **🎨 Multiple Templates**: Choose from Professional, Modern, and Academic template styles
- **📥 Multiple Format Support**: Upload resumes in PDF or DOCX format
- **📤 Dual Export**: Download enhanced resumes in both DOCX and PDF formats
- **💬 AI Chat Assistant**: Get personalized resume advice through an interactive chat interface
- **🔍 Smart Parsing**: Intelligent extraction of resume sections and information
- **✍️ Content Enhancement**: Transforms descriptions with strong action verbs and quantifiable achievements

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Groq API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Navodit-Sahai/AI-Powered-ResumeBuilder.git
   cd AI-Powered-ResumeBuilder
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the app**
   
   Open your browser and navigate to `http://localhost:8501`

## 📖 Usage

### Step 1: Upload Your Resume
- Click on the file uploader
- Select your resume (PDF or DOCX format)

### Step 2: Choose Template Style
Select from three professionally designed templates:
- **Professional**: Classic and formal - ideal for corporate roles
- **Modern**: Contemporary design - great for tech and creative fields
- **Academic**: Research-focused - perfect for academic positions

### Step 3: Enhance
- Click the "🚀 Enhance My Resume" button
- Wait for AI processing to complete

### Step 4: Review & Download
- Review ATS score improvements
- View enhanced resume text
- Download in DOCX or PDF format

### Chat Assistant
Ask questions like:
- "How can I improve my skills section?"
- "What action verbs should I use?"
- "How do I quantify my achievements?"

## 🏗️ Project Structure

```
ai-resume-builder/
├── app.py                          # Main Streamlit application
├── style.css                       # Custom styling
├── requirements.txt                # Python dependencies
├── pydantic_objects.py            # Data models
├── .env                           # Environment variables (create this)
├── .gitignore                     # Git ignore rules
│
├── src/
│   ├── agent/
│   │   └── ResumeAgent.py         # Main orchestration agent
│   │
│   ├── parsers/
│   │   └── parser.py              # PDF/DOCX parsing
│   │
│   ├── templates/
│   │   ├── professional_template.py
│   │   ├── modern_template.py
│   │   └── academic_template.py
│   │
│   └── tools/
│       ├── ats_service.py         # ATS scoring logic
│       ├── enhance_service.py     # AI content enhancement
│       ├── extraction_service.py  # Structured data extraction
│       └── render_service.py      # Document generation
│
└── output/                        # Generated resumes (auto-created)
```

## 🔧 Components

### Resume Parser
Extracts text from PDF and DOCX files using LangChain document loaders.

### ATS Scorer
Evaluates resumes based on:
- Keywords and relevance (20 points)
- Formatting and structure (20 points)
- Contact information (10 points)
- Quantifiable achievements (20 points)
- Appropriate length (10 points)
- Action verbs usage (20 points)

### Content Enhancer
Uses Groq's Llama model to:
- Strengthen action verbs
- Add professional language
- Optimize for ATS systems
- Improve clarity and impact

### Resume Generator
Creates beautifully formatted documents with:
- Professional typography
- Consistent styling
- ATS-friendly formatting
- Template-specific design elements

## 🎨 Template Styles

### Professional
- Classic corporate design
- Dark blue accent colors
- Traditional section organization
- Horizontal line separators

### Modern
- Contemporary visual style
- Colored backgrounds and sections
- Emoji icons for sections
- Tech-focused layout

### Academic
- Research-oriented format
- Education section prioritized
- Brown accent colors
- Publication-ready layout

## 🛠️ Technologies Used

- **Streamlit**: Web application framework
- **LangChain**: LLM orchestration and document processing
- **Groq AI**: High-performance LLM inference (Llama 3.3 70B)
- **python-docx**: DOCX file generation
- **ReportLab**: PDF file generation
- **PyPDF**: PDF text extraction
- **Pydantic**: Data validation and modeling

## 📊 ATS Scoring Breakdown

The ATS scorer evaluates your resume across multiple dimensions:

| Category | Points | What It Checks |
|----------|--------|----------------|
| Keywords | 20 | Relevant technical and industry terms |
| Formatting | 20 | Proper sections (Education, Experience, Skills) |
| Contact Info | 10 | Email and phone number presence |
| Achievements | 20 | Quantifiable results (percentages, numbers) |
| Length | 10 | Optimal word count (400-800 words) |
| Action Verbs | 20 | Strong verbs (developed, managed, led) |
| **Total** | **100** | Overall ATS compatibility score |

## 🎯 Best Practices

### Content Enhancement
- Use action verbs: "Developed", "Managed", "Led", "Implemented"
- Quantify achievements: "Increased sales by 35%"
- Include relevant keywords from job descriptions
- Keep descriptions concise and impactful

### Formatting
- Maintain clear section headings
- Use consistent formatting throughout
- Keep resume length between 1-2 pages
- Include all contact information

### Template Selection
- **Corporate/Finance**: Use Professional template
- **Tech/Startup**: Use Modern template
- **Research/Academia**: Use Academic template

## 🔐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Your Groq API key for AI features | Yes |

## 📝 API Rate Limits

Be aware of Groq API rate limits when processing multiple resumes. The application uses:
- **Model**: `llama-3.3-70b-versatile`
- **Temperature**: 0.3 for enhancement, 0.7 for chat

## 🐛 Troubleshooting

### Common Issues

**Resume not parsing correctly**
- Ensure the file is a valid PDF or DOCX
- Check that text is not embedded as images
- Try re-saving the file in a standard format

**Low ATS score**
- Add more relevant keywords
- Include quantifiable achievements
- Use strong action verbs
- Ensure all required sections are present

**Generated files not downloading**
- Check the `output/` directory permissions
- Ensure sufficient disk space
- Try refreshing the page

**API errors**
- Verify your Groq API key is correct
- Check your API rate limits
- Ensure stable internet connection

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Groq AI for providing high-performance LLM inference
- LangChain for excellent LLM tooling
- Streamlit for the intuitive web framework
- The open-source community for various libraries used

## 📧 Contact & Support

For issues, questions, or suggestions:
- Open an issue on [GitHub](https://github.com/Navodit-Sahai/AI-Powered-ResumeBuilder/issues)
- Visit the live demo: [AI Resume Builder](https://ai-powered-resumebuilder-ksjbmzztuyi2hmknprndd8.streamlit.app)

**Developer**: [Navodit Sahai](https://github.com/Navodit-Sahai)

## 🎓 Future Enhancements

- [ ] Job description matching analysis
- [ ] Multi-language support
- [ ] Cover letter generation
- [ ] LinkedIn profile optimization
- [ ] Industry-specific templates
- [ ] Resume comparison feature
- [ ] Export to more formats (LaTeX, HTML)
- [ ] Batch processing for multiple resumes

---

**Built with ❤️ by [Navodit Sahai](https://github.com/Navodit-Sahai) using Streamlit & LangChain**

© 2024 AI Resume Builder | Powered by Groq AI
