import math
from pathlib import Path

from data import group_matches, groups
import pandas as pd
import numpy as np

def apply_match(standings, t1, t2, s1, s2):
    standings[t1]["gf"] += s1
    standings[t1]["ga"] += s2
    standings[t1]["gd"] += s1 - s2

    standings[t2]["gf"] += s2
    standings[t2]["ga"] += s1
    standings[t2]["gd"] += s2 - s1

    if s1 > s2:
        standings[t1]["pts"] += 3
    elif s2 > s1:
        standings[t2]["pts"] += 3
    else:
        standings[t1]["pts"] += 1
        standings[t2]["pts"] += 1

def set_match_result(t1, t2, s1, s2):
    for matches_list in group_matches.values():

        for match in matches_list:

            if {match["team1"], match["team2"]} == {t1, t2}:

                match["played"] = True

                if match["team1"] == t1:
                    match["score1"] = s1
                    match["score2"] = s2
                else:
                    match["score1"] = s2
                    match["score2"] = s1

                return True

    return False

def format_group_odds(group_odds):
    formatted = {}

    for group, teams, in groups.items():
        rows = []

        for team in teams:
            rows.append({
                "Team": team,
                "Qualification %": group_odds[team]
            })

        df = pd.DataFrame(rows)

        df = df.sort_values("Qualification %", ascending=False)

        formatted[group] = df

    return formatted

def style_group_table(df):
    def color_value(val):
        if val >= 90:
            return "background-color: #1f7a1f; color: white;"
        elif val >= 75:
            return "background-color: #2d8f2d; color: white;"
        elif val >= 60:
            return "background-color: #b38f00; color: white;"
        else:
            return "background-color: #8b1a1a; color: white;"

    styled = df.style.map(
        color_value,
        subset=["Qualification %"]
    )

    return styled

def get_unplayed_opponents(team):
    options = []

    group = next((k for k, v in groups.items() if team in v), None)

    for match in group_matches[group]:
        if match['played'] == False:
            if match["team1"] == team:
                options.append(match["team2"])
            elif match["team2"] == team:
                options.append(match["team1"])

    return options

def get_group(team_name):
    for group_letter, teams in groups.items():
        if team_name in teams:
            return group_letter
    return None
