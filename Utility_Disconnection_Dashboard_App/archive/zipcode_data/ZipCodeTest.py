import sys
import pandas as pd
import plotly.express as px
import json

import os

# from mapboxgl.utils import create_color_stops, df_to_geojson
# from mapboxgl.viz import CircleViz


zipcode_data = json.load(
        open('./Zipcode_Data/ca_california_zip_codes_geo.min.json', 'r'))
    # extract zipcode for id matching

df = pd.read_csv('./Zipcode_Data/socalPrepared.csv') 


def average_price_by_zipcode_interactive(df, mapbox_style="open-street-map"): #  "stamen-toner" open-street-map
    zipcode_data = json.load(
        open('./Zipcode_Data/ca_california_zip_codes_geo.min.json', 'r'))
    # extract zipcode for id matching
    for feature in zipcode_data['features']:
        feature['id'] = feature['properties']['ZCTA5CE10']

    fig = px.choropleth_mapbox(
        data_frame=df,
        locations='zipcode',
        geojson=zipcode_data,
        color='Number of Disconnections',
        mapbox_style=mapbox_style,
        zoom=10,
        height=700,
        color_continuous_scale=['green', 'blue', 'red', 'gold'],
        title='Number of Disconnection by Zip Code for CA. Map Style: open-street-map',
        labels={'price': 'Average Price'},
        opacity=.7,
        # center={
        #     'lat': df.latitude.mode()[0],
        #     'lon': df.longitude.mode()[0]
        # }
        center = {"lat": 38.561144, "lon": -121.424042},
        )
    fig.update_geos(fitbounds='locations', visible=True)
    fig.update_layout(margin={"r": 0, "l": 0, "b": 0})
    # fig.show()
    return fig

# def get_location_interactive(df=df, zipcode_data=zipcode_data, mapbox_style="open-street-map"):
#     fig = px.scatter_mapbox(
#         df,
#         lat="lat",
#         lon="lon",
#         # color='Number of Disconnections',
#         hover_data=["zipcode", "Number of Disconnections"],
#         # color_continuous_scale=["green", 'blue', 'red', 'gold'],
#         # zoom=11.5,
#         # # range_color=[0, df['price'].quantile(0.95)], # to negate outliers
#         # height=700,
#         # title='Number of Disconnections interactive map. Map Style: open-street-map',
#         # opacity=.5,
#         color_discrete_sequence=["fuchsia"], zoom=3, height=300,
#         # center={
#         #     'lat': ,
#         #     'lon': df.longitude.mode()[0]
#         # })
#         # center = {"lat": 38.561144, "lon": -121.424042}
#     )
#     # print("Extracting features")
#     # for feature in zipcode_data['features']:
#     #     feature['id'] = feature['properties']['ZCTA5CE10']
#     # print("Extraced features")
#     # fig = px.choropleth_mapbox(
#     #     df, 
#     #     geojson = zipcode_data, 
#     #     color = "Number of Disconnections",
#     #     locations = 'zipcode', 
#     #     # featureidkey = "properties.name",
#     #     color_continuous_scale = 'Reds',
#     #     zoom = 3.5, 
#     #     center = {"lat": 38.561144, "lon": -121.424042},
#     #     mapbox_style = "open-street-map",
#     #     # opacity = 0.65
#     # )
#     fig.update_layout(mapbox_style=mapbox_style)
#     fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#     return fig

def get_location_interactive(df=df, zipcode_data=zipcode_data, mapbox_style=''):
    token = "pk.eyJ1IjoiaHNqb3NoaSIsImEiOiJjbDYxZW91MWgwNGJsM2NwZnF2c3RpeDZlIn0.5NVRGYm1ORxHMhgGWQqzjw"
    us_cities = df
    fig = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="zipcode", hover_data=["zipcode", "Number of Disconnections"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
    fig.update_layout(mapbox_style="mapbox://styles/hsjoshi/cl6r0gq7b001814rstvpghyfr", mapbox_accesstoken=token)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


if __name__ == "__main__":
    
    df = pd.read_csv('./Zipcode_Data/sample.csv')
    fig = average_price_by_zipcode_interactive(df)
    # fig = get_location_interactive(df)
    # fig  = mapboxTest()
    fig.show()
    sys.exit(1)