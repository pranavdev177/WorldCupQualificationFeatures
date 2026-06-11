import streamlit as st

import data
from simulation.groups import get_all_groups
from simulation.qualification import get_round_of_32_matchups

def likely_matchups():
    st.sidebar.header("Simulation Settings")

    n_sims = st.sidebar.slider('Number of Simulations', min_value=100, max_value=10000, value=2500, step=100)
    matchups_to_show = st.sidebar.slider('Matchups to Show', min_value=5, max_value=100, value=20, step=1)

    one_team_only = st.sidebar.selectbox(
        "Only Look For 1 Team:",
        data.all_teams,
        placeholder="Choose a team",
        index=None
    )

    run = st.sidebar.button("Run Simulation")

    if run:
        with st.spinner('Running simulations...'):
            run_simulation(n_sims, matchups_to_show, one_team_only)

def run_simulation(sims_to_run, matchups_to_show, one_team_only):
    matchup_counts = {}

    for i in range(sims_to_run):

        group_results = get_all_groups()
        games = get_round_of_32_matchups(group_results)


        for game in games:
            teams = [game.partition('_')[0], game.partition('_')[2]]
            teams.sort()

            alpha_game = f'{teams[0]}_{teams[1]}'

            if alpha_game not in matchup_counts:
                matchup_counts[alpha_game] = 1
            else:
                matchup_counts[alpha_game] += 1

    matchup_counts = dict(sorted(matchup_counts.items(), key=lambda item: item[1], reverse=True))


    if one_team_only:
        matchup_counts = {
            k: v for k, v in matchup_counts.items() if one_team_only in k.split("_")
        }

    if matchups_to_show < len(matchup_counts) and not one_team_only:
        matchup_counts = dict(list(matchup_counts.items())[:matchups_to_show])



    display_cards(matchup_counts, sims_to_run)


def display_cards(matchup_counts, sims_ran):
    num_columns = 2

    # Create the master structural grid columns
    grid_cols = st.columns(num_columns)

    for idx, (key, value) in enumerate(matchup_counts.items()):
        team1 = key.partition("_")[0]
        team2 = key.partition("_")[2]

        chance_of_matchup = f"{round(value / sims_ran * 100, 1)}%"


        target_column = grid_cols[idx % num_columns]

        with target_column:
            with st.container(border=True):
                # Setup internal columns inside the card for flags and metrics
                col1, col2, col3, col4 = st.columns([2, 1, 2, 2])

                with col1:
                    st.image(data.flag_paths[team1], use_container_width=True)
                    st.markdown(f"<p style='text-align: center; font-weight: bold; margin-top: 5px;'>{team1}</p>",
                                unsafe_allow_html=True)

                with col2:
                    st.markdown("<h4 style='text-align: center; line-height: 2;'>VS</h4>", unsafe_allow_html=True)

                with col3:
                    st.image(data.flag_paths[team2], use_container_width=True)
                    st.markdown(f"<p style='text-align: center; font-weight: bold; margin-top: 5px;'>{team2}</p>",
                                unsafe_allow_html=True)

                with col4:
                    st.metric(label="Likelihood", value=chance_of_matchup)

    #st.write(group_results)

