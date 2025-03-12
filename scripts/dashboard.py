import funcs
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, html, dcc, callback, Input, Output

# Launch Dash app
app = Dash(__name__)

# Load and process data
df = funcs.DataProcessing.process_data("../data/data.csv")
funnel_data = funcs.DataProcessing.prep_funnel_data(df)

# Prepare figures
funnel_fig = funcs.Graphing.funnel(funnel_data)

# Dashboard layout
app.layout = html.Div([

    # Heading
    html.H1(children="Organic Social Dashboard", style={"textAlign":"center"}),

    # Date picker
    funcs.Interaction.date_picker_range(df),

    # Funnel Graph: Leads
    dcc.Graph(id="funnel-graph"),

    #Div: Split pie charts
    html.Div([
        # Pie 1: Organic Social Stage
        html.Div([
            # Social-stage pie chart
            dcc.Graph(id="social-stage-pie"),
        ], style={"width": "40%", "padding": "20px"}),

        # Pie 2: Industry Distribution
        html.Div([
            # Industry-stage pie chart
            dcc.Graph(id="industry-dist-pie"),
        ], style={"width": "40%", "padding": "20px"})
    ], style={"display": "flex", "justify-content": "center"}
    ),

    # Area Plot: Engagers over Time
    dcc.Graph(id="lot-area-plot")
])

# Callback to update figures
@callback(
    Output("funnel-graph", "figure"),
    Output("social-stage-pie", "figure"),
    Output("industry-dist-pie", "figure"),
    Output("lot-area-plot", "figure"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date")
)
def update_figs(start_date, end_date):
    # Filter df by date
    filtered_df = df[(df["createdate"] >= start_date) & (df["createdate"] <= end_date)]

    # Create/update funnel fig with filtered data
    funnel_data = funcs.DataProcessing.prep_funnel_data(filtered_df)
    funnel_fig = funcs.Graphing.funnel(funnel_data)

    # Create/update organic social pie fig with filtered data
    organic_social_pie_data = funcs.DataProcessing.prep_social_stage_pie_data(filtered_df)
    social_stage_pie_fig = funcs.Graphing.social_stage_pie(organic_social_pie_data)

    # Create/update industry dist pie fig with filtered data
    industry_dist_pie_data = funcs.DataProcessing.prep_industry_dist_pie_data(filtered_df)
    industry_dist_pie_fig = funcs.Graphing.industry_dist_pie(industry_dist_pie_data)

    # Create/update leads over time area plot
    leads_over_time_data = funcs.DataProcessing.prep_leads_over_time_data(filtered_df)
    leads_over_time_fig = funcs.Graphing.leads_over_time_area(leads_over_time_data)

    # Return updated figures
    return funnel_fig, social_stage_pie_fig, industry_dist_pie_fig, leads_over_time_fig



if __name__ == "__main__":
    app.run_server(debug=True)
