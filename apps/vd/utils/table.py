import dash_ag_grid as dag
import pandas as pd
from dash import dcc,html,dash_table, Output, Input, State

def table_dag(df = pd.DataFrame):
    return html.Div(children=[dag.AgGrid(
                        id="table-dag-resultados",
                        rowData=df.to_dict("records"),
                        columnDefs=[{"field": i,} for i in df.columns],#"cellStyle": {'font-size': 18}
                        defaultColDef = {
                            "resizable": True,
                            "initialWidth": 130,
                            "wrapHeaderText": True,
                            "autoHeaderHeight": True,
                            "minWidth":130,
                            "sortable": True, 
                            "filter": True
                        },
                        #rowClassRules={"bg-primary fw-bold": "['TOTAL'].includes(params.data.Periodo)"},
                        className="ag-theme-alpine headers1",
                        #dashGridOptions = {"domLayout": "autoHeight"},
                        #getRowId="params.data.State",
                        columnSize="sizeToFit",
                        #style={"height": None}
                    )])
