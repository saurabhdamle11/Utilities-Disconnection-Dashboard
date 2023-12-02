# Standard imports
import sys
import json

# Third party imports
import pandas as pd
import plotly.express as px
from dash import dcc

# Local imports
from .config import (
    COLD_PROTECTIONS_PATH, HEAT_PROTECTIONS_PATH, INDIVIDUAL_PROTECTIONS_PATH, PROCEDURAL_REQUIREMENTS_PATH,
    POLICY_WRITEUP_PATH, US_STATES_SHAPE_PATH,
    STATE_CODE_TO_NAME, STATE_CODES
)


# Read the protections data and add the states codes for visualizations
cold_protection = pd.read_csv(COLD_PROTECTIONS_PATH)
heat_protection = pd.read_csv(HEAT_PROTECTIONS_PATH)
individual_protection = pd.read_csv(INDIVIDUAL_PROTECTIONS_PATH)
# administrative_requirement = pd.read_csv(ADMINISTRATIVE_REQUIREMENTS_PATH)
procedural_requirement = pd.read_csv(PROCEDURAL_REQUIREMENTS_PATH)
policy_writeup = pd.read_csv(POLICY_WRITEUP_PATH)

with open(US_STATES_SHAPE_PATH) as json_file:
    geojson = json.load(json_file)

# Append the states codes to the protection policies data to generate visualizations
cold_protection["Code"] = STATE_CODES
heat_protection["Code"] = STATE_CODES
individual_protection["Code"] = STATE_CODES
# administrative_requirement["Code"] = STATE_CODES
procedural_requirement["Code"] = STATE_CODES

# Fix Nan values
cold_protection.fillna("", inplace=True)
heat_protection.fillna("", inplace=True)

# To be removed in later iterations, currently used for map visualization
old_state = ""


def get_policy_description(state="IN"):
    """
    Gets the markdown for a detailed policy description of the selected state
    """
    state = STATE_CODE_TO_NAME[state]
    state_writeup = policy_writeup[policy_writeup["State"] == str(state)]
    return_state = dcc.Markdown(
        " ##### Selected State is: "
        + str(state)
        + "  \n \n"
        + " Covered utilities: "
        + str(state_writeup["Covered"].values[0])
        + "  \n \n"
        + "[Click for more state policy information](https://github.com/jgumaer/Disconnection_Policies/raw/main/"
        + str(state_writeup["URL"].values[0])
        + ".pdf)"
        + " \n \n"
        + " Last updated: January 30, 2023",
        link_target="_blank",
    )
    # link = html.A(
    #     "Questions? Email us",
    #     target="_blank",
    #     href="mailto:enjlab@indiana.edu",
    # )
    return return_state


