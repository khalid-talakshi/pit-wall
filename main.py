import numpy as np
import pandas as pd
import streamlit as st
import datetime as dt
from fastf1 import get_event_schedule
from utils import type_to_options, get_session_data


def main():
    st.sidebar.title("Pit Wall")
    year = st.sidebar.selectbox(
        "Year",
        options=reversed([i for i in range(2018, dt.datetime.now().year + 1)]),
        index=None,
        placeholder="Select Year",
    )
    round_select = None
    session_select = None

    if year:
        schedule = get_event_schedule(year, include_testing=False)
        print(schedule[["RoundNumber", "EventName"]])
        sessions = schedule[["RoundNumber", "EventName"]]
        round_select = st.sidebar.selectbox(
            "Event",
            options=sessions,
            format_func=lambda x: sessions[sessions["RoundNumber"] == x][
                "EventName"
            ].item(),
            index=None,
            placeholder="Select Event",
        )
        st.title(f"Pit Wall Analysis for {year}")
    else:
        st.title("Pit Wall Analysis")
        st.subheader("Select a year from the sidebar to view data.")

    if round_select is not None:
        event = schedule.get_event_by_round(round_select)
        st.write(
            f"Selected Year: {year}, Selected Round: {event['EventName']} (Round {event['RoundNumber'].item()})"
        )
        session_select = st.sidebar.selectbox(
            "Session",
            options=type_to_options(event["EventFormat"]),
            index=None,
            placeholder="Select Session",
        )

    if session_select is not None:
        session = get_session_data(event, session_select)
        session.load()
        if session is not None:
            st.subheader(f"{session_select} Data")
            st.dataframe(session.results)
        else:
            st.write("Session data not available.")


if __name__ == "__main__":
    main()
