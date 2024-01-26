from pathlib import Path
from typing import List, Tuple
import numpy as np
import pandas as pd

import plotly.graph_objects as go


def plot_multiple_dfs(dfs_and_columns: List[Tuple[str, pd.DataFrame, List[str]]]):
    fig = go.Figure()

    for name, df, columns in dfs_and_columns:
        for column in columns:
            if column in df.columns:
                fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines', name=f'{name}: {column}'))

    fig.update_layout(
        title='Compare DFs',
        xaxis_title='DateTime',
        yaxis_title='Value',
        legend_title='Variable'
    )

    return fig
