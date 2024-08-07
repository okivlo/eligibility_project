from datetime import datetime
import streamlit as st

import pandas as pd
from utils.save_df_as_excel import save_and_format_df_as_excel


def strip_datetime_str(researcher: pd.Series, phd_column_to_choose) -> datetime | None:
    """Strips datetime strings of the PhD Defense Date to be the correct format.

    Args:
        researcher (pd.Series): the row corresponding with one researcher.
        phd_column_to_choose (str|datetime): Which column to reference against. Used when children are applicable.
    """
    phd_date = researcher[phd_column_to_choose]

    # Convert the PhD date string to a datetime object
    try:
        phd_date = datetime.strptime(str(phd_date), "%Y-%m-%d")
        return phd_date
    except ValueError as e:
        st.error(
            f"There seems to be a problem with converting the PhD defense date of researcher "
            f"{researcher['First Name']} {researcher['Last name']}"
            f"original error: {e}"
        )
        return None  # Return None if there's an error in date conversion


def calculate_nwo_talent_eligibility(researcher: pd.Series) -> str | None:
    """
    A function to calculate whether a researcher is eligible for an NWO talent grant.
    Args:
        researcher: The row of the researchers dataframe corresponding to a single researcher.

    Returns:
        The grant the researcher can apply for and until when.
    """
    if pd.isna(researcher["Children corrected PhD date"]):
        return None

    # Define the reference dates for the grants eligibility check
    reference_date_veni = datetime(year=datetime.now().year, month=1, day=1)
    reference_date_vidi = datetime(year=datetime.now().year, month=10, day=1)
    reference_date_vici = datetime(year=datetime.now().year, month=3, day=1)

    # Read the PhD defense date from the row
    phd_date = strip_datetime_str(
        researcher=researcher, phd_column_to_choose="Children corrected PhD date"
    )

    # Calculate the difference in years between the reference dates and the PhD defense date
    years_diff_veni = (reference_date_veni - phd_date).days / 365.25
    years_diff_vidi = (reference_date_vidi - phd_date).days / 365.25
    years_diff_vici = (reference_date_vici - phd_date).days / 365.25

    # Check Veni eligibility first
    if (
        -5 <= years_diff_veni < 3
    ):  # Veni eligibility within three years after the defense.
        last_eligible_year_veni = phd_date.year + 3
        return "Veni " + str(last_eligible_year_veni)

    # If not eligible for Veni, check Vidi eligibility
    elif (
        3 <= years_diff_vidi < 8
    ):  # Vidi eligibility within eight years after the defense.
        last_eligible_year_vidi = phd_date.year + 8
        return "Vidi " + str(last_eligible_year_vidi)

    # If not eligible for Vidi, check Vici eligibility
    elif (
        8 <= years_diff_vici < 15
    ):  # Vici eligibility within fifteen years after the defense.
        last_eligible_year_vici = phd_date.year + 15
        return "Vici " + str(last_eligible_year_vici)

    # If not eligible for any return none
    else:
        return None


def calculate_nwo_oc_eligibility(researcher: pd.Series) -> str | None:
    """
    A function to calculate whether a researcher is eligible for an NWO other grant.
    Args:
        researcher: The row of the researchers dataframe corresponding to a single researcher.

    Returns:
        The grant the researcher can apply for and until when.
    """
    if pd.isna(researcher["PhD Defense Date"]):
        return None

    # Define the reference dates for the grants eligibility check
    reference_date_xs = datetime(year=datetime.now().year, month=3, day=19)
    reference_date_m = datetime(year=datetime.now().year, month=11, day=1)
    reference_date_l = datetime(year=datetime.now().year, month=9, day=1)

    # Read the PhD defense date from the row
    phd_date = strip_datetime_str(
        researcher=researcher, phd_column_to_choose="PhD Defense Date"
    )

    # Calculate the difference in years between the reference dates and the PhD defense date
    years_diff_xs = (reference_date_xs - phd_date).days / 365.25
    years_diff_m = (reference_date_m - phd_date).days / 365.25
    years_diff_l = (reference_date_l - phd_date).days / 365.25

    # Check xs eligibility first
    if 5 <= years_diff_xs < 10:  # xs eligibility within three years after the defense.
        last_eligible_year_xs = phd_date.year + 10
        return "Xs " + str(last_eligible_year_xs)

    # If not eligible for xs, check M/L eligibility
    elif 16 < years_diff_l:
        return "M/L"

    # If not eligible for L, check M eligibility
    elif 10 < years_diff_m:
        return "M"

    # If not eligible for any return none
    else:
        return None


