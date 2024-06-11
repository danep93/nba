from typing import List

import streamlit as st
import re
from constants import COMPARE_METRICS, CSV_INPUT_PATH, GAME_NUMBER, PID, PLAYER_NAME, GAME_DATE, \
    DEFAULT_MANY_PLAYERS_IDS, DEFAULT_HOLISTIC_PLAYER_IDS
from analyzer import DataAnalyzer
from models import PlayerComp, PlayerFilter, PercentileFilter
from vizualization.timeseries import get_timeseries_chart
from vizualization.utils import get_colored_stats

# todo: allow multiple filters
# todo: allow checkboxes for filters to only apply to some people

@st.experimental_dialog("Adding a stats based filter")
def create_stats_filter() -> PlayerFilter:
    pf = None
    field_key = st.selectbox("Filter by field", COMPARE_METRICS.keys())
    operator = st.selectbox("Select operator", [">", "==", "<"])
    value = st.number_input("Enter value", step=1, value=0)
    if st.button("Submit"):
        pf = PlayerFilter(field=COMPARE_METRICS[field_key], operator=operator, value=value)
        st.session_state.player_filters = [pf]
        st.rerun()


def main():
    # MELT DF
    # VIZ
    da = DataAnalyzer(path=CSV_INPUT_PATH, table_name="ots")
    if 'player_filters' not in st.session_state:
        st.session_state.player_filters = []
    players = list(set(da.df['PLAYER_NAME'] + ' (' + da.df['PLAYER_ID'].astype(str) + ')'))


    st.header("Many stats many players")
    holistic_players = st.multiselect("Select players (maximum 5)",
                                      players, default=DEFAULT_HOLISTIC_PLAYER_IDS, max_selections=5)
    holistic_player_comps = []
    for player in holistic_players:
        holistic_player_id = re.findall(r'\((.*?)\)', player)[0]
        holistic_player_name = player.split('(')[0].strip()
        holistic_player_comps.append(PlayerComp(
            player_id=holistic_player_id,
            description=holistic_player_name,
        ))
    st.dataframe(da.get_holistic_comp_df(holistic_player_comps))




    st.header("One stat many players over time")

    # DISPLAY AND RECORD METRIC TO COMPARE
    compare_stat_name = st.selectbox("Select a stat to compare", COMPARE_METRICS.keys())
    compare_stat = COMPARE_METRICS[compare_stat_name]

    # DISPLAY AND RECORD PLAYERS TO COMPARE
    selected_players = st.multiselect("Select players (maximum 10)",
                                      players, default=DEFAULT_MANY_PLAYERS_IDS, max_selections=10)

    group_by_season = st.checkbox("Group by season")
    playoffs_only = st.checkbox("Playoffs only")
    for f in st.session_state.player_filters:
        st.button(f'Filter: {f.pretty_print()}')
    add_filter = st.button("Add a stats based filter")
    if add_filter:
        create_stats_filter()

    player_comps = []
    for player in selected_players:
        player_id = re.findall(r'\((.*?)\)', player)[0]
        player_name = player.split('(')[0].strip()
        player_comps.append(PlayerComp(
            player_id=player_id,
            description=player_name,
            filters=st.session_state.player_filters,
            playoffs_only=playoffs_only,
            group_by_season=group_by_season,
        ))
    if st.session_state.player_filters:
        st.write("player filters are {}".format(st.session_state.player_filters[0].pretty_print()))

    # GET DF
    df = da.get_timeseries_comp_df(compare_stat, player_comps)
    melted_df = df.melt(
        id_vars=[GAME_NUMBER, PID, PLAYER_NAME, GAME_DATE],
        value_vars=compare_stat, var_name='metric',
        value_name=compare_stat_name
    )

    chart = get_timeseries_chart(
        df=melted_df,
        x=GAME_NUMBER,
        y=compare_stat_name,
        color=PLAYER_NAME,
        tooltip=[compare_stat_name, PLAYER_NAME, GAME_DATE]
    )
    st.altair_chart(chart, use_container_width=True)

    # write np stats
    for p in player_comps:
        st.markdown(get_colored_stats(p, compare_stat_name, melted_df), unsafe_allow_html=True)

    # END TIMESERIES PORTION
    # BEGIN PERCENTILES PORTION
    # DISPLAY AND RECORD PLAYERS TO COMPARE
    st.title("Lookup based on percentile rankings")
    pct_filters = []

    # pct_metric_names = st.multiselect("Select stats", COMPARE_METRICS.keys())
    # percentile = st.number_input("Min Percentile", step=1, value=95)
    # agg = st.selectbox("Aggregated by", ['mean','min','max','sum'])

    # Allow user to select stats in the first column
    pct_metric_names = st.multiselect("Select stats", list(COMPARE_METRICS.keys()), default=['POINTS','ASSISTS'])
    col1, col2 = st.columns([1, 1])

    # Allow user to input percentile in the second column
    with col1:
        percentile = st.number_input("Min Percentile", step=1, value=98)

    # Allow user to select aggregation method in the third column
    with col2:
        agg = st.selectbox("Aggregated by", ['mean', 'min', 'max', 'sum'])
    for metric in pct_metric_names:
        pct_filters.append(PercentileFilter(field=COMPARE_METRICS[metric], value=percentile, agg=agg))
    results = da.get_percentile_players(pct_filters)
    st.dataframe(results)


    # for metric in pct_metric_names:
    #     with st.popover(metric):
    #         value = st.number_input("Enter value", step=1, value=95, key=f"{metric}_value")
    #         # value = st.slider('Select minimum percentile', 0, 100, 95, key=f'{metric}_value')
    #         agg = st.selectbox("Aggregated by", ['mean','min','max','sum'], key=f'{metric}_agg')
    #     pct_filters.append(PercentileFilter(field=COMPARE_METRICS[metric], value=value, agg=agg))

    # search_pcts = st.button('Search')
    # if search_pcts:



# cols = st.columns(len(selected_players) + 1)
# for i in range(0, len(selected_players)+1):
#     with cols[i]:
#         if i == 0:
#             name = st.checkbox('All', value=True)
#         else:
#             name = st.checkbox(f'{selected_players[i-1].split(" ")[0]}')


if __name__ == "__main__":
    main()
