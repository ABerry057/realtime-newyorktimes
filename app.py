import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
import dash
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objects as go

from database import fetch_all_bpa_as_df

# Definitions of constants. This projects uses extra CSS stylesheet at `./assets/style.css`
COLORS = ['rgb(25,100,126)', 'rgb(40,175,176)', 'rgb(221,222,205)', 'rgb(238,229,229)']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/custom_style.css']

# Define the dash app first
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Define component functions


def page_header():
    """
    Returns the page header as a dash `html.Div`
    """
    return html.Div(id='header', children=[
        html.Div([html.H3('Real Time New York Times')],
                 className="ten columns")
    ], className="row")


def description():
    """
    Returns overall project description in markdown
    """
    return html.Div(children=[dcc.Markdown('''
        ### The News. Visualized.
        The New York Times provides publicly-accessible APIs with the goal of encouraging innovation through crowdsourcing.
        The Times would like the general community of developers to help gain insight into how the dissemination of information can be re-imagined. 
        Additionally, giving the public access to their data is inline with their core journalistic values; to inform the public.

        The Times APIs provide data illuminating the titles and abstracts of the most popular articles over time. 
        This data can be leveraged to analyze and ultimately visualize the most popular topics in a given time period. 
        Natural language processing allows us to determine a topic area for an article and which keywords are most frequently used. 
        By examining word choice in popular articles and visualizing this information via this Web App, we are be able to identify trends and democratize this information to the public. 
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")


def static_stacked_trend_graph(stack=False):
    """
    Returns scatter line plot of all power sources and power load.
    If `stack` is `True`, the 4 power sources are stacked together to show the overall power
    production.
    """
    df = fetch_all_bpa_as_df()
    if df is None:
        return go.Figure()
    sources = ['Wind', 'Hydro', 'Fossil/Biomass', 'Nuclear']
    x = df['Datetime']
    fig = go.Figure()
    for i, s in enumerate(sources):
        fig.add_trace(go.Scatter(x=x, y=df[s], mode='lines', name=s,
                                 line={'width': 2, 'color': COLORS[i]},
                                 stackgroup='stack' if stack else None))
    fig.add_trace(go.Scatter(x=x, y=df['Load'], mode='lines', name='Load',
                             line={'width': 2, 'color': 'orange'}))
    title = 'Energy Production & Consumption under BPA Balancing Authority'
    if stack:
        title += ' [Stacked]'
    fig.update_layout(template='plotly_dark',
                      title=title,
                      plot_bgcolor='#23272c',
                      paper_bgcolor='#23272c',
                      yaxis_title='MW',
                      xaxis_title='Date/Time')
    return fig


def interaction_description():
    """
    Returns description of interactive component
    """
    return html.Div(children=[
        dcc.Markdown('''
        # Lorem ipsum
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
        Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        ''', className='eleven columns', style={'paddingLeft': '5%'})
    ], className="row")


def interaction_tool():
    """
    Returns the iteraction tool as a dash `html.Div`. The view is a 8:3 division between
    visualization and controls.
    """
    return html.Div(children=[
        html.Div(children=[dcc.Graph(id='interaction-figure')], className='nine columns'),

        html.Div(children=[
            # datePicker tool
            html.Div([
                html.H5("Choose a date to explore contemporary news"),
                dcc.DatePickerSingle(
                    id='my-date-picker-single',
                    min_date_allowed=dt(1900, 1, 1),
                    max_date_allowed=dt(2018, 12, 31),
                    initial_visible_month=dt(2010, 8, 15),
                    date=str(dt(2010, 8, 15, 23, 59, 59))
                ),
                html.Div(id='output-container-date-picker-single')
            ]),
            # dropdown for sections
            html.Div([
                html.H5("Choose a section of the paper to filter by"),
                    dcc.Dropdown(
                        id='section-dropdown',
                        options=[
                            {'label': "All Sections", 'value': 'all'},
                            {'label': 'World', 'value': 'world'},
                            {'label': 'U.S.', 'value': 'us'},
                            {'label': 'N.Y. / Region', 'value': 'nyregion'},
                            {'label': 'Business', 'value': 'business'},
                            {'label': 'Technology', 'value': 'technology'},
                            {'label': 'Science', 'value': 'science'},
                            {'label': 'Health', 'value': 'health'},
                            {'label': 'Sports', 'value': 'sports'},
                            {'label': 'Opinion', 'value': 'opinion'},
                            {'label': 'Arts', 'value': 'arts'},
                            {'label': 'Style', 'value': 'style'},
                            {'label': 'Travel', 'value': 'travel'},
                            {'label': 'Jobs', 'value': 'jobs'},
                            {'label': 'Real Estate', 'value': 'realestate'},
                            {'label': 'Autos', 'value': 'autos'}
                        ],
                        value='all'
                    ),
                    html.Div(id='dd-output-container')
            ])
        ], className='three columns', style={'marginLeft': 5, 'marginTop': '10%'}),
    ], className='row eleven columns')


def suggestions():
    """
    Returns the text for suggested searches and filters pertaining to interesting topics/trends.
    """
    return html.Div(children=[
        dcc.Markdown('''
            # Suggestions
            Start your exploration by searching by the following date and section combinations:

            1. 04/15/1912 - Filter by 'World'
            2. 12/08/1941 - Filter by 'World'
            3. 07/21/1969 - Filter by 'Science'
            4. 08/10/1974 - Filter by 'Politics'

            What trends to you observe? Can you see reoccuring topics appear in different sections? What other historical events or patterns can you find?

        ''', className='row eleven columns', style={'paddingLeft': '5%'}),
    ], className='row')


# Sequentially add page components to the app's layout
def dynamic_layout():
    return html.Div([
        page_header(),
        html.Hr(),
        description(),
        # dcc.Graph(id='trend-graph', figure=static_stacked_trend_graph(stack=False)),
        dcc.Graph(id='stacked-trend-graph', figure=static_stacked_trend_graph(stack=True)),
        interaction_description(),
        interaction_tool(),
        suggestions(),
    ], className='row', id='content')


# set layout to a function which updates upon reloading
app.layout = dynamic_layout


# Defines the dependencies of interactive components

@app.callback(
    Output('interaction-figure', 'figure'),
    [Input('my-date-picker-single', 'date')])
def update_figure(date):
    if date is not None:
        return dict(
        data=[
            dict(
                x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                   2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                y=[219, 146, 112, 800, 124, 180, 236, 207, 236, 263,
                   350, 430, 474, 526, 488, 537, 500, 439],
                name='Rest of world',
                marker=dict(
                    color='rgb(55, 83, 109)'
                )
            ),
            dict(
                x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                   2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
                   299, 340, 403, 549, 499],
                name='China',
                marker=dict(
                    color='rgb(26, 118, 255)'
                )
            )
        ],
        layout=dict(
            title='US Export of Plastic Scrap',
            showlegend=True,
            legend=dict(
                x=0,
                y=1.0
            ),
            margin=dict(l=40, r=0, t=40, b=30)
        )
    )


@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('section-dropdown', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)

# @app.callback(
#     dash.dependencies.Output('interaction-figure', 'figure'),
#     )
# def what_if_handler(wind, hydro):
#     """Changes the display graph of supply-demand"""
#     df = fetch_all_bpa_as_df(allow_cached=True)
#     x = df['Datetime']
#     supply = df['Wind'] * wind + df['Hydro'] * hydro + df['Fossil/Biomass'] + df['Nuclear']
#     load = df['Load']

#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=x, y=supply, mode='none', name='supply', line={'width': 2, 'color': 'pink'},
#                   fill='tozeroy'))
#     fig.add_trace(go.Scatter(x=x, y=load, mode='none', name='demand', line={'width': 2, 'color': 'orange'},
#                   fill='tonexty'))
#     fig.update_layout(template='plotly_dark', title='Supply/Demand after Power Scaling',
#                       plot_bgcolor='#23272c', paper_bgcolor='#23272c', yaxis_title='MW',
#                       xaxis_title='Date/Time')
#     return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=1050, host='0.0.0.0')
