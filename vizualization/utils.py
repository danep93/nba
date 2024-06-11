import numpy as np
import pandas as pd
from constants import PID
from models import PlayerComp


def highlight_max(s):
    is_max = s == s.max()
    result = ['background-color: yellow' if v else '' for v in is_max]
    return result

def get_colored_stats(p: PlayerComp, compare_stat_name: str, df: pd.DataFrame) -> str:
    stats = calculate_stats(df.loc[df[PID] == p.player_id, [compare_stat_name]])
    colored_stats = (
        f"<span style='color: Black;'>{p.description} {compare_stat_name}:</span> "
        f"<span style='color: Blue;'>Min: {stats['min']:.2f}</span> "
        f"<span style='color: Red;'>Max: {stats['max']:.2f}</span> "
        f"<span style='color: Green;'>Avg: {stats['avg']:.2f}</span> "
        f"<span style='color: Orange;'>Std-Dev: {stats['stddev']:.2f}</span>"
    )
    return f"<div>{colored_stats}</div>"


def calculate_stats(player_data):
    stats= {
        'min': np.min(player_data),
        'max': np.max(player_data),
        'avg': np.round(np.mean(player_data),2),
        'stddev': np.std(player_data).item()
    }
    return stats
