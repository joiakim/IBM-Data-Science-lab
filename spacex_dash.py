# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options=[{'label': 'ALL', 'value': 'ALL'},
                                                                          {'label': 'CCAFS LC-40',
                                                                           'value': 'CCAFS LC-40'},
                                                                          {'label': 'VAFB SLC-4E',
                                                                           'value': 'VAFB SLC-4E'},
                                                                          {'label': 'KSC LC-39A',
                                                                           'value': 'KSC LC-39A'},
                                                                          {'label': 'CCAFS SLC-40',
                                                                           'value': 'CCAFS SLC-40'}],
                                             value='ALL', placeholder="Select a Launch Site here", searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == "ALL":
        fig = px.pie(spacex_df, values='class', names='Launch Site',
                     title='launch site data')
        return fig
    elif entered_site == "CCAFS LC-40" or "VAFB SLC-4E" or "KSC LC-39A" or "CCAFS SLC-40":
        fda = spacex_df[spacex_df['Launch Site'] == entered_site]['class'].value_counts().to_frame()
        fda[entered_site] = ['Sucess', 'fails']
        figz = px.pie(fda, values='class', names=entered_site,
                      title=entered_site)
        return figz


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_scatter_chart(entered_site, valuex):
    er = range(valuex[0], valuex[1])
    for a in spacex_df["Payload Mass (kg)"]:
        if a not in er:
            spacex_df.drop(labels=spacex_df[spacex_df["Payload Mass (kg)"] == a].index.tolist()[0], axis=0)
    spacex_df
    if entered_site == 'ALL':
        fig1 = px.scatter(ex, x=ex["Payload Mass (kg)"], y=ex["class"],
                          color="Booster Version Category")
        return fig1
    elif entered_site == "CCAFS LC-40" or "VAFB SLC-4E" or "KSC LC-39A" or "CCAFS SLC-40":
        ex = spacex_df[spacex_df['Launch Site'] == entered_site]
        ex1 = ex
        fig2 = px.scatter(ex1, x=ex1["Payload Mass (kg)"], y=ex1["class"], color="Booster Version Category")
        return fig2


# Run the app
if __name__ == '__main__':
    app.run_server()


