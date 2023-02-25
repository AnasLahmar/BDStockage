import streamlit as st
import pandas as pd
import streamlit as st
import json
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd 
import allfunction as all
import random
from io import BytesIO
import base64
import pickle
from xlsxwriter import Workbook
import streamlit as st
import pandas as pd
import base64

def get_data():
    data = st.session_state.get("data")
    if data is None:
        try:
            with open("data.pickle", "rb") as f:
                data = pickle.load(f)
        except FileNotFoundError:
            data = []
        st.session_state["data"] = data
    return data




def save_data(data):
    df = pd.DataFrame(data)
    with pd.ExcelWriter("data.xlsx") as writer:
        df.to_excel(writer, index=False)


def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_excel(index=False)
    b64 = base64.b64encode(object_to_download.encode()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{download_filename}">{download_link_text}</a>'
    return href

data = get_data()

c1,c2,c3=st.columns(3)
value1 = c1.text_input("Enter Ref:")
value2 = c2.text_input("Enter EPN:")
value3 = c3.text_input("Enter Compenent:")

if st.button("Add to Excel file"):
    if value1 and value2 and value3:
        data.append({'Ref': value1, 'EPN': value2, 'Compenent': value3})
        st.write("Dataframe:", pd.DataFrame(data))
        save_data(data)
        st.write("Data added to Excel file!")
    else:
        st.warning("Please fill in all fields.")

if len(data) > 0:
    st.write(pd.DataFrame(data))
    st.markdown("## Download Excel file")
    tmp_download_link = download_link(pd.DataFrame(data), "data.xlsx", "Click here to download your data!")
    st.markdown(tmp_download_link, unsafe_allow_html=True)
