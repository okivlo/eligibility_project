"""Helper functions for the eligibility project."""

from typing import List

import pandas as pd


def filter_out_function_names(
    hr_list: pd.DataFrame, function_names: List
) -> pd.DataFrame:
    """
    filters out all functions that do not at least contain any part of the entries in the function_name list.

    Args:
        hr_list (pd.Dataframe): The hr-list df. Needs to contain column "Functienaam"
        function_names (List): A list of all function names to filter on.

    Returns:
        A filtered hr list dataframe.
    """
    filtered_df = hr_list[
        hr_list["Functienaam"].str.contains("|".join(function_names), case=False)
    ]
    return filtered_df
