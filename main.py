import datetime as dt

import streamlit as st
from fastf1 import get_event_schedule
from fastf1.plotting import get_compound_color, get_driver_style
import plotly.graph_objects as go

from utils import get_driver_info, get_info_table, get_session_data, type_to_options

race_tabs = ["Race Results", "Driver Explorer", "Driver Telemetry"]
qualifying_tabs = ["Race Results", "Driver Lap Times", "Driver Telemetry"]
practice_tabs = ["Driver Lap Times"]


def generate_lap_stint_chart(session, laps, driver):
    pass


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
            key="laptime_driver_select",
        )

        laps = (
            list(
                map(
                    lambda x: int(x),
                    session.laps.pick_drivers([selected_driver])["LapNumber"].unique(),
                )
            )
            if selected_driver
            else []
        )

        selected_lap = st.selectbox(
            "Select Lap",
            options=["All", "Fastest", *laps],
            placeholder="Select Lap",
            label_visibility="collapsed",
            key="laptime_lap_select",
        )

        accurate = st.checkbox("Accurate Laps Only", value=False)

    if selected_driver is None:
        st.info("Please select a driver to view lap times.")
        return

    driver = drivers[drivers["DriverNumber"] == selected_driver].iloc[0]

    laps = session.laps.pick_drivers([selected_driver])

    if accurate:
        laps = laps.pick_accurate()

    if selected_lap == "Fastest":
        laps = laps.pick_fastest()

    elif selected_lap != "All":
        laps = laps.pick_laps(int(selected_lap))

    laps = laps.reset_index(drop=True)

    print(laps)

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
        "Stint",
    ]
    st.write(laps[columns])

    options = ["LapTime", "Sector1Time", "Sector2Time", "Sector3Time"]
    selected_series = st.segmented_control(
        "Select Series to Plot",
        options=options,
        key="series_select",
        default="LapTime",
        label_visibility="collapsed",
    )

    driver_style = get_driver_style(driver["DriverId"], ["color"], session)

    print(driver_style)

    fig = go.Figure()
    fig.add_trace(
        go.Box(
            x=laps[selected_series],
            name="Lap Time",
            fillcolor=driver_style["color"],
            marker=dict(color="#aaa"),
        )
    )

    st.plotly_chart(fig, use_container_width=True, theme="streamlit")

    tyre_color_map = {}

    for compound in laps["Compound"].unique():
        tyre_color_map[compound] = get_compound_color(compound, session)

    stint_groups = laps.groupby("Stint")

    fig = go.Figure()
    for stint, stint_laps in stint_groups:
        fig.add_trace(
            go.Scatter(
                x=stint_laps["TyreLife"],
                y=stint_laps["LapTime"],
                mode="markers+lines",
                marker=dict(
                    color=[tyre_color_map[comp] for comp in stint_laps["Compound"]],
                    size=10,
                    opacity=0.8,
                ),
                line=dict(width=2, color="gray"),
                name=f"Stint {int(stint)}",
            )
        )

    st.plotly_chart(fig, use_container_width=True, theme="streamlit")


def generate_driver_telemetry_tab(session):
    st.subheader("Driver Telemetry")
    drivers = get_driver_info(session)

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
            key="telemetry_driver_select",
        )
        lap_number = st.selectbox(
            "Select Lap Number",
            options=session.laps.pick_drivers([selected_driver])["LapNumber"].unique(),
            index=None,
            placeholder="Select Lap Number",
            label_visibility="collapsed",
            key="telemetry_lap_select",
        )

    if selected_driver is None:
        st.info("Please select a driver to view telemetry.")
        return

    print("selected_driver", selected_driver)

    driver = drivers[drivers["DriverNumber"] == selected_driver].iloc[0]

    driver_style = get_driver_style(driver["DriverId"], ["color"], session)

    print(driver_style)

    if lap_number is None:
        st.info("Please select a lap number to view telemetry.")
        return

    lap = session.laps.pick_drivers([selected_driver]).pick_laps(lap_number).iloc[0]
    telemetry = lap.get_telemetry()
    time = (
        telemetry["Time"].dt.total_seconds()
        - telemetry["Time"].dt.total_seconds().min()
    )

    options = ["Throttle", "Brake", "Speed", "RPM", "nGear"]
    selected_series = st.segmented_control(
        "Select Series to Plot",
        options=options,
        key="telemetry_series_select",
        default="Throttle",
        label_visibility="collapsed",
    )

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=time,
            y=telemetry[selected_series],
            mode="lines",
            name="Throttle",
            line=dict(color=driver_style["color"], width=2),
        )
    )

    st.plotly_chart(fig, use_container_width=True, theme="streamlit")

    map = go.Figure()
    map.add_trace(
        go.Scatter(
            x=telemetry["X"],
            y=telemetry["Y"],
            mode="markers",
            marker=dict(
                color=telemetry[selected_series],
                colorscale="Viridis",
                size=5,
                colorbar=dict(title=selected_series),
            ),
            name="Track Map",
        )
    )

    st.plotly_chart(map, use_container_width=True, theme="streamlit")


def generate_qualifying_tabs(session):
    tab1, tab2 = st.tabs(qualifying_tabs)
    with tab1:
        st.subheader("Qualifying Results")
        st.write(get_info_table(session, "Qualifying").reset_index(drop=True))
    with tab2:
        generate_driver_lap_times_tab(session)


def generate_race_tabs(session):
    tab1, tab2, tab3 = st.tabs(race_tabs)
    with tab1:
        st.subheader("Race Results")
        st.write(get_info_table(session, "Race").reset_index(drop=True))
    with tab2:
        generate_driver_lap_times_tab(session)
    with tab3:
        generate_driver_telemetry_tab(session)


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
