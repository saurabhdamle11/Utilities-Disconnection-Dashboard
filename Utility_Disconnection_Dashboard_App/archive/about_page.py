from dash import Dash, html
import app_config as cfg

# Add the CSS styles here
EMAIL_BUTTON_STYLE = {
    "background-color": "#a90533",
    "border": "none",
    "color": "black",
    "padding": "10px 20px",
    "textAlign": "center",
    "text-decoration": "none",
    "display": "inline-block",
    "margin": "4px 2px",
    "border-radius": "16px",
    "font-weight": "bold",
    "color": "white",
    "hover-active-background-color": "white",
}

about_text = html.Div(
    id="about-page",
    children=[
        html.H4("CONTACT US"),
        html.H1("Contact the Energy Justice Lab"),
        html.P("The O'Neill School of Public and Environmental Affairs"),
        html.Br(),
        html.P("Indiana University"),
        html.P("1315 E. Tenth Street, A319"),
        html.P("Bloomington, IN, 47405-1701"),
        html.Br(),
        html.P("(812) 856-0920"),
        html.Br(),
        html.A("Email us", id="email-button", href="mailto:tsamant@iu.edu", style=EMAIL_BUTTON_STYLE),
    ],
    style={
        "position": "fixed",
        "top": 0,
        "left": "18rem",
        "bottom": 0,
        "width": "40rem",
        "padding": "2rem 1rem",
    },
)

about_image = html.Div(
    html.Img(src=Dash().get_asset_url(cfg._ABOUT_PAGE_IMAGE)),
    style={
        "position": "fixed",
        "left": "50rem",
        "margin-left": "2rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem",
    },
)

about_page = html.Div(
    [
        about_text,
        about_image,
    ],
    style={"width": "auto"},
)


def display_about_page():
    return about_page
