# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
print(max_payload)
site = spacex_df['Launch Site'].unique()
sites = np.append(site,'All sites')

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options=sites,
                                            value='All sites',
                                            placeholder='Select a launch site',
                                            searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min =0,
                                                max =10000 ,
                                                step = 1000,
                                                # marks={0: '0',10000: '10000'},
                                                value= [min_payload,max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(site_i):
    filtered_df = spacex_df
    # print(site_i)
    if site_i == 'All sites':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Success Launch by Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==site_i]
        df_s = filtered_df['class'].value_counts().reset_index()
        df_s.columns = ['value', 'count']
        fig = px.pie(df_s, values='count', 
        names='value', 
        title=f'Total Success Launch for {site_i}')
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),Input('payload-slider', 'value')]
)
def get_scatter_chart(site_i,payload_i):
    print(payload_i)
    # df_f2 = spacex_df
    df_f2 = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_i[0],payload_i[1])]
    if site_i == 'All sites':
        fig = px.scatter(df_f2, x="Payload Mass (kg)",
                     y="class",
                     color="Booster Version Category",
                     title='Correlation between success and payload for all sites')
        return fig
    else:
        df_f2 = spacex_df[spacex_df['Launch Site']==site_i]
        df_f2 = df_f2[df_f2['Payload Mass (kg)'].between(payload_i[0],payload_i[1])]
        fig = px.scatter(df_f2, x="Payload Mass (kg)",
                     y="class",
                     color="Booster Version Category",
                     title=f'Correlation between success and payload for{site_i}')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server(port=8051)
