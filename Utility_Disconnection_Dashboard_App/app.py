# Third party imports
from dash import Dash, html, dcc, callback_context, State
from dash.dependencies import Input, Output
from dash_bootstrap_templates import ThemeSwitchAIO
import dash_bootstrap_components as dbc

# Local imports
import disconnection_policies
import utility_disconnections
import service_territories
import config


# Initialize the application
app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}],
    title="Utility Disconnections Dashboard",
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# Needed by gunicorn when running in production.
server = app.server

app.index_string = '''
<!DOCTYPE html>
<html lang='en'>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# region nav_bar components

nav_bar = dbc.Row(
    [
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dbc.Row(
                        [
                            dbc.Col(
                                html.A(
                                    html.Img(src="assets/home.png", height="30px", alt="Home Image"),
                                    target="_blank",href="https://utilitydisconnections.org"), width=2,
                                style={"display": "flex", "justify-content": "end"}
                            ),
                            dbc.Col(
                                html.H1("Utility Disconnections Dashboard", style={"margin": "0"}),
                                width=8,
                                style={"display": "flex", "justify-content": "start"}
                            ),
                            # dbc.Col(
                            #     ThemeSwitchAIO(
                            #         aio_id="theme",
                            #         themes=[dbc.themes.BOOTSTRAP, dbc.themes.DARKLY],
                            #         icons={"left": "fa fa-moon", "right": "fa fa-sun"}
                            #     ),
                            #     width=2,
                            #     style={"display": "flex", "justify-content": "end"}
                            # )
                        ],
                        style={"align-items": "center"}  # Row style
                    )
                ),
                style={"border": "none"}  # Card style
            )
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Label(dcc.Dropdown(
                                    id="main-dropdown",
                                    value="Utility Disconnections",
                                    options=["Utility Disconnections","Disconnection Policies","Service Territories"],
                                    clearable=False, searchable=False, multi=False,
                                    style={"width": "360px", "color": "black"},
                                    loading_state={"is_loading ": True}
                                )),
                                width=11
                            ),
                            dbc.Col(
                                html.Div([html.Img(src="assets/ic.jpg", height="20px", alt="Main Dropdown Info", id='main-dropdown-tooltip'),
                                dbc.Tooltip(config.TOOLTIPS["main-dropdown-tooltip"],target='main-dropdown-tooltip')]),
                                # html.Button(
                                #     id="main-dropdown-tooltip",
                                #     value=config.TOOLTIPS["main-dropdown-tooltip"],
                                #     disabled=False,
                                #     type="submit",
                                #     className="Tooltip"
                                # ),
                                width=1,
                                style={"display": "flex", "justify-content": "center", "padding": "0"}
                            ),
                        ],
                        style={"align-items": "center"}  # Row style
                    )
                ),
                style={"border": "none"},  # Card style
            ),
            width=4
        )
    ],
    class_name="g-0",
    style={"width": "100%", "height": "10%"}  # Row style
)
# endregion


# =======================================================================================================================


# region content placeholder components
content = dbc.Row(
    # Create the content to be rendered on the UI
    [
        dbc.Col(
            [
                dbc.Row(id="map-placeholder"),
                dbc.Row(id="text-below-map-placeholder")
            ], width=8
        ),
        dbc.Col(
            [
                dbc.Row(id="filter-placeholder"),
                dbc.Row(id="mini-graph-placeholder")
            ], width=4
        ),
    ],
    style={"width": "100%", "height": "70%", "margin": "0"}
)
# endregion


# =======================================================================================================================


# region service_territories modal

service_territories_modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Utility Disconnections Dashboard")),
        dbc.ModalBody(
            dcc.Markdown(
                "Welcome to the utility disconnections dashboard, "
                + "as produced by the IU [Energy Justice Lab](https://energyjustice.indiana.edu/index.html)."
                + " \n\n"
                + "This dashboard has two interfaces: utility disconnections by state, "
                + "utility, and year; and utility disconnection protections."
                + " \n\n"
                + "This website is still a beta version and will be updated periodically "
                + "before the release of the final version.",
                link_target="_blank",
            )
        ),
        dbc.ModalFooter(dbc.Button("Close", id="close", className="ms-auto", n_clicks=0)),
    ],
    id="modal",
    is_open=False,
)
# endregion


# =======================================================================================================================


# region callbacks to inject content components into the placeholders
@app.callback(
    Output("map-placeholder", "children"),
    Input("main-dropdown", "value")
)
def update_map_placeholder(toggle):
    """
    Switches between disconnection visualization and Utility disconnections
    for the main map depending on the dropdown option
    """
    if toggle == "Utility Disconnections":
        component_id = "state-data-visualization"
        graph = utility_disconnections.visualization.get_map()
    elif toggle == "Disconnection Policies":
        component_id = "policies-visualization"
        graph = disconnection_policies.visualization.get_map()
    elif toggle == "Service Territories":
        component_id = "service-territories-viz"
        graph = service_territories.visualization.plot_map()
    return dbc.Card(
        dbc.CardBody(
            [
                dcc.Graph(
                    id=component_id,
                    figure=graph,
                    style={"height": "77.5vh"}
                )
            ]
        ), style={"padding": "0px"}
    )


@app.callback(
    Output("text-below-map-placeholder", "children"),
    Input("main-dropdown", "value"),
    Input("state-data-visualization", "clickData")
)
def update_text_below_map_placeholder(toggle, selected_state):
    """
    This injects descriptions about the selected state into text-below-map
    only renders when Utility Disconnection is selected in the dropdown main-dropdown
    """
    if toggle == "Utility Disconnections":
        if selected_state is None:
            state = "IN"
        else:
            state = selected_state["points"][0]["location"]
        return dbc.Card(dbc.CardBody(utility_disconnections.visualization.get_state_description(state)), outline=False)

    else:
        return


@app.callback(
    Output("filter-placeholder", "children"),
    Input("main-dropdown", "value")
)
def update_filter_placeholder(toggle):
    """
    Inject filter_menu_state or filter_menu_disconnection into filter-content
    depending on the option selected in the dropdown with id main-dropdown
    """
    if toggle == "Utility Disconnections":
        return dbc.Card(
            dbc.CardBody(
                [
                    # Year:
                    html.P("Year"),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Label(dcc.Dropdown(
                                    options=["All"]+sorted(utility_disconnections.config.YEARS, reverse=True),
                                    value=[2022],
                                    id="year-filter",
                                    multi=True,
                                    loading_state={"is_loading ": True},
                                    style={"width": "360px", "color": "black"},
                                    className='dropdown-class',
                                )),
                                width=11
                            )
                        ],
                        style={"align-items": "center"}  # Row style
                    ),
                    html.Hr(),
                    html.P("Month"),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Label(dcc.Dropdown(
                                    options=["All"]+utility_disconnections.config.MONTHS,
                                    value=["All"],
                                    id="month-filter",
                                    multi=True,
                                    style={"width": "360px", "color": "black"},
                                    className='dropdown-class',
                                )),
                                width=11
                            )
                        ],
                        style={"align-items": "center"}  # Row style
                    ),
                    html.Hr(),
                    html.P("Indicator"),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Label(dcc.Dropdown(
                                    options=utility_disconnections.config.INDICATORS,
                                    value=utility_disconnections.config.INDICATORS[0],
                                    id="indicator-filter",
                                    multi=False,
                                    clearable=False,
                                    style={"width": "360px", "color": "black"},
                                    className='dropdown-class',
                                )),
                                width=11
                            ),
                            dbc.Col(
                                html.Div([html.Img(src="assets/ic.jpg", height="20px", alt="Indicator Dropdown Info", id='indicator-dropdown-tooltip'),
                                dbc.Tooltip(config.TOOLTIPS["indicator-filter-tooltip"],target='indicator-dropdown-tooltip')]),
                                # html.Button(
                                #     id="indicator-filter-tooltip",
                                #     value=config.TOOLTIPS["indicator-filter-tooltip"],
                                #     disabled=False,
                                #     type="submit",
                                #     className="Tooltip"
                                # ),
                                width=1,
                                style={"display": "flex", "justify-content": "center", "padding": "0"}
                            ),
                            
                        ]
                    ),
                    html.P("Scope"),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Label(dcc.Dropdown(
                                    options=utility_disconnections.config.SCOPE,
                                    value=utility_disconnections.config.SCOPE[0],
                                    id="scope-filter",
                                    multi=False,
                                    clearable=False,
                                    style={"width": "360px", "color": "black"},
                                    className='dropdown-class',
                                )),
                                width=11
                            ),
                            dbc.Col(
                                html.Div([html.Img(src="assets/ic.jpg", height="20px", alt="Indicator Dropdown Info", id='scope-dropdown-tooltip'),
                                dbc.Tooltip(config.TOOLTIPS["scope-filter-tooltip"],target='scope-dropdown-tooltip')]),
                                # html.Button(
                                #     id="indicator-filter-tooltip",
                                #     value=config.TOOLTIPS["indicator-filter-tooltip"],
                                #     disabled=False,
                                #     type="submit",
                                #     className="Tooltip"
                                # ),
                                width=1,
                                style={"display": "flex", "justify-content": "center", "padding": "0"}
                            ),
                        ]
                    )
                ]
            ), style={"padding": "0px"}
        )

    elif toggle == "Disconnection Policies":
        return dbc.Card(
            dbc.CardBody(
                [
                    # Protection Type:
                    html.P("Protection Type"),

                    dbc.Row(
                        [
                            dbc.Col(
                                html.Label(dcc.Dropdown(
                                    id="protection-type-dropdown",
                                    value=disconnection_policies.config.PROTECTION_TYPE[0],
                                    options=disconnection_policies.config.PROTECTION_TYPE,
                                    clearable=False,
                                    searchable=False,
                                    multi=False,
                                    style={"width": "360px", "color": "black"},
                                    className='dropdown-class',
                                )),
                                width=11
                            ),
                            dbc.Col(
                                html.Div([html.Img(src="assets/ic.jpg", height="20px", alt="Protection Type Dropdown Info", id='protection-type-dropdown-tooltip'),
                                dbc.Tooltip(config.TOOLTIPS["protection-type-tooltip"],target='protection-type-dropdown-tooltip')]),
                                # html.Button(
                                #     id="protection-type-tooltip",
                                #     value=config.TOOLTIPS["protection-type-tooltip"],
                                #     disabled=False,
                                #     type="submit",
                                #     className="Tooltip"
                                # ),
                                width=1,
                                style={"display": "flex", "justify-content": "center", "padding": "0"}
                            ),
                        ],
                        style={"align-items": "center"}  # Row style
                    ),
                    html.Hr(),
                    html.P("Policy"),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Label(dcc.Dropdown(
                                    id="policy-name-dropdown",
                                    value=disconnection_policies.config.POLICY_NAMES["Cold-based Protections"][0],
                                    options=disconnection_policies.config.POLICY_NAMES["Cold-based Protections"],
                                    clearable=False,
                                    searchable=False,
                                    multi=False,
                                    style={"width": "360px", "color": "black"},
                                    loading_state={"is_loading ": True},
                                    className='dropdown-class',
                                )),
                                width=11
                            ),
                            dbc.Col(
                                html.Div([html.Img(src="assets/ic.jpg", height="20px", alt="Policy Dropdown Info", id='policy-dropdown-tooltip'),
                                dbc.Tooltip(config.TOOLTIPS["policy-name-tooltip"],target='policy-dropdown-tooltip')]),
                                # html.Button(
                                #     id="policy-name-tooltip",
                                #     value=config.TOOLTIPS["policy-name-tooltip"],
                                #     disabled=False,
                                #     type="submit",
                                #     className="Tooltip"
                                # ),
                                width=1,
                                style={"display": "flex", "justify-content": "center", "padding": "0"}
                            ),
                        ],
                        style={"align-items": "center"}  # Row style
                    )
                ]
            ), style={"padding": "0px"}
        )

    elif toggle == "Service Territories":
        return dbc.Card(
                dbc.CardBody(
                    [
                        # Year:
                        html.P("Year"),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Label(dcc.Dropdown(
                                        options=["All"]+sorted(utility_disconnections.config.YEARS, reverse=True),
                                        value=[2022],
                                        id="year-filter",
                                        multi=True,
                                        loading_state={"is_loading ": True},
                                        style={"width": "360px", "color": "black"},
                                        className='dropdown-class',
                                    )),
                                    width=11
                                )
                            ],
                            style={"align-items": "center"}  # Row style
                        ),
                        html.Hr(),
                        html.P("Month"),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Label(dcc.Dropdown(
                                        options=["All"]+utility_disconnections.config.MONTHS,
                                        value=["All"],
                                        id="month-filter",
                                        multi=True,
                                        style={"width": "360px", "color": "black"},
                                        className='dropdown-class',
                                    )),
                                    width=11
                                )
                            ],
                            style={"align-items": "center"}  # Row style
                        ),
                        html.Hr(),
                        html.P("Indicator"),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Label(dcc.Dropdown(
                                        options=utility_disconnections.config.INDICATORS,
                                        value=utility_disconnections.config.INDICATORS[0],
                                        id="indicator-filter",
                                        multi=False,
                                        clearable=False,
                                        style={"width": "360px", "color": "black"},
                                        className='dropdown-class',
                                    )),
                                    width=11
                                ),
                                dbc.Col(
                                    html.Div([html.Img(src="assets/ic.jpg", height="20px", alt="Indicator Dropdown Info", id='indicator-dropdown-tooltip'),
                                    dbc.Tooltip(config.TOOLTIPS["indicator-filter-tooltip"],target='indicator-dropdown-tooltip')]),
                                    # html.Button(
                                    #     id="indicator-filter-tooltip",
                                    #     value=config.TOOLTIPS["indicator-filter-tooltip"],
                                    #     disabled=False,
                                    #     type="submit",
                                    #     className="Tooltip"
                                    # ),
                                    width=1,
                                    style={"display": "flex", "justify-content": "center", "padding": "0"}
                                ),
                                
                            ]
                        ),
                        html.Hr(),
                        html.P("State"),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Label(dcc.Dropdown(
                                        options=["All"]+list(service_territories.config.STATE_CODE_TO_NAME.values()),
                                        value=["All"],
                                        id="state-filter",
                                        multi=False,
                                        style={"width": "360px", "color": "black"},
                                        className='dropdown-class',
                                    )),
                                    width=11
                                )
                            ],
                            style={"align-items": "center"}  # Row style                            
                        )
                    ]
                ), style={"padding": "0px"}
            )
##################################################################################
    elif toggle == "Gas":
            return dbc.Card(
                    dbc.CardBody(
                        [
                            # Year:
                            html.P("Year"),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Label(dcc.Dropdown(
                                            options=["All"]+sorted(utility_disconnections.config.YEARS, reverse=True),
                                            value=[2022],
                                            id="year-filter",
                                            multi=True,
                                            loading_state={"is_loading ": True},
                                            style={"width": "360px", "color": "black"},
                                            className='dropdown-class',
                                        )),
                                        width=11
                                    )
                                ],
                                style={"align-items": "center"}  # Row style
                            ),
                            html.Hr(),
                            html.P("Month"),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Label(dcc.Dropdown(
                                            options=["All"]+utility_disconnections.config.MONTHS,
                                            value=["All"],
                                            id="month-filter",
                                            multi=True,
                                            style={"width": "360px", "color": "black"},
                                            className='dropdown-class',
                                        )),
                                        width=11
                                    )
                                ],
                                style={"align-items": "center"}  # Row style
                            ),
                            html.Hr(),
                            html.P("Indicator"),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Label(dcc.Dropdown(
                                            options=utility_disconnections.config.INDICATORS,
                                            value=utility_disconnections.config.INDICATORS[0],
                                            id="indicator-filter",
                                            multi=False,
                                            clearable=False,
                                            style={"width": "360px", "color": "black"},
                                            className='dropdown-class',
                                        )),
                                        width=11
                                    ),
                                    dbc.Col(
                                        html.Div([html.Img(src="assets/ic.jpg", height="20px", alt="Indicator Dropdown Info", id='indicator-dropdown-tooltip'),
                                        dbc.Tooltip(config.TOOLTIPS["indicator-filter-tooltip"],target='indicator-dropdown-tooltip')]),
                                        # html.Button(
                                        #     id="indicator-filter-tooltip",
                                        #     value=config.TOOLTIPS["indicator-filter-tooltip"],
                                        #     disabled=False,
                                        #     type="submit",
                                        #     className="Tooltip"
                                        # ),
                                        width=1,
                                        style={"display": "flex", "justify-content": "center", "padding": "0"}
                                    ),
                                    
                                ]
                            ),
                            html.Hr(),
                            html.P("State"),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Label(dcc.Dropdown(
                                            options=["All"]+list(service_territories.config.STATE_CODE_TO_NAME.values()),
                                            value=["All"],
                                            id="state-filter",
                                            multi=False,
                                            style={"width": "360px", "color": "black"},
                                            className='dropdown-class',
                                        )),
                                        width=11
                                    )
                                ],
                                style={"align-items": "center"}  # Row style                            
                            )
                        ]
                    ), style={"padding": "0px"}
                )


@app.callback(
    Output("mini-graph-placeholder", "children"),
    Input("main-dropdown", "value")
)
def update_mini_graph_placeholder(toggle):
    """
    Switches child component of mini_map_card
    Injects mini_map if dropdown option is Utility Disconnection
    Injects policies_mini_map if dropdown option is Disconnection Policies
    """
    if toggle == "Utility Disconnections":
        return dbc.Card(
            dbc.CardBody(
                [
                    dcc.Graph(
                        id="bar-graph-visualization",
                        figure=utility_disconnections.visualization.get_bar_graph(),
                        # style={"height": "50vh"},
                        # config={"displayModeBar": False},
                    )
                ]
            ),
            outline=False,
        )
    elif toggle == "Disconnection Policies":
        return dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        id="policy-description",
                        # style={"height": "50vh"}
                    )
                ]
            ),
            outline=False
        )
    elif toggle == "Service Territories":
        return dbc.Card(
            dbc.CardBody(
                [
                    dcc.Graph(
                        id="bar-graph-visualization",
                        figure=service_territories.visualization.get_bar_graph(),
                        # style={"height": "50vh"},
                        # config={"displayModeBar": False},
                    )
                ]
            ),
            outline=False,
        )
# endregion


# =======================================================================================================================


# region tooltip callbacks:
"""
@app.callback(
    Output("main-dropdown-tooltip", "value"),
    Input("main-dropdown", "value")
)
def update_main-dropdown_tooltip(toggle):
    return constants.TOOLTIPS["main-dropdown-tooltip"][toggle]


@app.callback(
    Output("year-filter-tooltip", "value"),
    Input("year-filter", "value")
)
def update_year_slider_tooltip(toggle):
    return constants.TOOLTIPS["year-filter-tooltip"][toggle]


@app.callback(
    Output("month-filter-tooltip", "value"),
    Input("month-filter", "value")
)
def update_month_slider_tooltip(toggle):
    return constants.TOOLTIPS["month-filter-tooltip"][toggle]


@app.callback(
    Output("indicator-filter-tooltip", "value"),
    Input("indicator-filter", "value")
)
def update_indicator_filter_tooltip(toggle):
    return constants.TOOLTIPS["indicator-filter-tooltip"][toggle]


@app.callback(
    Output("protection-type-tooltip", "value"),
    Input("protection_type", "value")
)
def update_protection_type_tooltip(toggle):
    return constants.TOOLTIPS["protection-type-tooltip"][toggle]


@app.callback(
    Output("policy-name-tooltip", "value"),
    Input("policy_name", "value")
)
def update_policy_name_tooltip(toggle):
    return constants.TOOLTIPS["policy-name-tooltip"][toggle]
"""
# endregion


# =======================================================================================================================


# region content component callbacks
@app.callback(
    Output("year-filter", "value"),
    Input("year-filter", "value")
)
def update_year_filter(selected):
    """
    if "All" is selected at anytime: remove every year but "All"
    if a year is selected after "All": remove "All"
    """
    if not selected:  # empty
        return
    if (selected[-1] == "All"):
        return "All"
    elif (selected[0] == "All"):
        return selected[1:]
    return selected


@app.callback(
    Output("month-filter", "value"),
    Input("month-filter", "value")
)
def update_month_filter(selected):
    """
    if "All" is selected at anytime: remove every month but "All"
    if a month is selected after "All": remove "All"
    """
    if not selected:  # empty
        return
    if (selected[-1] == "All"):
        return "All"
    elif (selected[0] == "All"):
        return selected[1:]
    return selected


@app.callback(
    Output("state-filter", "value"),
    Input("state-filter", "value")
)
def update_state_filter(selected):
    """
    if "All" is selected at anytime: remove every state but "All"
    if a state is selected after "All": remove "All"
    """
    if not selected:  # empty
        return
    if (selected[-1] == "All"):
        return "All"
    elif (selected[0] == "All"):
        return selected[1:]
    return selected

@app.callback(
    Output("policies-visualization", "figure"),
    Output("policy-name-dropdown", "options"),
    Output("policy-name-dropdown", "value"),
    Input("protection-type-dropdown", "value"),
    Input("policy-name-dropdown", "value"),
    Input("policies-visualization", "clickData"),
)
def update_disconnection_map(protection_type, policy_name, selected_state):
    """
    This callback updates the disconnection policies visualization.
    """
    if selected_state is None:
        state = "IN"
    else:
        state = selected_state["points"][0]["location"]

    if policy_name in disconnection_policies.config.POLICY_NAMES[protection_type]:
        policy = policy_name
    else:
        policy = disconnection_policies.config.POLICY_NAMES[protection_type][0]
    return (
        disconnection_policies.visualization.get_map(protection_type, policy, state),
        disconnection_policies.config.POLICY_NAMES[protection_type],
        policy,
    )


@app.callback(
    Output("policy-description", "children"),
    Input("protection-type-dropdown", "value"),
    Input("policy-name-dropdown", "value"),
    Input("policies-visualization", "clickData")
)
def updated_policy_description(protection_type, policy_name, selected_state):
    if selected_state is None:
        state = "IN"
    else:
        state = selected_state["points"][0]["location"]

    return disconnection_policies.visualization.get_policy_description(state)


@app.callback(
    [Output("state-data-visualization", "figure")],
    [
        Input("state-data-visualization", "clickData"),
        Input("month-filter", "value"),
        Input("year-filter", "value"),
        Input("indicator-filter", "value"),
    ],
)
def updated_state_disconnection_viz(state, months, years, indicator_filter):
    """
    This callback updates the state visualization map on selected year and month
    """
    if state is None:
        state = "IN"
    else:
        state = state["points"][0]["location"]
    # print("*** State:" + state)
    if indicator_filter != "Number of disconnections":
        per_captia = True
    else:
        per_captia = False
    return [utility_disconnections.visualization.get_map(state, months, years, per_captia)]


@app.callback(
    [Output("service-territories-viz", "figure")],
    [
        #Input("service-territories-viz", "clickData"),
        Input("month-filter", "value"),
        Input("year-filter", "value"),
        Input("indicator-filter", "value"),
        Input("state-filter", "value"),
    ],
)
def updated_service_territories_viz(months, years, indicator_filter, state):
    """
    This callback updates the service territories visualization map on selected year and month
    """
    # if state is None:
    #     state = "Indiana"
    # else:
    #     state = state["points"][0]["location"]
    # print("*** State:" + state)
    if indicator_filter != "Number of disconnections":
        per_captia = True
    else:
        per_captia = False

    return [service_territories.visualization.plot_map( years, months, state)]


# @app.callback(
#     Output("modal", "is_open", allow_duplicate=True),
#     Input("close", "n_clicks"),
#     State("modal", "is_open"),
#     Input("month-filter", "value"),
#     Input("year-filter", "value"),
#     Input("indicator-filter", "value"),
#     Input("state-filter", "value"),
#     prevent_initial_call=True
# )
# def close_service_territories_modal(n, is_open,months, years, indicator_filter, state):
#     print(len([service_territories.visualization.plot_map( years, months, state)]))
#     if len([service_territories.visualization.plot_map( years, months, state)])>0:
#         return not is_open
#     return is_open

@app.callback(
    [
        Output("bar-graph-visualization", "figure"),
    ],
    [
        Input("state-data-visualization", "clickData"),
        Input("month-filter", "value"),
        Input("year-filter", "value"),
        Input("indicator-filter", "value"),
    ],
)
def updated_state_disconnection_viz_mini_map(state, months, years, indicator_filter):
    if state is None:
        state = "IN"
    else:
        state = state["points"][0]["location"]
    # print("* State:" + state)
    if indicator_filter != "Number of disconnections":
        per_captia = True
    else:
        per_captia = False
    return [utility_disconnections.visualization.get_bar_graph(state, months, years, per_captia)]
# endregion


# =======================================================================================================================


# region service_territories modal callback

@app.callback(
    Output("modal", "is_open"),
    Input("close", "n_clicks"),
    State("modal", "is_open"),
)
def close_service_territories_modal(n, is_open):
    if n > 0:
        return not is_open
    return is_open

# endregion

# =======================================================================================================================


# region about_us bar component
about_us = dbc.Card(
    # Card for the navigation bar below the map
    dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.A(
                            [
                                html.Img(
                                    src="assets/Energy_Justice_Lab_Logo.png", alt="Link to Energy Justice Lab Site",
                                    style={"float": "left", "position": "relative", "padding-left": "10px"},
                                )
                            ],
                            target="_blank",
                            href="https://energyjustice.indiana.edu",
                        ),
                        width=3
                    ),
                    dbc.Col(
                        html.A(
                            "Questions? Share Data? Email Us!",
                            target="_blank",
                            href="mailto:enjlab@indiana.edu",
                            style={"align-items": "center", "justify-content": "center", "display": "flex"},
                        ),
                        width=3
                    ),
                    dbc.Col(
                        html.A(
                            "Technical Documentation",
                            target="_blank",href="https://utilitydisconnections.org/doc/utility-disconnections-dashboard-technical-documentation_20230529.pdf"
                        ),
                        width=3
                    ),
                    dbc.Col(id="download-btn-placeholder", width=3)
                ]
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Download Disconnection Policies Data")),
                    dbc.ModalBody("Please select the data to download"),
                    dbc.ModalFooter(
                        html.Div(
                            [
                                dbc.Button(
                                    "Download Selected Data",
                                    id="policy-selected-btn",
                                    className="me-1",
                                ),
                                dbc.Button(
                                    "Download All",
                                    id="policy-all-btn",
                                    className="me-1"
                                ),
                                dcc.Download(id="policy-download-component")
                            ]
                        )
                    )
                ],
                id="policy-download-modal",
                is_open=False,
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Download Utility Disconnections Data")),
                    dbc.ModalBody("Please select the data to download"),
                    dbc.ModalFooter(
                        html.Div(
                            [
                                dbc.Button(
                                    "Download Selected Data",
                                    id="discon-selected-btn",
                                    className="me-1",
                                ),
                                dbc.Button(
                                    "Download All",
                                    id="discon-all-btn",
                                    className="me-1"
                                ),
                                dcc.Download(id="discon-download-component")
                            ]
                        )
                    )
                ],
                id="discon-download-modal",
                is_open=False,
            )
        ]
    )
)
# endregion


# =======================================================================================================================


# region callback to inject download buttons into the about_us placeholders
@app.callback(
    Output("download-btn-placeholder", "children"),
    Input("main-dropdown", "value")
)
def update_download_button_placeholder(toggle):
    """
    To decouple "Disconnection Policies" and "Utility Disconnections" for the callbacks, use buttons with distinct ids.
    This callback handles that.
    """
    if toggle == "Disconnection Policies":
        return dbc.Button(
            "Download Data",
            id="policy-download-data-btn",
            n_clicks=0,
            class_name="text-center",
            color="primary",
            style={"textAlign": "right", "float": "right"},
        )

    elif toggle == "Utility Disconnections":
        return dbc.Button(
            "Download Data",
            id="discon-download-data-btn",
            n_clicks=0,
            class_name="text-center",
            color="primary",
            style={"textAlign": "right", "float": "right"},
        )
# endregion


# =======================================================================================================================


# region abous_us bar callbacks
@app.callback(
    Output("policy-download-modal", "is_open"),
    Output("policy-download-component", "data"),
    Input("policy-download-data-btn", "n_clicks"),
    Input("policy-selected-btn", "n_clicks"),
    Input("policy-all-btn", "n_clicks"),
    State("protection-type-dropdown", "value"),
    prevent_initial_call=True
)
def policy_download_modal(download_btn, selected_btn, all_btn, protection):
    trigger = callback_context.triggered_id
    if trigger == "policy-download-data-btn" and download_btn != 0:
        return True, None
    else:
        if trigger == "policy-all-btn":
            file = disconnection_policies.utils.get_all_data()
            filename = "Disconnection Policy Data [all protection types].xlsx"
            return False, dcc.send_file(file, filename=filename)
        elif trigger == "policy-selected-btn":
            file = disconnection_policies.utils.get_selected_data(protection)
            filename = f"Disconnection Policy Data [{protection}].xlsx"
            return False, dcc.send_file(file, filename=filename)
        else:
            return False, None


@app.callback(
    Output("discon-download-modal", "is_open"),
    Output("discon-download-component", "data"),
    Input("discon-download-data-btn", "n_clicks"),
    Input("discon-selected-btn", "n_clicks"),
    Input("discon-all-btn", "n_clicks"),
    State("state-data-visualization", "clickData"),
    prevent_initial_call=True
)
def discon_download_modal(download_btn, selected_btn, all_btn, click_data):
    trigger = callback_context.triggered_id
    if trigger == "discon-download-data-btn" and download_btn != 0:
        return True, None
    else:
        if trigger == "discon-all-btn":
            pass
            file = utility_disconnections.utils.get_all_data()
            filename = "Utility Disconnections Data [all states].xlsx"
            return False, dcc.send_file(file, filename=filename)
        elif trigger == "discon-selected-btn":
            if click_data is None:
                state = "IN"
            else:
                state = click_data["points"][0]["location"]
            file = utility_disconnections.utils.get_selected_data(state)
            filename = f"Utility Disconnections Data [{state}].xlsx"
            return False, dcc.send_file(file, filename=filename)
        else:
            return False, None
# endregion


# =======================================================================================================================


# region welcome modal component
# welcome_modal = dbc.Modal(
#     [
#         dbc.ModalHeader(dbc.ModalTitle("Utility Disconnections Dashboard")),
#         dbc.ModalBody(
#             dcc.Markdown(
#                 "Welcome to the utility disconnections dashboard, "
#                 + "as produced by the IU [Energy Justice Lab](https://energyjustice.indiana.edu/index.html)."
#                 + " \n\n"
#                 + "This dashboard has two interfaces: utility disconnections by state, "
#                 + "utility, and year; and utility disconnection protections."
#                 + " \n\n"
#                 + "This website is still a beta version and will be updated periodically "
#                 + "before the release of the final version.",
#                 link_target="_blank",
#             )
#         ),
#         dbc.ModalFooter(dbc.Button("Close", id="close", className="ms-auto", n_clicks=0)),
#     ],
#     id="modal",
#     is_open=True,
# )
# endregion


# =======================================================================================================================


# region welcome modal callback
# @app.callback(
#     Output("modal", "is_open"),
#     Input("close", "n_clicks"),
#     State("modal", "is_open"),
# )
# def close_welcome_modal(n, is_open):
#     if n > 0:
#         return not is_open
#     return is_open
# endregion


# =======================================================================================================================


# region Jason's zipcode data code

# zipcode_data_visualization = dbc.Card(
#     dbc.CardBody(
#         dcc.Graph(id="zipcode-visualization", figure=get_location_interactive(), style={"height": "50vh"}), width=4
#     )
# )

# inside update_map_placeholder() callback
    # elif "btn-nclicks-3" in changed_id:  # id="zipcode-visualization",
    #     # figure = get_location_interactive()
    #     return [
    #         html.H3("Zipcode level data", style={"textAlign": "center"}),
    #         # filter_menu_disconnection,
    #         dcc.Graph(
    #             id="zipcode-visualization",
    #             figure=get_location_interactive(),
    #             style={"height": "77.5vh"}
    #             # config = {'displayModeBar': False}
    #         ),
    #     ]

# @app.callback(
#     Output("zipcode-visualization", "figure"),
#     [
#         Input("btn-nclicks-1", "n_clicks"),
#         Input("btn-nclicks-2", "n_clicks"),
#         #  Input('btn-nclicks-3', 'n_clicks')
#     ],
# )
# def zipcodeVisualization(btn1, btn2):
#     changed_id = [p["prop_id"] for p in callback_context.triggered][0]
#     if "btn-nclicks-3" in changed_id:  # State Disconnection:
#         return get_location_interactive()


# print("data loading")
# zipcode_data = json.load(open("./Zipcode_Data/ca_california_zip_codes_geo.min.json", "r"))
# # extract zipcode for id matching

# df = pd.read_csv("./Zipcode_Data/Sample_data_all_zipcode_inCSV.csv")

# print("data loaded")
# # zipcode_figure = get_location_interactive(df, zipcode_data)
# # print("generated plot")

# endregion


app.layout = html.Div(
    [
        dcc.Location(id="url"),
        nav_bar,
        content,
        about_us,
        service_territories_modal
    ],
    # style={"height": "100vh", "width": "100vw"}
)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=80, debug=True)
