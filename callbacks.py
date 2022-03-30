import os, sys
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


from app import app

# path[0] leest het bestand in de huidige map. (path[1] leest de python locatie op het os
df1 = pd.read_csv(os.path.join(sys.path[0], 'assets\\Life expectancy.csv'))
df2 = pd.read_csv(os.path.join(sys.path[0], 'assets\\iso.csv'))
years = df1['Year'].unique()
countries = df1['Entity'].unique()
iso = df2['ISO']
combined = pd.merge(df1, df2)

@app.callback(
    [
    Output('barchart-1', 'figure'),
    Output('year-1', 'children')
    ],
    Input('year-slider', 'value'),
    Input('dropdown-country', 'value')
    )
def update_visual(slctd_year, slctd_cntry):
    life = df1[df1['Year'] == slctd_year]
    country = df1[df1['Entity'] == slctd_cntry]

    fig1 = px.bar(
        life,
        x=life['Entity'],
        y=life['Life expectancy'],
        # template='simple white'
    )

    fig1.update_traces(
            # lambda trace: trace == country marker_color='#9D3469' else marker_color='rgb(33, 60, 99)
            marker_color='rgb(33, 60, 99)',
    )   

    fig1.update_layout(
            height= 720,
            width= 1080,
            margin=dict(l=20, r=30, t=50, b=30),
            plot_bgcolor='rgb(0,0,0,0)',
            legend_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgb(0,0,0,0)',
            font_color='#909090'
        )
        
    fig1["data"][0]["marker"]["color"] = ["#9D3469" if c == slctd_cntry else "#213C63" for c in fig1["data"][0]["x"]]
    
    # fig1.for_each_trace(
    #     lambda trace: trace.update(marker_color='#9D3469') if trace == country else (),
    # )

    return fig1, 'Year: {0}'.format(slctd_year)


@app.callback(
    [
    Output('map-1', 'figure')
    ],
    Input('country', 'value'),
    Input('dropdown-country', 'value')
)
def update_map(chsn_cntry):
    country = df1[df1['Entity'] == chsn_cntry]
    mapdata = pd.merge(country, iso)
    combined = pd.merge(df1, df2)
    df3 = px.data.gapminder().query('year==2007')

    mapchart = px.choropleth(combined, locations='Entity',
                color='Life expectancy', # lifeExp is a column of gapminder
                hover_name='country', # column to add to hover information
                # projection = 'orthographic',
                color_continuous_scale=px.colors.sequential.Greys
                )
    dfmap = px.data.gapminder(). query('year==2007')

    mapchart = px.choropleth(dfmap, locations='iso_alpha',
                color='lifeExp', # lifeExp is a column of gapminder
                hover_name='country', # column to add to hover information
                color_continuous_scale=px.colors.sequential.Greys)

    

    return mapchart

@app.callback(
    [
    Output('gauge-1', 'figure')
    ],
    Input('dropdown-country1', 'value'),
    
)
def update_life(slctd_cntry):
 
    country = df1[df1['Entity'] == slctd_cntry]
    
    gauge1 = [go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = 320,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Speed", 'font': {'size': 24}},
        delta = {'reference': 400}, # , 'increasing': {'color': "RebeccaPurple"}},
        gauge = {
            'axis': {'range': [None, 500], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 250], 'color': 'lightgray'},
                {'range': [250, 400], 'color': 'darkgray'},
                {'range': [400, 500], 'color': 'gray'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 490
            }
        }
    ))]

    return gauge1
    # gauge1.update_layout(paper_bgcolor = "white", font = {'color': "darkblue", 'family': "Arial"})    
    
