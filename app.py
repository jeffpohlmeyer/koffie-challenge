# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

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


def create_pie_chart(df: pd.DataFrame) -> Figure:
    fig = px.pie(df, names="MAKE")
    return fig


def main():
    PAGE_SIZE = 20
    df = fetch_data()
    print(df.head())
    df1 = px.data.tips()
    print(df1.head())
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
            dcc.Graph(id="pie-chart", figure=create_pie_chart(df)),
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


if __name__ == "__main__":
    main()
