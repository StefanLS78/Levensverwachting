from dash import Dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Output, Input
from dash_extensions import BeforeAfter
import plotly.express as px
import plotly.graph_objects as go

from app import app
# import callbacks


########################################
# Add Data
########################################

# df = pd.read_csv('C:\\Users\\StefanSijbesmaDAAT\\Documents\\Scripting\\Test\\assets\\Life expectancy.csv')
# years = df['Year'].unique()
# country=df['Entity'].unique()

df1 = pd.read_csv(
    'C:\\Users\\StefanSijbesmaDAAT\\Documents\\Scripting\\Levensverwachting\\assets\\Life expectancy.csv')
df2 = pd.read_csv(
    'C:\\Users\\StefanSijbesmaDAAT\\Documents\\Scripting\\Levensverwachting\\assets\\iso.csv')
years = df1['Year'].unique()
country = df1['Entity'].unique()
iso = df2['ISO']
# combined = pd.merge(df1, df2)

# country = df1[df1['Entity'] == chsn_cntry]
# mapdata = pd.merge(country, iso)
#  combined = pd.merge(df1, df2)
df3 = px.data.gapminder().query('year==2007')

mapchart = px.choropleth(df3,
                         locations='iso_alpha',
                         color='lifeExp',  # lifeExp is a column of gapminder
                         hover_name='country',  # column to add to hover information
                         # colorscale = 'Blues',
                         # autocolorscale=False,
                         # color_continuous_scale=px.colors.sequential.Greys
                         )
mapchart.update_layout(
    title_text='Life expectancy in the world',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular',
    ),
)
########################################
# Create Auxiliary Components Here
########################################


def navbar():
    return html.Nav([  # navbar on top of the dashboard using html components
        html.Div([
            html.Div(
                html.H6('Levensverwachting'),
                className='h6-nav',
                style={
                    'text-align': 'left',
                    'margin-left': '30px',
                    'margin-top': '10px',
                }
            ),
            html.Div(
                html.P('Een schets van de levensverwachting door de jaren heen'),
                style={
                    'text-align': 'left',
                    'margin-left': '30px',
                    'margin-top': '10px',
                }
            ),
        ], className='navbar six columns'),

        html.Div([
            dcc.Link(
                html.H6('Overview'),
                href='/overview',
                style={
                    'display': 'inline-block',
                    'margin-right': '30px',
                    'margin-top': '20px',
                }
            ),
            dcc.Link(
                html.H6('Comparison'),
                href='/comparison',
                style={
                    'display': 'inline-block',
                    'margin-right': '30px',
                    'margin-top': '20px',
                }
            ),
            dcc.Link(
                html.H6('Analysis'),
                href='/analysis',
                style={
                    'display': 'inline-block',
                    'margin-right': '30px',
                    'margin-top': '20px',
                }
            ),

        ], className='navbar six columns')
    ], className='navbar h6-nav')


########################################
# Create Page Layouts Here
########################################
# Layout Overview
layout_overview = html.Div([
    html.Div([
        html.Div([  # left column to show selection on map
            dcc.Dropdown(
                id='dropdown-country',
                options=[{'label': c, 'value': c} for c in country],
                value='Australia'
            ),
            dcc.Graph(
                id='Map-1',
            ),
        ], className='four columns body'),

        html.Div([  # main pane on the right barchart and slider
                    dcc.Graph(
                        id='barchart-1',
                    ),
            html.H4(
                id='year-1',
                style={
                    'text-align': 'center',
                    'color': '#213C63'
                }
            ),
            dcc.Slider(
                id='year-slider',
                min=years.min(),
                max=years.max(),
                marks={
                    1800: {'label': '1800', 'style': {'color': '#213C63'}},
                    1850: {'label': '1850', 'style': {'color': '#213C63'}},
                    1900: {'label': '1900', 'style': {'color': '#213C63'}},
                    1950: {'label': '1950', 'style': {'color': '#213C63'}},
                    2000: {'label': '2000', 'style': {'color': '#213C63'}},
                    2016: {'label': '2016', 'style': {'color': '#213C63'}},
                },
                # vertical=False,
                value=years.min() + 2,
                tooltip={"placement": "bottom",
                            "always_visible": False},

            ),
        ], className='eight columns body'),
    ])
], className='bg-color')


# Layout Comparison
layout_comparison = html.Div([
    html.Div([
        html.H4(('Levensverwachting'),
                style={
            'text-align': 'left',
            'margin-left': '30px',
            'margin-top': '10px',
        }
        ),
        html.P('vergelijking tussen 2 landen',
               style={
                   'text-align': 'left',
                   'margin-left': '30px',
                   'margin-top': '10px',
               }
               ),

    ], className='h4'),
    html.Div([
        dcc.Dropdown(
            id='dropdown-country1',
            options=[{'label': c, 'value': c} for c in country],
            value='Australia'
        ),
        dcc.Graph(
            id='gauge-1',
        ),
    ], className='four columns body')
])

# Layout Analysis
layout_analysis = html.Div('analysis'

                           )
