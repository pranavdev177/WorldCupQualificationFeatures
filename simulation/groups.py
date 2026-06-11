from simulation.match_sim import simulate_match
from helper import apply_match
from data import group_matches, groups


def init_standings(teams):
    return {
        team: {
            "pts": 0,
            "gf": 0,
            "ga": 0,
            "gd": 0
        }
        for team in teams
    }


def compute_group_standings(group):
    matches_list = group_matches[group]

    teams = set()

    for match in matches_list:
        teams.add(match["team1"])
        teams.add(match["team2"])

    standings = init_standings(teams)

    for match in matches_list:

        if match["played"]:
            score1 = int(match["score1"])
            score2 = int(match["score2"])
        else:
            # simulate unplayed match
            score1, score2 = simulate_match(match["team1"], match["team2"])

        apply_match(
            standings,
            match["team1"],
            match["team2"],
            score1,
            score2
        )

    return standings

def sort_standings(standings):

    return sorted(
        standings.items(),
        key=lambda x: (
            x[1]["pts"],
            x[1]["gd"],
            x[1]["gf"]
        ),
        reverse=True
    )

def get_group_table(group_letter):
    standings = compute_group_standings(group_letter)

    return sort_standings(standings)

def get_all_groups():
    group_results = {}

    for group in groups:
        group_results[group] = get_group_table(group)

    return group_results