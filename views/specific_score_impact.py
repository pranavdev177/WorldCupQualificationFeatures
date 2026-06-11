from components.group_tables import display_group_tables
from helper import get_unplayed_opponents, set_match_result
from simulation import qualification
import streamlit as st
import data

def show_specific_score_impact():
    st.sidebar.header("Choose the Game and Score")

    n_sims = st.sidebar.slider('Number of Simulations', min_value=100, max_value=5000, value=1000, step=100)

    button_placeholder = st.sidebar.empty()

    team_1 = st.sidebar.selectbox(
        "Team 1",
        data.all_teams,
        placeholder="Choose a team",
        index=None
    )

    if team_1:
        team_2 = st.sidebar.selectbox(
            "Team 2",
            get_unplayed_opponents(team_1),
            placeholder="Choose a team",
            index=None
        )

        if team_2:
            score_1 = st.sidebar.number_input(
                f"{team_1} Score",
                value=0,
                min_value=0
            )

            score_2 = st.sidebar.number_input(
                f"{team_2} Score",
                value=0,
                min_value=0
            )

            run = button_placeholder.button(
                "Run Simulations",
            )

            if run:
                set_match_result(team_1, team_2, score_1, score_2)
                results = qualification.get_qualification_percentages_running_sims(n_sims)
                data.reset_matches()

                display_group_tables(results, True)