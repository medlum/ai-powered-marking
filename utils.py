

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



model_help = ":red[Model with less parameters is faster but often at the expense of a quality answer.]"

rubrics_help = ":red[Upload the marking rubrics in PDF.]"

report_help =":red[Upload a student's internship report in PDF]"

eval_btn_help = ":red[Click to evaluate the internship report]"

intro_var = """
:gray[Assistive marking AI uses specific marking rubrics to evaluate reports.
Marking rubrics ought to include a **criterion** column with the appropriate breakdown.]
"""

disclaimer_var = "Disclaimer: This AI-powered tool is designed to assist in marking reports by providing helpful suggestions and evaluations. However, it may occasionally make errors or misinterpret content. Final judgment and accuracy should be verified by a qualified evaluator."

creator_var = "Andy Oh is the creator behind this AI-powered tool, designed to transform how educators manage their workload by introducing an innovative solution to streamline their tasks." 