import pandas as pd
import plotly.express as px
import random
import os

# Load dataset
apps = pd.read_csv("Play Store Data.csv")

# Clean and convert 'Installs' column
apps = apps[apps['Installs'].str.contains(r'^\d+[+,]?$', regex=True, na=False)].copy()
apps['Installs'] = apps['Installs'].str.replace('[+,]', '', regex=True).astype(float)

# Exclude app categories starting with A, C, G, S
apps = apps[~apps['Category'].str.startswith(('A', 'C', 'G', 'S'))]

# Get top 5 categories by total installs
top5_categories = apps.groupby('Category')['Installs'].sum().nlargest(5).index
apps = apps[apps['Category'].isin(top5_categories)]

# Assign ISO-3 country codes randomly (simulated)
iso3_countries = ['USA', 'IND', 'BRA', 'GBR', 'DEU', 'FRA', 'RUS', 'CHN', 'JPN', 'KOR']
apps['Country'] = [random.choice(iso3_countries) for _ in range(len(apps))]

# Group by Country and Category to get total installs
grouped = apps.groupby(['Country', 'Category'])['Installs'].sum().reset_index()

# Create choropleth
fig = px.choropleth(
    grouped,
    locations="Country",
    locationmode="ISO-3",
    color="Installs",
    hover_name="Category",
    title="Global Installs by Category (Top 5 Categories)",
    color_continuous_scale="Viridis",
)

# Ensure 'static' directory exists
os.makedirs("static", exist_ok=True)

# Save as HTML
fig.write_html("static/choropleth.html")

# Optionally display
fig.show()

# Optional function for embedding in other HTML files
def get_choropleth_html():
    return fig.to_html(full_html=False)
