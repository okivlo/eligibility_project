import pandas as pd
from datetime import timedelta, datetime

# Constants
NUM_ROWS = 7670  # Approximately 20 years, considering leap years
START_DATE = datetime(2005, 1, 1)  # Starting from January 1, 2003


def create_test_dataset():
    """Create a test dataset with a range of approx 20 years"""
    df = pd.DataFrame(
        {
            "First Name": ["Test"] * NUM_ROWS,
            "Tussenv.": ["T"] * NUM_ROWS,
            "Last Name": ["User"] * NUM_ROWS,
            "Initials": ["TU"] * NUM_ROWS,
            "FTE": [1.0] * NUM_ROWS,
            "Faculty": ["Test Faculty"] * NUM_ROWS,
            "Research Group": ["Test Group"] * NUM_ROWS,
            "PhD Defense Date": [
                (START_DATE + timedelta(days=i)).strftime("%Y-%m-%d")
                for i in range(NUM_ROWS)
            ],
            "Employment Start Date": ["2024-01-01"] * NUM_ROWS,
            "Employment Termination Date": [
                (START_DATE + timedelta(days=NUM_ROWS)).strftime("%Y-%m-%d")
            ]
            * NUM_ROWS,
            "Birth Date": [(START_DATE - timedelta(days=365 * 25)).strftime("%Y-%m-%d")]
            * NUM_ROWS,
            # Assuming 25 years old at start
            "Gender": ["Non-binary"] * NUM_ROWS,
            "Count of children applicable": [0] * NUM_ROWS,
            "Remarks": ["No remarks"] * NUM_ROWS,
            "Children corrected PhD date": ["2023-01-01"] * NUM_ROWS,
        }
    )

    # Define the Excel writer using xlsxwriter as the engine
    writer = pd.ExcelWriter("test_data.xlsx", engine="xlsxwriter")

    # Convert the dataframe to an XlsxWriter Excel object.
    # Use `startrow=1` to start writing from the second row.
    df.to_excel(writer, sheet_name="Sheet1", index=False, startrow=1)

    # Close the Pandas Excel writer and output the Excel file
    writer._save()


if __name__ == "__main__":
    create_test_dataset()
