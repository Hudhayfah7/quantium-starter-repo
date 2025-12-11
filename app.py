import pandas as pd
from datetime import datetime

from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# -----------------------
# Load and prepare data
# -----------------------
df = pd.read_csv("processed/pink_morsel_sales.csv")

# Ensure correct types
df["date"] = pd.to_datetime(df["date"])
# Normalise regions to lowercase so filters work reliably
df["region"] = df["region"].str.lower()

PRICE_CHANGE_DATE = datetime(2021, 1, 15)

# -----------------------
# Colour scheme (dark theme)
# -----------------------
BACKGROUND = "#020617"     # page background (very dark navy)
CARD_BG = "#0b1220"        # cards / panels
CARD_BORDER = "#1f2937"
TEXT_MAIN = "#f9fafb"
TEXT_MUTED = "#9ca3af"
ACCENT = "#f97373"         # main accent / line colour
GOOD = "#22c55e"           # green for increase
BAD = "#f97316"            # orange for decrease


def compute_kpis(region_value: str):
    """
    Compute total sales before and after the price change,
    optionally filtered by region.
    """
    if region_value == "ALL":
        df_filtered = df.copy()
    else:
        df_filtered = df[df["region"] == region_value].copy()

    before = df_filtered[df_filtered["date"] < PRICE_CHANGE_DATE]["sales"].sum()
    after = df_filtered[df_filtered["date"] >= PRICE_CHANGE_DATE]["sales"].sum()
    diff = after - before
    return before, after, diff


def build_figure(region_value: str):
    """
    Build the time-series sales figure for the selected region
    (or all regions).
    """
    if region_value == "ALL":
        df_filtered = df.copy()
    else:
        df_filtered = df[df["region"] == region_value].copy()

    # Aggregate daily sales
    daily_sales = (
        df_filtered.groupby("date", as_index=False)["sales"]
        .sum()
        .sort_values("date")
    )

    # Handle edge case: no data
    if daily_sales.empty:
        fig = px.line()
        fig.update_layout(
            title="No data available for this selection",
            template="plotly_dark",
            xaxis_title="Date",
            yaxis_title="Sales Revenue (£)",
            paper_bgcolor=CARD_BG,
            plot_bgcolor=CARD_BG,
            font=dict(color=TEXT_MAIN),
        )
        return fig

    fig = px.line(
        daily_sales,
        x="date",
        y="sales",
        title="Daily Pink Morsel Sales",
    )

    # Use accent colour and thicker line
    fig.update_traces(line=dict(color=ACCENT, width=3))

    # Vertical line & label using shapes (works for all Plotly versions)
    y_min = daily_sales["sales"].min()
    y_max = daily_sales["sales"].max()

    fig.add_shape(
        type="line",
        x0=PRICE_CHANGE_DATE,
        x1=PRICE_CHANGE_DATE,
        y0=y_min,
        y1=y_max,
        xref="x",
        yref="y",
        line=dict(color="#f97316", dash="dash"),
    )

    fig.add_annotation(
        x=PRICE_CHANGE_DATE,
        y=y_max,
        xref="x",
        yref="y",
        text="Price change",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40,
        font=dict(color="#f97316", size=11),
        bgcolor="rgba(15,23,42,0.9)",
        bordercolor="#f97316",
        borderwidth=1,
    )

    # Shade before/after regions
    fig.add_vrect(
        x0=daily_sales["date"].min(),
        x1=PRICE_CHANGE_DATE,
        fillcolor="rgba(59,130,246,0.18)",  # blue-ish
        opacity=0.18,
        layer="below",
        line_width=0,
    )
    fig.add_vrect(
        x0=PRICE_CHANGE_DATE,
        x1=daily_sales["date"].max(),
        fillcolor="rgba(34,197,94,0.18)",  # green-ish
        opacity=0.18,
        layer="below",
        line_width=0,
    )

    # Layout styling for dark theme
    fig.update_layout(
        title="Daily Sales Trend",
        title_x=0.5,
        template="plotly_dark",
        xaxis_title="Date",
        yaxis_title="Sales Revenue (£)",
        font=dict(family="Segoe UI, Arial", size=14, color=TEXT_MAIN),
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        xaxis=dict(gridcolor="#1f2937"),
        yaxis=dict(gridcolor="#1f2937"),
    )

    # Hover formatting
    fig.update_traces(
        hovertemplate="Date: %{x|%d-%b-%Y}"
        "<br>Revenue: £%{y:,.2f}<extra></extra>"
    )

    return fig


