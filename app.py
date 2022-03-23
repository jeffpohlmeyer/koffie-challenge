# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from typing import Literal

from dash import Dash, html, dash_table, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure


def fetch_data() -> pd.DataFrame:
    df = pd.read_parquet("./sample.parquet")
    df.MODEL_YEAR = df.MODEL_YEAR.astype("int")
    return df


def format_name(i: str) -> str:
    return i.replace("_", " ").title()


def create_pie_chart(
    df: pd.DataFrame, chart_type: Literal["MAKE", "MODEL_YEAR"]
) -> Figure:
    return px.pie(df, names=chart_type)


def create_bar_chart(
    df: pd.DataFrame, chart_type: Literal["MAKE", "MODEL_YEAR"]
) -> Figure:
    return px.bar(df[chart_type].value_counts().sort_index())


# def create_bubble_chart(df: pd.DataFrame) -> pd.DataFrame:
#     df1 = df.copy()
#     df1 = df1.groupby(["MAKE", "MODEL_YEAR"]).size().reset_index(name="count")
#     return px.density_heatmap(
#         df1, x="MAKE", y="MODEL_YEAR"
#     )
#     makes = list(df1.MAKE.unique())
#     makes.sort()
#     years = list(df1.MODEL_YEAR.unique())
#     years.sort()
#
#     df_new = pd.DataFrame(columns=makes, index=years)
#     for make in makes:
#         df_make = df1[df1.MAKE == make]
#         df_make.set_index("MODEL_YEAR", inplace=True)
#         df_new[make] = df_make["count"]
#     df_new.fillna(0, inplace=True)
#     return px.density_heatmap(
#         df_new,
#     )


def main():
    PAGE_SIZE = 20
    df = fetch_data()
    # create_bubble_chart(df)
    # print(df.head())
    # df1 = px.data.tips()
    # print(df1.head())
    app = Dash(__name__)
    app.layout = html.Div(
        children=[
            dash_table.DataTable(
                data=df.to_dict("records"),
                id="datatable-paging",
                columns=[{"name": format_name(i), "id": i} for i in df.columns],
                page_current=0,
                page_size=PAGE_SIZE,
                page_action="custom",
            ),
            dcc.Graph(id="make-chart", figure=create_pie_chart(df, "MAKE")),
            dcc.Graph(id="year-chart", figure=create_bar_chart(df, "MODEL_YEAR")),
            dcc.Graph(id="make-bar-chart", figure=create_bar_chart(df, "MAKE")),
            # dcc.Graph(id='heatmap', figure=create_bubble_chart(df))
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

    app.run_server(debug=True)


def test():
    df = fetch_data()
    return create_bubble_chart(df)


if __name__ == "__main__":
    # df = px.data.tips()
    # x = test()
    main()
