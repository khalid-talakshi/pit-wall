import datetime as dt

import streamlit as st
from fastf1 import get_event_schedule
import plotly.graph_objects as go

from utils import get_driver_info, get_info_table, get_session_data, type_to_options

race_tabs = ["Race Results", "Driver Lap Times"]
qualifying_tabs = ["Race Results", "Driver Lap Times"]
practice_tabs = ["Driver Lap Times"]


def generate_driver_lap_times_tab(session):
    st.subheader("Driver Lap Times")
    drivers = get_driver_info(session)

    # Form
    with st.container(
        horizontal=True, gap="small", vertical_alignment="center", border=True
    ):
        selected_driver = st.selectbox(
            "Select Driver",
            options=drivers,
            format_func=lambda x: drivers[drivers["DriverNumber"] == x][
                "FullName"
            ].item(),
            index=None,
            placeholder="Select Driver",
            label_visibility="collapsed",
        )
        accurate = st.checkbox("Accurate Laps Only", value=False)
    if selected_driver is None:
        st.info("Please select a driver to view lap times.")
        return
    laps = session.laps.pick_drivers([selected_driver])
    if accurate:
        laps = laps.pick_accurate()
    laps = laps.reset_index(drop=True)
    laps["LapTime"] = laps["LapTime"].apply(
        lambda x: x.total_seconds() if x is not None else None
    )
    laps["Sector1Time"] = laps["Sector1Time"].apply(
        lambda x: x.total_seconds() if x is not None else None
    )
    laps["Sector2Time"] = laps["Sector2Time"].apply(
        lambda x: x.total_seconds() if x is not None else None
    )
    laps["Sector3Time"] = laps["Sector3Time"].apply(
        lambda x: x.total_seconds() if x is not None else None
    )
    columns = [
        "LapNumber",
        "LapTime",
        "Sector1Time",
        "Sector2Time",
        "Sector3Time",
        "Compound",
        "TyreLife",
    ]
    st.write(laps[columns])

    laps_box = (
        laps[["LapNumber", "LapTime", "Sector1Time", "Sector2Time", "Sector3Time"]]
        .melt(
            id_vars=["LapNumber"],
            value_vars=["LapTime", "Sector1Time", "Sector2Time", "Sector3Time"],
            var_name="Type",
            value_name="Time",
        )
    )

    st.write(laps_box)

    fig = go.Figure()
    fig.add_trace(
        go.Box(
            y=laps["LapTime"],
            boxpoints="all",
            jitter=0.5,
            pointpos=-1.8,
            name="Lap Time",
        )
    )

    st.plotly_chart(fig, use_container_width=True)


def generate_qualifying_tabs(session):
    tab1, tab2 = st.tabs(qualifying_tabs)
    with tab1:
        st.subheader("Qualifying Results")
        st.write(get_info_table(session, "Qualifying").reset_index(drop=True))
    with tab2:
        generate_driver_lap_times_tab(session)


def generate_race_tabs(session):
    tab1, tab2 = st.tabs(race_tabs)
    with tab1:
        st.subheader("Race Results")
        st.write(get_info_table(session, "Race").reset_index(drop=True))
    with tab2:
        generate_driver_lap_times_tab(session)


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
