import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
import re

def extract_hashtags(text):
    if isinstance(text, str):  # Check if the input is a string
        return re.findall(r'#\w+', text)
    return []  # Return an empty list if the input is not a string

st.header('Global Conflict Hashtag Data Analysis')

# Load the dataset
df = pd.read_csv('Data/conflicts_hashtag_search.csv')
hdf = pd.read_csv('Data/hashtag_data.csv')

# Convert 'creationDate' to datetime format
df['creationDate'] = pd.to_datetime(df['creationDate'])

st.subheader('Hourly Postings')

# Display the oldest and newest dates in the dataset
oldest_date = df['creationDate'].min()
newest_date = df['creationDate'].max()

# Add a date filter (optional: range or specific day)
start_date, end_date = st.date_input("Select date range", [oldest_date.date(), newest_date.date()])

# Convert start and end dates to timezone-aware timestamps if necessary
if start_date and end_date:
    # Compare the timezone of creationDate (drop timezone if needed)
    df['creationDate'] = df['creationDate'].dt.tz_localize(None)
    
    # Now filter the DataFrame for the selected date range
    df_filtered = df[(df['creationDate'] >= pd.to_datetime(start_date)) & 
                     (df['creationDate'] <= pd.to_datetime(end_date))]

    # Group by hour of posting
    df_filtered['hour'] = df_filtered['creationDate'].dt.hour
    hashtag_counts_by_hour = df_filtered.groupby('hour').size()

    # Plotting
    st.bar_chart(hashtag_counts_by_hour)
    
col1, col2 = st.columns(2)

with col1:
    st.write(f"**Oldest Post Date:** {oldest_date.date()}")

with col2:
    st.write(f"**Newest Post Date:** {newest_date.date()}")
    
st.subheader('Conflict Exposure on Hashtag')

# Allow the user to select conflict types
conflict_types = st.multiselect("Select conflict types", df['input'].unique())

# Allow the user to select the time interval (excluding irrelevant ones)
time_interval = st.selectbox("Select time interval", ["Hour", "Day (Sunday to Saturday)", "Week", "Month", "Year"])

# Filter the data by selected conflict types
df_conflict = df[df['input'].isin(conflict_types)]

# Function to group data based on time interval
def group_by_time(df, time_interval):
    if time_interval == "Hour":
        df['time_group'] = df['creationDate'].dt.hour
    elif time_interval == "Day (Sunday to Saturday)":
        # Group by day name and reorder to Sunday to Saturday
        df['time_group'] = df['creationDate'].dt.day_name()
        df['time_group'] = pd.Categorical(df['time_group'], 
                                          categories=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], 
                                          ordered=True)
    elif time_interval == "Week":
        df['time_group'] = df['creationDate'].dt.isocalendar().week
    elif time_interval == "Month":
        df['time_group'] = df['creationDate'].dt.month
    elif time_interval == "Year":
        df['time_group'] = df['creationDate'].dt.year
    return df

# Group the data by the selected time interval
df_grouped = group_by_time(df_conflict, time_interval)

# Aggregate views per selected time interval
conflict_exposure = df_grouped.groupby(['time_group', 'text']).agg({'viewsCount': 'sum'}).reset_index()

# Pivot to display the data for each conflict over time
conflict_exposure_pivot = conflict_exposure.pivot(index='time_group', columns='text', values='viewsCount')

# Display the data as a bar chart
st.bar_chart(conflict_exposure_pivot)

st.subheader('Hashtag WordCloud')

# Create a set to hold unique hashtags
unique_hashtags = set()

# Loop through the text column to extract hashtags
for text in df['text']:
    hashtags = extract_hashtags(text)
    unique_hashtags.update(hashtags)

# Convert the set back to a list for the multiselect widget
unique_hashtags_list = list(unique_hashtags)

# Create a multiselect widget for the user to choose hashtags
selected_hashtags = st.multiselect("Select hashtags to generate word clouds:", unique_hashtags_list)

# Generate a word cloud for each selected hashtag
for tag in selected_hashtags:
    # Extract the content related to the selected hashtag
    hashtag_content = df[df['text'].str.contains(tag, na=False)]['text']  # Use na=False to ignore NaN values
    
    # Combine all text for the specific hashtag
    text_data = ' '.join(hashtag_content)
    
    # Ensure there's text to create the word cloud
    if text_data.strip():
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
        
        # Display the word cloud using matplotlib
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f"Word Cloud for Hashtag: {tag}")
        st.pyplot(plt)
        
st.subheader('Most Trending Hashtag')

# Dropdown for metric selection
metric = st.selectbox("Select metric", ["commentsCount", "likesCount", "viewsCount"])

# Find the top 10 hashtags based on the selected metric
# Create a new dataframe to count occurrences of each hashtag
hashtag_counts = {}

# Loop through the text column again to aggregate metrics for each hashtag
for text in df['text']:
    hashtags = extract_hashtags(text)
    for hashtag in hashtags:
        if hashtag not in hashtag_counts:
            hashtag_counts[hashtag] = {metric: 0}
        hashtag_counts[hashtag][metric] += df.loc[df['text'] == text, metric].sum()

# Convert the dictionary to a DataFrame
top_hashtags = pd.DataFrame(hashtag_counts).T.reset_index()
top_hashtags.columns = ['hashtag', metric]  # Rename columns for clarity

# Sort and select the top 10 hashtags
top_hashtags = top_hashtags.sort_values(by=metric, ascending=False).head(10)

# Create a Plotly bar chart with gradient effect
fig = px.bar(
    top_hashtags,
    x='hashtag',  # Use 'hashtag' for the x-axis
    y=metric,
    color=metric,  # Color bars based on the metric value
    color_continuous_scale='Blues',  # Use a gradient color scale (Blues, Reds, Greens, etc.)
    labels={'hashtag': 'Hashtag', metric: f'Total {metric}'},
    title=f'Top 10 Hashtags by {metric.capitalize()}'
)

# Customize the layout for better visibility
fig.update_layout(
    width=800,
    height=500,
    xaxis_title='Hashtag',
    yaxis_title=f'Total {metric.capitalize()}',
    coloraxis_colorbar=dict(
        title=f'{metric.capitalize()}',
        tickvals=[top_hashtags[metric].min(), top_hashtags[metric].max()],
        ticktext=['Low', 'High']
    )
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)


st.subheader('Social Media Engagement Rate')

# Group by social media platform and calculate total likes, comments, and views
engagement_by_platform = df.groupby('fromSocial').agg({
    'likesCount': 'sum',
    'commentsCount': 'sum',
    'viewsCount': 'sum'
}).reset_index()

# Dropdown to select metric
metric = st.selectbox("Select engagement metric", ["likesCount", "commentsCount", "viewsCount"])

# Create a Plotly bar chart
fig = px.bar(
    engagement_by_platform,
    x='fromSocial',
    y=metric,
    color=metric,  # Color bars based on the metric value
    color_continuous_scale='Blues',  # Use a continuous color scale (Blues, Reds, Greens, etc.)
    labels={metric: f'Total {metric}'},
    title=f'Social Media Engagement by {metric.capitalize()}'
)

# Customize the layout for better visibility
fig.update_layout(
    width=800,
    height=500,
    coloraxis_colorbar=dict(
        title=f'{metric.capitalize()}',
        tickvals=[engagement_by_platform[metric].min(), engagement_by_platform[metric].max()],
        ticktext=['Low', 'High']
    )
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)
