from dash import html, dcc, register_page, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import numpy as np

register_page(__name__, path="/logistics")

# Load data
df = pd.read_csv("data/raw/supply_chain_data.csv")

# Dropdown options
product_types = df["Product type"].unique()
carriers = df["Shipping carriers"].unique()
locations = df["Location"].unique()
transport_modes = df["Transportation modes"].unique()

# Inventory logic function
def identify_inventory_issues(df, availability_threshold=30):
    df = df.copy()
    df["Stock_to_Sales_Ratio"] = df["Stock levels"] / df["Number of products sold"].replace(0, np.nan)
    df["Stock_to_Sales_Ratio"] = df["Stock_to_Sales_Ratio"].replace([np.inf, -np.inf], np.nan).fillna(0)

    overstocked = (
        df[df["Number of products sold"] > 0]
        .sort_values(by="Stock_to_Sales_Ratio", ascending=False)
        .head(5)
    )[
        ["SKU", "Product type", "Stock levels", "Availability", "Number of products sold", "Stock_to_Sales_Ratio"]
    ]

    sales_median = df["Number of products sold"].median()
    understocked = (
        df[
            (df["Availability"] <= availability_threshold)
            & (df["Number of products sold"] > sales_median)
        ]
        .sort_values(by="Number of products sold", ascending=False)
        .head(5)
    )[
        ["SKU", "Product type", "Stock levels", "Availability", "Number of products sold", "Stock_to_Sales_Ratio"]
    ]

    return overstocked, understocked

# Layout
layout = html.Div([
    html.H2("Logistics Dashboard", className="mb-4"),


    dbc.Row([
        # Sidebar Filters
        dbc.Col([
            html.H3("Filters", className="mb-4"),
            html.Label("Product Type"),
            dcc.Dropdown(product_types, id="logistics-product-type", multi=True),

            html.Label("Shipping Carrier"),
            dcc.Dropdown(carriers, id="logistics-carrier", multi=True),

            html.Label("Location"),
            dcc.Dropdown(locations, id="logistics-location", multi=True),

            html.Label("Transportation Mode"),
            dcc.Dropdown(transport_modes, id="logistics-mode", multi=True)
        ], width=2, style={"backgroundColor": "#f8f9fa", "padding": "20px"}),

        # Main Content
        dbc.Col(children =[
        # KPI Cards
            dbc.Row([
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H6("Avg Availability"), html.H4(id="kpi-availability")
                ]), color="primary", inverse=True), width=3),
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H6("Avg Stock Levels"), html.H4(id="kpi-stock")
                ]), color="info", inverse=True), width=3),
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H6("Avg Shipping Time"), html.H4(id="kpi-ship-time")
                ]), color="success", inverse=True), width=3),
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H6("Avg Shipping Cost"), html.H4(id="kpi-ship-cost")
                ]), color="danger", inverse=True), width=3),
            ], className="mb-4"),

            # Graphs
            dbc.Row([
                dbc.Col(dcc.Graph(id="shipping-time-boxplot"), width=6),
                dbc.Col(dcc.Graph(id="shipping-cost-bar"), width=6),
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id="availability-bar"), width=6),
                dbc.Col(dcc.Graph(id="scatter-stock-vs-ship-time"), width=6),
            ]),

            # Inventory Tables
            dbc.Row([
                dbc.Col([
                    html.H5("Top 5 Overstocked Products"),
                    dash_table.DataTable(
                        id="overstocked-table",
                        columns=[{"name": col, "id": col} for col in
                                 ["SKU", "Product type", "Stock levels", "Number of products sold"]],
                        style_table={"overflowX": "auto"},
                        page_size=5
                    )
                ], width=6),

                dbc.Col([
                    html.H5("Top 5 Understocked Products"),
                    dash_table.DataTable(
                        id="understocked-table",
                        columns=[{"name": col, "id": col} for col in
                                 ["SKU", "Product type", "Stock levels",  "Number of products sold"]],
                        style_table={"overflowX": "auto"},
                        page_size=5
                    )
                ], width=6)
            ])
        ])

    ])
], className="mt-4")

# Callback
@callback(
    Output("kpi-availability", "children"),
    Output("kpi-stock", "children"),
    Output("kpi-ship-time", "children"),
    Output("kpi-ship-cost", "children"),
    Output("shipping-time-boxplot", "figure"),
    Output("shipping-cost-bar", "figure"),
    Output("availability-bar", "figure"),
    Output("scatter-stock-vs-ship-time", "figure"),
    Output("overstocked-table", "data"),
    Output("understocked-table", "data"),
    Input("logistics-product-type", "value"),
    Input("logistics-carrier", "value"),
    Input("logistics-location", "value"),
    Input("logistics-mode", "value")
)
def update_logistics(ptypes, carriers, locs, modes):
    dff = df.copy()
    if ptypes: dff = dff[dff["Product type"].isin(ptypes)]
    if carriers: dff = dff[dff["Shipping carriers"].isin(carriers)]
    if locs: dff = dff[dff["Location"].isin(locs)]
    if modes: dff = dff[dff["Transportation modes"].isin(modes)]

    # KPIs
    kpi_avail = f"{dff['Availability'].mean():.1f}"
    kpi_stock = f"{dff['Stock levels'].mean():.1f}"
    kpi_ship_time = f"{dff['Shipping times'].mean():.1f} days"
    kpi_ship_cost = f"${dff['Shipping costs'].mean():.2f}"

    # Graphs
    fig1 = px.box(dff, x="Transportation modes", y="Shipping times", color="Transportation modes", title="Shipping Time by Carrier", template="plotly_white")
    fig2 = px.bar(
        dff.groupby("Transportation modes", as_index=False)["Shipping costs"].mean(),
        x="Transportation modes", y="Shipping costs", color="Transportation modes",
        title="Avg Shipping Cost by Mode", template="plotly_white"
    )
    fig3 = px.bar(
        dff.groupby(["Location", "Product type"], as_index=False)["Stock levels"].mean(),
        x="Location", y="Stock levels", color="Product type", barmode="group",
        title="Average Stock Levels by Location and Product Type", template="plotly_white"
    )
    fig4 = px.scatter(
        dff, x="Stock levels", y="Shipping times", color="Product type",
        title="Stock Levels vs Shipping Times", template="plotly_white"
    )

    # Inventory Tables
    over, under = identify_inventory_issues(dff)

    return (
        kpi_avail, kpi_stock, kpi_ship_time, kpi_ship_cost,
        fig1, fig2, fig3, fig4,
        over.to_dict("records"), under.to_dict("records")
    )