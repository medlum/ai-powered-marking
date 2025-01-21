import streamlit as st
from huggingface_hub import InferenceClient
from utils import *
from streamlit_extras.grid import grid
import streamlit as st
from pypdf import PdfReader
from streamlit_pdf_viewer import pdf_viewer

# ---------set up page config -------------#
st.set_page_config(page_title="AI-Powered Marking Assistant",
                   layout="wide",
                   page_icon="🐶",
                   initial_sidebar_state="expanded")

# ---------set button css-------------#

st.markdown(custom_css, unsafe_allow_html=True)

# --- Initialize the Inference Client with the API key ----#
client = InferenceClient(token=st.secrets.api_keys.huggingfacehub_api_token)

# ---------set model ------------#

if "model_select" not in st.session_state:
    st.session_state.model_select = "Qwen/Qwen2.5-72B-Instruct"
    
# ------- Store conversations with session state --------#
if 'msg_history' not in st.session_state:

    st.session_state.msg_history = []

    system_message = """
    - You are a lecturer from a polytechnic and has high expectations of the writing quality of reports written by your students. 
    - You are tasked to mark the student's internship report using the given marking rubrics available to you. 
    - The internship report is written after a 6 month internship program, and students should be able to articulate their
      learning experiences and share in-depth details about their work and what they learnt.
    - Assign a mark in the areas of:
            - Introduction
            - OJT Plan
            - Analysis and reflection on 3 experiences
            - Showcase of accomplished task/achievement
            - Diversity and inclusion
            - Influence of internship on future plan
            - Quality of writing

    - Write a short comment on each area after assigning the marks.
    - Tally the marks in each area.
    - Return the output with the areas, mark, comment in a table.
    - Return the total mark and overall comment as strings.
    """

    # system_message = """You are an AI assistant that are expert in coding."""

    st.session_state.msg_history.append(
        {"role": "system", "content": f"{system_message}"})

# ------- Set up header --------#
with st.sidebar:
    st.subheader("AI-Powered Marking")
    st.markdown(f'<span style="font-size:12px; color:gray;">{intro_var}</span>', unsafe_allow_html=True)
    st.divider()
    student_name = st.text_input(":blue[Enter student name]", placeholder="Name")
    model_id = st.selectbox(":blue[Select a model]", 
                            ["Qwen/Qwen2.5-72B-Instruct",
                            "Qwen/Qwen2.5-Coder-32B-Instruct",
                            "Qwen/QwQ-32B-Preview",
                            "meta-llama/Llama-3.3-70B-Instruct",
                            "meta-llama/Llama-3.1-8B-Instruct"
                            ],
                            index=0)
    
    upload_mark_rubric = st.file_uploader(":blue[Marking rubrics]", 'pdf')
    upload_student_report = st.file_uploader(":blue[Student's Internship report]", 'pdf')

if model_id:
    st.session_state.model_select = model_id

if upload_mark_rubric:

    mark_rubric = ""
    reader = PdfReader(upload_mark_rubric)
    num_pages = len(reader.pages)
    pages = reader.pages[:num_pages]
    for page in pages:
        mark_rubric += page.extract_text()

if upload_student_report:
    
    student_report = ""
    reader = PdfReader(upload_student_report)
    num_pages = len(reader.pages)
    pages = reader.pages[:num_pages]
    for page_num, page in enumerate(pages):
        student_report += page.extract_text()

    st.subheader(f"**Internship report has {num_pages} page(s)**")
    with st.container(height=400, border=True):
        pdf_viewer(upload_student_report.getvalue())

# ---- Input field for users to continue the conversation -----#

if st.sidebar.button(":material/search_insights: Evaluate Report"):

    st.session_state.msg_history.append({"role": "system",
                                             "content": f"Here are the marking rubrics to reference for marking: {mark_rubric}"})
    
    st.session_state.msg_history.append({"role": "system",
                                             "content": f"Mark this internship report: {student_report} for student name: {student_name}"})

    # ----- Create a placeholder for the streaming response ------- #
    with st.empty():
        # Stream the response

        stream = client.chat_completion(
            model=st.session_state.model_select,
            messages=st.session_state.msg_history,
            temperature=0.6,
            max_tokens=5524,
            top_p=0.7,
            stream=True,)

        # Initialize an empty string to collect the streamed content
        collected_response = ""

        # Stream the response and update the placeholder in real-time
        for chunk in stream:
            if 'delta' in chunk.choices[0] and 'content' in chunk.choices[0].delta:
                collected_response += chunk.choices[0].delta.content
                st.chat_message("assistant").write(collected_response)
        
        
    # Add the assistant's response to the conversation history
    st.session_state.msg_history.append(
        {"role": "assistant", "content": collected_response})
    
if st.sidebar.button(":material/refresh: Clear History"):

    del st.session_state.msg_history[1:]
    st.rerun()

    #evaluation = st.session_state.msg_history[-1]["content"]
    
    #st.download_button(label="Download Text", 
    #                   data=evaluation.encode('utf-8'), 
    #                   file_name="sample.text",
    #                   mime="text/plain")


