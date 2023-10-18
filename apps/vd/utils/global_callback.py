from dash import Input, Output,State,no_update,dcc,html
import plotly.graph_objs as go

def callback_opened_modal(
    app,
    modal_id ='',
    children_out_id = '', 
    id_button = '', 
    height_modal = 500, 
    type_children = 'Figure'
): 
    @app.callback(
        Output(modal_id, "opened"),
        Output(modal_id, "children"),
        Input(id_button, "n_clicks"),
        State(children_out_id,'figure'),
        State(modal_id, "opened"),
        prevent_initial_call=True,
    )
    #if type_children == 'Figure':
    def toggle_modal(n_clicks,figure, opened):
        
            fig=go.Figure(figure)
            fig.update_layout(height = height_modal)
        
            if n_clicks:
                return True,dcc.Graph(figure=fig)
            else:
                return not opened