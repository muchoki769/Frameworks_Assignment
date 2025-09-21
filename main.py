import re
from typing import Counter
from matplotlib import pyplot as plt
import pandas as pd
from wordcloud import WordCloud

# Data Loading and Basic Exploration
# Download and load the data
df = pd.read_csv('metadata.csv')
print(df.head())
print(df.describe())
# Basic data exploration
missing_counts=df.isna().sum()
print(missing_counts[missing_counts > 0])

# Data cleaning and prepation
# Handle missing data

threshold = len(df) * 0.5 # Drop columns with more than 50% missing values
df = df.dropna(axis=1, thresh=threshold)

df = df.fillna(df.mean(numeric_only=True)) # Fill the rest of missing numeric values with their mean

df.to_csv('metadata_clean.csv',index=False)

print(df.isna().sum())
# Prepare data for analysis
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['publish_year'] = df['publish_time'].dt.year
df['publish_month'] = df['publish_time'].dt.month
df['publish_day'] = df['publish_time'].dt.day
df['abstract_word_count'] = df['abstract'].fillna('').apply(lambda x: len(x.split()))
print(df[['publish_time','publish_year','abstract_word_count']].head())
df.to_csv('metadata_cleaned.csv', index=False)

# Data Analysis and Visualization 
#Perform basic analysis
papers_per_year = df['publish_year'].value_counts().sort_index()
print(papers_per_year)

top_journals = df['journal'].value_counts().head(10)
print(top_journals)

titles = ''.join(df['title'].dropna().tolist())
titles = re.sub(r'[^A-Za-z\s]', '', titles).lower()
words = titles.split()
stopwords = {'the','a','an','and','of','for','to','in','on','with','by','at','from'}
words = [w for w in words if w not in stopwords and len(w) > 2]
word_counts = Counter(words)
# print(word_counts.most_common(20))
wc_df = pd.DataFrame(word_counts.most_common(20), columns=['word', 'count'])
print(wc_df)

#Create visualizations
#plot
papers_per_year = df['publish_year'].value_counts().sort_index()
plt.figure(figsize=(8,5))
papers_per_year.plot(kind='line', marker='o')
plt.title('Number of Publications per Year')
plt.xlabel('Year')
plt.ylabel('Number of papers')
plt.grid(True)
plt.show()

#Bar chart
top_journals = df['journal'].value_counts().head(10)

plt.figure(figsize=(8,5))
top_journals.plot(kind='bar')
plt.title('Top 10 top journals Publishing COVID-19 Research')
plt.xlabel('Journal')
plt.ylabel('Number of Papers')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

#word_cloud for paper titles
titles = ''.join(df['title'].dropna().tolist())
titles = re.sub(r'[^A-Za-z\s]', '', titles).lower()

stopwords = {'the','a','an','and','of','for','to','in','on','with','by','at','from'}
words = [w for w in words if w not in stopwords and len(w) > 2]

# text_for_cloud = ''.join(words)
freqs = Counter(words)

wordcloud = WordCloud(width=800, height=400,
                      background_color='white').generate_from_frequencies(freqs)
plt.figure(figsize=(10,5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Most Frequent Words in Paper Titles')
plt.show()

#plot distribution of paper counts by source
if 'source_x' in df.columns:
    source_counts=df['source_x'].value_counts()

    plt.figure(figsize=(8,5))
    source_counts.plot(kind='bar')
    plt.title('Distribution of Papers by Source')
    plt.xlabel('Numbers of papers')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
else:
    print("No column named 'source_x'.Columns are:",df.columns)
    # print(df.columns)
    

