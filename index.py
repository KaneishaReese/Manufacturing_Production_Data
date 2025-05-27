from dash import Dash, dcc, html, page_container
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
print('App Created')
app.title = "Supply Chain Dashboard"

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dcc.Link("Home", href="/", className="nav-link")),
        dbc.NavItem(dcc.Link("Sales", href="/sales", className="nav-link")),
        dbc.NavItem(dcc.Link("Logistics", href="/logistics", className="nav-link")),
        dbc.NavItem(dcc.Link("Production", href="/production", className="nav-link")),
    ],
    brand="Supply Chain Analytics",
    color="dark",
    dark=True,
    fluid=True,
    className="mb-4"
)

app.layout = html.Div([
    navbar,
    page_container
])

if __name__ == "__main__":
    app.run()
