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
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
        ],
        value='ALL',
        placeholder='Select a Launch Site Here',
        searchable=True
    ),

    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(
        id='payload-slider',  
        min=0,  
        max=10000,  
        step=1000,  
        marks={i: f'{i}' for i in range(0, 10001, 1000)},  
        value=[0, 10000]  
    ),

    html.Br(),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
from dash import dcc, html, Input, Output
import plotly.express as px

# Define the callback function for updating the pie chart based on the selected launch site
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    # Check if 'ALL' is selected; if so, display success counts across all launch sites
    if entered_site == 'ALL':
        # Aggregate data for all sites, counting successful launches
        fig = px.pie(
            spacex_df, 
            names='class',  # Use the 'class' column for success (1) and failure (0) counts
            title='Total Success Launches for All Sites',
            hole=0.3  # Optional: donut chart style
        )
        fig.update_traces(textinfo='value+percent')  # Show both count and percentage on the pie
    else:
        # Filter data for the specific selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Create a pie chart showing the success (class=1) and failure (class=0) count
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Total Success and Failure Launches for site {entered_site}',
            hole=0.3
        )
        fig.update_traces(textinfo='value+percent')  # Show both count and percentage on the pie
    
    return fig

# TASK 4:
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_plot(selected_site, payload_range):
    # Filter the DataFrame based on the selected payload range
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & 
                            (spacex_df['Payload Mass (kg)'] <= high)]
    
    # Check if 'ALL' sites are selected
    if selected_site == 'ALL':
        # Plot scatter for all sites
        fig = px.scatter(
            filtered_df, 
            x='Payload Mass (kg)', 
            y='class', 
            color='Booster Version Category',  # Color points by Booster Version Category
            title='Payload vs. Outcome for All Launch Sites',
            labels={'class': 'Mission Outcome'}  # Customize label for y-axis
        )
    else:
        # Filter for the specific launch site
        site_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        # Plot scatter for the selected site
        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',  # Color points by Booster Version Category
            title=f'Payload vs. Outcome for {selected_site}',
            labels={'class': 'Mission Outcome'}  # Customize label for y-axis
        )
    
    fig.update_traces(marker=dict(size=10, opacity=0.6))  # Customize marker appearance
    fig.update_layout(xaxis_title='Payload Mass (kg)', yaxis_title='Launch Outcome')

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
