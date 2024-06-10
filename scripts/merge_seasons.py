import pandas as pd
from utils import clean_season_games, clean_player_scores
# combine them all
# filter out teams not in teams and preseason
# cast all columns correctly
from nba.constants import GID

# todo:(daniel) global group all and global playoffs button applied to override each filter. IF it gets clicked everything toggles on.
# todo: global mean/min/max/sum filters apply to all percentile stats
# todo: game number should maybe say season number or mixed (season + game) counter
# todo: tiles for player filters CSS inline to save space. Have some stats for people already loaded
# todo: sentence description in dynamic text stentences or tool tips
# todo:
input_path = "~/Desktop/nba_obt_backup/game_seasons/{}_players.csv"
output_path = '/nba/resources/player_games/old_combined_player_games.csv'
dfs = []
years = [x for x in range(1983,1986)]
for year in years:
    print("in year {}".format(year))
    df = pd.read_csv(input_path.format(year))
    clean_games = clean_season_games(df, year)
    clean_scores = clean_player_scores(df)
    season_box_scores = pd.merge(left=clean_scores, right=clean_games, on=GID, how='inner')
    season_box_scores['SEASON_YEAR'] = season_box_scores['SEASON_ID'].apply(lambda x: x[-4:])
    dfs.append(season_box_scores)
results = pd.concat(dfs)

# remove preseason and different teams


# results.to_csv(output_path, index=False)