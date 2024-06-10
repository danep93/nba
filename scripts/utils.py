import pandas as pd
import numpy as np
from nba_api.stats.endpoints import boxscoretraditionalv2
import time
from nba.constants import NBA_TEAMS, TID, SID, GID, GAME_COLS, PLAYER_COLS, MIN, NUM_PLAYER_RETRIES, \
    PLAYER_SLEEP
import logging


def clean_minutes_col(x):
    if isinstance(x,str):
        return int(x.split('.')[0])
    return x

def get_player_games(game_id: str):
    num_retries = 0
    while num_retries < NUM_PLAYER_RETRIES:
        try:
            boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(
                game_id=str(game_id), timeout=120).get_data_frames()[0]
            return clean_player_scores(boxscore)
        except Exception as e:
            logging.info("error on game {}: {}".format(game_id, e))
            num_retries += 1
            time.sleep(PLAYER_SLEEP + num_retries)
        finally:
            time.sleep(1)



def clean_season_games(games_df: pd.DataFrame, season_year: int) -> pd.DataFrame:
    nba_games = games_df[games_df[TID].astype(int).isin([np.int64(team_id) for team_id in NBA_TEAMS.values()])]
    season_games = nba_games.loc[
        (nba_games[SID].astype(str).str.contains(r'.*{}'.format(season_year))) &  # belongs in correct season
        (nba_games[GID].astype(str).str.contains('^[002|004|005]'))  # No preseason games.
        ]
    results = season_games.drop_duplicates(subset=GID)[GAME_COLS.keys()]
    for col, t in GAME_COLS.items():
        results[col] = results[col].astype(t)
    logging.info("Found {} games for season {}".format(len(results), season_year))
    return results


def clean_player_scores(game_df: pd.DataFrame) -> pd.DataFrame:
    players = game_df.dropna(subset=MIN)
    players = players.rename(columns={'TO': 'TURN'})  # TO is a reserved keyword in postgres
    # players.loc[:, PLUS_MINUS] = players[PLUS_MINUS].fillna(0)
    players.loc[:, MIN] = players[MIN].apply(lambda x: clean_minutes_col(x))
    player_stats = players[players[MIN] > 0][PLAYER_COLS.keys()]
    # DATA TYPING
    for col, t in PLAYER_COLS.items():
        player_stats[col] = player_stats[col].astype(t)
    return player_stats
