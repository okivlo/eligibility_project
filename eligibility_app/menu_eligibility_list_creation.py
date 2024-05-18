from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
from dateutil.relativedelta import relativedelta


def calculate_eligible_grant(row):
    veni_reference_date = datetime(year=datetime.now().year, month=1, day=1)
    vidi_reference_date = datetime(year=datetime.now().year, month=10, day=1)
    vici_reference_date = datetime(year=datetime.now().year, month=3, day=1)
    # Define the eligibility criteria for each grant option

    veni_criteria = (0, 3)  # Years of experience required for Veni grant
    vidi_criteria = (3, 8)  # Years of experience required for Vidi grant
    vici_criteria = (8, 15)  # Years of experience required for Vici grant

    # Calculate years of experience since PhD defense date
    veni_years_since_phd = (
        ((veni_reference_date - row["PhD Defense Date"]) / 365.25).get(key=0).days
    )
    vidi_years_since_phd = (
        ((vidi_reference_date - row["PhD Defense Date"]) / 365.25).get(key=0).days
    )
    vici_years_since_phd = (
        ((vici_reference_date - row["PhD Defense Date"]) / 365.25).get(key=0).days
    )

    print(veni_years_since_phd)
    # Determine the earliest eligible grant
    if veni_criteria[0] <= veni_years_since_phd <= veni_criteria[1]:
        return (veni_criteria[1] - veni_years_since_phd) + veni_reference_date
    elif vidi_criteria[0] <= vidi_years_since_phd <= vidi_criteria[1]:
        return (vidi_criteria[1] - vidi_years_since_phd) + vidi_reference_date
    elif vici_criteria[0] <= vici_years_since_phd <= vici_criteria[1]:
        return (veni_criteria[1] - vici_years_since_phd) + vici_reference_date
    else:
        return None


def calculate_eligibility():
    """Main function to create the eligibility list based on the researchers list."""
    st.subheader("Calculate Eligibility")
    researchers_list = st.file_uploader("Upload researchers list", type=["xlsx", "xls"])

    if researchers_list:
        try:
            researchers_df = pd.read_excel(io=researchers_list, header=1)
            st.write("Preview of uploaded Excel files:")
            st.write(researchers_df)

            researchers_df["Earliest Eligible Grant Date"] = researchers_df.apply(
                calculate_eligible_grant, axis=1
            )
            st.write("added earliest eligible grant date column")
            st.write(researchers_df)

        except Exception as e:
            st.error(
                f"An error occurred. Feel free to contact me with this error code: {e}"
            )


if __name__ == "__main__":
    date = datetime(year=2014, month=4, day=2)
    df = pd.DataFrame(data=[date], columns=["PhD Defense Date"])
    calculate_eligible_grant(df)
