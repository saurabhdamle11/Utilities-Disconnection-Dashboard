# Standard imports
import sys
import json
from typing import List

# Third party imports
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc

# Local imports
from .config import (
    STATE_CODE_TO_NAME, YEARS, MONTHS, US_STATES_SHAPE_PATH,
    DISCONNECTION_COUNT_DATA_PATH, DISCONNECTION_UTILITY_DATA_PATH,
    US_CENCUS_PATH, NO_DATA_PATH, WRITEUP_PATH
)


# Read the protections data and add the states codes for visualizations.
disconnection_count_data = pd.read_csv(DISCONNECTION_COUNT_DATA_PATH)
disconnection_utility_data = pd.read_csv(DISCONNECTION_UTILITY_DATA_PATH)
disconnection_utility_data = disconnection_utility_data[disconnection_utility_data['Service Type'] == "Gas" ]
us_census = pd.read_csv(US_CENCUS_PATH)  # not used
no_data = pd.read_csv(NO_DATA_PATH)  # not used
writeup = pd.read_csv(WRITEUP_PATH)

with open(US_STATES_SHAPE_PATH) as json_file:
    geojson = json.load(json_file)
state_lookup = {feature["properties"]["name"]: feature for feature in geojson["features"]}


def get_map(state_code: str = "MO", month: List[str] = ["January"], year: str = [2022], per_capita: bool = False, scope: bool = False):
    """Generates the State Disconnections Plotly map figure.

    Args:
        state_code: The state selected.
        month: The month(s) or "All" to filter on.
        year: The year(s) or "All" to filter on.

    Returns:
        A Plotly Choropleth map of the United States representing utility disconnection information.
    """

    # ~~ Data Filtering and Aggregation ~~ #

    # region Map Data Filter

    # Make sure our month and year filters are lists.
    year = [year] if type(year) != list else year
    month = [month] if type(month) != list else month

    if "All" in year or len(year) == 0:
        year = list(YEARS)
    if "All" in month or len(month) == 0:
        month = list(MONTHS)

    # Filter data by year and month.
    filtered_data_view = disconnection_count_data.loc[
        (disconnection_count_data["Year"].isin(year)) &
        (disconnection_count_data["Month"].isin(month))
    ]

    # Group by state and aggregate on sum of disconnections and mean of rate.
    filtered_data_view_totals = filtered_data_view.groupby(["State", "code"], as_index=False).agg(
        {"Number of Disconnections": "sum", "Disconnection Rate": "mean"}
    )

    filtered_data_view_totals_rate_drop = filtered_data_view_totals.dropna(subset=['Disconnection Rate'])

    # Filter for selected state highlighting.
    filtered_data_view_state_totals = filtered_data_view_totals.loc[filtered_data_view_totals["code"] == state_code]

    # Data related parameter variables for the various graph objects below.
    if per_capita:
        # Parameters for main map.
        color_values = filtered_data_view_totals["Disconnection Rate"]
        range_color = [0, filtered_data_view_totals["Disconnection Rate"].max()]
        color_continuous_midpoint = filtered_data_view_totals["Disconnection Rate"].quantile(.5)
        color_scheme = "teal"
        colorbar_title_text = "Disconnection Rate"
        custom_data = [filtered_data_view_totals["State"], np.round(filtered_data_view_totals["Disconnection Rate"] * 100,2)]
        hover_template = "<b>%{customdata[0]}</b><br /><br />Disconnection Rate: %{customdata[1]:,}%"

        # Parameters for selected state highlighting trace.
        state_color_values = filtered_data_view_state_totals["Disconnection Rate"]
        state_custom_data = [
            filtered_data_view_state_totals["State"],
            np.round(filtered_data_view_state_totals["Disconnection Rate"] * 100,2)
        ]
    else:
        # Parameters for main map.
        color_values = filtered_data_view_totals["Number of Disconnections"]
        range_color = [0, filtered_data_view_totals["Number of Disconnections"].max()]
        color_continuous_midpoint = filtered_data_view_totals["Number of Disconnections"].quantile(.5)
        color_scheme = "reds"
        colorbar_title_text = "No. of Disconnections"
        custom_data = [filtered_data_view_totals["State"], filtered_data_view_totals["Number of Disconnections"]]
        hover_template = "<b>%{customdata[0]}</b><br /><br />No. of Disconnections: %{customdata[1]:,}"

        # Parameters for selected state highlighting trace.
        state_color_values = filtered_data_view_state_totals["Number of Disconnections"]
        state_custom_data = [
            filtered_data_view_state_totals["State"],
            filtered_data_view_state_totals["Number of Disconnections"]
        ]

    # endregion Map Data Filter

    # ~~ Build Main Figure ~~ #

    # region Build Map

    # Generate Choropleth plot figure.
    fig = px.choropleth(
        # The DataFrame being mapped.
        filtered_data_view_totals,
        # The values used to determine the color.
        color=color_values,
        # Provides a way to inject custom data into the figure that can be referenced later.
        custom_data=custom_data,
        # The color scale on which the color values are placed.
        color_continuous_scale=color_scheme,
        # The range from minimum value to maximum value on color scale.
        range_color=range_color,

        color_continuous_midpoint = color_continuous_midpoint,
        # The field in the DataField returned for each component on the map.
        locations="code",
        # The Choropleth mode used to map the geolocation on the map to the "locations" column above.
        locationmode="USA-states",
        # The Choropleth geo map to use.
        scope="usa"
    )

    # Update the colorbar dimensions and labels.
    fig.update_coloraxes(
        colorbar_title_text=colorbar_title_text,
        colorbar_yanchor="bottom",
        colorbar_xanchor="right",
        colorbar_y=0.0,
        colorbar_x=1,
        colorbar_len=0.6,
        colorbar_orientation="h"
    )

    # Update map dimensions and hide unused legend (we only need the colorbar).
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0, pad=4, autoexpand=True),
        showlegend=False
    )

    # Update hover data template.
    fig.update_traces(hovertemplate=hover_template)

    # Update properties related to the geojson map features.
    fig.update_geos(showlakes=False)

    # endregion Build Map

    # ~~ Fill In Missing Data ~~ #

    # region Missing Data Trace

    # Generate placeholder DataFrame for missing data.
    missing_data = pd.DataFrame(np.empty((0, 2)), columns=["State", "code"])
    for code, state in STATE_CODE_TO_NAME.items():
        if per_capita:
        
            if state not in filtered_data_view_totals_rate_drop["State"].unique():
                missing_data = pd.concat([missing_data, pd.DataFrame({
                    "State": state,
                    "code": code,
                }, index=[0])], ignore_index=True)
        
        else:

            if state not in filtered_data_view_totals["State"].unique():
                missing_data = pd.concat([missing_data, pd.DataFrame({
                    "State": state,
                    "code": code,
                }, index=[0])], ignore_index=True)

    # Create a second Choropleth trace representing missing data for main figure.
    missing_plot_data = px.choropleth(
        missing_data,
        color_discrete_sequence=["rgb(169, 169, 169)"],
        custom_data=[missing_data["State"]],
        locations="code",
        locationmode="USA-states",
        scope="usa"
    ).update_traces(
        hovertemplate="<b>%{customdata[0]}</b><br /><br />No Data With Given Filters"
    ).data[0]

    # Add missing data trace to main figure.
    fig.add_trace(missing_plot_data)

    # endregion Missing Data Trace

    # ~~ Highlight Selected State ~~ #

    # region Selected Highlight Trace

    # Create a trace over the selected state and highlight its borders.
    if len(filtered_data_view_state_totals) > 0:
        highlight_plot_data = px.choropleth(
            filtered_data_view_state_totals,
            color=state_color_values,
            custom_data=state_custom_data,
            color_continuous_scale=color_scheme,
            range_color=range_color,
            locations="code",
            locationmode="USA-states",
            scope="usa"
        ).update_traces(
            hovertemplate=hover_template,
            marker=dict(line=dict(width=1.5, color="yellow"))
        ).data[0]

        # Add selected state highlighting trace to main figure.
        fig.add_trace(highlight_plot_data)

    # endregion Selected Highlight Trace

    return fig


