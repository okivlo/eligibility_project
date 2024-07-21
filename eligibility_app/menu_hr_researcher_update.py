"""Streamlit app menu item that filters the HR list to only contain researchers."""

from io import BytesIO
from typing import List

import pandas as pd
import streamlit as st
from seeds.function_names import function_names_researchers
from seeds.translation_dutch_english import translation_dict
from utils.filter_hr_list import filter_out_function_names


def calculate_phd_date_corrected_for_children(row):

    if pd.isna(row["PhD Defense Date"]):
        return None  # Return None if there is no PhD Defense Date

    children_count = (
        row["Count of children applicable"]
        if pd.notna(row["Count of children applicable"])
        else 0
    )

    # Calculate the adjustment period
    if row["Gender"] == "Female":
        months_to_subtract = 18 * children_count
    elif row["Gender"] == "Male":
        months_to_subtract = 6 * children_count
    else:
        return row["PhD Defense Date"]  # No adjustment if gender is not specified

    # Adjust the PhD Defense Date
    adjusted_date = pd.to_datetime(row["PhD Defense Date"]) + pd.DateOffset(
        months=months_to_subtract
    )
    formatted_date = adjusted_date.strftime('%Y-%m-%d')
    return formatted_date


def filter_df_add_column(
    hr_df: pd.DataFrame, function_name_parts: List
) -> pd.DataFrame:
    """Filters the hr dataframe on function name, makes all columns English.

    Args:
        hr_df (pd.DataFrame): The HR list formatted as a dataframe by the example.
        function_name_parts (List): A list with function names to filter the HR list on.

    """
    # Filter out all other functions of the function_names.
    filtered_df = filter_out_function_names(
        hr_list=hr_df, function_names=function_name_parts
    )

    # Rename columns
    filtered_df = filtered_df.rename(columns=translation_dict)
    filtered_df = filtered_df.drop(columns=["Medewerkersgroep"])

    # Convert datetime columns to the desired format.
    for column in filtered_df.select_dtypes(include="datetime").columns:
        filtered_df[column] = filtered_df[column].dt.strftime("%Y-%m-%d")

    # Also filters the termination date column as the date 9999 doesn't get recognized as a datetype format.
    filtered_df["Employment Termination Date"] = (
        filtered_df["Employment Termination Date"].astype(str).apply(lambda x: x[:-9])
    )

    return filtered_df


def merge_two_df(
    researchers_df: pd.DataFrame, filtered_hr_df: pd.DataFrame
) -> pd.DataFrame:
    """Function to merge the researchers dataframe and the Hr dataframe. This has to be done, so we do not lose the
    information that the grants office already filled in for researchers (Like sex and children.)

    Args:
        researchers_df (pd): The researchers dataframe.
        filtered_hr_df (pd): The hr list converted to a pandas dataframe.

    Returns:
        A pandas dataframe where the current researchers dataframe gets left joined on the filtered hr dataframe.
    """
    # Select columns to keep from researchers_df
    columns_to_keep = [
        "First Name",
        "Gender",
        "Count of children applicable",
        "Remarks",
        "Last name",
        "Initials",
        "PhD Defense Date",
    ]

    # Merge the dataframes on the specified keys
    merged_df = pd.merge(
        filtered_hr_df,
        researchers_df[columns_to_keep],
        how="left",
        left_on=["Last name", "Initials"],
        right_on=["Last name", "Initials"],
    )

    # Drop duplicates (in case there are duplicates after the merge)
    merged_df.drop_duplicates(inplace=True)

    # Merge the "PhD Defense Date_x" and "PhD Defense Date_y" columns
    merged_df["PhD Defense Date"] = merged_df["PhD Defense Date_y"].fillna(
        merged_df["PhD Defense Date_x"]
    )

    # Drop the extra "PhD Defense Date_y" column (We prioritize the grants office's PhD date.)
    merged_df.drop(columns=["PhD Defense Date_y"], inplace=True)
    # Convert date column to datetime first.
    merged_df["PhD Defense Date"] = pd.to_datetime(merged_df["PhD Defense Date"])
    # Convert date column to right format
    merged_df["PhD Defense Date"] = merged_df["PhD Defense Date"].dt.strftime(
        "%Y-%m-%d"
    )

    reordered_df = merged_df[
        [
            "First Name",
            "Tussenv.",
            "Last name",
            "Initials",
            "FTE",
            "Faculty",
            "Research Group",
            "PhD Defense Date",
            "Employment Start Date",
            "Employment Termination Date",
            "Function",
            "Birth Date",
            "Gender",
            "Count of " "children " "applicable",
            "Remarks",
        ]
    ]

    return reordered_df


