import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config and style
st.set_page_config(layout="wide")
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Load and clean data
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_cleaned.csv")
    
    # Parse date_added properly
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df.dropna(subset=['date_added'], inplace=True)

    # Feature engineering
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month_name()
    df['duration_value'] = df['duration'].str.extract(r'(\d+)').astype(float)
    df['duration_unit'] = df['duration'].str.extract(r'([a-zA-Z]+)')
    
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("📊 Filter Netflix Content")
content_type = st.sidebar.multiselect("Select Type", df['type'].unique(), default=df['type'].unique())
year_range = st.sidebar.slider("Select Year Range", int(df['year_added'].min()), int(df['year_added'].max()), (2015, 2021))
available_countries = df['country'].dropna().unique()
selected_countries = st.sidebar.multiselect("Select Countries", available_countries, default=["United States", "India"])

# Filtered DataFrame
filtered_df = df[
    (df['type'].isin(content_type)) &
    (df['year_added'].between(*year_range)) &
    (df['country'].isin(selected_countries))
]

# Dashboard Title
st.title("🎬 Netflix Content Dashboard")
st.markdown("Explore Netflix data including content type, ratings, trends, genres, and directors.")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Titles", filtered_df.shape[0])
col2.metric("Movies", filtered_df[filtered_df['type'] == 'Movie'].shape[0])
col3.metric("TV Shows", filtered_df[filtered_df['type'] == 'TV Show'].shape[0])

# Type Distribution
st.subheader("Content Type Distribution")
st.bar_chart(filtered_df['type'].value_counts())

# Rating Distribution
st.subheader("Top 8 Ratings")
top_ratings = filtered_df['rating'].value_counts().head(8)
st.bar_chart(top_ratings)

# Monthly Additions
st.subheader("Monthly Additions Trend")
monthly_order = ['January','February','March','April','May','June','July','August','September','October','November','December']
monthly = filtered_df['month_added'].value_counts().reindex(monthly_order)
st.line_chart(monthly.fillna(0))

# Yearly Additions
st.subheader("Yearly Additions Trend")
yearly = filtered_df['year_added'].value_counts().sort_index()
st.line_chart(yearly)

# Top 10 Directors
st.subheader("Top 10 Directors on Netflix")
top_directors = filtered_df['director'].value_counts().head(10)
st.bar_chart(top_directors)

# Top Genres (split for Movie and TV Show if needed)
st.subheader("Top 10 Genres")
top_genres = filtered_df['listed_in'].value_counts().head(10)
st.bar_chart(top_genres)

# Raw data
with st.expander("🔍 View Raw Data"):
    st.dataframe(filtered_df)

