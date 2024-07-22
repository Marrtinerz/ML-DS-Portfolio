# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv('spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_sites = spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options=[
                    {'label': 'All Sites', 'value': 'ALL'},
                    {'label': launch_sites[0], 'value': launch_sites[0]},
                    {'label': launch_sites[1], 'value': launch_sites[1]},
                    {'label': launch_sites[2], 'value': launch_sites[2]},
                    {'label': launch_sites[3], 'value': launch_sites[3]}
                ],
                value='ALL',
                placeholder="Select a Launch Site here",
                searchable=True
                ),
                                html.Br(),

                                # Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                min=0, max=10000, step=1000,
                marks={0: '0',
                       2000: '2000',
                       4000: '4000',
                       6000: '6000',
                       8000: '8000',
                       10000: '10000'},
                value=[min_payload, max_payload]),

                                # Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])



# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]

    if entered_site == 'ALL':
        #all_site_data = spacex_df.groupby(by='Launch Site')['class'].mean().reset_index()
        fig = px.pie(spacex_df, values='class',
        names='Launch Site',
        title='Total Success Launches By Site')
        return fig
    else:
        site_data = filtered_df['class'].value_counts().reset_index()
        fig = px.pie(site_data, values='count',
        names='class',
        title = 'Launch Outcomes for Site {}'.format(entered_site))
        return fig
# 
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
             [Input(component_id='site-dropdown', component_property='value'),
             Input(component_id='payload-slider', component_property='value')]
)

def update_scatterplot(entered_site, payload_range):
    low, high = payload_range

    if entered_site == 'ALL':
        mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
        fig = px.scatter(spacex_df[mask], x='Payload Mass (kg)', y='class',
        color='Booster Version', title='Correlation Between Payload and Success for All Sites')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        mask = (filtered_df['Payload Mass (kg)'] > low) & (filtered_df['Payload Mass (kg)'] < high)
        fig = px.scatter(filtered_df[mask], x='Payload Mass (kg)', y='class',
        color='Booster Version', title='Correlation Between Payload and Success for Site {}'.format(entered_site))
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()