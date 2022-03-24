from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from geopy import Location
from geopy.geocoders import Nominatim
from plotly.graph_objs import Figure

import koffie_frontend_challenge


def fetch_data(file_path: str = "./sample.parquet") -> pd.DataFrame:
    df = pd.read_parquet(file_path)
    return df.copy()


def format_name(name: str) -> str:
    """
    A method that simply replaces the _ character with a space and
    title-cases a column name in the dataframe for display purposes

    :param name: The string to convert to title case
    :return: A title-cased, properly spaced string.
    """
    return name.replace("_", " ").title()


def create_variable_map(
    lat: Optional[float] = None, lon: Optional[float] = None
) -> Figure:
    """
    This method dynamically creates a map. If a point is passed in via the
    lat and lon args then it will center the map on that point and zoom in.
    If nothing is passed in then the map is just a map of the USA.

    :param lat: Optional latitude parameter of the point to display on the map
    :param lon: Optional longitude parameter of the point to display on the map
    :return: A plotly.graph_objects Figure object
    """

    # By default we want a marker size of 20 and a zoom of 6
    marker = dict(size=20)
    zoom = 6

    # If we don't have a lat _or_ long then we just want to center the map on
    # the USA and zoom out.
    if not lat or not lon:
        marker["size"] = 0
        lat = 37.0902
        lon = -95.7129
        zoom = 2

    # Create the figure and set the layout
    fig = go.Figure(go.Scattermapbox(lat=[lat], lon=[lon], marker=marker))
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            zoom=zoom,
            center=dict(lat=lat, lon=lon),
        ),
        height=600,
    )
    return fig


def create_static_map(df: pd.DataFrame) -> Figure:
    """
    This method simply aggregates the data by state and displays the
    results on a Choropleth map. I'm not sure _exactly_ what the
    dataset represents so I'm just assuming that the state listed is a
    truck's state of registration.

    :param df: The dataframe of all data from `sample.parquet`
    :return: A plotly.graph_object Figure
    """

    # Aggregate the dataframe by state
    data = df.value_counts(subset=["STATE"])

    # Fetch all of the locations in the index
    locations = [x[0] for x in data.index.tolist()]

    # Create the figure and set the layout
    fig = go.Figure(
        data=go.Choropleth(
            locations=locations,
            z=data,
            locationmode="USA-states",
            colorscale="Sunset",
        )
    )
    fig.update_layout(geo_scope="usa")
    return fig


def geocode(val: str) -> Location:
    """
    There is *NO* error handling/checking on this. In a short time-frame I'm
    just crossing my fingers and hoping this works most of the time. With more
    time I would handle edge cases and not founds, but this is a rabbit hole I
    don't really want to go down right now.

    :param val: A string that _should_ be in the format of <city>, <state>.
    :return: A `geopy` Location element
    """
    geolocator = Nominatim(user_agent="test_app")
    return geolocator.geocode(val)


def create_bar_chart(df: pd.DataFrame, chart_type: str) -> Figure:
    """

    :param df: The dataframe of all data from `sample.parquet`
    :param chart_type: Can be either "MAKE" or "MODEL_YEAR". Can add more as needed.
    :return: A plotly.graph_object Figure (express calls graph_object)
    """
    if chart_type != "MAKE" and chart_type != "MODEL_YEAR":
        raise ValueError("Must be either 'MAKE' or 'MODEL_YEAR'")
    return px.bar(df[chart_type].value_counts().sort_index())


