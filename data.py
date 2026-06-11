import pandas as pd
import numpy as np

def get_power_rating(team):

    row = teams.loc[teams["team"] == team].iloc[0]

    elo = row["elo"]

    market = float(
        row["winning_probability_percent"]
        .replace("%", "")
    )

    market_elo = 1500 + 400 * np.log10(
        market / 0.0326
    )

    return (
        0.65 * elo +
        0.35 * market_elo
    )

teams = pd.read_csv("large_data/teams.csv")
teams["power_rating"] = teams["team"].apply(get_power_rating)

team_ratings = dict(
    zip(
        teams["team"],
        teams["power_rating"]
    )
)

groups = {
    "A": ["Mexico", "South Africa", "South Korea", "Czechia"],
    "B": ["Canada", "Bosnia", "Qatar", "Switzerland"],
    "C": ["Brazil", "Morocco", "Haiti", "Scotland"],
    "D": ["United States", "Paraguay", "Australia", "Turkey"],
    "E": ["Germany", "Curacao", "Ivory Coast", "Ecuador"],
    "F": ["Netherlands", "Japan", "Sweden", "Tunisia"],
    "G": ["Belgium", "Egypt", "Iran", "New Zealand"],
    "H": ["Spain", "Cape Verde", "Saudi Arabia", "Uruguay"],
    "I": ["France", "Senegal", "Iraq", "Norway"],
    "J": ["Argentina", "Algeria", "Austria", "Jordan"],
    "K": ["Portugal", "DR Congo", "Uzbekistan", "Colombia"],
    "L": ["England", "Croatia", "Ghana", "Panama"]
}

all_teams = sorted(
    team
    for teams_in_group in groups.values()
    for team in teams_in_group
)

matches_df = pd.read_csv("large_data/matches.csv")

group_matches = {}

def reset_matches():
    group_matches.clear()

    group_df = matches_df.drop_duplicates(
        subset=["group", "team1", "team2"]
    )

    for group in groups:
        group_matches[group] = (
            group_df[group_df["group"] == group]
            .to_dict("records")
        )

global sim_scores
sim_scores = [
    (0,0),
    (1,0),
    (0,1),
    (1,1),
    (2,0),
    (0,2),
    (2,1),
    (1,2),
    (2,2),
    (3,0),
    (0,3),
    (3,1),
    (1,3)
]

flag_paths = {
    "Algeria": "assets/flags/dz.svg",
    "Argentina": "assets/flags/ar.svg",
    "Australia": "assets/flags/au.svg",
    "Austria": "assets/flags/at.svg",
    "Belgium": "assets/flags/be.svg",
    "Bosnia": "assets/flags/ba.svg",
    "Brazil": "assets/flags/br.svg",
    "Canada": "assets/flags/ca.svg",
    "Cape Verde": "assets/flags/cv.svg",
    "Colombia": "assets/flags/co.svg",
    "Croatia": "assets/flags/hr.svg",
    "Curacao": "assets/flags/cw.svg",
    "Czechia": "assets/flags/cz.svg",
    "DR Congo": "assets/flags/cd.svg",
    "Ecuador": "assets/flags/ec.svg",
    "Egypt": "assets/flags/eg.svg",
    "England": "assets/flags/gb-eng.svg",
    "France": "assets/flags/fr.svg",
    "Germany": "assets/flags/de.svg",
    "Ghana": "assets/flags/gh.svg",
    "Haiti": "assets/flags/ht.svg",
    "Iran": "assets/flags/ir.svg",
    "Iraq": "assets/flags/iq.svg",
    "Ivory Coast": "assets/flags/ci.svg",
    "Japan": "assets/flags/jp.svg",
    "Jordan": "assets/flags/jo.svg",
    "Mexico": "assets/flags/mx.svg",
    "Morocco": "assets/flags/ma.svg",
    "Netherlands": "assets/flags/nl.svg",
    "New Zealand": "assets/flags/nz.svg",
    "Norway": "assets/flags/no.svg",
    "Panama": "assets/flags/pa.svg",
    "Paraguay": "assets/flags/py.svg",
    "Portugal": "assets/flags/pt.svg",
    "Qatar": "assets/flags/qa.svg",
    "Saudi Arabia": "assets/flags/sa.svg",
    "Scotland": "assets/flags/gb-sct.svg",
    "Senegal": "assets/flags/sn.svg",
    "South Africa": "assets/flags/za.svg",
    "South Korea": "assets/flags/kr.svg",
    "Spain": "assets/flags/es.svg",
    "Sweden": "assets/flags/se.svg",
    "Switzerland": "assets/flags/ch.svg",
    "Tunisia": "assets/flags/tn.svg",
    "Turkey": "assets/flags/tr.svg",
    "United States": "assets/flags/us.svg",
    "Uruguay": "assets/flags/uy.svg",
    "Uzbekistan": "assets/flags/uz.svg",
}

global team_chances
team_chances = None

# ROUND_OF_32_TEMPLATE = [
#     (("A", 1), ("B", 1)),
#     (("E", 0), ("3P", 0)),
#     (("F", 0), ("C", 1)),
#     (("C", 0), ("F", 1)),
#     (("I", 0), ("3P", 1)),
#     (("E", 1), ("I", 1)),
#     (("A", 0), ("3P", 2)),
#     (("L", 0), ("3P", 3)),
#     (("G", 0), ("3P", 4)),
#     (("D", 0), ("3P", 5)),
#     (("K", 1), ("L", 1)),
#     (("H", 0), ("J", 1)),
#     (("B", 0), ("3P", 6)),
#     (("J", 0), ("H", 1)),
#     (("K", 0), ("3P", 7)),
#     (("D", 1), ("G", 1)),
# ]

round_of_32_template = [
    ("A1", "B1"),
    ("E0", "3P0"),
    ("F0", "C1"),
    ("C0", "F1"),
    ("I0", "3P1"),
    ("E1", "I1"),
    ("A0", "3P2"),
    ("L0", "3P3"),
    ("G0", "3P4"),
    ("D0", "3P5"),
    ("K1", "L1"),
    ("H0", "J1"),
    ("B0", "3P6"),
    ("J0", "H1"),
    ("K0", "3P7"),
    ("D1", "G1"),
]