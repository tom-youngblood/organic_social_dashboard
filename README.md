# Organic Social Dashboard

## Project Details
This GitHub repository contains an interactive dashboard built with Python, Plotly, and Dash to visualize engagement data from LinkedIn.

<p align="center">
  <img src="demo/preview.png" alt="Dashboard Preview" width="600"/>
</p>


### Data Pipeline
The data for this project is generated through the following custom pipeline, integrated in a separate GitHub Repository:
1. **LinkedIn Posts** – Created by the content team at CoEfficient Labs.
2. **PhantomBuster** – Scrapes engagement data from LinkedIn posts.
3. **Google BigQuery** – Stores raw engagement data.
4. **HubSpot** – Stores enriched engagement data for further analysis.
5. **PhantomBuster** - Enriches HubSpot data.
6. **Apollo** - Enriches HubSpot Data

## Libraries
- Plotly
- Dash
- Pandas
- NumPy


## File Structure
```
organic_social_dashboard/
├── scripts/
│   ├── dashboard.py  # Main dashboard application    
│   └── funcs.py      # Functions used in main dashboard applicaton      
├── data/
│   └── data.csv      # Static dataset from organic_social_pipeline
├── requirements.txt       
├── README.md     
```

## Instructions
```bash
cd scripts
python dashboard.py
```

### Interactivity
Dashboard allows for filtering by:
- **Date**: Date in which lead was scraped
- **Industry**: Industry of corresponding lead
- **Post**: Post from which lead was scraped from
- **Latest Funding Stage**: Most recently reported (within Apollo DB) stage of company

Note: All filters can be applied at the same time.