# -----------------------
# Build Dash app
# -----------------------
app = Dash(__name__)

# Fixed region radio options
region_options = [
    {"label": "All", "value": "ALL"},
    {"label": "North", "value": "north"},
    {"label": "East", "value": "east"},
    {"label": "South", "value": "south"},
    {"label": "West", "value": "west"},
]

app.layout = html.Div(
    style={
        "backgroundColor": BACKGROUND,
        "padding": "40px 16px",
        "minHeight": "100vh",
        "fontFamily": "Segoe UI, system-ui, -apple-system, BlinkMacSystemFont",
    },
    children=[
        html.Div(
            style={"maxWidth": "1100px", "margin": "0 auto"},
            children=[
                # Header
                html.H1(
                    "Pink Morsel Sales Dashboard",
                    style={
                        "textAlign": "center",
                        "color": TEXT_MAIN,
                        "marginBottom": "6px",
                        "fontWeight": "600",
                        "letterSpacing": "0.03em",
                    },
                ),
                html.H3(
                    "Sales performance before and after the 15 January 2021 price change",
                    style={
                        "textAlign": "center",
                        "color": TEXT_MUTED,
                        "marginBottom": "32px",
                        "fontWeight": "400",
                        "fontSize": "15px",
                    },
                ),

                # Controls row
                html.Div(
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "alignItems": "center",
                        "marginBottom": "22px",
                        "gap": "12px",
                        "flexWrap": "wrap",
                    },
                    children=[
                        html.Div(
                            children=[
                                html.Label(
                                    "Region",
                                    style={
                                        "fontWeight": "600",
                                        "color": TEXT_MAIN,
                                        "display": "block",
                                        "marginBottom": "8px",
                                        "fontSize": "14px",
                                    },
                                ),
                                dcc.RadioItems(
                                    id="region-radio",
                                    options=region_options,
                                    value="ALL",
                                    labelStyle={
                                        "display": "inline-block",
                                        "marginRight": "18px",
                                        "fontSize": "14px",
                                        "color": TEXT_MAIN,
                                    },
                                    inputStyle={
                                        "marginRight": "6px",
                                        "accentColor": ACCENT,
                                    },
                                    style={
                                        "backgroundColor": CARD_BG,
                                        "padding": "10px 12px",
                                        "borderRadius": "999px",
                                        "boxShadow": "0 2px 8px rgba(0,0,0,0.35)",
                                        "border": f"1px solid {CARD_BORDER}",
                                    },
                                ),
                            ]
                        ),
                        html.Div(
                            "Tip: Use the region filter to explore how different markets reacted to the price change.",
                            style={
                                "color": TEXT_MUTED,
                                "fontSize": "13px",
                                "fontStyle": "italic",
                                "maxWidth": "380px",
                            },
                        ),
                    ],
                ),

                # KPI cards
                html.Div(
                    id="kpi-row",
                    style={
                        "display": "flex",
                        "gap": "16px",
                        "marginBottom": "26px",
                        "flexWrap": "wrap",
                    },
                    children=[
                        html.Div(
                            style={
                                "flex": "1",
                                "minWidth": "220px",
                                "background": CARD_BG,
                                "borderRadius": "14px",
                                "padding": "16px 20px",
                                "boxShadow": "0 4px 14px rgba(0,0,0,0.45)",
                                "border": f"1px solid {CARD_BORDER}",
                            },
                            children=[
                                html.Div(
                                    "Total Sales BEFORE",
                                    style={
                                        "fontSize": "12px",
                                        "color": TEXT_MUTED,
                                        "marginBottom": "8px",
                                        "textTransform": "uppercase",
                                        "letterSpacing": "0.12em",
                                    },
                                ),
                                html.Div(
                                    id="kpi-before",
                                    style={
                                        "fontSize": "22px",
                                        "fontWeight": "600",
                                        "color": TEXT_MAIN,
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            style={
                                "flex": "1",
                                "minWidth": "220px",
                                "background": CARD_BG,
                                "borderRadius": "14px",
                                "padding": "16px 20px",
                                "boxShadow": "0 4px 14px rgba(0,0,0,0.45)",
                                "border": f"1px solid {CARD_BORDER}",
                            },
                            children=[
                                html.Div(
                                    "Total Sales AFTER",
                                    style={
                                        "fontSize": "12px",
                                        "color": TEXT_MUTED,
                                        "marginBottom": "8px",
                                        "textTransform": "uppercase",
                                        "letterSpacing": "0.12em",
                                    },
                                ),
                                html.Div(
                                    id="kpi-after",
                                    style={
                                        "fontSize": "22px",
                                        "fontWeight": "600",
                                        "color": TEXT_MAIN,
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            style={
                                "flex": "1",
                                "minWidth": "240px",
                                "background": CARD_BG,
                                "borderRadius": "14px",
                                "padding": "16px 20px",
                                "boxShadow": "0 4px 14px rgba(0,0,0,0.45)",
                                "border": f"1px solid {CARD_BORDER}",
                            },
                            children=[
                                html.Div(
                                    "Difference",
                                    style={
                                        "fontSize": "12px",
                                        "color": TEXT_MUTED,
                                        "marginBottom": "8px",
                                        "textTransform": "uppercase",
                                        "letterSpacing": "0.12em",
                                    },
                                ),
                                html.Div(
                                    id="kpi-diff",
                                    style={
                                        "fontSize": "16px",
                                        "fontWeight": "600",
                                        "color": TEXT_MAIN,
                                    },
                                ),
                            ],
                        ),
                    ],
                ),

                # Graph card
                html.Div(
                    style={
                        "background": CARD_BG,
                        "borderRadius": "16px",
                        "padding": "18px 18px 8px",
                        "boxShadow": "0 6px 22px rgba(0,0,0,0.6)",
                        "border": f"1px solid {CARD_BORDER}",
                    },
                    children=[
                        dcc.Graph(
                            id="sales-chart",
                            figure=build_figure("ALL"),
                            style={"height": "500px"},
                        )
                    ],
                ),

                # Footer
                html.P(
                    "Built as part of the Quantium Data Analytics Virtual Experience Program.",
                    style={
                        "textAlign": "center",
                        "marginTop": "40px",
                        "color": TEXT_MUTED,
                        "fontSize": "13px",
                    },
                ),
            ],
        )
    ],
)


# -----------------------
# Callbacks
# -----------------------
@app.callback(
    [
        Output("sales-chart", "figure"),
        Output("kpi-before", "children"),
        Output("kpi-after", "children"),
        Output("kpi-diff", "children"),
    ],
    [Input("region-radio", "value")],
)
def update_dashboard(selected_region):
    fig = build_figure(selected_region)
    before, after, diff = compute_kpis(selected_region)

    before_text = f"£{before:,.2f}"
    after_text = f"£{after:,.2f}"

    if diff >= 0:
        diff_text = f"+£{abs(diff):,.2f} increase after price change"
        diff_text = html.Span(diff_text, style={"color": GOOD})
    else:
        diff_text = f"-£{abs(diff):,.2f} decrease after price change"
        diff_text = html.Span(diff_text, style={"color": BAD})

    return fig, before_text, after_text, diff_text


if __name__ == "__main__":
    print("Starting Dash server...")
    app.run(debug=True)