def get_bar_graph(state="MO", month=["January"], year=[2022], per_captia=False):
    """
    Creates the bar graph, filtered by selected state, month and year.
    """
    state = STATE_CODE_TO_NAME[state]

    year = [year] if type(year) != list else year
    month = [month] if type(month) != list else month

    if "All" in year or len(year) == 0:
        year = list(YEARS)
    if "All" in month or len(month) == 0:
        month = list(MONTHS)

    # Filter data by state, year, and month
    filtered_data_view = disconnection_utility_data.loc[
        (disconnection_utility_data["State"] == state) &
        (disconnection_utility_data["Year"].isin(year)) &
        (disconnection_utility_data["Month"].isin(month))
    ]

    # Sort data by the Total Disconnections values
    sorted_disconnections = filtered_data_view.sort_values(by="Total Disconnections")
    avg_disconnection_rate = filtered_data_view.groupby(['Utility Name'],as_index=False).agg({'Disconnection Rate':'mean'})
    avg_disconnection_rate = avg_disconnection_rate.dropna()
    avg_disconnection_rate['Disconnection Rate'] = avg_disconnection_rate['Disconnection Rate']*100

    draft_template = go.layout.Template()
    #     draft_template.layout.annotations = [
    #     dict(
    #         name="draft watermark",
    #         text="Energy Justice Lab, 2023",
    #         textangle=0,
    #         opacity=1,
    #         font=dict(color="black", size=10),
    #         xref="paper",
    #         yref="paper",
    #         x=0.5,
    #         y=-0.11,
    #         showarrow=False,
    #     )
    # ]
    # Generate the plot
    if per_captia:
        title = "Average Disconnection Rate <br> by Utilities in " + state
        fig = px.bar(
            avg_disconnection_rate,
            x="Utility Name",
            y="Disconnection Rate",
            color="Utility Name",
            custom_data=[avg_disconnection_rate['Utility Name'],np.round(avg_disconnection_rate['Disconnection Rate'],2)],
            range_color=[0, sorted_disconnections["Disconnection Rate"].max()],
            color_discrete_sequence=px.colors.qualitative.Antique,
            title=title,
        )
        fig.update_yaxes(title="Disconnection Rate (%)")
        fig.update_traces(hovertemplate="<b>%{customdata[0]}</b><br />Disconnection Rate: %{customdata[1]:,}%<extra></extra>")

    else:
        title = "Total Disconnections by Utilities <br> in " + state
        fig = px.bar(
            sorted_disconnections,
            x="Utility Name",
            y="Total Disconnections",
            color="Utility Name",
            custom_data = [sorted_disconnections['Utility Name'],sorted_disconnections['Month'],sorted_disconnections['Year'],sorted_disconnections['Total Disconnections']],
            range_color=[0, sorted_disconnections["Total Disconnections"].max()],
            color_discrete_sequence=px.colors.qualitative.Antique,
            title=title,
        )
        fig.update_traces(hovertemplate="<b>%{customdata[0]}</b><br />%{customdata[1]}, %{customdata[2]}<br />Disconnections: %{customdata[3]}<extra></extra>")

    fig.update_xaxes(visible=False)

    fig.update_layout(template=draft_template)

    fig.update_layout(
        margin=dict(l=50, r=20, b=20, t=40, pad=0, autoexpand=True),
        geo=dict(
            bgcolor="rgba(173, 167, 164, 1)",
            lakecolor="rgba(173, 167, 164, 1)",
            landcolor="rgba(173, 167, 164, 1)",
            subunitcolor="rgba(173, 167, 164, 1)",
        ),
        legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="left", x=0),
    )

    return fig


def get_state_description(state="IN"):
    """
    Gets the detailed description about the selected state.
    """
    state = STATE_CODE_TO_NAME[state]
    selected_writeup = writeup[writeup["State"] == str(state)]
    writeup_data_date = selected_writeup["Date on Dashboard"].values[0]
    if str(writeup_data_date) != "nan":
        return_state = dcc.Markdown(
            str(selected_writeup["State Docket Long Narrative"].values[0])
            + " \n\n"
            + "Available Data Range: "
            + str(writeup_data_date)
        )
    else:
        return_state = dcc.Markdown(str(selected_writeup["State Docket Long Narrative"].values[0]))

    return return_state


if __name__ == "__main__":
    # To test the visualization independently.
    fig = get_map()
    fig2 = get_bar_graph()
    fig.show()
    fig2.show()
    sys.exit(1)
