from views.specific_score_impact import show_specific_score_impact
from views.current_odds import show_current_odds
from views.game_impact import show_game_impact
from views.likely_matchups import likely_matchups

from streamlit_option_menu import option_menu
import streamlit as st
import importlib
import helper
import data


importlib.reload(helper)

if __name__ == "__main__":
    data.reset_matches()

st.set_page_config(
    page_title="World Cup Simulator",
    page_icon="🏆",
    layout="wide"
)

st.sidebar.title("🏆 World Cup Simulator")

selected = option_menu(
    menu_title=None,
    options=[
        "Current Odds",
        "Game Impact",
        "Specific Score Impact",
        "Likely Matchups",
    ],
    icons = [
        "bar-chart",
        "graph-up",
        "dribbble",
        "shield-shaded"
    ],
    orientation="horizontal",
)

if selected == "Current Odds":
    show_current_odds()

if selected == "Game Impact":
    show_game_impact()

if selected == "Specific Score Impact":
    show_specific_score_impact()

if selected == "Likely Matchups":
    likely_matchups()
