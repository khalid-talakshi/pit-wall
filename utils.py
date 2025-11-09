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
