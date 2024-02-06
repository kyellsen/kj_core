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


def plot_polar_multiple(dfs_and_names: List[Tuple[str, pd.DataFrame]],
                        columns: List[str]) -> go.Figure:
    """
    Erstellt einen gemeinsamen Polar-Plot für verschiedene DataFrames.

    Parameters:
    - dfs_and_names (List[Tuple[str, pd.DataFrame]]): Liste von Tupeln, wobei jedes Tupel aus einem String (Name) und einem DataFrame besteht.
    - columns (List[str], optional): Liste der Spalten, die dargestellt werden sollen. Standardmäßig sind dies Neigungswerte in Ost-West und Nord-Süd Richtung.

    Returns:
    - go.Figure: Ein Plotly Figure-Objekt, das den Polar-Plot darstellt.
    """

    fig = go.Figure()

    for name, df in dfs_and_names:
        if all(column in df for column in columns):
            x, y = columns
            r = np.sqrt(df[x] ** 2 + df[y] ** 2)
            theta = np.degrees(np.arctan2(df[y], df[x]))

            fig.add_trace(go.Scatterpolar(
                r=r,
                theta=theta,
                mode='markers',
                name=name,
                marker=dict(size=5)
            ))

    # Layout-Anpassungen
    fig.update_layout(
        title='Polar Plot of Tree Inclination Across Different Processing States',
        polar=dict(
            radialaxis=dict(visible=True),
            angularaxis=dict(direction="clockwise", period=360)
        ),
        legend_title='Processing State'
    )

    return fig
