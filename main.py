import streamlit as st
import re
from nba.constants import COMPARE_METRICS, CSV_INPUT_PATH, GAME_NUMBER, PID, PLAYER_NAME, GAME_DATE
from nba.analyzer import DataAnalyzer
from models import PlayerComp, PlayerFilter, PercentileFilter
from nba.vizualization.timeseries import get_timeseries_chart
from nba.vizualization.utils import get_colored_stats

def main():
    # MELT DF
    # VIZ
    da = DataAnalyzer(path=CSV_INPUT_PATH, table_name="ots")
    player_comps = []

    st.title("Compare specific players over time")

    # DISPLAY AND RECORD METRIC TO COMPARE
    compare_stat_name = st.selectbox("Select a stat", COMPARE_METRICS.keys())
    compare_stat = COMPARE_METRICS[compare_stat_name]

    # DISPLAY AND RECORD PLAYERS TO COMPARE
    players = list(set(da.df['PLAYER_NAME'] + ' (' + da.df['PLAYER_ID'].astype(str) + ')'))
    selected_players = st.multiselect("Select players", players)

    for player in selected_players:
        player_id = re.findall(r'\((.*?)\)', player)[0]
        player_name = player.split('(')[0].strip()
        with st.popover(player):
            field_key = st.selectbox("Select field", COMPARE_METRICS.keys(), key=player_id+"_field")
            operator = st.selectbox("Select operator", [">", "==", "<"], key=player_id+"_operator")
            value = st.number_input("Enter value", step=1, value=0, key=player_id+"_value")
            pf = [PlayerFilter(field=COMPARE_METRICS[field_key], operator=operator, value=value)]
            playoffs = st.checkbox("Playoffs only", key=player_id+"_cb")
            groupby = st.checkbox("Group by season", key=player_id + "_gb")
            player_comps.append(PlayerComp(
                player_id=player_id,
                description=player_name,
                filters=pf,
                playoffs_only=playoffs,
                group_by_season=groupby
            ))

    line_button_clicked = st.button("Generate Line Graph")
    if line_button_clicked:

        # GET DF
        df = da.get_player_comp_df(compare_stat, player_comps)
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
    st.title("Lookup players based on percentile rankings")
    pct_metric_names = st.multiselect("Select stats", COMPARE_METRICS.keys())
    pct_filters = []

    for metric in pct_metric_names:
        with st.popover(metric):
            value = st.number_input("Enter value", step=1, value=95, key=f"{metric}_value")
            # value = st.slider('Select minimum percentile', 0, 100, 95, key=f'{metric}_value')
            agg = st.selectbox("Aggregated by", ['mean','min','max','sum'], key=f'{metric}_agg')
        pct_filters.append(PercentileFilter(field=COMPARE_METRICS[metric], value=value, agg=agg))

    search_pcts = st.button('Search')
    if search_pcts:
        results = da.get_percentile_players(pct_filters)
        st.write(results)




if __name__ == "__main__":
    main()
