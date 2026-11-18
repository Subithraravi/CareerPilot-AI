import streamlit as st
import tempfile
from pathlib import Path

from src.services.document_service import extract_document_text

# --------------------------------
# 1. Page configuration
# --------------------------------
def read_uploaded_file(uploaded_file):
    """Read text from an uploaded PDF, DOCX, or TXT file."""

    if uploaded_file is None:
        return ""

    filename = uploaded_file.name
    extension = Path(filename).suffix.lower()

    if uploaded_file.size > 5 * 1024 * 1024:
        raise ValueError("File size must be below 5 MB.")

    if extension == ".txt":
        return uploaded_file.getvalue().decode(
            "utf-8",
            errors="replace",
        )

    if extension not in [".pdf", ".docx"]:
        raise ValueError("Unsupported file format.")

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension,
        ) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_path = temp_file.name

        return extract_document_text(temp_path, filename)

    finally:
        if temp_path:
            Path(temp_path).unlink(missing_ok=True)

            
st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide",
)

# --------------------------------
# 2. Application title
# --------------------------------

st.title("🚀 CareerPilot AI")

st.subheader(
    "Your Agentic AI Career, Resume & Interview Assistant"
)

st.write(
    "Upload your resume, understand skill gaps, "
    "prepare for interviews, and build your GenAI career."
)

# --------------------------------
# 3. Sidebar navigation
# --------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a feature",
    [
        "Dashboard",
        "Resume Analyzer",
        "Job Match",
        "RAG Career Chat",
        "Interview Coach",
        "Learning Roadmap",
    ],
)

# --------------------------------
# 4. Dashboard
# --------------------------------

if page == "Dashboard":

    st.header("Welcome to CareerPilot AI")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="AI Agents",
            value="Coming Soon",
        )

    with col2:
        st.metric(
            label="RAG Knowledge Base",
            value="Not Connected",
        )

    with col3:
        st.metric(
            label="Resume Analysis",
            value="Ready to Build",
        )

    st.info(
        "This is the initial UI. "
        "We will connect the LLM, RAG pipeline, "
        "agent workflow, MCP tools, and APIs in later stages."
    )

# --------------------------------
# 5. Placeholder pages
# --------------------------------

elif page == "Resume Analyzer":

    st.header("📄 Resume Analyzer")

    st.write(
        "Upload your resume to extract its text."
    )

    uploaded_resume = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx"],
        key="resume_upload",
    )

    if uploaded_resume is not None:

        file_name = uploaded_resume.name

        if uploaded_resume.size > 5 * 1024 * 1024:
            st.error("File is too large. Maximum size is 5 MB.")

        else:
            try:
                suffix = Path(file_name).suffix.lower()

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix,
                ) as temp_file:

                    temp_file.write(uploaded_resume.getvalue())
                    temp_path = temp_file.name

                try:
                    extracted_text = extract_document_text(
                        temp_path,
                        file_name,
                    )
                finally:
                    Path(temp_path).unlink(missing_ok=True)

                if extracted_text:
                    st.success("Resume text extracted successfully!")

                    st.text_area(
                        "Extracted Resume Text",
                        value=extracted_text,
                        height=350,
                    )

                    st.caption(
                        "This is text extraction only. "
                        "AI analysis will be added next."
                    )

                else:
                    st.warning(
                        "No text found. "
                        "The PDF may be scanned or image-based."
                    )

            except Exception as error:
                st.error(
                    f"Unable to process this file: {error}"
                )

elif page == "Job Match":

    st.header("🎯 Resume–Job Match")

    st.write(
        "We will compare your resume with "
        "a job description and identify skill gaps."
    )

elif page == "RAG Career Chat":

    st.header("💬 RAG Career Assistant")

    st.write(
        "Ask questions based on your uploaded "
        "career documents and job descriptions."
    )

elif page == "Interview Coach":

    st.header("🎤 Interview Coach")

    st.write(
        "Practise technical questions and "
        "receive feedback on your answers."
    )

elif page == "Learning Roadmap":

    st.header("🗺️ Learning Roadmap")

    st.write(
        "Generate a personalised learning plan "
        "based on your target role and skill gaps."
    )

# --------------------------------
# 6. Footer
# --------------------------------

st.divider()

st.caption(
    "CareerPilot AI | Built with Python and Streamlit"
)