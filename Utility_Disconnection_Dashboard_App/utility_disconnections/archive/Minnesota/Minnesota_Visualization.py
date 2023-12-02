import geopandas as gpd
import plotly.express as px
import app_config as cfg


# This function creates visualization for Minnesota
def create_minnesota_disconenction_map():
    # Read the data
    df = gpd.read_file(cfg._MINNESOTA_DATA)

    # Create the visualization
    fig = px.choropleth(
        df,
        locations="State",
        color="Utility Name",
        color_continuous_scale="inferno",
        locationmode="USA-states",
        scope="usa",
        range_color=(0, 10),
        height=800,
        width="auto",
        labels={
            "Residential Customers": "%# Residential Customers",
            "Total Past Due": "%# Past Due Residential Customers",
        },
    )

    # Set the title of the visualization
    fig.update_layout(title_text="Minnesota State Disconnections", title_x=0.5)
    return fig
