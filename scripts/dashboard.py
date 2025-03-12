import funcs
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
from dash import Dash, html, dcc, callback, Input, Output

# Launch Dash app
app = Dash(__name__)

# Load and process data
df = funcs.DataProcessing.process_data("../data/data.csv")

# Custom color palette
colabs_blues = ["#78BFEC","#6EACD5","#6499BF","#5A86A9","#507494","#46637F","#3B526A","#304256","#253343"]

# Create custom color palette template
pio.templates["colabs_blues"] = go.layout.Template(
    layout=go.Layout(colorway=colabs_blues)
)

# Apply template to all plots
pio.templates.default = "colabs_blues"

# Dashboard layout
app.layout = html.Div([

    # Banner
    html.Div(
        children="Organic Social Dashboard",
        style={
            "backgroundColor": "#78BFEC",
            "color": "white",
            "padding": "20px",
            "fontWeight": "Bold",
            "fontSize": "4rem",
            "fontFamily": "Open Sans, sans-serif"
        }
    ),

    # Date picker and dropdown menus
    html.Div([
        # Industry drop-down
        html.Div([funcs.Interaction.industry_dd(df)],
            style={"width": "20%", "padding": "5"}),
        # Post drop-down
        html.Div([funcs.Interaction.post_dd(df)],
            style={"width": "20%", "padding": "5"}),
        # Venture-Backed drop-down
        html.Div([funcs.Interaction.venture_backed_dd(df)],
            style={"width": "20%", "padding": "5"}),
    ], style={
        "display": "flex",
        "justify-content": "center"
        }),

    # Date picker
    html.Div([
        html.Div([funcs.Interaction.date_picker_range(df)],
        style={"width": "20%", "padding": "5"}),
    ], style={"display": "flex", "justify-content": "left"}),

    # Div: left -- funnel, right -- lead-table
    html.Div([
        # Left -- funel
        html.Div([
            dcc.Graph(id="funnel-graph")
        ], style={"width": "40%", "padding": "20px"}),
        # Right -- leads over time area chart
        html.Div([
            dcc.Graph(id="lot-area-plot")
        ], style={"width": "40%", "padding": "20px"})
    ], style={"display": "flex", "justify-content": "center"}
    ),

    # Div: Split pie charts
    html.Div([
        # Left -- Pie 1: Organic Social Stage
        html.Div([
            # Social-stage pie chart
            dcc.Graph(id="social-stage-pie"),
        ], style={"width": "40%", "padding": "20px"}),

        # Left -- Pie 2: Industry Distribution
        html.Div([
            # Industry-stage pie chart
            dcc.Graph(id="industry-dist-pie"),
        ], style={"width": "40%", "padding": "20px"})
    ], style={"display": "flex", "justify-content": "center"}
    ),

    # Sankey figure
    dcc.Graph(id="sankey-graph"),

    # Lead Table
    dcc.Graph(id="lead-table"),
])

# Callback to update figures
@callback(
    Output("funnel-graph", "figure"),
    Output("social-stage-pie", "figure"),
    Output("industry-dist-pie", "figure"),
    Output("lot-area-plot", "figure"),
    Output("lead-table", "figure"),
    Output("sankey-graph", "figure"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date"),
    Input("industry-dd", "value"),
    Input("post-dd", "value"),
    Input("vb-dd", "value")
)
def update_figs(start_date, end_date, industry, post, vb_stage):
    # Filter df by date
    filtered_df = df[(df["createdate"] >= start_date) & (df["createdate"] <= end_date)]

    # Filter by industry
    if industry and industry != "Industry":
        filtered_df = filtered_df[filtered_df["industry"] == industry]

    # Filter by post
    if post and post != "Post Name":
        filtered_df = filtered_df[filtered_df["post_name"] == post]

    # Filter by funding stage
    if vb_stage and vb_stage != "Latest Funding Stage":
        filtered_df = filtered_df[filtered_df["latest_funding_stage"] == vb_stage]

    # Create/update funnel fig with filtered data
    funnel_data = funcs.DataProcessing.prep_funnel_data(filtered_df)
    funnel_fig = funcs.Graphing.funnel(funnel_data)

    # Create/update organic social pie fig with filtered data
    organic_social_pie_data = funcs.DataProcessing.prep_social_stage_pie_data(filtered_df)
    organic_social_stage_pie_fig = funcs.Graphing.social_stage_pie(organic_social_pie_data)

    # Create/update industry dist pie fig with filtered data
    industry_dist_pie_data = funcs.DataProcessing.prep_industry_dist_pie_data(filtered_df)
    industry_dist_pie_fig = funcs.Graphing.industry_dist_pie(industry_dist_pie_data)

    # Create/update leads over time area plot
    leads_over_time_data = funcs.DataProcessing.prep_leads_over_time_data(filtered_df)
    leads_over_time_fig = funcs.Graphing.leads_over_time_area(leads_over_time_data)

    # Create/update table figure
    lead_table_fig = funcs.Graphing.lead_table(filtered_df)

    # Create/update post distribution sankey figure
    post_distribution_sankey_data = funcs.DataProcessing.prep_post_distribution_sankey_data(filtered_df)
    post_distribution_sankey_fig = funcs.Graphing.post_distribution_sankey(post_distribution_sankey_data)

    # Return updated figures
    return funnel_fig, organic_social_stage_pie_fig, industry_dist_pie_fig, leads_over_time_fig, lead_table_fig, post_distribution_sankey_fig

if __name__ == "__main__":
    app.run_server(debug=True)
