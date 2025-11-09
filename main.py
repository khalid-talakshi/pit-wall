import numpy as np
import pandas as pd
import streamlit as st
import datetime as dt
from fastf1 import get_event_schedule

CONVENTIONAL_OPTIONS = ["Practice 1", "Practice 2", "Practice 3", "Qualifying", "Race"]
SPRINT_OPTIONS = ["Practice 1", "Qualifying", "Practice 2", "Sprint", "Race"]
SPRINT_QUALIFYING_OPTIONS = ["Practice 1", "Sprint Qualifying", "Sprint", "Qualifying", "Race"]
SPRINT_SHOOTOUT_OPTIONS = ["Practice 1", "Qualifying", "Sprint Shootout", "Sprint", "Race"]

def type_to_options(event_type: str) -> list:
    if event_type == "conventional":
        return CONVENTIONAL_OPTIONS
    elif event_type == "sprint":
        return SPRINT_OPTIONS
    elif event_type == "sprint_qualifying":
        return SPRINT_QUALIFYING_OPTIONS
    elif event_type == "sprint_shootout":
        return SPRINT_SHOOTOUT_OPTIONS
    else:
        return CONVENTIONAL_OPTIONS

def get_session_data(event, session_option: str):
    if session_option == "Practice 1":
        return event.get_practice(1)
    elif session_option == "Practice 2":
        return event.get_practice(2)
    elif session_option == "Practice 3":
        return event.get_practice(3)
    elif session_option == "Qualifying":
        return event.get_qualifying()
    elif session_option == "Sprint":
        return event.get_sprint()
    elif session_option == "Sprint Qualifying":
        return event.get_sprint_qualifying()
    elif session_option == "Sprint Shootout":
        return event.get_sprint_shootout()
    elif session_option == "Race":
        return event.get_race()
    else:
        return None


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
            format_func=lambda x: sessions[sessions["RoundNumber"] == x]["EventName"].item(),
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
