
from dash import html, dcc, register_page, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

register_page(__name__, path="/production")

# Load data
df = pd.read_csv("data/raw/supply_chain_data.csv")

# Dropdown options
product_types = df["Product type"].unique()
suppliers = df["Supplier name"].unique()
locations = df["Location"].unique()

# Layout
layout = html.Div([
    html.H2("Production Dashboard", className="mb-4"),

    dbc.Row([
        # Filters
        dbc.Col([
            html.Label("Product Type"),
            dcc.Dropdown(product_types, id="prod-product-type", multi=True),

            html.Label("Supplier"),
            dcc.Dropdown(suppliers, id="prod-supplier", multi=True),

            html.Label("Location"),
            dcc.Dropdown(locations, id="prod-location", multi=True)
        ], width=2, style={"backgroundColor": "#f8f9fa", "padding": "20px"}),

        # Main Content
        dbc.Col(children =[
            # KPI Cards
            dbc.Row([
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H6("Avg Manufacturing Lead Time"), html.H4(id="kpi-manuf-lead")
                ]), color="primary", inverse=True), width=3),
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H6("Avg Manufacturing Cost"), html.H4(id="kpi-manuf-cost")
                ]), color="info", inverse=True), width=3),
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H6("Inspection Pass Rate"), html.H4(id="kpi-inspect-pass")
                ]), color="success", inverse=True), width=3),
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H6("Avg Defect Rate"), html.H4(id="kpi-defect-rate")
                ]), color="danger", inverse=True), width=3)
            ], className="mb-4"),

            # Charts
            dbc.Row([
                dbc.Col(dcc.Graph(id="box-manuf-lead-time"), width=6),
                dbc.Col(dcc.Graph(id="bar-manuf-costs"), width=6)
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id="bar-inspection-results"), width=6),
                dbc.Col(dcc.Graph(id="bar-defect-rates"), width=6)
            ])
        ])
    ])
], className="mt-4")
# Callback
@callback(
    Output("kpi-manuf-lead", "children"),
    Output("kpi-manuf-cost", "children"),
    Output("kpi-inspect-pass", "children"),
    Output("kpi-defect-rate", "children"),
    Output("box-manuf-lead-time", "figure"),
    Output("bar-manuf-costs", "figure"),
    Output("bar-inspection-results", "figure"),
    Output("bar-defect-rates", "figure"),
    Input("prod-product-type", "value"),
    Input("prod-supplier", "value"),
    Input("prod-location", "value")
)
def update_production(ptypes, suppliers, locs):
    dff = df.copy()
    if ptypes: dff = dff[dff["Product type"].isin(ptypes)]
    if suppliers: dff = dff[dff["Supplier name"].isin(suppliers)]
    if locs: dff = dff[dff["Location"].isin(locs)]

    # KPIs
    lead_time = f"{dff['Manufacturing lead time'].mean():.1f} days"
    cost = f"${dff['Manufacturing costs'].mean():.2f}"
    defect = f"{dff['Defect rates'].mean():.2f}%"
    if "Inspection results" in dff.columns:
        pass_rate = dff["Inspection results"].value_counts(normalize=True).get("Pass", 0) * 100
        inspection = f"{pass_rate:.1f}%"
    else:
        inspection = "N/A"

    # Charts
    if ptypes:
        fig1 = px.histogram(
            dff, x="Manufacturing lead time", color="Product type",
            title="Lead Time Distribution (Filtered by Product Type)", template="plotly_white",
        )
    else:
        fig1 = px.box(dff, x="Product type", y="Manufacturing lead time", color="Product type",
                      title="Manufacturing Lead Time by Product Type", template="plotly_white")

    if suppliers:
        # Histogram of individual cost values from filtered suppliers
        fig2 = px.histogram(
            dff, x="Manufacturing costs", color="Supplier name",
            title="Manufacturing Cost Distribution (Filtered by Supplier)", template="plotly_white",
        )
    else:
        # Bar chart for all suppliers
        fig2 = px.bar(
            dff.groupby("Supplier name", as_index=False)["Manufacturing costs"].mean(),
            x="Supplier name", y="Manufacturing costs", color="Supplier name",
            title="Average Manufacturing Costs by Supplier", template="plotly_white"
        )

    fig3 = px.histogram(dff, x="Inspection results", color="Product type", barmode="group",
                        title="Inspection Results by Product Type", template="plotly_white")

    fig4 = px.bar(dff.groupby("Product type", as_index=False)["Defect rates"].mean(),
                  x="Product type", y="Defect rates", color="Product type",
                  title="Average Defect Rate by Product Type", template="plotly_white")

    return lead_time, cost, inspection, defect, fig1, fig2, fig3, fig4
