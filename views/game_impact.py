from helper import get_unplayed_opponents
import streamlit as st
from components.group_tables import display_group_tables
from simulation import qualification
import data

def show_game_impact():
    st.title("Impacts of a Game")
    st.sidebar.header("Choose the Game")

    n_sims = st.sidebar.slider('Number of Simulations', min_value=100, max_value=2500, value=1000, step=100)

    button_placeholder = st.sidebar.empty()

    team_1 = st.sidebar.selectbox(
        "Team 1",
        data.all_teams,
        placeholder="Choose a team",
        index=None
    )


    if team_1:
        st.sidebar.image(data.flag_paths[team_1], width=200)

        team_2 = st.sidebar.selectbox(
            "Team 2",
            get_unplayed_opponents(team_1),
            placeholder="Choose a team",
            index=None
        )

        if team_2:
            st.sidebar.image(data.flag_paths[team_2], width=200)

            run = button_placeholder.button(
                "Run Simulations",
            )

            if run:
                handle_scores(team_1, team_2, n_sims)

def handle_scores(team1, team2, sims):
    qual_percentages = []

    with st.spinner('Running simulations...'):
        for score in data.sim_scores:
            qual_percentages.append(qualification.qualification_odds_given_result(team1, team2, score[0], score[1], sims))

    cols_per_row = 2

    results_list = list(qual_percentages)

    for i in range(0, len(results_list), cols_per_row):
        cols = st.columns(cols_per_row)

        for j in range(cols_per_row):
            if i + j < len(results_list):
                with cols[j]:
                    show_score_card(
                        results_list[i + j],
                        team1,
                        team2
                    )

def show_score_card(result, team1, team2):
    with st.container(border=True):

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.image(data.flag_paths[team1], width=100)

            if "change_t1" in result:
                st.metric(
                    label="Chance to qualify",
                    value=f"{result[team1]:.1f}%",
                    delta=f"{result["change_t1"]}%"
                )
            else:
                st.metric(
                    label="Chance to qualify",
                    value=f"{result[team1]:.1f}%"
                )

        with col2:
            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    padding-top:35px;
                ">
                    <h1>{result['score1']} - {result['score2']}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.image(data.flag_paths[team2], width=100)

            if "change_t2" in result:
                st.metric(
                    label="Chance to qualify",
                    value=f"{result[team2]:.1f}%",
                    delta=f"{result["change_t2"]}%"
                )
            else:
                st.metric(
                    label="Chance to qualify",
                    value=f"{result[team2]:.1f}%"
                )