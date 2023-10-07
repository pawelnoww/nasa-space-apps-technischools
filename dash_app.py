import dash
from dash import dcc, html, dash_table
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px

# Initialize the Dash app
app = dash.Dash(__name__)

# Read the data from the CSV file
df = pd.read_csv('Meteorite_Landings.csv')
df = df.loc[df['year'] < 2023]

# fig = px.histogram(df, x='mass (g)', nbins=30)
# fig.update_xaxes(type='log')  # Set the x-axis scale to logarithmic

# Define the layout of the app
app.layout = html.Div([
    html.H1('Meteorite Landings'),

    # Create a Dash DataTable to display the data
    html.Div([
        html.H2('Meteorite data'),
        dash_table.DataTable(
            id='table',
            columns=[
                {"name": col, "id": col} for col in df.columns
            ],
            data=df.to_dict('records'),
            page_size=10,
            sort_action='native',
            filter_action='native'
        ),
    ]),

    # Histograms
    html.Div([
        html.H2('Histogram'),
        dcc.Dropdown(
            id='histogram-dropdown',
            options=[{'label': col, 'value': col} for col in ['mass (g)', 'year']],
            value='mass (g)',
            multi=False
        ),
        dcc.Graph(id='histogram-chart')
    ]),
    # html.Div([
    #     dcc.Graph(figure=px.bar(df.groupby(['year'])['year'].count()))
    # ]),


    # Bar plots
    html.Div([
        html.H2('Barplot'),
        dcc.Dropdown(
            id='barplot-dropdown',
            options=[{'label': col, 'value': col} for col in ['nametype', 'recclass', 'fall', 'year', 'reclat', 'reclong']],
            value='year',  # Default column selection
            multi=False  # Allow single column selection
        ),
        # dcc.Graph(figure=px.histogram(df, x='mass (g)', nbins=20)),
        dcc.Graph(id='bar-chart')
    ])
])


# Callback to update the bar chart based on the selected column
@app.callback(
    Output('bar-chart', 'figure'),
    Input('barplot-dropdown', 'value')
)
def update_bar_chart(selected_column):
    # Group the data by the selected column and count the number of occurrences
    data = df.groupby([selected_column])[selected_column].count().reset_index(name='count')
    # Create a bar chart
    fig = px.bar(data, x=selected_column, y='count')
    return fig


@app.callback(
    Output('histogram-chart', 'figure'),
    Input('histogram-dropdown', 'value')
)
def update_histogram_chart(selected_column):
    fig = px.histogram(df, x=selected_column, nbins=15)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