def get_map(protection_type="", policy_type="", state="IN"):
    """
    This function create the disconnection policies visualization.
    """
    # state_old = state
    state = STATE_CODE_TO_NAME[state]

    # Filter the selected data
    if protection_type == "Cold-based Protections" or protection_type == "":
        data = cold_protection
        if policy_type == "":
            policy_type = data.columns[1]
    if protection_type == "Heat-based Protections":
        data = heat_protection
        if policy_type == "":
            policy_type = data.columns[1]
    if protection_type == "Protection for Individuals":
        data = individual_protection
        if policy_type == "":
            policy_type = data.columns[1]
    # if protection_type == 'Administrative Requirements':
    #     data = administrative_requirement
    #     if policy_type == '':
    #         policy_type = data.columns[1]
    if protection_type == "Procedural Requirements":
        data = procedural_requirement
        if policy_type == "":
            policy_type = data.columns[1]

    # Prepare a lookup dictionary for selecting highlight areas in geojson
    # state_lookup = {feature["properties"]["name"]: feature for feature in geojson["features"]}
    # state = "Indiana"
    # print(type(state))
    # print(state)
    # print(state_lookup[state])

    if data[policy_type].iloc[0] == "Yes":
        legend_direction = "normal"
    else:
        legend_direction = "reversed"

    fig = px.choropleth(
        data[["State", policy_type, "Code"]],
        locations="Code",
        locationmode="USA-states",
        color=policy_type,
        scope="usa",
        color_discrete_map={"Yes": "rgb(80,125,176)", "No": "rgb(255,188,120)"},
        custom_data= [data["State"], policy_type]
    )

    
    filtered_state = data[data["State"] == state]
    # fig.update_traces(marker_opacity=1)

    fig2 = px.choropleth(
        filtered_state,
        locations="Code",
        # geojson=state_lookup[state],
        locationmode="USA-states",
        color=policy_type,
        scope="usa",
        color_discrete_map={"Yes": "rgb(80,125,255)", "No": "rgb(255,188,1)"},
        custom_data= [filtered_state["State"], policy_type]
    )
    # remove_legend = fig2.data[0]
    global old_state
    if state != old_state:
        fig2.update_traces(
            showlegend=False,
            hovertemplate=None,
            hoverinfo="skip"
        )  # marker_opacity=0.95
        # remove_legend.update_coloraxes(showscale=False)
        fig.add_trace(fig2.data[0])
        old_state = state

    fig.update_traces(hoverinfo="skip",hovertemplate="<b>%{customdata[0]}</b><br /><br />" + protection_type + "<br />" + str(policy_type) +": %{customdata[1]}<extra></extra>")

    # global old_state
    # if state != old_state:
    #     print("I am here")
    #     fig.add_trace(
    #         # px.choropleth_mapbox(
    #         #     data, geojson=state_lookup[state],
    #         #     # color=policy_type,
    #         #     locations="State",
    #         #     featureidkey="properties.name",
    #         #     color_discrete_sequence=["grey"],
    #         #     hover_name="State",
    #         #     hover_data=[str(policy_type), "Website"],
    #         #     opacity=1
    #         # )

    #         .data[0]
    #     )
    #     old_state = state

    # ------------------------------------#

    # hover_template = 'State: '+ state + \
    #         '<br>' + str(policy_type)+
    # fig.update_traces(hovertemplate=hover_template)

    fig.update_geos(showcountries=True, countrycolor="Black", showsubunits=True, subunitcolor="Black")

    # Update the layout
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0, pad=4, autoexpand=True),
        # geo=dict(
        #     bgcolor='rgba(173, 167, 164, 1)',
        #     lakecolor='rgba(173, 167, 164, 1)',
        #     landcolor='rgba(173, 167, 164, 1)',
        #     subunitcolor='rgba(173, 167, 164, 1)',
        # ),
        geo=dict(showlakes=False),
        dragmode=False,
        legend=dict(orientation="h", yanchor="bottom", y=0.04, xanchor="right", x=1, traceorder = legend_direction),
        # title = dict(
        #     text="Sanya Carley and David Konisky, 2023, \"Utility Disconnections Dashboard,\" Energy Justice Lab",
        #     y=0.01,
        #     x=0.5,
        #     font=dict(size = 10)
        # ),
    )
    return fig


def get_bar_graph(protection_type="", policy_type=""):
    """
    NO LONGER USED
    This function will be used to visualize the mini graph for policies
    """
    # Filter the selected data
    if protection_type == "Cold Protections" or protection_type == "":
        data = cold_protection
        if policy_type == "":
            policy_type = data.columns[1]
    if protection_type == "Heat-based Protections":
        data = heat_protection
        if policy_type == "":
            policy_type = data.columns[1]
    if protection_type == "Protection for Individuals":
        data = individual_protection
        if policy_type == "":
            policy_type = data.columns[1]
    # if protection_type == 'Administrative Requirements':
    #     data = administrative_requirement
    #     if policy_type == '':
    #         policy_type = data.columns[1]
    if protection_type == "Procedural Requirements":
        data = procedural_requirement
        if policy_type == "":
            policy_type = data.columns[1]

    # Generate the plot
    title = protection_type
    # fig = px.histogram(
    #     data,
    #     x=policy_type,
    #     y='State',
    #     color=policy_type,
    #     barmode='group',
    #     title=title,
    #     height=400
    # )
    # print(policy_type)
    fig = px.histogram(
        data,
        x=policy_type,
        # y='State',
        color=policy_type,
        title=title,
        color_discrete_sequence=["orange", "blue"]
        # height=300
    )

    fig.update_xaxes(visible=False)

    fig.update_layout(
        margin=dict(
            l=20,
            r=20,
            b=20,
            t=40,
            pad=0,
            autoexpand=True,
        ),
        # geo=dict(
        #     bgcolor='rgba(173, 167, 164, 1)',
        #     lakecolor='rgba(173, 167, 164, 1)',
        #     landcolor='rgba(173, 167, 164, 1)',
        #     subunitcolor='rgba(173, 167, 164, 1)',
        # ),
        legend=dict(orientation="h", yanchor="top", y=0, xanchor="left", x=0),
        # yaxis={'visible': False},
        yaxis_title="No. of States",
    )
    return fig


"""
To test the visualization independently.
"""
if __name__ == "__main__":
    # fig = disconnection_policies_visualization('', '')
    fig = get_bar_graph()
    fig.show()
    sys.exit(1)
