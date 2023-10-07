import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=['/static/dash-styles.css', dbc.themes.LUX])

# Read the data from the CSV file
df = pd.read_csv('Meteorite_Landings.csv')
print(df['mass (g)'].describe())
df = df.loc[df['year'] < 2023]

# fig = px.histogram(df, x='mass (g)', nbins=30)
# fig.update_xaxes(type='log')  # Set the x-axis scale to logarithmic

# Define the layout of the app
app.layout = html.Div([
    # Create a Dash DataTable to display the data
    html.Div([
        html.H2('Meteorite data', className='header'),
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
        html.H2('Histogram', className='header'),
        dcc.Dropdown(
            id='histogram-dropdown',
            options=[{'label': col, 'value': col} for col in ['mass (g)', 'year']],
            value='mass (g)',
            multi=False,
            style={'width': '10vw'}
        ),
        dcc.Graph(id='histogram-chart')
    ]),
    # html.Div([
    #     dcc.Graph(figure=px.bar(df.groupby(['year'])['year'].count()))
    # ]),

    # Bar plots
    html.Div([
        html.H2('Barplot', className='header'),
        dcc.Dropdown(
            id='barplot-dropdown',
            options=[{'label': col, 'value': col} for col in
                     ['nametype', 'recclass', 'fall', 'year', 'reclat', 'reclong']],
            value='year',  # Default column selection
            multi=False,  # Allow single column selection
            style={'width': '10vw'}
        ),
        # dcc.Graph(figure=px.histogram(df, x='mass (g)', nbins=20)),
        dcc.Graph(id='bar-chart')
    ])
],
    className="content")

# Callback to update the bar chart based on the selected column

import plotly.graph_objects as go
import numpy as np


@app.callback(
    Output('histogram-chart', 'figure'),
    Input('histogram-dropdown', 'value')
)
def update_histogram_chart(selected_column):
    if selected_column == 'mass (g)':
        # Define the logarithmically spaced bins
        num_bins = 30  # Adjust as needed
        custom_bin_edges = np.logspace(0, np.log10(60000001), num_bins + 1)

        # Calculate the histogram using NumPy
        hist, bins = np.histogram(df[selected_column].dropna(), bins=custom_bin_edges)

        # Create a histogram trace
        fig = go.Figure(go.Bar(x=bins, y=hist, width=[bins[i + 1] / 2 - bins[i] / 2 for i in range(len(bins) - 1)]))

        # Update the x-axis to use a logarithmic scale
        fig.update_xaxes(type='log')

        # Update the layout as needed
        fig.update_layout(
            xaxis_title=selected_column,
            yaxis_title='Frequency',
        )
    # TODO sprobowac zrobic tez taka log scale dla 'year', ale odwrocona (wiekszosc danych jest blisko 2000r)
    else:
        # For other columns, use default binning
        fig = px.histogram(df, x=selected_column, nbins=15)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