def save_and_format_df_as_excel(updated_researchers_dataframe: pd.DataFrame) -> BytesIO:
    """Function to save the updated hr dataframe as an Excel file with the correct formatting.

    Args:
        updated_researchers_dataframe (pd.DataFrame): The updated researchers dataframe.

    Returns:
        BytesIO: The Excel file in the requested format.
    """
    excel_buffer = BytesIO()

    with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
        # Write the DataFrame to Excel starting from the second row.
        updated_researchers_dataframe.to_excel(
            writer, startrow=1, index=False, sheet_name="Sheet1"
        )

        # Get the xlsxwriter workbook and worksheet objects.
        workbook = writer.book
        worksheet = writer.sheets["Sheet1"]

        # Define cell formats.
        header_format = workbook.add_format(
            {
                "bold": True,
                "text_wrap": True,
                "valign": "top",
                "fg_color": "#D7E4BC",
                "border": 1,
            }
        )
        workbook.add_format({"text_wrap": True, "valign": "top", "border": 1})
        alternating_color = workbook.add_format({"fg_color": "#F2F2F2"})

        # Apply formatting to headers (starting from the second row.)
        for col_num, value in enumerate(updated_researchers_dataframe.columns.values):
            worksheet.write(1, col_num, value, header_format)

        # Apply alternating row color.
        for row_num in range(
            2, len(updated_researchers_dataframe) + 2
        ):  # Start from the second row
            if row_num % 2 == 0:
                worksheet.set_row(row_num, None, alternating_color)

        # Enable sorting by clicking on column headers.
        worksheet.autofilter(
            1,
            0,
            len(updated_researchers_dataframe) + 1,
            len(updated_researchers_dataframe.columns) - 1,
        )

        # Adjust column width based on the length of the text.
        for i, col in enumerate(updated_researchers_dataframe.columns):
            column_len = max(
                updated_researchers_dataframe[col].astype(str).map(len).max(), len(col)
            )
            worksheet.set_column(i, i, column_len)

    excel_data = excel_buffer.getvalue()

    return excel_data


def update_researchers_list() -> None:
    """Main function to update the researchers list based on the current researchers Excel file and the new HR file."""
    st.title("Upload HR file")
    st.write(
        "Here you can upload the new HR excel file and filter out all the non-researchers. Then we obtain the "
        "extra data from the older researchers list and add it to the new researchers list."
    )
    st.write("---\n")

    # File uploader for HR list
    hr_file = st.file_uploader("Upload HR List Excel file", type=["xlsx", "xls"])
    researchers_file = st.file_uploader(
        "Upload the researchers excel file", type=["xlsx", "xls"]
    )
    st.write("---\n")

    # Open HR file and perform filtering
    if hr_file and researchers_file:
        try:

            # Open HR and Researcher's Excel file
            hr_df = pd.read_excel(io=hr_file, header=2)
            researchers_df = pd.read_excel(io=researchers_file, header=1)

            # Filter the HR list.
            filtered_df = filter_df_add_column(
                hr_df, function_name_parts=function_names_researchers
            )

            # Merge both dataframes.
            merged_df = merge_two_df(
                researchers_df=researchers_df, filtered_hr_df=filtered_df
            )

            # Calculate adjusted phd defense date based on children.
            merged_df["Children corrected PhD date"] = merged_df.apply(
                calculate_phd_date_corrected_for_children, axis=1
            )

            # Format merged tables as excel data.
            excel_data = save_and_format_df_as_excel(merged_df)

            st.write(
                "The HR file has been filtered and the existing additional information from the provided "
                "researchers list have been added as well. "
                "This is a preview, but you can download the file with all found "
                "researchers below."
            )
            st.write(merged_df)
            st.write("---\n")

            # Create a download button
            st.download_button(
                label="Download researchers list",
                data=excel_data,
                file_name="new_researchers_list.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_button",
            )

        except Exception as e:
            st.error(
                f"An error occurred. Feel free to contact me with this error code: {e}"
            )
