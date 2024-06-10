from nba.analyzer import DataAnalyzer
from nba.models import PlayerFilter, PlayerComp

da = DataAnalyzer(path='/nba/resources/player_games/2022_players.csv', table_name="ots")
compare_stat = "PTS"


player_comps = [
    PlayerComp(player_id=1628971, description="BruceBrown", group_by='GAME_ID', filters=[PlayerFilter(field='MIN',operator='>',value=15)]),
    PlayerComp(player_id=1631128, description="Christian")
]


# results = da.compare_players_over_time('PTS', filters)
df = da.get_player_comp_df('PTS', player_comps)
results = da._get_compare_sql('PTS', player_comps)
print(results)





#     st.session_state.pct_filters = []  # List to store filters
#     st.session_state.form_count = 1
#     for i in range(st.session_state.form_count):
#         create_form(i)
#
#     if st.button('Add Another Filter'):
#         st.session_state.form_count += 1  # Increment the form count
#
#     st.write("Current Filters:")
#     for i, filter_obj in enumerate(st.session_state.pct_filters):
#         st.write(f"Filter {i + 1}: {filter_obj.field}")
#
#     # with st.form(f"pct_form_{fcounter}"):
#     #     st.write("Percentile filter")
#     #     slider_val = st.slider("Form slider")
#     #     pct_metric = COMPARE_METRICS[st.selectbox("Select players", COMPARE_METRICS.keys())]
#     # pct_filters.append()
#
#
#
#
# def create_form(i):
#     with st.form(key=f'form_{i}'):
#         pct_metric = COMPARE_METRICS[st.selectbox("Select players", COMPARE_METRICS.keys(), key=f"stat_{i}")]
#         value = st.slider('Select minimum percentile', 0, 100, 10, key=f'value_{i}')
#         agg = st.selectbox('Select Aggregation', ['mean', 'min', 'max'], key=f'agg_{i}')
#         submitted = st.form_submit_button('Add')
#         if submitted:
#             st.session_state.pct_filters.append(PercentileFilter(field=pct_metric, value=value, agg=agg))
#             st.success(f"Filter added: Stat={pct_metric}, Value={value}, Aggregation={agg}")

    # Every form must have a submit button.
    #     submitted = st.form_submit_button("Submit")
    #     if submitted:
    #         st.write("slider", slider_val, "checkbox", checkbox_val)
    #
    # st.write("Outside the form")


    # with st.popover(player):
    #     player_comps.append(PlayerComp(
    #         player_id=player_id,
    #         description=player_name,
    #         filters=[PlayerFilter(
    #             field=COMPARE_METRICS[st.selectbox("Select field", COMPARE_METRICS.keys(), key=player_id + "_field")],
    #             operator=st.selectbox("Select operator", [">", "==", "<"], key=player_id + "_operator"),
    #             value=st.number_input("Enter value", step=1, value=0, key=player_id + "_value"))
    #         ]
    #     ))



    # pct_button_clicked = st.button("Start Percentile Lookup")
    # pct_filters = [PercentileFilter(
    #     field=COMPARE_METRICS[st.selectbox("Select a percentile filter", COMPARE_METRICS.keys())],
    #     value=st.number_input("Percentile", step=10, value=50),
    #     agg=st.selectbox("Select an agg function", ['mean', 'min', 'max'])
    # )]
    # if pct_button_clicked:
    #     results = da.get_percentile_players(pct_filters).head(10)
    #     st.write(results)




# #
# def add_slider(percentiles):
#     new_percentile = max(percentiles) + 1
#     percentiles.append(new_percentile)
#     filters[f'Percentile {new_percentile}'] = st.slider(f'Percentile {new_percentile}', min_value=0.0, max_value=1.0, value=(0.0, 1.0), step=0.01)


