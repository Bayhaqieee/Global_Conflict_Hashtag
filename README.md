# Global Conflict Hashtag Dataset Analysis

Welcome to the **Hashtag Sightseeing**! This dashboard provides insights into news happing around the world, and Global Conflicts that still blooming right now!

## Live App

Check out the live version of the app here: [🚧 **On Progress**]()

## Project Status

🚧 **Status**: `On Progress!`

## Features

Here's a description of the Streamlit functions and features that were created for your dashboard:

- **Highest and Lowest Posting Time for the Most Hashtags**
    - **Widget:** A date input widget is used to filter data by a selected date range.

- **Conflict Showing High Exposure on Hashtags**
    - **Widget:** A multi-select widget lets users choose conflict types from the dataset to analyze.

- **Hashtag with the Most Comments, Likes, and Views**
    - **Widget:** A dropdown widget enables users to switch between comments, likes, and views as the engagement metric.

- **Higher Engagement of Social Media Used for Sharing Hashtags**
    - **Widget:** A bar chart visualizes engagement metrics (likes, comments, views) for each social media platform in the dataset.

- **Engagement Over Time**
    - **Widget:** A line chart allows users to visualize engagement trends over time for the selected engagement metric (likes, comments, views).

- **Author Analysis (Top Authors by Engagement)**
    - **Widget:** A bar chart shows the top authors ranked by engagement metrics such as likes.

- **Hashtag Word Cloud**
    - **Widget:** A word cloud displays frequently occurring words in the hashtags.

- **Engagement by Hashtag Length**
    - **Widget:** A line chart shows the relationship between hashtag length and engagement metrics.

- **Engagement by Social Platform Over Time**
    - **Widget:** A line chart enables users to compare engagement trends across social media platforms.

## Technologies

- **Python:** The primary programming language used for data analysis, manipulation, and visualization tasks.
- **Streamlit:** A web application framework that allows for the easy creation of interactive data applications and dashboards directly from Python scripts.
- **Pandas:** A powerful library for data manipulation and analysis, providing data structures like DataFrames to handle structured data efficiently.
- **Matplotlib:** A plotting library for creating static, interactive, and animated visualizations in Python; it provides a flexible framework for customizing plots.
- **Seaborn:** A statistical data visualization library based on Matplotlib, offering a high-level interface for drawing attractive and informative statistical graphics.
- **NLTK:** The Natural Language Toolkit, a suite of libraries and programs for natural language processing (NLP) in Python, used for text processing tasks.
- **WordCloud:** A library to generate word clouds, visualizing text data where the size of each word indicates its frequency or importance in the text.
- **Scikit-learn:** A machine learning library that provides simple and efficient tools for data mining and data analysis, built on NumPy, SciPy, and Matplotlib.
- **Datetime:** A built-in Python module for manipulating dates and times, providing classes for date and time arithmetic.
- **Re:** The regular expression library in Python, used for string searching and manipulation based on patterns.
- **Collections:** A built-in module that provides alternatives to Python’s general-purpose built-in containers like lists and dictionaries, including specialized data structures like namedtuples, defaultdicts, and Counter.

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/Bayhaqieee/Global_Conflict_Hashtag.git
    ```

2. Navigate to the project directory:
    ```bash
    cd dashboard
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application locally:
    ```bash
    streamlit run Dashboard/dashboard.py
    ```