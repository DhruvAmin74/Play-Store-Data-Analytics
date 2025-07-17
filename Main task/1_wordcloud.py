import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# Load datasets
reviews = pd.read_csv("User Reviews.csv")
apps = pd.read_csv("Play Store Data.csv")

# Step 1: Filter Health & Fitness apps
health_apps = apps[apps['Category'] == 'HEALTH_AND_FITNESS']['App'].unique()

# Step 2: Filter positive sentiment reviews for these apps
filtered_reviews = reviews[
    (reviews['App'].isin(health_apps)) &
    (reviews['Sentiment'] == 'Positive') &
    (reviews['Translated_Review'].notnull())
]

# Step 3: Prepare stopwords list and generate word cloud
stopwords = set(STOPWORDS)
stopwords.update([app.lower() for app in health_apps])  # Remove app names too

# Combine reviews into one string
text = " ".join(filtered_reviews['Translated_Review'].astype(str))

# Generate and save the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords).generate(text)

# Save the word cloud image **before** displaying it
wordcloud.to_file("static/wordcloud.png")

# Optional: display it using matplotlib
plt.figure(figsize=(15, 7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Word Cloud for 5-Star Reviews (Health & Fitness Apps)", fontsize=16)
plt.show()