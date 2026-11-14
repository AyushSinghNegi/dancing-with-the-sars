"""Charts (Plotly). One axis per chart, thin marks, recessive grid, text in ink colours."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from . import ui

WATER = "#3d8ef0"
SLIDE = "#f0743a"


def _font():
    return dict(family="IBM Plex Sans, sans-serif", size=13, color=ui.ink())


def _layout(fig, height=300, title=None):
    grid = ui.hairline()
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=40 if title else 10, b=10), font=_font(),
                      title=dict(text=title, x=0, font=dict(size=15)) if title else None,
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False,
                      hoverlabel=dict(bgcolor="#111c30" if ui.dark() else "white", font=_font(),
                                      bordercolor=grid))
    fig.update_xaxes(showgrid=False, linecolor=grid, ticks="outside", tickcolor=grid)
    fig.update_yaxes(gridcolor=grid, zeroline=False)
    return fig


def rainfall(df: pd.DataFrame, before: str, after: str, events=("2026-07-03", "2026-07-08"), passes=None):
    tr = ui.tr
    lab = {"events": tr("floods and landslides reported", "पूर आणि भूस्खलनाच्या घटना"),
           "p1": tr("radar pass 1", "रडार निरीक्षण १"), "p2": tr("radar pass 2", "रडार निरीक्षण २"),
           "y": tr("mm per day", "मिमी प्रतिदिन"), "pass": tr("NISAR pass", "निसार निरीक्षण")}
    ink, muted = ui.ink(), ui.muted()
    d = df[(df["date"] >= pd.Timestamp("2026-06-15")) & (df["date"] <= pd.Timestamp("2026-07-31"))]
    fig = go.Figure(go.Bar(x=d["date"], y=d["precip_mm"], marker=dict(color=WATER, line=dict(width=0)),
                           hovertemplate="%{x|%d %b}: %{y:.1f} mm<extra></extra>"))
    e0, e1 = pd.Timestamp(events[0]), pd.Timestamp(events[1]) + pd.Timedelta(days=1)
    fig.add_vrect(x0=e0, x1=e1, fillcolor=SLIDE, opacity=0.12 if ui.dark() else 0.08, line_width=0)
    fig.add_annotation(x=pd.Timestamp(after) + pd.Timedelta(days=1), y=0.84, yref="paper", text=lab["events"],
                       showarrow=False, xanchor="left", font=dict(size=12, color=muted))
    for date, label, side in ((before, lab["p1"], "right"), (after, lab["p2"], "left")):
        fig.add_vline(x=pd.Timestamp(date).timestamp() * 1000, line=dict(color=ink, width=2, dash="dot"))
        # Labels point away from each other so they never overlap on a narrow phone screen.
        fig.add_annotation(x=pd.Timestamp(date), y=1.0, yref="paper", text=label, showarrow=False, yanchor="bottom",
                           xanchor=side, xshift=-3 if side == "right" else 3, font=dict(size=12, color=ink))
    if passes is not None and len(passes):
        pp = passes[(passes["date"] >= pd.Timestamp("2026-06-15")) & (passes["date"] <= pd.Timestamp("2026-07-31"))]
        fig.add_trace(go.Scatter(x=pp["date"], y=[-6] * len(pp), mode="markers", cliponaxis=False,
                                 marker=dict(symbol="triangle-up", size=10, color=ink),
                                 customdata=pp["orbit"],
                                 hovertemplate=lab["pass"] + " %{x|%d %b} (%{customdata})<extra></extra>"))
        fig.update_yaxes(range=[-10, None])
    fig.update_yaxes(title_text=lab["y"])
    _layout(fig, 330)
    fig.update_layout(margin=dict(t=34))
    return fig


def timeline(df: pd.DataFrame):
    """Open water on every same-orbit NISAR pass: one line, one axis (km²), each point labelled."""
    d = df.copy()
    d["date"] = pd.to_datetime(d["date"])
    d = d.sort_values("date")
    col = "water_in_jrc_extent_km2" if "water_in_jrc_extent_km2" in d else "water_km2"
    d["water_km2"] = d[col]
    same = d[d["same_mode_as_primary"].astype(str).str.lower() == "true"]
    other = d[d["same_mode_as_primary"].astype(str).str.lower() != "true"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=same["date"], y=same["water_km2"], mode="lines+markers+text",
                             line=dict(color=WATER, width=2.5),
                             marker=dict(size=10, color=WATER, line=dict(width=2, color=ui.surface())),
                             fill="tozeroy", fillcolor="rgba(61,142,240,.10)",
                             text=[f"{v:.0f}" for v in same["water_km2"]], textposition="top center",
                             textfont=dict(size=12, color=ui.ink()), cliponaxis=False,
                             hovertemplate="%{x|%d %b}: %{y:.1f} km²<extra></extra>"))
    if len(other):
        fig.add_trace(go.Scatter(x=other["date"], y=other["water_km2"], mode="markers",
                                 marker=dict(size=9, color="rgba(0,0,0,0)", line=dict(color=WATER, width=2)),
                                 hovertemplate="%{x|%d %b}: %{y:.1f} km² (different radar mode)<extra></extra>"))
    lo = max(0, float(d["water_km2"].min()) * 0.85)
    fig.update_yaxes(title_text=ui.tr("water surface, km²", "पाण्याचा पृष्ठभाग, चौ. किमी"),
                     range=[lo, float(d["water_km2"].max()) * 1.12])
    return _layout(fig, 300)
