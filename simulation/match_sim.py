from data import team_ratings
import numpy as np

def get_elo(team):
    return team_ratings[team]

def expected_score(t1, t2):
    elo_1 = get_elo(t1)
    elo_2 = get_elo(t2)

    diff = elo_1 - elo_2

    goals_1 = 1.6 + diff / 600
    goals_2 = 1.6 - diff / 600

    goals_1 = max(0.2, goals_1)
    goals_2 = max(0.2, goals_2)

    return goals_1, goals_2

def simulate_match(t1, t2):
    lambda_1, lambda_2 = expected_score(t1, t2)

    goals_1 = np.random.poisson(lambda_1)
    goals_2 = np.random.poisson(lambda_2)

    return goals_1, goals_2


