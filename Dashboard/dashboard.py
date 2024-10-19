import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

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