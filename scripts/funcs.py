import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, html, dcc, callback, Input, Output, dash_table

class Graphing:
    def funnel(funnel_df):
        """Returns marketing funnel plot (plotly figure)."""
        # Funnel Figure
        funnel_fig = go.Figure(go.Funnel(
            x=funnel_df["Count"],
            y=funnel_df["Stage"],
            textposition = "inside",
            textinfo="value+percent initial",

        ))

        # Update funnel figure
        funnel_fig.update_layout(autosize=True,
                                 margin=dict(l=200, r=10, t=80, b=50),
                                 title={"text": "Stage Funnel",
                                        "x": 0.5,
                                        "xanchor": "center"
                                 },
                                 yaxis={"showticklabels": True,
                                        "title_text": ""
                                       }
                                )
        return funnel_fig

    def social_stage_pie(social_stage_pie_df):
        """Returns pie chart: lead stage (plotly figure)"""
        # Create pie fig
        pie_fig = px.pie(social_stage_pie_df,
                 names="Stage",
                 labels="Stage",
                 values="Count",
                 hole=0.5
                )

        # Update layout of pie fig
        pie_fig.update_layout(showlegend=False,
                              title={
                                  "text": "Distribution of Organic Social Stage",
                                  "x": 0.5,
                                  "xanchor": "center"}
                             )

        # Update pie slices
        pie_fig.update_traces(
            textinfo="label+percent",
        )

        return pie_fig

    def industry_dist_pie(industry_stage_pie_df):
        """Returns pie chart: industry distribution (plotly figure)"""
        # Create pie fig
        pie_fig = px.pie(industry_stage_pie_df,
                 names="Industry",
                 values="Count",
                 hole=0.5
                )

        # Update layout of pie fig
        pie_fig.update_layout(showlegend=False,
                              title={
                                  "text": "Lead Industry Distribution (Top 10)",
                                  "x": 0.5,
                                  "xanchor": "center"}
                             )

        # Update pie slices
        pie_fig.update_traces(
            textinfo="label+percent",
        )

        return pie_fig

    def leads_over_time_area(leads_over_time_df):
        """Returns bar chart (previously area): leads over time (plotly figure)"""
        # Leads Over Time
        leads_over_time_fig = px.bar(leads_over_time_df, x="Date", y="Count")
        # Title
        leads_over_time_fig.update_layout(
            title={
            "text": "Leads Over Time",
            "x": 0.5,
            "xanchor": "center"
            }
        )
        return leads_over_time_fig

    def lead_table(filtered_df):
        """Creates DataFrame containing leads under the current filter."""
        # Plotly go table figure
        table_fig = go.Figure(
            data=[go.Table(
                header=dict(values=list(filtered_df.columns)),
                cells=dict(values=[filtered_df[col].tolist() for col in filtered_df.columns])
            )]
        )

        # Title table
        table_fig.update_layout(title={
            "text": "Filtered Lead Table",
            "x": 0.5,
            "xanchor": "center"})
        return table_fig

    def post_distribution_sankey(post_distribution_sankey_df):
        """Creates sankey plot: post distribution (plotly figure)"""
        # Further prep data
        post_names = list(post_distribution_sankey_df["post_name"].unique())
        stages = list(post_distribution_sankey_df["organic_social_stage"].unique())
        labels = post_names + stages
        num_posts = len(post_names)
        source = [post_names.index(p) for p in post_distribution_sankey_df["post_name"]]
        target = [stages.index(s) + num_posts for s in post_distribution_sankey_df["organic_social_stage"]]
        values = post_distribution_sankey_df["vid"].tolist()

        # Sankey figure
        sankey_fig = go.Figure(data=[go.Sankey(
            node=dict(
                label=labels
            ),
            link=dict(
                source=source,
                target=target,
                value=values
            )
        )])

        # Title sankey figure
        sankey_fig.update_layout(
            title={
                "text": "Lead Flow: Post to Organic Social Stage",
                "x": 0.5,
                "xanchor": "center"
            }
        )
        return sankey_fig