def main():
    # Initialize params, fetch data, instantiate app
    PAGE_SIZE = 20
    df = fetch_data()
    size = df.size
    clicks = 0
    columns = [{"name": format_name(i), "id": i} for i in df.columns]

    app = Dash(__name__)

    server = app.server

    """
    Since I've never worked with Plotly and Dash I wasn't sure just
    how much of the markup generation should have been abstracted 
    out so I just left it all in here.  The main structure of the 
    page is as follows:
    <body>
      <div id="main-header">
        <div>
          <h1 id="main-title"></h1>
          <h2 class="sub-title"></h2>
          <h2 class="sub-title"></h2>
        </div>
        <div id="table-search">
          <div id="text-search">
            <label for="column-input"></label>
            <input id="column-input" />
          </div>
          <div>
            <label for="column-dropdown"></label>
            <select id="column-dropdown></select>
          </div>
          <button>Submit</button>
        </div>
      </div>
      <TableComponent />        <-- This is the React component included
      <div id="map">
        <div id="map-container">
          <h3 id="map-title"></h3>
          <div id="map-figure"></div>
        </div>
      </div>
      <div id="bar-charts">
        <div class="jvp-chart">
          <h3></h3>
          <div id="year-chart"></div>
        </div>
        <div class="jvp-chart">
          <h3></h3>
          <div id="make-bar-chart"></div>
        </div>
        <div class="jvp-chart">
          <h3></h3>
          <div id="static-map-figure"></div>
        </div>
      </div>
    </body>
    """

    app.layout = html.Div(
        children=[
            html.Div(
                id="main-header",
                children=[
                    html.Div(
                        children=[
                            html.H1(
                                id="main-title",
                                children=[
                                    html.Span(
                                        "Interactive Table of ",
                                        className="main-title-element",
                                    ),
                                    html.Code(
                                        "sample.parquet", className="main-title-element"
                                    ),
                                    html.Span(
                                        " dataset.", className="main-title-element"
                                    ),
                                ],
                            ),
                            html.H2(
                                "Click on any column to sort", className="sub-title"
                            ),
                            html.H2(
                                "Click on any row to display the location in the map below the table",
                                className="sub-title",
                            ),
                        ]
                    ),
                    html.Div(
                        id="table-search",
                        children=[
                            html.Div(
                                id="text-search",
                                children=[
                                    html.Label("Search Text", htmlFor="column-input"),
                                    dcc.Input(
                                        id="column-input",
                                        type="text",
                                    ),
                                ],
                            ),
                            html.Div(
                                children=[
                                    html.Label("Columns", htmlFor="column-dropdown"),
                                    dcc.Dropdown(
                                        list(map(lambda x: x.get("name"), columns)),
                                        columns[0].get("name"),
                                        id="column-dropdown",
                                    ),
                                ]
                            ),
                            html.Button("Submit", id="submit-button", n_clicks=0),
                        ],
                    ),
                ],
            ),
            koffie_frontend_challenge.TableComponent(
                data=df.to_dict("records"),
                id="datatable",
                columns=columns,
                page_current=0,
                page_size=PAGE_SIZE,
                total_results=size,
                ascending=0,
            ),
            html.Hr(className="divider"),
            html.Div(
                id="map",
                children=[
                    html.Div(
                        id="map-container",
                        children=[
                            html.H3(id="map-title"),
                            dcc.Graph(id="map-figure", figure={}),
                        ],
                    )
                ],
            ),
            html.Div(
                id="bar-charts",
                children=[
                    html.Div(
                        className="jvp-chart",
                        children=[
                            html.H3("Vehicle Count by Model Year"),
                            dcc.Graph(
                                id="year-chart",
                                figure=create_bar_chart(df, "MODEL_YEAR"),
                            ),
                        ],
                    ),
                    html.Div(
                        className="jvp-chart",
                        children=[
                            html.H3("Vehicle Count by Make"),
                            dcc.Graph(
                                id="make-bar-chart",
                                figure=create_bar_chart(df, "MAKE"),
                            ),
                        ],
                    ),
                    html.Div(
                        className="jvp-chart",
                        children=[
                            html.H3("Map of reports per US state"),
                            dcc.Graph(
                                id="static-map-figure", figure=create_static_map(df)
                            ),
                        ],
                    ),
                ],
            ),
        ]
    )

    @app.callback(
        [Output("map-title", "children"), Output("map-figure", "figure")],
        Input("datatable", "location"),
        State("datatable", "report_number"),
    )
    def update_dash_map(location, report_number):
        """
        This is the code that just updates the map with the passed in location.
        It geocodes it and tries to update the map with the returned lat and lon

        :param location: A <city>, <state> style string
        :param report_number: The report number associated with the clicked row
        :return: Tuple[str, Figure] a string to indicate what was found and an
            updated figure to refresh the necessary location on the page.
        """
        if not location:
            return "Click the Table to Display a Location", create_variable_map()
        geocoded = geocode(location)

        # This is what constitutes "error handling" for a location not found.
        if not geocoded:
            return f"Location titled {location} was not found", create_variable_map()
        fig = create_variable_map(geocoded.latitude, geocoded.longitude)
        return f"Report Number {report_number}: {location}", fig

    @app.callback(
        [Output("datatable", "data"), Output("datatable", "page_current")],
        [
            Input("datatable", "page_current"),
            Input("datatable", "column"),
            Input("datatable", "ascending"),
            Input("submit-button", "n_clicks"),
            State("column-dropdown", "value"),
            State("column-input", "value"),
        ],
    )
    def update_table(page_current, column, ascending, n_clicks, dropdown, input_val):
        """
        This method handles all dataframe manipulation:
        - Filtering by a text value in a given column
        - Sorting a single column ascending or descending
        - Pagination

        :param page_current: The current page of the table
        :param column: The (optional) column that is being sorted
        :param ascending: (Optional) whether the sort is ascending (1), descending (-1), or none(0)
        :param n_clicks: I think this is just needed to listen to button clicks
        :param dropdown: The value of the #column-dropdown select element
        :param input_val: The value for which the user is searching in the aforementioned column
        :return: An updated dataframe and the current page
        """

        data = df.copy()
        """
        Filtering
        """
        # Check to see if the event that triggered the callback was a click on the submit button
        if clicks != n_clicks:
            if input_val is not None:
                # If we have an input value then get the ID of the selected column
                _col = [x.get("id") for x in columns if x.get("name") == dropdown]
                if _col[0]:
                    # If the column exists then do a case-insensitive str.contains on the column
                    # in the dataframe
                    data = data[data[_col[0]].str.contains(input_val, case=False)]

        """
        Sorting
        """
        if ascending == -1 and column is not None:
            data.sort_values(column, ascending=False, inplace=True)
        if ascending == 1 and column is not None:
            data.sort_values(column, inplace=True)

        """
        Pagination
        """
        # Whatever the current page, return only a PAGE_SIZE sized slice of the dataframe
        return (
            data.iloc[
                page_current * PAGE_SIZE : (page_current + 1) * PAGE_SIZE
            ].to_dict("records"),
            page_current,
        )

    app.run_server(debug=True)


if __name__ == "__main__":
    main()
