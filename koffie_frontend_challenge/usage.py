from typing import Literal, Optional, Tuple

from dash import Dash, html, dash_table, dcc
from dash.dependencies import Input, Output, State
from geopy.geocoders import Nominatim
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objs import Figure

import koffie_frontend_challenge


app = Dash(__name__)


def fetch_data() -> pd.DataFrame:
    df = pd.read_parquet("./sample.parquet")
    # df.MODEL_YEAR = df.MODEL_YEAR.astype("int")
    return df.copy()


def format_name(i: str) -> str:
    return i.replace("_", " ").title()


def create_map(lat: Optional[float] = None, lon: Optional[float] = None) -> Figure:
    marker = dict(size=20)
    zoom = 6
    if not lat or not lon:
        marker["size"] = 0
        lat = 37.0902
        lon = -95.7129
        zoom = 2
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


def geocode(val: str) -> str:
    geolocator = Nominatim(user_agent="test_app")
    return geolocator.geocode(val)

def create_pie_chart(
    df: pd.DataFrame, chart_type: Literal["MAKE", "MODEL_YEAR", "MAKE_AND_MODEL"]
) -> Figure:
    return px.pie(df, names=chart_type)


def create_bar_chart(
    df: pd.DataFrame, chart_type: Literal["MAKE", "MODEL_YEAR", "MAKE_AND_MODEL"]
) -> Figure:
    return px.bar(df[chart_type].value_counts().sort_index())



def main():
    PAGE_SIZE = 20
    df = fetch_data()
    size = df.size
    clicks = 0
    columns = [{"name": format_name(i), "id": i} for i in df.columns]
    # df["MAKE_AND_MODEL"] = df["MAKE"] + df["MODEL"]
    # create_bubble_chart(df)
    # print(df.head())
    # df1 = px.data.tips()
    # print(df1.head())
    app = Dash(__name__)
    app.layout = html.Div(
        children=[
            # html.Div(
            #     dash_table.DataTable(
            #         data=df.to_dict("records"),
            #         id="datatable-paging",
            #         columns=[{"name": format_name(i), "id": i} for i in df.columns],
            #         page_current=0,
            #         page_size=PAGE_SIZE,
            #         page_action="custom",
            #     ),
            # ),
            html.Div(id='main-header', children=[
                html.Div(children=[
                    html.H1("blah blah", id="main-title"),
                    html.H2("Click on any column to sort", id="sub-title")
                ]),
                html.Div(
                    id="table-search",
                    children=[
                        html.Div(
                            id='text-search',
                            children=[
                                html.Label("Search Text"),
                                dcc.Input(
                                    id="column-input",
                                    type="text",
                                ),
                            ]
                        ),
                        html.Div(
                            children=[
                                html.Label("Columns"),
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
            ]),

            koffie_frontend_challenge.TableComponent(
                label="my-label",
                data=df.to_dict("records"),
                id="datatable",
                columns=columns,
                page_current=0,
                page_size=PAGE_SIZE,
                total_results=size,
                ascending=0,
            ),
            html.Hr(className='divider'),
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
            html.Div(children=[
                html.H3("Vehicle Count by Model Year"),
                dcc.Graph(id="year-chart", figure=create_bar_chart(df, "MODEL_YEAR")),
            ]),
            html.Div(children=[
                html.H3("Vehicle Count by Make"),
                dcc.Graph(id="make-bar-chart", figure=create_bar_chart(df, "MAKE")),

            ]),
            dcc.Graph(id="make-chart", figure=create_pie_chart(df, "MAKE")),
            # dcc.Graph(
            #     id="make-and-model-bar-chart",
            #     figure=create_bar_chart(df, "MAKE_AND_MODEL"),
            # ),
            # dcc.Graph(id="heatmap", figure=create_bubble_chart(df)),
            # dcc.Graph(id="make-chart", figure=create_pie_chart(df)),
        ]
    )
    #
    # @app.callback(
    #     Output("datatable", "data"),
    #     Input("datatable", "page_current"),
    #     Input("datatable", "page_size"),
    # )
    # def update_table(page_current, page_size):
    #     return df.iloc[
    #         page_current * page_size : (page_current + 1) * page_size
    #     ].to_dict("records")

    @app.callback(
        [Output("map-title", "children"), Output("map-figure", "figure")],
        Input("datatable", "location"),
        State("datatable", "report_number"),
    )
    def update_dash_map(location, report_number):
        if not location:
            return "Click the Table to Display a Location", create_map()
        data = geocode(location)
        if not data:
            return f"Location titled {location} was not found", create_map()
        fig = create_map(data.latitude, data.longitude)
        return f"Report Number {report_number}: {location}", fig

    @app.callback(
        [Output("datatable", "data"), Output("datatable", "page_current")],
        [
            Input("datatable", "page_current"),
            Input("datatable", "column"),
            Input("datatable", "ascending"),
            Input('submit-button', 'n_clicks'),
            State('column-dropdown', 'value'),
            State('column-input', 'value')
        ],
    )
    def update_table(page_current, column, ascending, n_clicks, dropdown, input_val):
        data = df.copy()
        if clicks != n_clicks:
            if input_val is not None:
                _col = [x.get('id') for x in columns if x.get('name') == dropdown]
                if _col[0]:
                    data = data[data[_col[0]].str.contains(input_val, case=False)]
        if ascending == -1 and column is not None:
            data.sort_values(column, ascending=False, inplace=True)
        if ascending == 1 and column is not None:
            data.sort_values(column, inplace=True)
        return (
            data.iloc[
                page_current * PAGE_SIZE : (page_current + 1) * PAGE_SIZE
            ].to_dict("records"),
            page_current,
        )

    app.run_server(debug=True)


if __name__ == "__main__":
    # df = px.data.tips()
    # x = test()
    main()
    # df = fetch_data()

    # el = df.iloc[26]
    # blah = el["CITY"] + "," + el["STATE"]
    # x = geocode(blah)
    # lat = x.latitude
    # lon = x.longitude
    # fig = go.Figure(go.Scattermapbox(lat=[lat], lon=[lon], marker={"size": 20}))
    # fig.update_layout(
    #     mapbox=dict(
    #         style="open-street-map",
    #         zoom=6,
    #         center=dict(lat=lat, lon=lon),
    #     ),
    #     height=600,
    #     width=600,
    # )
    # fig.show()
