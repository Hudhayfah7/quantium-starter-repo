import pandas as pd
from datetime import datetime

from dash import Dash, dcc, html
import plotly.express as px

print("Loading data and building app...")

# ---- Load and prepare data ----
df = pd.read_csv("processed/pink_morsel_sales.csv")

# Convert date to datetime and sort
df["date"] = pd.to_datetime(df["date"])
daily_sales = (
    df.groupby("date", as_index=False)["sales"]
      .sum()
      .sort_values("date")
)

# Create line chart
fig = px.line(
    daily_sales,
    x="date",
    y="sales",
    title="Daily Pink Morsel Sales"
)

# Add vertical line for price change date
price_change_date = datetime(2021, 1, 15)
fig.add_vline(
    x=price_change_date,
    line_dash="dash",
    line_color="red",
)
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales (Revenue)",
    template="plotly_white",
    title_x=0.5,
    font=dict(color="#333")
)
# Shade before vs after price change visually
fig.add_vrect(
    x0=daily_sales["date"].min(),
    x1=price_change_date,
    fillcolor="lightblue",
    opacity=0.15,
    layer="below",
    line_width=0,
)

fig.add_vrect(
    x0=price_change_date,
    x1=daily_sales["date"].max(),
    fillcolor="lightgreen",
    opacity=0.15,
    layer="below",
    line_width=0,
)

# ---- Build Dash app ----
app = Dash(__name__)

app.layout = html.Div(
    style={
        "backgroundColor": "#f8f9fa",
        "padding": "40px",
        "minHeight": "100vh",
        "fontFamily": "Arial"
    },
    children=[
        html.H1(
            "Pink Morsel Sales Visualiser",
            style={
                "textAlign": "center",
                "color": "#333",
                "marginBottom": "10px"
            }
        ),
        html.H3(
            "Comparing sales before and after the 15 January 2021 price change",
            style={
                "textAlign": "center",
                "color": "#555",
                "marginBottom": "30px",
                "fontWeight": "normal"
            }
        ),
        dcc.Graph(
            id="sales-chart",
            figure=fig,
            style={
                "border": "1px solid #ddd",
                "borderRadius": "10px",
                "padding": "10px",
                "background": "white",
                "boxShadow": "0 2px 6px rgba(0,0,0,0.1)"
            }
        ),
        html.P(
            "Built as part of the Quantium Data Analytics Virtual Experience Program.",
            style={
                "textAlign": "center",
                "marginTop": "30px",
                "color": "#777",
                "fontSize": "14px"
            }
        )
    ]
)

if __name__ == "__main__":
    print("Starting Dash server...")
    app.run(debug=True)