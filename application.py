import streamlit as st
import json
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd 
import base64
import os
#==============================================Start=============================================================
#=======================================define All function needed=========================================






# Interface Application------------------------------------------------------------------------------------------
st.write(""" ## BD Storage""")

selected=option_menu(
    menu_title="Main Menu",
    options=["Home","Storage","Processing"],
    icons=["house","bar-chart"],
    menu_icon="cast",  # optional
    default_index=0,
    orientation="horizontal",  
    styles={
        "nav-link-selected": {"background-color": "#4B9OFF"},
    } 

     )
#========================================================Accueil===========================================
if selected=="Home":
    # creer une animation
    # Add logo to the sidebar
    logo = "log.png"
    st.sidebar.image(logo, use_column_width=True)
    def load_lottiefile(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)
    lottie_coding = load_lottiefile("pc.json")  # replace link to local lottie file
    st_lottie(
    lottie_coding,
    speed=1,
    reverse=False,
    loop=True,
    quality="low", # medium ; high

    height=None,
    width=None,
    key=None,
)
#======================================================Data Overview=======================================
m = st.markdown("""
            <style>
            div.stButton > button:first-child {
                background-color:#4B9DFF;
                color:#ffffff;
            }
            div.stButton > button:hover {
                background-color: #00ff00;
                color:#ff0000;
                }
            </style>""", unsafe_allow_html=True)
if selected=="Storage":
    logo = "log.png"
    st.sidebar.image(logo, use_column_width=True)
    def load_lottiefile(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)
    #------------------------------------------------------------------------------------------
    # Define a function to get the dataframe from the session
    # Define a function to get the dataframe
    #===================BUTTON 
    

    import os

    # Function to load data
    def load_data():
        if os.path.exists("data.xlsx"):
            data = pd.read_excel("data.xlsx")
        else:
            data = pd.DataFrame(columns=["Ref", "EPN", "Component"])
        return data

    # Function to save data
    def save_data(data):
        data.to_excel("data.xlsx", index=False)

    # Load the data
    data = load_data()
    def clear_excel_file():
        # Create an empty DataFrame with the same columns as the original Excel file
        columns = ["Ref", "EPN", "Component"]
        data = pd.DataFrame(columns=columns)

        # Save the empty DataFrame to the Excel file
        data.to_excel("data.xlsx", index=False)

        # Return a message indicating that the Excel file has been cleared
        return "Excel file has been cleared."

    # Add the input boxes
    c1, c2, c3 = st.columns(3)
    value1 = c1.text_input("Enter Ref:")
    value2 = c2.text_input("Enter EPN:")
    value3 = c3.text_input("Enter Component:")

    # Add the button to add to Excel file
    button2 = st.button("Add to Excel file")

    # If the button is clicked, add the data to the DataFrame and save to Excel file
    if button2:
        if value1 and value2 and value3:
            data = data.append({"Ref": value1, "EPN": value2, "Component": value3}, ignore_index=True)
            save_data(data)
            st.success("Data added to Excel file!")
        else:
            st.warning("Please fill in all fields.")

    # Show the data
    # Add the download button
   # if len(data) > 0:
    #    st.sidebar.download_button("Download Excel file", data.to_excel, file_name="data.xlsx")
    
    button = st.sidebar.button("Download Excel file")
    import io
    if button:
    # Convert the dataframe to bytes
        towrite = io.BytesIO()
        downloaded_file = data.to_excel(towrite, encoding='utf-8', index=False, header=True)
        towrite.seek(0)  # Reset the stream position

        # Send the file to the user to download
        b64 = base64.b64encode(towrite.read()).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="my_file.xlsx">Download Excel file</a>'
        st.sidebar.markdown(href, unsafe_allow_html=True)
    
    if st.checkbox("Show Data"):
        st.write(data)
   


