from simulation.groups import get_all_groups
import data
from helper import set_match_result, get_group
import streamlit as st
from large_data.third_place_team import THIRD_PLACE_TABLE

def get_qualified_teams(group_results):
    qualified = []

    third_place = []

    for group, table in group_results.items():
        qualified.append(table[0])
        qualified.append(table[1])

        third_place.append(table[2])

    third_place.sort(
        key=lambda x: (
            x[1]["pts"],
            x[1]["gd"],
            x[1]["gf"]
        ),
        reverse=True
    )

    qualified += third_place[:8]

    return qualified


def get_round_of_32_matchups(results):
    third_place = []

    team_spot = {}

    for group, table in results.items():
        team_spot[f"{group}0"] = table[0][0]
        team_spot[f"{group}1"] = table[1][0]

        third_place.append(table[2])

    third_place.sort(
        key=lambda x: (
            x[1]["pts"],
            x[1]["gd"],
            x[1]["gf"]
        ),
        reverse=True
    )

    string = ''

    for third_place_team in third_place[:8]:
        string += get_group(third_place_team[0])

    string = "".join(sorted(string))
    key = THIRD_PLACE_TABLE[string]

    for third_place_team in third_place[:8]:
        index = key.index(get_group(third_place_team[0]))
        team_spot[f"3P{index}"] = third_place_team[0]

    matches = []

    for game in data.round_of_32_template:
        matches.append(f"{team_spot[game[0]]}_{team_spot[game[1]]}")
        #st.write(f"{team_spot[game[0]]} vs {team_spot[game[1]]}")

    return matches


def get_qualification_percentages_running_sims(num_sims):
    qualification_counts = {}

    for team in data.teams["team"]:
        qualification_counts[team] = 0

    for _ in range(num_sims):

        group_results = get_all_groups()
        qualified = get_qualified_teams(group_results)

        for team, stats in qualified:
            qualification_counts[team] += 1

    for item in qualification_counts:
        qualification_counts[item] /= num_sims
        qualification_counts[item] *= 100
        qualification_counts[item] = round(qualification_counts[item], 2)

    return qualification_counts


def qualification_odds_given_result(t1, t2, s1, s2, simulations=1000):
    data.reset_matches()
    set_match_result(t1, t2, s1, s2)

    qualification_counts = get_qualification_percentages_running_sims(simulations)

    if data.team_chances:
        return {
            t1: qualification_counts[t1],
            t2: qualification_counts[t2],
            'score1':s1,
            'score2':s2,
            'change_t1':round((qualification_counts[t1] - data.team_chances[t1]), 1),
            'change_t2':round((qualification_counts[t2] - data.team_chances[t2]), 1),
        }
    else:
        return {
            t1: qualification_counts[t1],
            t2: qualification_counts[t2],
            'score1': s1,
            'score2': s2
        }
