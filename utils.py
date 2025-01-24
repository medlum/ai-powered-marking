

# custom CSS for buttons
btn_css = """
<style>
    .stButton > button {
        color: #383736; 
        border: none; /* No border */
        padding: 5px 22px; /* Reduced top and bottom padding */
        text-align: center; /* Centered text */
        text-decoration: none; /* No underline */
        display: inline-block; /* Inline-block */
        font-size: 8px !important;
        margin: 4px 2px; /* Some margin */
        cursor: pointer; /* Pointer cursor on hover */
        border-radius: 30px; /* Rounded corners */
        transition: background-color 0.3s; /* Smooth background transition */
    }
    .stButton > button:hover {
        color: #383736; 
        background-color: #c4c2c0; /* Darker green on hover */
    }
</style>
"""

image_css = """
<style>
.stImage img {
    border-radius: 50%;
    #border: 5px solid #f8fae6;
}
</style>

"""


system_message_var = """
- Mark the student's internship report using the given marking rubrics available to you. 
- The internship report is written after a 6 month internship program, and students should be able to articulate their
learning experiences and share in-depth details about their work and what they learnt.
- Assign a mark in the criterion of:
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
- Return the total mark and overall comment in strings.

"""



model_help = ":blue[Models with less parameters have faster inference speed but often at the expense of a more quality answer.]"

rubrics_help = ":blue[Upload a set of marking rubrics with a **criterion** column in PDF.]"

report_help =":blue[Report with more than 3,000 words may experience '*max limit token error*'. Click on **Clear History** and try again.]"

eval_btn_help = ":blue[Click to evaluate the internship report]"

intro_var = """
:blue[While AI marking can help with consistency and efficiency, it's crucial to review and verify the marks and feedback generated.]
"""

disclaimer_var = "Disclaimer: This AI-powered tool is designed to assist in marking reports by providing helpful suggestions and evaluations. However, it may occasionally make errors or misinterpret content. Final judgment and accuracy should be verified by a qualified evaluator."

creator_var = "Andy Oh is the creator behind this AI-powered tool, designed to transform how educators manage their workload by introducing an innovative solution to streamline their tasks." 