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