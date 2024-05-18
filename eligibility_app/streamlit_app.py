"""The entry point of the streamlit application."""

import streamlit as st
from menu_eligibility_list_creation import calculate_eligibility
from menu_hr_update import update_researchers_list


def eligibility_app():
    """Creates a streamlit application with different menu options. These correspond to the different files starting
    with 'menu_'
    """

    # Create menu item
    st.sidebar.title("Menu")
    menu_selection = st.sidebar.selectbox(
        "Select where you want to go",
        [
            "Home page",
            "Update researchers list with HR list",
            "Create Eligibility List",
        ],
    )

    # Homepage
    if menu_selection == "Home page":
        st.title("Welcome to the Eligibility Helper.")
        st.write("---")
        st.info(
            "I made this in my free time to lighten the load of you grants officers. If anything is unclear, if "
            "you have feedback, or if you have a request for the implementation, feel free to shoot me a message at"
            "i.vloothuis@gmail.com."
        )

    # Routes to menu_hr_update
    elif menu_selection == "Update researchers list with HR list":
        update_researchers_list()

    # Routes to menu_eligibility_list_creation
    elif menu_selection == "Create Eligibility List":
        calculate_eligibility()


if __name__ == "__main__":
    eligibility_app()
