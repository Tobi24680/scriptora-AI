import os
from crewai import Agent, Task, Crew
from crewai.llm import LLM
import streamlit as st

# PDF Imports
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

HF_TOKEN = os.getenv("HF_TOKEN")

llm = LLM(
    model="google/gemini-2.5-flash-lite",
    api_key=HF_TOKEN
)

researcher = Agent(
    role="Researcher",
    goal="Research topic clearly",
    backstory="Expert researcher",
    llm=llm
)

writer = Agent(
    role="Writer",
    goal="Write simple article",
    backstory="Professional writer",
    llm=llm
)

def run_crew(topic: str):
    task1 = Task(
        description=f"Research about {topic}",
        expected_output="A comprehensive research summary",
        agent=researcher
    )

    task2 = Task(
        description=f"Write an article about {topic}",
        expected_output="A well-written article",
        agent=writer
    )

    crew = Crew(
        agents=[researcher, writer],
        tasks=[task1, task2]
    )

    return crew.kickoff()


# ✅ PROFESSIONAL PDF FUNCTION
def create_pdf(title, content, filename="Scriptora_Article.pdf"):

    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title Style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=22,
        textColor=colors.HexColor("#5A189A"),
        spaceAfter=20
    )

    # Heading Style
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor("#240046"),
        spaceAfter=10
    )

    normal_style = styles["Normal"]

    # Add Title
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 0.3 * inch))

    # Format Content
    for line in content.split("\n"):

        line = line.strip()

        if line.startswith("#"):
            clean_heading = line.replace("#", "").strip()
            elements.append(Paragraph(clean_heading, heading_style))

        elif line.isupper():
            elements.append(Paragraph(line, heading_style))

        else:
            elements.append(Paragraph(line, normal_style))

        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)
    return filename


if __name__ == "__main__":

    st.set_page_config(page_title="Scriptora AI", page_icon="🖋️", layout="wide")

    # Button Hover Style
    st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #7B2CBF;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        height: 3em;
        width: 100%;
        transition: 0.3s ease-in-out;
    }
    div.stButton > button:first-child:hover {
        background-color: #9D4EDD;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.title("🖋️ Scriptora AI")
        st.markdown("*An Autonomous Research And Writing Intelligence Agent*")
        st.divider()
        st.info("Scriptora uses multi-agents to ensure high-quality drafts.")
        st.divider()

        st.markdown("## About the Developer")
        st.markdown("""
        **SHREERAM M K**  
        AI & ML Developer | Multi-Agent Systems Enthusiast  
        Passionate about building intelligent AI systems 
        that automate research, writing, and productivity workflows.
        """)

        st.divider()
        st.markdown("📧 Email: sumathidevan2005@gmail.com")
        st.markdown("💻 GitHub: https://github.com/Tobi24680")

        st.divider()
        st.caption("Scriptora AI...")
        st.caption("© 2026 Scriptora AI")
        st.caption("Engineering the future of Research and Writing")

    # Main UI
    st.title("Draft Your Next Masterpiece")
    st.title("SCRIPTORA AI")

    st.markdown("""
    Welcome to Scriptora AI, your autonomous research and writing assistant. 
    Enter a topic below and let our multi-agent crew generate a comprehensive article for you.
    """)

    st.markdown("### How It Works")
    st.markdown("1. **Input Your Topic**")
    st.markdown("2. **Generate Content**")
    st.markdown("3. **Download Your Article as PDF**")

    st.divider()

    topic_input = st.text_input(
        "Enter your topic or headline:",
        placeholder="The future of AI..."
    )

    if st.button("Generate with Scriptora"):
        if topic_input:
            with st.status("Scriptora Multi Agents System is Initializing...", expanded=True) as status:
                st.write("🔍 Conducting deep research analysis...")
                result = run_crew(topic_input)
                status.update(label="Research Complete!", state="complete", expanded=False)

            st.markdown("---")

            article_content = result.raw
            st.markdown(article_content)

            # Create Professional PDF
            pdf_file = create_pdf(topic_input, article_content)

            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="📥 Download Article as PDF",
                    data=f,
                    file_name="Scriptora_Article.pdf",
                    mime="application/pdf"
                )

        else:
            st.warning("Please provide a research topic to get started.")

    st.markdown("---")
    st.caption("© 2026 Scriptora AI | Developed By SHREERAM M K | All rights reserved.")
    st.caption("Discover . Draft . Deliver .")
    st.caption("Disclaimer: Generated content should be reviewed before use.")
