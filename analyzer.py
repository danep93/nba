import pandas as pd

from models import PlayerComp, PercentileFilter
from typing import List
import duckdb
import os
from errors import CSVDataLoadError
import numpy as np
from constants import PID, PLAYER_NAME, GAME_DATE, GID, GAME_NUMBER, SEASON_YEAR, PLAYER_COLS, GAME_COLS, HOLISTIC_STATS
import streamlit as st
from functools import reduce
import os

from vizualization.utils import highlight_max


# DONE todo: use pydantic validator, don't load df if validator fails
# DONE todo: add linear backoff retry to API call and put in util function
# todo: use PANdantic validator when ingesting, not constants file. SEPARATE INGESTINO FOLDER
# todo: add all type inference
# todo: clean earlier files and store somewhere. Join later
# todo: store sql template statements in a sql_constants file

class DataAnalyzer:
    df: pd.DataFrame
    def __init__(self, path, table_name):
        self.table_name = table_name
        if not hasattr(self, 'df') or self.df is None:
            self.df = self._load_csv_from_local(self.get_relative_path(path))
            if 'column00' in self.df.columns:
                self.df.drop('column00', axis=1, inplace=True)

    def get_relative_path(self, file_name):
        script_dir = os.path.dirname(__file__)  # Get the directory of the Streamlit script
        file_path = os.path.join(script_dir, "resources", file_name)  # Construct the file path
        return file_path

    @st.cache_data
    def _load_csv_from_local(_self, path) -> pd.DataFrame:
        if not os.path.exists(path):
            raise CSVDataLoadError(f"Error: Path '{path}' does not exist")
        if not os.path.isfile(path):
            raise CSVDataLoadError(f"Error: '{path}' is not a file")
        if not path.lower().endswith('.csv'):
            raise CSVDataLoadError(f"Error: '{path}' is not a CSV file")
        with duckdb.connect(database=':memory:') as con:
            sql = f"CREATE or replace TABLE {_self.table_name} as select * from '{path}'"
            con.execute(sql)
            return con.execute(f"select * from {_self.table_name}").fetchdf().sort_values(by=PLAYER_NAME)

    def get_display_name(self, player_id, full=False):
        name = self.df.loc[self.df[PID] == np.int64(player_id), PLAYER_NAME][0]
        if not full:
            name = name.split(' ')[0]
        return name


    def get_timeseries_comp_df(self, compare_stat, player_comps: List[PlayerComp]):
        player_dfs = []
        # date_col = GAME_DATE
        df = self.df.copy()
        df[compare_stat] = pd.to_numeric(df[compare_stat], errors='coerce')
        # df = df.dropna(subset=[compare_stat])
        for p in player_comps:
            player_df = df.loc[df[PID] == np.int64(p.player_id)].sort_values(by=GAME_DATE, ascending=True)
            if p.filters:
                filters = " AND ".join([f"{x.field} {x.operator} {x.value}" for x in p.filters])
                player_df = player_df.query(filters)
            if p.playoffs_only:
                # todo:(daniel.epstein) make a dedicated bool column?
                player_df = player_df.loc[player_df[GID].astype(str).str.startswith(('004', '005', '4', '5'))]
            if p.group_by_season:
                # date_col = SEASON_YEAR
                player_df[GAME_DATE] = player_df[SEASON_YEAR].astype(str) + ' SEASON'
                player_df = player_df.groupby([PID, PLAYER_NAME, GAME_DATE])[compare_stat].mean(numeric_only=True).reset_index()

            player_df = player_df[[PID, PLAYER_NAME, GAME_DATE, compare_stat]].sort_values(by=GAME_DATE, ascending=True).reset_index(drop=True)
            player_dfs.append(player_df)
        return pd.concat(player_dfs).reset_index(names=GAME_NUMBER)

    def get_holistic_comp_df(self, player_comps: List[PlayerComp]):
        player_dfs = []
        cols = HOLISTIC_STATS + [PID, PLAYER_NAME]
        # returns player_name, season, Pts, Ast, Reb, Overall Rating
        df = self.df.copy()
        for p in player_comps:
            player_df = df.loc[df[PID] == np.int64(p.player_id)].sort_values(by=GAME_DATE, ascending=True)
            if p.group_by_season:
                player_df[PLAYER_NAME] = player_df[PLAYER_NAME] + "_" + player_df[SEASON_YEAR]
            player_df = player_df[cols].groupby([PID, PLAYER_NAME]).mean().apply(lambda x: round(x,2)).astype(str).reset_index()

            player_df = player_df.sort_values(by=PLAYER_NAME, ascending=True).reset_index(drop=True)
            player_dfs.append(player_df)
        merged = pd.concat(player_dfs).drop(columns=[PID]).reset_index(drop=True)
        merged = merged.style.apply(highlight_max, subset=pd.IndexSlice[:, HOLISTIC_STATS])
        return merged
        # grouped by career by default


    def get_percentile_players(self, pct_filters: List[PercentileFilter]):
        dfs = []
        for f in pct_filters:
            df = self.df.copy().groupby([PID,PLAYER_NAME]).agg({f.field: f.agg}).reset_index()
            pct_col_name = f'PCT_{f.field}'
            df[pct_col_name] = df[f.field].rank(pct=True).round(2)
            df = df.loc[df[pct_col_name] >= f.value/100]
            df[f.field] = df[f.field].round(2)
            dfs.append(df)
        for df in dfs:
            print(f"this one has {df.columns}")
        merged_df = (reduce(lambda left, right: pd.merge(left, right, on=[PID, PLAYER_NAME], how='inner'), dfs))
        merged_df = merged_df.sort_values(by=[f.field for f in pct_filters], ascending=False).reset_index(drop=True)
        merged_df.drop(columns=[PID], inplace=True)
        return merged_df


