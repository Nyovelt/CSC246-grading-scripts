from grade import CSV_FILE, OUTPUT_CSV_FILE
import pandas as pd

# Load the submissions from CSV
def load_submissions() -> pd.DataFrame:
    return pd.read_csv(CSV_FILE)

# Save the graded submissions back to a CSV file
def update_submissions(df) -> None:
    df.to_csv(OUTPUT_CSV_FILE, index=False)


