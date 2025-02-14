import streamlit as st
from huggingface_hub import InferenceClient
from utils import *
from streamlit_extras.grid import grid
from pypdf import PdfReader
from streamlit_pdf_viewer import pdf_viewer

# ---------set up page config -------------#
st.set_page_config(page_title="Assistive Marking AI Tool",
                   layout="wide",
                   page_icon="🐶",
                   initial_sidebar_state="expanded")

# ---------set css-------------#
st.markdown(btn_css, unsafe_allow_html=True)
st.markdown(image_css, unsafe_allow_html=True)

# --- Initialize the Inference Client with the API key ----#
try:
    client = InferenceClient(token=st.secrets.api_keys.huggingfacehub_api_token)
except Exception as e:
    st.error(f"Error initializing Inference Client: {e}")
    st.stop()

# ---------set model ------------#
if "model_select" not in st.session_state:
    st.session_state.model_select = "Qwen/Qwen2.5-72B-Instruct"

# ------- initialize first system message --------#
if 'msg_history' not in st.session_state:
    st.session_state.msg_history = []
    system_message = """
    Your name is Cosmo, a friendly AI assistant to a teacher that provides helpful assistance.
    Prompt the user to upload the marking rubrics and student's report if it is not available in your system.
    Look back at the chat history to find information if needed.
    """
    st.session_state.msg_history.append(
        {"role": "system", "content": f"{system_message}"}
    )

# ------- write chat conversations of session state --------#
for msg in st.session_state.msg_history:
    if msg['role'] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# ------- create side bar --------#
with st.sidebar:
    st.title(":rainbow[Cosmo]. :gray[Your friendly assistive marking AI]", help=intro_var)
    st.image('cosmo.jpeg', width=80)
    student_name = st.text_input(":blue[**Enter student name**]", placeholder="Name")
    model_id = st.selectbox(":blue[**Select an AI model**]", 
                            ["Qwen/Qwen2.5-72B-Instruct",
                             "Qwen/Qwen2.5-Coder-32B-Instruct",
                             "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
                             #"Qwen/QwQ-32B-Preview",
                             "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF",
                             "meta-llama/Llama-3.3-70B-Instruct",
                             "meta-llama/Llama-3.1-8B-Instruct"],
                            index=0,
                            help=model_help)
    
    upload_mark_rubric = st.file_uploader(":blue[**Upload marking rubrics**]", 'pdf', help=rubrics_help)
    upload_student_report = st.file_uploader(":blue[**Upload a report**]", 'pdf', help=report_help)
    evaluate_btn = st.button(":material/search_insights: Evaluate Report", type="primary")
    clear_btn = st.button(":material/refresh: Clear History", type="primary")
    st.markdown(f'<span style="font-size:12px; color:gray;">{disclaimer_var}</span>', unsafe_allow_html=True)
    
    #<div class="stImage st-emotion-cache-1dvmtd8 e1wa958q0" data-testid="stImage"><div data-testid="stImageContainer" class="st-emotion-cache-1v0mbdj e1wa958q1"><img src="http://localhost:8501/media/31bb050bccea069e88f4266924aea2d4d2e1dea57405cc3e795a6803.jpg" alt="0" style="width: 100px; max-width: 100%;"></div></div>
# -- set model to session state ---# 
if model_id:
    st.session_state.model_select = model_id

#--- extract pdf and add to session state---#
if upload_mark_rubric:
    try:
        #st.toast("Mark rubrics uploaded!", icon="✅")
        mark_rubric = ""
        reader = PdfReader(upload_mark_rubric)
        for page in reader.pages:
            mark_rubric += page.extract_text()
        st.session_state.msg_history.append({
            "role": "system",
            "content": f"Use this marking rubrics to reference for assigning marks: {mark_rubric}"
        })
    except Exception as e:
        st.error(f"Error processing marking rubrics: {e}")

if upload_student_report:
    try:
        #st.toast("Report uploaded!", icon="✅")
        student_report = ""
        reader = PdfReader(upload_student_report)
        for page in reader.pages:
            student_report += page.extract_text()
        st.session_state.msg_history.append({
            "role": "system",
            "content": f"Mark this report: {student_report} for student name: {student_name}"
        })
    except Exception as e:
        st.error(f"Error processing student report: {e}")

# ------- if evaluate button click, set mark task to system --------#
button_pressed = ""

if evaluate_btn:
    try:
        with st.sidebar:
            st.divider()
            st.write(":grey[**Report Preview**]")
            pdf_viewer(upload_student_report.getvalue())
            
        system_message = """
        - Mark the student's report using the given marking rubrics available to you. 
        - Assign a mark for each of the criterion in the marking rubrics.
        - Do not assign more than the maximum mark found in each criterion.
        - Write a feedback for each criterion on the areas that are good or lacking and cite specific examples.
        - Tally the marks in each area.
        - Return the output with the areas, mark, comment in a table.
        - Return the total mark and an overall comment in strings.    
        """
        st.session_state.msg_history.append({
            "role": "system", "content": f"{system_message}"
        })
        button_pressed = "Please mark the report using the marking rubric given to you."
    except Exception as e:
        st.error(f"Error during evaluation: {e}")

# ---- Input field for users to continue the conversation -----#
if user_input := (st.chat_input("How would you like to refine the report?") or button_pressed):
    st.session_state.msg_history.append({"role": "user", "content": user_input})
    if not button_pressed:
        st.chat_message("user").write(user_input)
    try:
        with st.empty():
            stream = client.chat_completion(
                model=st.session_state.model_select,
                messages=st.session_state.msg_history,
                temperature=0.6,
                max_tokens=5524,
                top_p=0.7,
                stream=True,
            )
            collected_response = ""
            for chunk in stream:
                if 'delta' in chunk.choices[0] and 'content' in chunk.choices[0].delta:
                    collected_response += chunk.choices[0].delta.content
                    st.chat_message("assistant").write(collected_response)
            st.session_state.msg_history.append({
                "role": "assistant", "content": collected_response
            })
    except Exception as e:
        st.error(f"Error generating response: {e}")

if clear_btn:
    try:
        del st.session_state.msg_history[1:]
        st.rerun()
    except Exception as e:
        st.error(f"Error clearing history: {e}")




# Load your image

