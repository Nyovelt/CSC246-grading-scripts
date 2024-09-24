import pandas as pd
from submission_loader import load_submissions, update_submissions
from grade import GRADESCOPE_EXPORT_DIR
from grade_submission import grade_submission
def grade(submissions: pd.DataFrame) -> None:
# Iterate through each student's submission
    for idx, row in submissions.iterrows():
        submission_id = row['Assignment Submission ID']
        submission_path = f"{GRADESCOPE_EXPORT_DIR}submission_{submission_id}"

        # Compile and run tests for each submission
        score, comments = grade_submission(submission_path)

        # Update the score and comments in the dataframe
        submissions.at[idx, 'Score'] = score
        # df.at[idx, 'Comments'] = comments
        print(f"Graded submission {submission_id}: {score} points")


# load
submissions: pd.DataFrame = load_submissions()

# grade
grade(submissions)
update_submissions(submissions)
