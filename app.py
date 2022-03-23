# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import random
from typing import Literal, Optional

from dash import Dash, html, dash_table, dcc
from dash.dependencies import Input, Output, State
from geopy.geocoders import Nominatim
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objs import Figure

import koffie_frontend_challenge


def fetch_data() -> pd.DataFrame:
    df = pd.read_parquet("./sample.parquet")
    # df.MODEL_YEAR = df.MODEL_YEAR.astype("int")
    return df.copy()


def format_name(i: str) -> str:
    return i.replace("_", " ").title()


def get_count(
    df: pd.DataFrame, chart_type: Literal["MAKE", "MODEL_YEAR", "MAKE_AND_MODEL"]
) -> pd.DataFrame:
    df1 = df.copy()
    return df1[chart_type].value_counts()


def create_pie_chart(
    df: pd.DataFrame, chart_type: Literal["MAKE", "MODEL_YEAR", "MAKE_AND_MODEL"]
) -> Figure:
    return px.pie(df, names=chart_type)


def create_bar_chart(
    df: pd.DataFrame, chart_type: Literal["MAKE", "MODEL_YEAR", "MAKE_AND_MODEL"]
) -> Figure:
    return px.bar(df[chart_type].value_counts().sort_index())


def create_bubble_chart(df: pd.DataFrame) -> pd.DataFrame:
    df1 = df.copy()
    df1 = df1.groupby(["MAKE", "MODEL_YEAR"])
    return df1
    # return px.scatter(df1, x="MODEL_YEAR", y="MAKE", size="INCIDENTS")
    # makes = list(df1.MAKE.unique())
    # makes.sort()
    # years = list(df1.MODEL_YEAR.unique())
    # years.sort()
    #
    # df_new = pd.DataFrame(columns=makes, index=years)
    # for make in makes:
    #     df_make = df1[df1.MAKE == make]
    #     df_make.set_index("MODEL_YEAR", inplace=True)
    #     df_new[make] = df_make["count"]
    # df_new.fillna(0, inplace=True)
    # return px.density_heatmap(
    #     df_new,
    # )


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
        width=600,
    )
    return fig


def main():
    PAGE_SIZE = 20
    df = fetch_data()
    df["MAKE_AND_MODEL"] = df["MAKE"] + df["MODEL"]
    df = df.iloc[:40]
    # create_bubble_chart(df)
    # print(df.head())
    # df1 = px.data.tips()
    # print(df1.head())
    app = Dash(__name__)
    app.layout = html.Div(
        children=[
            html.Div(
                dash_table.DataTable(
                    data=df.to_dict("records"),
                    id="datatable-paging",
                    columns=[{"name": format_name(i), "id": i} for i in df.columns],
                    page_current=0,
                    page_size=PAGE_SIZE,
                    page_action="custom",
                ),
            ),
            koffie_frontend_challenge.TableComponent(
                id="input", value="my-value", label="my-label"
            ),
            html.Div(id="output"),
            # html.H3(id="tbl-out"),
            # dcc.Graph(id="map", figure={}),
            # dcc.Graph(id="make-chart", figure=create_pie_chart(df, "MAKE")),
            # dcc.Graph(id="year-chart", figure=create_bar_chart(df, "MODEL_YEAR")),
            # dcc.Graph(id="make-bar-chart", figure=create_bar_chart(df, "MAKE")),
            # dcc.Graph(
            #     id="make-and-model-bar-chart",
            #     figure=create_bar_chart(df, "MAKE_AND_MODEL"),
            # ),
            # dcc.Graph(id="heatmap", figure=create_bubble_chart(df)),
            # dcc.Graph(id="make-chart", figure=create_pie_chart(df)),
        ]
    )

    @app.callback(
        Output("datatable-paging", "data"),
        Input("datatable-paging", "page_current"),
        Input("datatable-paging", "page_size"),
    )
    def update_table(page_current, page_size):
        return df.iloc[
            page_current * page_size : (page_current + 1) * page_size
        ].to_dict("records")

    @app.callback(
        [Output("tbl-out", "children"), Output("map", "figure")],
        Input("datatable-paging", "active_cell"),
        State("datatable-paging", "page_current"),
    )
    def blah(cell, page_current):
        if not cell:
            return "Click the Table", create_map()
        row = cell.get("row") + (PAGE_SIZE * page_current)
        el = df.iloc[row]
        data = geocode(el["CITY"] + "," + el["STATE"])
        fig = create_map(data.latitude, data.longitude)
        return str(el.CITY), fig

    app.run_server(debug=True)


def test():
    df = fetch_data()
    return create_bubble_chart(df)


def geocode(val: str) -> str:
    geolocator = Nominatim(user_agent="test_app")
    return geolocator.geocode(val)


def geocode_df(df: pd.DataFrame) -> pd.DataFrame:
    df["DATA"] = df.apply(lambda x: geocode(x["CITY"] + "," + x["STATE"]))


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