class DataProcessing:
    def process_data(path):
        """Prepares .csv data for dashboarding."""
        # Load Data
        df = pd.read_csv(path).drop(columns=["Unnamed: 0"])

        # Convert createdate to datetime
        df['createdate'] = pd.to_datetime(df['createdate'] / 1000, unit='s')
        df['createdate'] = df['createdate'].dt.strftime('%Y-%m-%d')
        return df

    def get_stage_count(df, stage_name):
        """Returns count of sales stages (int) for the given lead. Used in prep_funnel_data."""
        result = df.loc[df["Stage"] == stage_name, "Count"]
        return result.values[0] if not result.empty else 0

    def prep_funnel_data(filtered_df):
        """Returns DataFrame containing prepared funnel data."""
        # Full funnel data
        funnel_data = filtered_df.groupby("organic_social_stage")["vid"].count().reset_index()

        # Bottom of Funnel Metrics
        bofu_stages = ["Intro Call Scheduled",
                       "Reschedule Intro Call",
                       "Intro Call No Show",
                       "Intro Call Completed",
                       "Brief Call Scheduled",
                       "Brief Call No Show",
                       "Brief Call Showed",
                       "Script Review Scheduled",
                       "Script Review No-Show",
                       "Script Review Showed",
                       "Onboard",
                       "Closed Won"]

        # Fitler data to get Bottom of Funnel Metrics
        bofu = funnel_data[funnel_data["organic_social_stage"].isin(bofu_stages)]
        bofu.columns = ["Stage", "Count"]

        # Get counts for each stage: Intro Call
        ics = DataProcessing.get_stage_count(bofu, "Intro Call Scheduled")
        icrs = DataProcessing.get_stage_count(bofu, "Reschedule Intro Call")
        icns = DataProcessing.get_stage_count(bofu, "Intro Call No Show")
        icc = DataProcessing.get_stage_count(bofu, "Intro Call Completed")

        # Get counts for each stage: Creative Brief
        cbs = DataProcessing.get_stage_count(bofu, "Brief Call Scheduled")
        cbns = DataProcessing.get_stage_count(bofu, "Brief Call No Show")
        cbc = DataProcessing.get_stage_count(bofu, "Brief Call Showed")

        # Get counts for each stage: Script Review
        srs = DataProcessing.get_stage_count(bofu, "Script Review Scheduled")
        srns = DataProcessing.get_stage_count(bofu, "Script Review No-Show")
        src = DataProcessing.get_stage_count(bofu, "Script Review Showed")

        # Get counts for each stage: Onboard and Closed Won
        ob = DataProcessing.get_stage_count(bofu, "Onboard")
        cw = DataProcessing.get_stage_count(bofu, "Closed Won")

        # Collect totals
        ics_lt = ics + icrs + icns + icc + cbs + cbns + cbc + srs + srns + src + ob + cw
        icc_lt = icc + cbs + cbc + cbns + srs + srns + src + ob + cw
        cbs_lt = cbs + cbc + cbns + srs + srns + src + ob + cw
        cbc_lt = cbc + srs + srns + src + ob + cw
        srs_lt = srs + srns + src + ob + cw
        src_lt = src + ob + cw
        ob_lt = ob + cw
        cw_lt = cw

        # Assemble data for funnel
        funnel_dict = {"Stage": ["Intro Call Scheduled",
                                 "Intro Call Completed",
                                 "Creative Brief Scheduled",
                                 "Creative Brief Completed",
                                 "Script Review Scheduled",
                                 "Script Review Completed",
                                 "Onboarded",
                                 "Closed Won"],
                       "Count": [ics_lt,
                                 icc_lt,
                                 cbs_lt,
                                 cbc_lt,
                                 srs_lt,
                                 src_lt,
                                 ob_lt,
                                 cw]
        }

        funnel_df = pd.DataFrame(funnel_dict)
        return funnel_df

    def prep_social_stage_pie_data(filtered_df):
        """Prepares DataFrame for social_stage_pie."""
        return filtered_df.groupby(by="organic_social_stage")["vid"].count().reset_index().rename(columns={"organic_social_stage":"Stage", "vid": "Count"}).sort_values(by="Count", ascending=False)

    def prep_industry_dist_pie_data(filtered_df):
        """Prepares DataFrame for industry_dist_pie."""
        return filtered_df.groupby(by="industry")["vid"].count().reset_index().rename(columns={"industry":"Industry", "vid": "Count"}).sort_values(by="Count", ascending=False)[:10]

    def prep_leads_over_time_data(filtered_df):
        """Prepares DataFrame for leads_over_time_bar"""
        return filtered_df.groupby("createdate")["vid"].count().reset_index().rename(columns={"createdate": "Date", "vid": "Count"})

    def prep_post_distribution_sankey_data(filtered_df):
        """Prepares DataFrame for post_distribution_sankey"""
        return filtered_df.groupby(["post_name", "organic_social_stage"])["vid"].count().reset_index()

class Interaction:
    def date_picker_range(df):
        """Returns date picker object"""
        return dcc.DatePickerRange(
            id="date-picker",
            start_date=df["createdate"].min(),
            end_date=df["createdate"].max(),
            display_format="YYYY-MM-DD"
        )

    def industry_dd(df):
        """Returns industry dropdown object"""
        industry_options = ["Industry"] + df["industry"].dropna().unique().tolist()
        return dcc.Dropdown(id="industry-dd",
                            options = industry_options,
                            value="Industry"
                            )

    def post_dd(df):
        """Returns industry dropdown object"""
        post_options = ["Post Name"] + df["post_name"].dropna().unique().tolist()
        return dcc.Dropdown(id="post-dd",
                            options = post_options,
                            value="Post Name"
                            )

    def venture_backed_dd(df):
        """Returns venture backed dropdown object"""
        vb_options = ["Latest Funding Stage"] + df["latest_funding_stage"].dropna().unique().tolist()
        return dcc.Dropdown(id="vb-dd",
                            options = vb_options,
                            value="Latest Funding Stage"
                            )
