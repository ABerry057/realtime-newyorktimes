import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
import dash
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objects as go
import pymongo
import pandas as pd
import datetime

from get_data import get_word_to_count_dict, get_document_keywords_list, get_articles_from_one_month

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
        ''', className='eleven columns')], className="row")


def interaction_description():
    """
    Returns description of interactive component.
    """
    return html.Div(children=[
        dcc.Markdown('''
        # Lorem ipsum
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
        Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        ''', className='eleven columns')
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
                    initial_visible_month=dt(2014, 9, 15),
                    date=str(dt(2015, 9, 15, 23, 59, 59))
                ),
                html.Div(id='output-container-date-picker-single'),
                html.Br(),
                html.H6("Possible dates: 01/01/1900 - 12/31/2018")
            
            ]),
            # dropdown for sections
            # html.Div([
            #     html.H5("Choose a section of the paper to filter by"),
            #         dcc.Dropdown(
            #             id='section-dropdown',
            #             options=[
            #                 {'label': "All Sections", 'value': 'all'},
            #                 {'label': 'World', 'value': 'world'},
            #                 {'label': 'U.S.', 'value': 'us'},
            #                 {'label': 'N.Y. / Region', 'value': 'nyregion'},
            #                 {'label': 'Business', 'value': 'business'},
            #                 {'label': 'Technology', 'value': 'technology'},
            #                 {'label': 'Science', 'value': 'science'},
            #                 {'label': 'Health', 'value': 'health'},
            #                 {'label': 'Sports', 'value': 'sports'},
            #                 {'label': 'Opinion', 'value': 'opinion'},
            #                 {'label': 'Arts', 'value': 'arts'},
            #                 {'label': 'Style', 'value': 'style'},
            #                 {'label': 'Travel', 'value': 'travel'},
            #                 {'label': 'Jobs', 'value': 'jobs'},
            #                 {'label': 'Real Estate', 'value': 'realestate'},
            #                 {'label': 'Autos', 'value': 'autos'},
            #                 {'label': 'Archive'},
            #                 {'label': 'None'}
            #             ],
            #             value='all'
            #         ),
            #         html.Div(id='dd-output-container')
            # ])
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

            1. 05/15/1912
            2. 12/08/1941
            3. 07/21/1969
            4. 08/10/1974

            What trends to you observe? Can you see reoccuring topics appear in different sections? What other historical events or patterns can you find?

        ''', className='row eleven columns'),
    ], className='row')

def about_page():
    """
    Returns markdown for about page.
    """
    return html.Div(children=[
        html.Div(html.Img(src="/assets/nyt_icon.jpg", className="md-icon"), id="image-wrapper"),
        dcc.Markdown('''
            # About
            
            The New York Times provides publicly accessible APIs with the goal of encouraging innovation through crowdsourcing. The Times would like the general community of developers to help gain insight into how the dissemination of information can be reimagined. Additionally, 
            giving the public access to their data is inline with their core journalistic values; to inform the public. The Times APIs will provide
            data illuminating the titles and abstracts of the most popular articles over time.  This data can be leveraged to analyze and ultimately 
            visualize the most popular topics in a given time period. Natural language processing will allow us to determine a topic area for an 
            article and which keywords are most frequently used. By examining word choice in popular articles over time and visualizing this 
            information via a Web App we will be able to identify trends over time and democratize this information to the public. 

            More generally, we may also be able to determine what topics were salient in a given time period. By looking at the keywords we may also be able to determine news that was highly covered and saturated the percentage of all topics in the articles. For example in 2010, 
            the Iraq war and Helmand province was highly covered. This information is particularly interesting because it can help readers understand 
            which topics are highly covered, and which ones are glanced over and therefore signal what the New York Times deems as newsworthy. 

        '''),
    ], className='row')

