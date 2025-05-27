from dash import html, dcc, register_page, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

register_page(__name__, path="/sales")

# Load your cleaned data
df = pd.read_csv("data/raw/supply_chain_data.csv")

# Unique filter values
product_types = df["Product type"].unique()
suppliers = df["Supplier name"].unique()
locations = df["Location"].unique()

layout = html.Div([
    html.H2("Sales Dashboard", className="mb-4"),

    dbc.Row([
        # Sidebar Filters
        dbc.Col([
            html.H3("Filters", className="mb-4"),
            html.Label("Product Type"),
            dcc.Dropdown(product_types, id="sales-product-filter", multi=True),

            html.Label("Supplier"),
            dcc.Dropdown(suppliers, id="sales-supplier-filter", multi=True),

            html.Label("Location"),
            dcc.Dropdown(locations, id="sales-location-filter", multi=True)
        ], width=2, style={"backgroundColor": "#f8f9fa", "padding": "20px"}),
        # Main Content
        dbc.Col([
            # KPIs
            dbc.Row([
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H6("Total Revenue"), html.H4(id="kpi-total-revenue")
                ]), color="success", inverse=True), width=4),
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H6("Avg Price"), html.H4(id="kpi-avg-price")
                ]), color="primary", inverse=True), width=4),
                dbc.Col(dbc.Card(dbc.CardBody([
                    html.H6("Total Products Sold"), html.H4(id="kpi-total-sold")
                ]), color="info", inverse=True), width=4),
                # dbc.Col(dbc.Card(dbc.CardBody([
                #     html.H6("Total Cost"), html.H4(id="kpi-total-cost")
                # ]), color="danger", inverse=True), width=3),
            ], className="mb-4"),
            dbc.Row([
                dbc.Col(html.Div([
                    html.H5("Top 5 Selling Products", className="mt-4"),
                    dash_table.DataTable(
                        id="top-products-table",
                        columns=[
                            {"name": "SKU", "id": "SKU"},
                            {"name": "Product type", "id": "Product type"},
                            {"name": "Number of products sold", "id": "Number of products sold"},
                            {"name": "Revenue generated", "id": "Revenue generated", "type": "numeric",
                             "format": {"specifier": "$,.2f"}}
                        ],
                        style_table={"overflowX": "auto"},
                        style_cell={"padding": "5px", "textAlign": "left"},
                        style_header={"backgroundColor": "lightgrey", "fontWeight": "bold"},
                        page_size=5
                    )
                ]), width=12)
            ]),
            # Graphs
            dbc.Row([
                dbc.Col(dcc.Graph(id="bar-revenue-by-product"), width=6),
                dbc.Col(dcc.Graph(id="bar-sales-by-location"), width=6)
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id="scatter-price-vs-sold"), width=12)
            ]),

        ], width=10)
    ]),

], className="mt-4")

@callback(
    Output("kpi-total-revenue", "children"),
    Output("kpi-avg-price", "children"),
    Output("kpi-total-sold", "children"),
    # Output("kpi-total-cost", "children"),
    Output("bar-revenue-by-product", "figure"),
    Output("bar-sales-by-location", "figure"),
    Output("scatter-price-vs-sold", "figure"),
    Output("top-products-table", "data"),
    Input("sales-product-filter", "value"),
    Input("sales-supplier-filter", "value"),
    Input("sales-location-filter", "value")
)
def update_sales_dashboard(product_types, suppliers, locations):
    # Filter the DataFrame
    filtered = df.copy()
    if product_types:
        filtered = filtered[filtered["Product type"].isin(product_types)]
    if suppliers:
        filtered = filtered[filtered["Supplier name"].isin(suppliers)]
    if locations:
        filtered = filtered[filtered["Location"].isin(locations)]

    # --- KPI CALCULATIONS ---
    total_revenue = filtered["Revenue generated"].sum()
    avg_price = filtered["Price"].mean()
    total_sold = filtered["Number of products sold"].sum()
    total_cost = filtered["Costs"].sum()

    # --- CHARTS ---
    # Revenue by Product Type
    if product_types:
        # Histogram: Distribution of revenue values within selected product types
        fig_revenue = px.histogram(
            filtered,
            x="Revenue generated",
            color="Product type",
            nbins=20,
            title="Revenue Distribution by Product Type",
            template="plotly_white",
        )
    else:
        # Bar chart: Total revenue per product type
        fig_revenue = px.bar(
            filtered.groupby("Product type", as_index=False)["Revenue generated"].sum(),
            x="Product type", y="Revenue generated",
            title="Total Revenue by Product Type",
            color="Product type", template="plotly_white"
        )

    # Sales by Location
    fig_sales = px.bar(
        filtered.groupby("Location", as_index=False)["Number of products sold"].sum(),
        x="Location", y="Number of products sold", title="Products Sold by Location",
        color="Location", template="plotly_white"
    )

    # Price vs Products Sold
    fig_scatter = px.scatter(
        filtered, x="Price", y="Number of products sold", color="Product type",
        title="Price vs. Number of Products Sold", template="plotly_white"
    )

    top_products = (
        filtered.groupby(["SKU", "Product type"], as_index=False)
        .agg({"Number of products sold": "sum", "Revenue generated": "sum"})
        .sort_values(by="Revenue generated", ascending=False)
        .head(5)
    )

    # Return values for all outputs
    return (
        f"${total_revenue:,.2f}",
        f"${avg_price:,.2f}",
        f"{int(total_sold)}",
        # f"${total_cost:,.2f}",
        fig_revenue,
        fig_sales,
        fig_scatter,
        top_products.to_dict("records")
    )
