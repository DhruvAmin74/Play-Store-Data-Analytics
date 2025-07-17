import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Load data
apps_df = pd.read_csv('Play Store Data.csv')

# Clean and convert
apps_df['Reviews'] = pd.to_numeric(apps_df['Reviews'], errors='coerce')
apps_df['Installs'] = apps_df['Installs'].str.replace('[+,]', '', regex=True)
apps_df['Installs'] = pd.to_numeric(apps_df['Installs'], errors='coerce')

# Apply filters
filtered_apps = apps_df[
    ~apps_df['App'].str.lower().str.startswith(('x', 'y', 'z')) &
    apps_df['Category'].str.startswith(('E', 'C', 'B')) &
    (apps_df['Reviews'] > 500)
].copy()

# Parse dates
filtered_apps['Last Updated'] = pd.to_datetime(filtered_apps['Last Updated'], errors='coerce')
filtered_apps['YearMonth'] = filtered_apps['Last Updated'].dt.to_period('M')

# Group by month and category
installs_over_time = (
    filtered_apps.groupby(['YearMonth', 'Category'])['Installs']
    .sum()
    .reset_index()
    .sort_values(['Category', 'YearMonth'])
)

# MoM growth
installs_over_time['Prev_Installs'] = installs_over_time.groupby('Category')['Installs'].shift(1)
installs_over_time['MoM_Growth'] = (
    (installs_over_time['Installs'] - installs_over_time['Prev_Installs']) /
    installs_over_time['Prev_Installs']
) * 100

# Convert for plotting
installs_over_time['YearMonth'] = installs_over_time['YearMonth'].dt.to_timestamp()

# Plot the chart
fig = go.Figure()
categories = installs_over_time['Category'].unique()

for category in categories:
    df_cat = installs_over_time[installs_over_time['Category'] == category]
    fig.add_trace(go.Scatter(x=df_cat['YearMonth'], y=df_cat['Installs'],
                             mode='lines+markers', name=category))
    
    # Highlight MoM growth > 20%
    highlight = df_cat[df_cat['MoM_Growth'] > 20]
    fig.add_trace(go.Scatter(x=highlight['YearMonth'], y=highlight['Installs'],
                             mode='lines', fill='tozeroy', line=dict(width=0),
                             name=f'{category} >20% Growth',
                             fillcolor='rgba(0, 200, 0, 0.2)', showlegend=False))

fig.update_layout(
    title='Monthly Installs Trend by Category (>20% MoM Growth Highlighted)',
    xaxis_title='Month',
    yaxis_title='Total Installs',
    template='plotly_white'
)

fig.update_yaxes(type="log")

# Save the figure as HTML
fig.write_html("static/timeseries.html")

# Optional display
fig.show()

# Optional: HTML snippet function
def get_timeseries_html():
    return fig.to_html(full_html=False)
