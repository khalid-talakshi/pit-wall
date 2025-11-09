import numpy as np
import pandas as pd

from constants import (
    CONVENTIONAL_OPTIONS,
    SPRINT_OPTIONS,
    SPRINT_QUALIFYING_OPTIONS,
    SPRINT_SHOOTOUT_OPTIONS,
)


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


def get_info_table(session, session_option):
    RACE_KEYS = [
        "ClassifiedPosition",
        "Points",
        "FullName",
        "TeamName",
        "GridPosition",
        "Laps",
        "Status",
    ]

    QUALIFYING_KEYS = [
        "Position",
        "FullName",
        "TeamName",
        "Q1",
        "Q2",
        "Q3",
    ]
    session.results["Q1"] = session.results["Q1"].apply(
        lambda x: x.total_seconds() if pd.notnull(x) else np.nan
    )
    session.results["Q2"] = session.results["Q2"].apply(
        lambda x: x.total_seconds() if pd.notnull(x) else np.nan
    )
    session.results["Q3"] = session.results["Q3"].apply(
        lambda x: x.total_seconds() if pd.notnull(x) else np.nan
    )
    if session_option == "Race":
        return session.results[RACE_KEYS]
    elif session_option == "Qualifying":
        return session.results[QUALIFYING_KEYS]
    else:
        return None
