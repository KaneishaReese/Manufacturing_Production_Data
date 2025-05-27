# pages/home.py
from dash import html, register_page

register_page(__name__, path="/")

layout = html.Div([
    html.H1("Welcome to the Supply Chain Dashboard"),
    html.P("This tool provides interactive views of our sales and logistics performance. Use the navigation bar above to explore key insights."),

    html.H2("Sales Dashboard"),
    html.Ul([
        html.Li("View total revenue, average price, and product sales volume."),
        html.Li("Use filters (Product Type, Supplier, Location) to customize insights."),
        html.Li("Explore trends like revenue distribution or price vs. units sold."),
        html.Li("The table shows the top 5 best-selling products."),
        html.Li("When no filters are applied, you'll see summarized views. Filtering reveals detailed patterns."),
    ]),

    html.H2("Logistics Dashboard"),
    html.Ul([
        html.Li("Monitor availability, stock levels, shipping times, and shipping costs."),
        html.Li("Use filters to focus on specific products, carriers, locations, or transport modes."),
        html.Li("View KPIs to understand average performance metrics."),
        html.Li("Charts provide insight into stock health, shipment efficiency, and inventory risk."),
        html.Li("Two tables identify products that may be overstocked or understocked based on sales activity and stock levels."),
    ]),

    html.H2("Production Dashboard"),
    html.Ul([
        html.Li("Explore key metrics including manufacturing lead time, production cost, inspection results, and defect rates."),
        html.Li("Use filters (Product Type, Supplier, Location) to customize the view."),
        html.Li("Charts adjust dynamically based on selections:"),
        html.Ul([
            html.Li("If no product type is selected, you'll see a boxplot comparing lead times across all product types."),
            html.Li("If one or more product types are selected, the chart becomes a histogram showing the distribution of lead times."),
            html.Li("Likewise, if no supplier is selected, you'll see a bar chart comparing average manufacturing costs by supplier."),
            html.Li("Selecting a supplier changes the chart to a histogram showing the distribution of individual manufacturing costs."),
        ]),
        html.Li("Other visuals include defect rate trends and pass/fail inspection summaries.")
    ]),

    html.P("📌 Tip: Hover over charts for more detailed information. Tables can be sorted or filtered directly in the app."),

    html.P([
        "The data used in this dashboard comes from a public dataset on Kaggle: ",
        html.A("Supply Chain Dataset by Amir Motefaker",
               href="https://www.kaggle.com/datasets/amirmotefaker/supply-chain-dataset/data",
               target="_blank", style={"color": "#007bff", "textDecoration": "underline"}),
        ". The dataset has been cleaned and enriched for educational and demonstration purposes."
    ]),
])
