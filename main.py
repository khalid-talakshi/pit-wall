import datetime as dt

import streamlit as st
from fastf1 import get_event_schedule

from utils import get_info_table, get_session_data, type_to_options

race_tabs = ["Race Results", "Driver Lap Times"]
qualifying_tabs = ["Race Results", "Driver Lap Times"]
practice_tabs = ["Driver Lap Times"]


def generate_qualifying_tabs(session):
    tab1, tab2 = st.tabs(qualifying_tabs)
    with tab1:
        st.subheader("Qualifying Results")
        st.write(get_info_table(session, "Qualifying").reset_index(drop=True))
    with tab2:
        st.subheader("Driver Lap Times")


def generate_race_tabs(session):
    tab1, tab2 = st.tabs(race_tabs)
    with tab1:
        st.subheader("Race Results")
        st.write(get_info_table(session, "Race").reset_index(drop=True))
    with tab2:
        st.subheader("Driver Lap Times")


def generate_main_view(event, session, session_option):
    st.subheader(f"{event['EventName']} - {session.session_info['Name']} Leaderboard")
    if session_option == "Race":
        generate_race_tabs(session)
    elif session_option == "Qualifying":
        generate_qualifying_tabs(session)


def main():
    st.sidebar.title("Pit Wall")
    st.title("Pit Wall Analysis")

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
    else:
        st.subheader("Select a year from the sidebar to view data.")

    if round_select is not None:
        event = schedule.get_event_by_round(round_select)
        session_select = st.sidebar.selectbox(
            "Session",
            options=type_to_options(event["EventFormat"]),
            index=None,
            placeholder="Select Session",
        )

    if session_select is not None:
        session = get_session_data(event, session_select)
        session.load()
        generate_main_view(event, session, session_select)


if __name__ == "__main__":
    main()