def calculate_erc_eligibility(researcher: pd.Series) -> str | None:
    """
    A function to calculate whether a researcher is eligible for an ERC grant.
    Args:
        researcher: The row of the researchers dataframe corresponding to a single researcher.

    Returns:
        The grant the researcher can apply for and until when.
    """
    if pd.isna(researcher["PhD Defense Date"]):
        return None

    # Define the reference dates for the grants eligibility check
    reference_date_starting = datetime(year=datetime.now().year, month=1, day=1)
    reference_date_consolidator = datetime(year=datetime.now().year, month=1, day=1)
    reference_date_advanced = datetime(year=datetime.now().year, month=1, day=1)

    if researcher["Gender"] == "Female":
        phd_date = strip_datetime_str(
            researcher=researcher, phd_column_to_choose="Children corrected PhD date"
        )
    else:
        phd_date = strip_datetime_str(
            researcher=researcher, phd_column_to_choose="PhD Defense Date"
        )
    phd_date_advanced = strip_datetime_str(
        researcher=researcher, phd_column_to_choose="PhD Defense Date"
    )

    # Calculate the difference in years between the reference dates and the PhD defense date
    years_diff_starting = (reference_date_starting - phd_date).days / 365.25
    years_diff_consolidator = (reference_date_consolidator - phd_date).days / 365.25
    years_diff_advanced = (reference_date_advanced - phd_date_advanced).days / 365.25

    # Check StG eligibility first
    if (
        2 <= years_diff_starting < 7
    ):  # xs eligibility within three years after the defense.
        last_eligible_year_starting = phd_date.year + 7
        return "StG " + str(last_eligible_year_starting)

    # If not eligible for StG, check CoG eligibility
    elif 7 <= years_diff_consolidator < 12:
        last_eligible_year_consolidator = phd_date.year + 12
        return "CoG " + str(last_eligible_year_consolidator)

    # If not eligible for L, check M eligibility
    elif 12 <= years_diff_advanced:
        return "AdG"

    # If not eligible for any return none
    else:
        return None


def calculate_msca_eligibility(researcher: pd.Series) -> str | None:
    """
    A function to calculate whether a researcher is eligible for an MSCA postdoctoral fellowship grant.
    Args:
        researcher: The row of the researchers dataframe corresponding to a single researcher.

    Returns:
        The grant the researcher can apply for and until when.
    """
    if pd.isna(researcher["PhD Defense Date"]):
        return None

    # Define the reference date for the grants eligibility check
    reference_date = datetime(year=2024, month=9, day=11)  # Deadline for submission

    # Parse the PhD defense date and contract start date
    phd_date = strip_datetime_str(researcher, phd_column_to_choose="PhD Defense Date")
    contract_start_date = datetime.strptime(
        researcher["Employment Start Date"], "%Y-%m-%d"
    )

    # Calculate the difference in years between the reference date and the PhD defense date
    years_since_phd = (reference_date - phd_date).days / 365.25

    # Check eligibility based on years since PhD
    if years_since_phd >= 8:
        return None

    # Check if they have been in NL for more than 12 months in the last 3 years
    months_in_nl = (reference_date - contract_start_date).days / 30.44
    if months_in_nl > 12:
        return None

    last_eligible_year_msca = phd_date.year + 8  # 8 years post-PhD rule
    return f"Eligible until {last_eligible_year_msca}"


def calculate_eligibility():
    """Main function to create the eligibility list based on the researchers list."""
    st.subheader("Calculate Eligibility")
    researchers_list = st.file_uploader("Upload researchers list", type=["xlsx", "xls"])

    if researchers_list:
        try:
            researchers_df = pd.read_excel(io=researchers_list, header=1)

            st.write("Preview of uploaded Excel file:")
            st.write(researchers_df)
            st.write("---\n")
            st.write("Preview of researchers list with calculated grants:")

            researchers_df["Eligible NWO Talent"] = researchers_df.apply(
                calculate_nwo_talent_eligibility, axis=1
            )

            researchers_df["Eligible NWO OC"] = researchers_df.apply(
                calculate_nwo_oc_eligibility, axis=1
            )

            researchers_df["Eligible ERC"] = researchers_df.apply(
                calculate_erc_eligibility, axis=1
            )

            researchers_df["eligible MSCA"] = researchers_df.apply(
                calculate_msca_eligibility, axis=1
            )
            st.write(researchers_df)

            excel_data = save_and_format_df_as_excel(
                updated_researchers_dataframe=researchers_df
            )

            # Create a download button
            st.download_button(
                label="Download eligibility list",
                data=excel_data,
                file_name="new_eligibility_list.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_button",
            )

        except Exception as e:
            st.error(
                f"An error occurred. Feel free to contact me with this error code: {e}"
            )
