from collections import Counter
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

df = pd.read_csv("metadata.csv")

# App title&description
st.title("COVID-19 Research Explorer")
st.write("This app lets you explore a sample of the COVID-19 research dataset")

# show sample of data
st.subheader("Dataset preview")
st.dataframe(df.head())

#dropdown for journal
journals = df['journal'].dropna().unique()
selected_journal = st.selectbox("Filter by journal", options=["ALL"] + list(journals))

if selected_journal != "All":
    filtered_df = df[df['journal'] == selected_journal]
else:
    filtered_df = df

# slider for publication year
if 'publish_time' in df.columns:
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    min_year = int(df['year'].min(skipna=True))
    max_year = int(df['year'].max(skipna=True))
    year_range = st.slider("Select Year Range",
                            min_value=min_year,
                            max_value=max_year,
                            value=(min_year,max_year))
    filtered_df = df[(df['year'] >= year_range[0]) & 
                              (df['year'] <= year_range[1])]
#Visualization 1: publications over time 
st.subheader("Publications Over Time")

if 'year' in filtered_df.columns:
    # convert to numeric, coerce errors to NaN
    filtered_df['year'] = pd.to_numeric(filtered_df['year'], errors='coerce')

    # drop NaNs (and zeros if needed)
    filtered_df = filtered_df.dropna(subset=['year'])
    filtered_df = filtered_df[filtered_df['year'] != 0]

    counts = filtered_df['year'].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(12,6))
    counts.plot(kind='bar', ax=ax, color='skyblue')

    ax.set_xlabel('Year')
    ax.set_ylabel("Number of papers")
    ax.set_title('Number of Papers per Year')

    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

#Visualization 2: Word Cloud of Titles 
st.subheader("Word Cloud of paper Titles")
text = " ".join(filtered_df['title'].dropna().astype(str))
freqs = Counter(text)

if freqs:
    wordcloud = WordCloud(width=800,height=400,background_color='white').generate_from_frequencies(freqs)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
else:
    st.write("No titles available to generate a word cloud.")    