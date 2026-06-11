from components.group_tables import display_group_tables
from simulation import qualification
import streamlit as st
import data

def show_current_odds():
    st.title("🏆 Current World Cup Odds")

    st.sidebar.header("Simulation Settings")

    n_sims = st.sidebar.slider('Number of Simulations', min_value=100, max_value=5000, value=1000, step=100)
    run = st.sidebar.button("Run Simulation")


    if run:
        with st.spinner('Running simulations...'):
            group_odds = qualification.get_qualification_percentages_running_sims(n_sims)
            data.team_chances = group_odds

    if data.team_chances:
        display_group_tables(data.team_chances)

