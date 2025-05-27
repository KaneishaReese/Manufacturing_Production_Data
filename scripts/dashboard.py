import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

# Load your cleaned data
df = pd.read_csv("../data/raw/supply_chain_data.csv")

# Initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Unique values for filters
product_types = df['Product type'].unique()
suppliers = df['Supplier name'].unique()
locations = df['Location'].unique()

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Supply Chain Dashboard", className="mb-4"),
            html.Label("Product Type"),
            dcc.Dropdown(product_types, id="product-type-filter", multi=True),

            html.Label("Supplier"),
            dcc.Dropdown(suppliers, id="supplier-filter", multi=True),

            html.Label("Location"),
            dcc.Dropdown(locations, id="location-filter", multi=True)
        ], width=2, style={"backgroundColor": "#f8f9fa", "padding": "20px"}),

        dbc.Col([
            dbc.Row([
                    dbc.Col(dbc.Card([
                        dbc.CardBody([
                            html.H6("Avg Manufacturing Cost", className="card-title"),
                            html.Div(id="kpi-manufacturing", className="kpi-box")
                        ])
                    ], color="primary", inverse=True), width=3),

                    dbc.Col(dbc.Card([
                        dbc.CardBody([
                            html.H6("Avg Shipping Cost", className="card-title"),
                            html.Div(id="kpi-shipping", className="kpi-box")
                        ])
                    ], color="info", inverse=True), width=3),

                    dbc.Col(dbc.Card([
                        dbc.CardBody([
                            html.H6("Avg Lead Time", className="card-title"),
                            html.Div(id="kpi-lead", className="kpi-box")
                        ])
                    ], color="success", inverse=True), width=3),

                    dbc.Col(dbc.Card([
                        dbc.CardBody([
                            html.H6("Avg Defect Rate", className="card-title"),
                            html.Div(id="kpi-defects", className="kpi-box")
                        ])
                    ], color="danger", inverse=True), width=3),
                ], className="mb-4"),


            dbc.Row([
                dbc.Col(dcc.Graph(id="bar-manufacturing-cost"), width=6),
                dbc.Col(dcc.Graph(id="bar-shipping-cost"), width=6),
            ]),

            dbc.Row([
                dbc.Col(dcc.Graph(id="line-lead-times"), width=6),
                dbc.Col(dcc.Graph(id="scatter-stock-vs-sales"), width=6),
            ]),

            dbc.Row([
                dbc.Col(html.Div([
                    html.H5("Overstocked & Understocked SKUs"),
                    dash_table.DataTable(id="stock-table", page_size=5, style_table={"overflowX": "auto"})
                ]), width=12)
            ])
        ], width=9)
    ])
], fluid=True)

from dash.dependencies import Input, Output

@app.callback(
    Output("kpi-manufacturing", "children"),
    Output("kpi-shipping", "children"),
    Output("kpi-lead", "children"),
    Output("kpi-defects", "children"),
    Input("product-type-filter", "value"),
    Input("supplier-filter", "value"),
    Input("location-filter", "value")
)
def update_kpis(selected_types, selected_suppliers, selected_locations):
    filtered_df = df.copy()

    if selected_types:
        filtered_df = filtered_df[filtered_df['Product type'].isin(selected_types)]
    if selected_suppliers:
        filtered_df = filtered_df[filtered_df['Supplier name'].isin(selected_suppliers)]
    if selected_locations:
        filtered_df = filtered_df[filtered_df['Location'].isin(selected_locations)]

    avg_manufacturing_cost = filtered_df['Manufacturing costs'].mean()
    avg_shipping_cost = filtered_df['Shipping costs'].mean()
    avg_lead_time = filtered_df['Lead time'].mean()
    avg_defect_rate = filtered_df['Defect rates'].mean()

    return (
        f"${avg_manufacturing_cost:.2f}",
        f"${avg_shipping_cost:.2f}",
        f"{avg_lead_time:.1f} days",
        f"{avg_defect_rate:.2f}%"
    )


if __name__ == "__main__":
    app.run(debug=True)