if selected== 'Processing':
    logo = "log.png"
    st.sidebar.image(logo, use_column_width=True)
    def load_lottiefile(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)
    # Function to load data
    def load_data():
        if os.path.exists("data.xlsx"):
            data = pd.read_excel("data.xlsx")
        else:
            data = pd.DataFrame(columns=["Ref", "EPN", "Component"])
        return data

    # Function to save data
    def save_data(data):
        data.to_excel("data.xlsx", index=False)

    # Function to search for a value in the Excel file
    def search_excel_file(search_value):
        # Load the data from the Excel file
        data = pd.read_excel("data.xlsx")

        # Convert columns to string type
        data["Ref"] = data["Ref"].astype(str)
        data["EPN"] = data["EPN"].astype(str)
        data["Component"] = data["Component"].astype(str)

        # Check if the search value exists in any of the columns
        search_results = data[data["Ref"].str.contains(search_value, na=False) |
                            data["EPN"].str.contains(search_value, na=False) |
                            data["Component"].str.contains(search_value, na=False)]

        # If any rows contain the search value, return those rows
        if not search_results.empty:
            return search_results
        # If no rows contain the search value, return a message
        else:
            return "No matching results found."
    forme=st.sidebar.selectbox("Processing",["Select","ViewData","Search","Delete"])
    # Load the data
    data = load_data()
    if forme=="ViewData":
        st.write(data.head(data.shape[0]))
    if forme=="Search":
        # Add the input box for the search value
        search_value = st.text_input("Enter a value to search for:")

        # Add the button to search for the value
        button1 = st.button("Search")

        # If the button is clicked, search for the value and display the results
        c1,c2=st.columns(2)
        if button1:
            if search_value:
                results = search_excel_file(search_value)
                if isinstance(results, pd.DataFrame):
                    #st.write(results)
                    c1.write(results)
                    c2.success("For this value : {}, there is {} row (s)".format(search_value,results.shape[0]))
   
                else :
                    st.warning("This value doesn't exist !")
                    
                    
            else:
                st.warning("Please enter a search value.")
    
    if forme=="Delete":
        # Add the input boxes for deleting rows
        def clear_excel_file():
            # Create an empty DataFrame with the same columns as the original Excel file
            columns = ["Ref", "EPN", "Component"]
            data = pd.DataFrame(columns=columns)

            # Save the empty DataFrame to the Excel file
            data.to_excel("data.xlsx", index=False)
            # Return a message indicating that the Excel file has been cleared
            return "Excel file has been cleared."
         # Add the button to clear the Excel file
        button4 = st.sidebar.button("Clear All")
        if button4:
            clear_excel_file()
            data = pd.DataFrame(columns=["Ref", "EPN", "Component"])
            st.sidebar.write("Excel file cleared!")
            st.sidebar.success("All Rows are deleting from Excel file!")
        if data.shape[0]!=0: 
            st.info('You can delete a specific Value or Row as you want !')
            c1, c2 = st.columns(2)
            delete_value = c1.text_input("Enter value to delete:")
            delete_index = c2.text_input("Enter index to delete:")

            # Add the button to delete rows
            button3 = st.button("Delete rows")

            # If the button is clicked, delete rows based on the provided value or index
            if button3:
                if delete_value:
                    if data["Ref"].dtype == object:
                        data = data[~data["Ref"].str.contains(delete_value)]
                    if data["EPN"].dtype == object:
                        data = data[~data["EPN"].str.contains(delete_value)]
                    if data["Component"].dtype == object:
                        data = data[~data["Component"].str.contains(delete_value)]    
                    else:
                        st.warning("Cannot search for string value in non-string column.")
                    save_data(data)
                    st.success("Rows deleted from Excel file!")
                elif delete_index:
                    data = data.drop(int(delete_index))
                    save_data(data)
                    st.success("Row deleted from Excel file!")
                else:
                    st.warning("Please provide a value or index to delete.")
        else :
            st.info("The Excel file is empty")
        








        #============================================FIN=========================================================
       