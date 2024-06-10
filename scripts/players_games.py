import pandas as pd
from typing import List
from nba.constants import GID, SEASON_START, CSV_OUTPUT_PATH
import logging
from nba_api.stats.endpoints import leaguegamefinder as lgf
import time
from utils import clean_season_games, get_player_games

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_season_games(season_year: int) -> pd.DataFrame:
    # returns one row per game. Contains facts like winning team
    games_df = lgf.LeagueGameFinder(
        league_id_nullable='00',
        date_from_nullable=SEASON_START.format(str(season_year)),
        date_to_nullable=SEASON_START.format(str(season_year+1)),
    ).get_data_frames()[0]
    results = clean_season_games(games_df, season_year)
    return results


def get_player_stats(game_ids: List[str]) -> pd.DataFrame:
    # returns one row per player-game. Contains facts like player rebounds, pts, etc...
    dfs = []
    start_time = time.time()
    for i in range(0, len(game_ids)):
        dfs.append(get_player_games(game_ids[i]))
        if i % 100 == 0:
            logging.info("at row {}".format(i))
    logging.info("got all games in {} seconds".format(time.time() - start_time))
    return pd.concat(dfs)


def main():
    # https://github.com/swar/nba_api/issues/220
    years = [x for x in range(1983,1986)]
    for year in years:
        games = get_season_games(year)
        player_stats = get_player_stats(list(games[GID]))
        obt = pd.merge(left=player_stats, right=games, how='left', on=GID)
        obt.to_csv(CSV_OUTPUT_PATH.format(year), index=False)


if __name__ == "__main__":
    main()
