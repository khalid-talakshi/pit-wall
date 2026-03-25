import streamlit as st

def driver_selectbox(drivers, key="laptime_driver_select"):
    return st.selectbox(
        "Select Driver",
        options=drivers,
        format_func=lambda x: drivers[drivers["DriverNumber"] == x]["FullName"].item(),
        index=None,
        placeholder="Select Driver",
        label_visibility="collapsed",
        key=key,
    )
