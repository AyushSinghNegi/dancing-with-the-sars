"""Charts (Plotly). One axis per chart, thin marks, recessive grid, text in ink colours."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from . import ui

FONT = dict(family="IBM Plex Sans, sans-serif", size=13, color=ui.INK)
GRID = "#e3e7e6"


def _layout(fig, height=300, title=None):
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=40 if title else 10, b=10), font=FONT,
                      title=dict(text=title, x=0, font=dict(size=15)) if title else None,
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False,
                      hoverlabel=dict(bgcolor="white", font=FONT))
    fig.update_xaxes(showgrid=False, linecolor=GRID, ticks="outside", tickcolor=GRID)
    fig.update_yaxes(gridcolor=GRID, zeroline=False)
    return fig


def rainfall(df: pd.DataFrame, before: str, after: str, events=("2026-07-03", "2026-07-08")):
    mr = ui.lang() == "mr"
    lab = {"events": "पूर आणि भूस्खलनाच्या घटना" if mr else "floods and landslides reported",
           "p1": "रडार निरीक्षण १" if mr else "radar pass 1", "p2": "रडार निरीक्षण २" if mr else "radar pass 2",
           "y": "मिमी प्रतिदिन" if mr else "mm per day"}
    d = df[(df["date"] >= pd.Timestamp("2026-06-15")) & (df["date"] <= pd.Timestamp("2026-07-31"))]
    fig = go.Figure(go.Bar(x=d["date"], y=d["precip_mm"], marker=dict(color="#2a78d6", line=dict(width=0)),
                           hovertemplate="%{x|%d %b}: %{y:.1f} mm<extra></extra>"))
    e0, e1 = pd.Timestamp(events[0]), pd.Timestamp(events[1]) + pd.Timedelta(days=1)
    fig.add_vrect(x0=e0, x1=e1, fillcolor="#eb6834", opacity=0.08, line_width=0)
    fig.add_annotation(x=pd.Timestamp(after) + pd.Timedelta(days=1), y=0.84, yref="paper", text=lab["events"],
                       showarrow=False, xanchor="left", font=dict(size=12, color=ui.MUTED))
    for date, label, side in ((before, lab["p1"], "right"), (after, lab["p2"], "left")):
        fig.add_vline(x=pd.Timestamp(date).timestamp() * 1000, line=dict(color=ui.INK, width=2, dash="dot"))
        # Labels point away from each other so they never overlap on a narrow phone screen.
        fig.add_annotation(x=pd.Timestamp(date), y=1.0, yref="paper", text=label, showarrow=False, yanchor="bottom",
                           xanchor=side, xshift=-3 if side == "right" else 3, font=dict(size=12, color=ui.INK))
    fig.update_yaxes(title_text=lab["y"])
    _layout(fig, 330)
    fig.update_layout(margin=dict(t=34))
    return fig


def timeline(df: pd.DataFrame):
    d = df.copy()
    d["date"] = pd.to_datetime(d["date"])
    same = d[d["same_mode_as_primary"].astype(str).str.lower() == "true"]
    other = d[d["same_mode_as_primary"].astype(str).str.lower() != "true"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=same["date"], y=same["water_outside_permanent_flat_km2"], mode="lines+markers",
                             line=dict(color="#2a78d6", width=2), marker=dict(size=9),
                             hovertemplate="%{x|%d %b}: %{y:.1f} km²<extra></extra>"))
    if len(other):
        fig.add_trace(go.Scatter(x=other["date"], y=other["water_outside_permanent_flat_km2"], mode="markers",
                                 marker=dict(size=9, color="white", line=dict(color="#2a78d6", width=2)),
                                 hovertemplate="%{x|%d %b}: %{y:.1f} km² (different radar mode)<extra></extra>"))
    fig.update_yaxes(title_text="km² of water outside rivers and reservoirs", rangemode="tozero")
    return _layout(fig, 300)