def additional_page():
    """
    Returns markdown for additional info page.
    """
    return html.Div(children=[
        html.Div(html.Img(src="/assets/nyt_icon.jpg", className="md-icon"), className="image-wrapper"),
        dcc.Markdown('''
            This project leverages the official NYT API (https://developer.nytimes.com/apis). The data set used is built incrementally with every 
            call to the API. As a result, the size of the data set is only limited by the maximum allowed calls to the API with our API 
            key (10 calls per minute). The data is then stored using MongoDB and transformed through NLP techniques. The output of the NLP function
            returns a nested list where each element in the larger list contained the ID number of the article and another nested list within
            the list containing the article keywords. To transform the data, the nest list was passed through a function that returns a list for each
            article in the following format : [{keyword: count}]. A list comprehension is used to sort the most frequently occurring words and is then 
            converted into a Pandas dataframe. This process is outlined in the chart below:
        '''),
        html.Div(html.Img(src="/assets/Query_Path.jpg", className="md-image"), className="image-wrapper"),
        dcc.Markdown('''
            The Pandas dataframe is then visualized via Plotly and the resulting web app is constructed in Dash 
            and interactive graph is made possible through Plotly. The resulting technology stack is the NYT API to MongoDB to Dash. This stack is displayed 
            in the chart below:
        '''),
        html.Div(html.Img(src="/assets/schem.jpg", className="md-image"), className="image-wrapper"),
        dcc.Markdown('''
        For more details on the ETL and visualization processes, please see the following notebooks:

        ETL_EDA Notebook:

        https://github.com/ABerry057/realtime-newyorktimes/blob/master/ETL_EDA.ipynb

        Visualization (with enhancement) Notebook:

        https://github.com/ABerry057/realtime-newyorktimes/blob/master/Visualization.ipynb
        ''')
    ])

def overall_layout():
    """
    Returns the navigation bar with radio buttons for each page of the site and content below.
    """
    return html.Div([
            dcc.RadioItems(options=[
                {'label': i, 'value': i} for i in ['Visualization', 'About', 'Additional Info']
            ], value='Visualization',
            id='navigation-links',
            className='radio-toolbar'),
            html.Div(id='body')
        ])

# Sequentially add page components to the app's layout
def viz_page():
    return html.Div([
        page_header(),
        html.Hr(),
        description(),
        # interaction_description(),
        interaction_tool(),
        suggestions()
    ], className='row', id="viz-content")

app.config.suppress_callback_exceptions = True
app.layout = html.Div([
    overall_layout()
])

# Defines the dependencies of interactive components
@app.callback(Output('body', 'children'), [Input('navigation-links', 'value')])
def display_children(value):
    if value == 'Visualization':
        return html.Div(viz_page(), 
                id="visualization-page",
                className="main-content"
                )
    elif value == 'About':
        return html.Div(about_page(),
                id="about-page",
                className="main-content"
                )

    else:
        return html.Div(additional_page(),
                    id="additional-info-page",
                    className="main-content"
                    )

   
@app.callback(
    Output('interaction-figure', 'figure'),
    [Input('my-date-picker-single', 'date')])
def update_figure(date):
    KW_LIMIT = 10 # key word limit
    month = date[5:7]
    if month.startswith('0'):
        month = month.replace('0','')
    month = int(month)
    year = int(date[0:4])
    day = int(date[8:10])
    raw_data = get_document_keywords_list(get_articles_from_one_month(db, year, month))
    data = get_word_to_count_dict(raw_data)
    sorted_list = sorted(data,key=lambda x:-x[1])[:KW_LIMIT]
    df = pd.DataFrame(sorted_list, columns=['Keyword', 'Count'])

    bars = go.Bar(x=df['Keyword'],
                  y=df['Count'],
                  marker = dict(
                      color = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe']
                     )
                )
    d = datetime.date(year, month, day)
    f_date = d.strftime("%B") + " " + str(d.year) #grab only month and year
    return {
        'data': [bars],
        'layout': go.Layout(title=f'New York Times Top 10 Key Words in {f_date}',
                            hovermode="closest",
                            xaxis={'title': "Key Word", 'titlefont': {'color': 'black', 'size': 14, 'family': 'Open Sans'},
                                   'tickfont': {'size': 9, 'color': 'black', 'family': 'Open Sans'},
                                   'tickangle': 30},
                            yaxis={'title': "Count", 'titlefont': {'color': 'black', 'size': 14, 'family': 'Open Sans'},
                                   'tickfont': {'color': 'black', 'family': 'Opens Sans'},
                                   'tickangle': 0})}


# @app.callback(
#     dash.dependencies.Output('dd-output-container', 'children'),
#     [dash.dependencies.Input('section-dropdown', 'value')])
# def update_output(value):
#     return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    client = pymongo.MongoClient("mongodb+srv://team:dummyPassword@cluster0-6vgfj.mongodb.net/test?retryWrites=true&w=majority")
    db = client.new_york_times
    app.run_server(debug=True, port=1050, host='0.0.0.0')
