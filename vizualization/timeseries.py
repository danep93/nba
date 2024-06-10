import pandas as pd
from typing import List
import altair as alt

def get_timeseries_chart(df: pd.DataFrame, x: str, y: str, color: str, tooltip: List[str]):
    # Create line chart with tooltips
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=f'{x}:Q',
        y=f'{y}:Q',
        color=f'{color}:N',
        tooltip=tooltip
    ).properties(
        width=600,
        height=400
    ).interactive()
    return chart
