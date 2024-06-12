CSV_INPUT_PATH = "all_nba_games.csv"
CSV_OUTPUT_PATH = "/nba/resources/player_games/{}_players.csv"
NUM_PLAYER_RETRIES = 5
PLAYER_SLEEP = 20
SEASON_START = "09/01/{}"

DEFAULT_MANY_PLAYERS_IDS = [
        "Stephen Curry (201939)",
        "Damian Lillard (203081)",
        "Luka Doncic (1629029)",
        "Kyrie Irving (202681)"
]
DEFAULT_HOLISTIC_PLAYER_IDS = [
        'Kobe Bryant (977)',
        'LeBron James (2544)',
        'Michael Jordan (893)',
]

HOLISTIC_STATS = ['PTS','AST','REB','STL','BLK','TURN','PF']

NBA_TEAMS = {'ATL': 1610612737, 'BOS': 1610612738, 'CLE': 1610612739, 'NOP': 1610612740, 'CHI': 1610612741, 'DAL': 1610612742, 'DEN': 1610612743, 'GSW': 1610612744, 'HOU': 1610612745, 'LAC': 1610612746, 'LAL':1610612738, 'MIA': 1610612748, 'MIL': 1610612749, 'MIN': 1610612750, 'BKN': 1610612751, 'NYK': 1610612752, 'ORL': 1610612753, 'IND': 1610612754, 'PHI': 1610612755, 'PHX': 1610612756, 'POR': 1610612757, 'SAC': 1610612758, 'SAS': 1610612759, 'OKC': 1610612760, 'TOR': 1610612761, 'UTA': 1610612762, 'MEM': 1610612763, 'WAS': 1610612764, 'DET': 1610612765, 'CHA': 1610612766}
COMPARE_METRICS = {
        'POINTS': 'PTS',
        'ASSISTS': 'AST',
        'STEALS': 'STL',
        'MINUTES': 'MIN',
        'FIELD_GOALS_MADE': 'FGM',
        'FIELD_GOALS_ATTEMPTED': 'FGA',
        'FIELD_GOAL_PERCENTAGE': 'FG_PCT',
        'THREE_POINTERS_ATTEMPTED': 'FG3A',
        'THREE_POINTERS_MADE': 'FG3M',
        'THREE_POINTER_PERCENTAGE': 'FG3_PCT',
        'FREE_THROWS_ATTEMPTED': 'FTA',
        'FREE_THROWS_MADE': 'FTM',
        'PLUS MINUS': 'PLUS_MINUS',
        'OFFENSIVE_REBOUNDS': 'OREB',
        'DEFENSIVE_REBOUNDS': 'DREB',
        'REBOUNDS': 'REB',
        'BLOCKS': 'BLK',
        'TURNOVERS': 'TURN',
        'PERSONAL_FOULS': 'PF'
}

GID = 'GAME_ID'
PID = 'PLAYER_ID'
SID = 'SEASON_ID'
TID = 'TEAM_ID'
MIN = 'MIN'
PLAYOFFS = 'PLAYOFFS'
PLUS_MINUS = 'PLUS_MINUS'
PLAYER_NAME = 'PLAYER_NAME'
GAME_DATE = 'GAME_DATE'
GAME_NUMBER = 'GAME_NUMBER'
SEASON_YEAR = 'SEASON_YEAR'
PLAYER_COLS = {
        'GAME_ID': str,
        'TEAM_ID': str,
        'PLAYER_ID': str,
        'PLAYER_NAME': str,
        'START_POSITION': str,
        'MIN': 'Int64',
        'FGM': 'Int64',
        'FGA': 'Int64',
        'FG_PCT': float,
        'FG3M': 'Int64',
        'FG3A': 'Int64',
        'FG3_PCT': float,
        'FTM': 'Int64',
        'FTA': 'Int64',
        'FT_PCT': float,
        'OREB': 'Int64',
        'DREB': 'Int64',
        'REB': 'Int64',
        'AST': 'Int64',
        'STL': 'Int64',
        'BLK': 'Int64',
        'TURN': 'Int64',
        'PF': 'Int64',
        'PTS': 'Int64',
        'PLUS_MINUS': 'Int64',
}
GAME_COLS = {
       'SEASON_ID': str,
       'GAME_ID': str,
       'GAME_DATE': str,
       'SEASON_YEAR': str,
}
