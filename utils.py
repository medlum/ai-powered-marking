

# custom CSS for buttons
custom_css = """
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


intro_var = """
This app marks using specific marking rubrics from INT6. 
It includes introduction, OJT Plan, analysis and reflection on 3 experiences, 
showcase of accomplished task/achievement, diversity and inclusion, influence of internship on future plan and quality of writing.

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

model_help = ":red[Model with less than 32B parameter are faster but at the expense of a better answer.]"

rubrics_help = ":red[Upload the marking rubrics from INT6 in PDF]"

report_help =":red[Upload a student's internship report in PDF]"

eval_btn_help = ":red[Click to evaluate the internship report]"