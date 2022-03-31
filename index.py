import sys
print(sys.executable)




from dash import dcc
from dash import html
from dash import Output, Input

from app import app
from layouts import navbar
from layouts import layout_overview, layout_comparison, layout_analysis
import callbacks

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
            dcc.Location(id='url', refresh=False),
            navbar(),
            html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    """_summary_

    Args:
        pathname (_type_): _description_

    Returns:
        _type_: _description_
    """    
    
    if pathname == '/':
        return layout_overview
    elif pathname == '/overview':
        return layout_overview
    elif pathname == '/comparison':
        return layout_comparison
    elif pathname == '/analysis':
        return layout_analysis
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(port='5000', host='127.0.0.1', debug=True)
    
