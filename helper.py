from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
from textblob import TextBlob

extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df


def create_wordcloud(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


# Sentiment analysis function
def get_sentiment(message):
    analysis = TextBlob(message)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity < 0:
        return 'Negative'
    else:
        return 'Neutral'


def add_sentiment_column(df):
    df['sentiment'] = df['message'].apply(get_sentiment)
    return df


# Sentiment-based most busy users
def most_busy_users_sentiment(df):
    sentiment_grouped = df.groupby(['user', 'sentiment']).size().unstack(fill_value=0)
    return sentiment_grouped


# Sentiment-based word cloud
def create_sentiment_wordcloud(selected_user, df, sentiment_type):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df = df[df['sentiment'] == sentiment_type]

    # Use the existing word cloud function to generate word clouds by sentiment
    return create_wordcloud(selected_user, df)


def monthly_timeline(selected_user, df, sentiment_type=None):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter by sentiment type if provided
    if sentiment_type:
        df = df[df['sentiment'] == sentiment_type]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    # Create 'time' column in "Month-Year" format for plotting
    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)

    return timeline


def daily_timeline(selected_user, df, sentiment_type=None):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter by sentiment type if provided
    if sentiment_type:
        df = df[df['sentiment'] == sentiment_type]

    # Group by date to get daily message counts
    timeline = df.groupby('only_date').count()['message'].reset_index()

    return timeline


# Helper to get activity per day of the week
def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()

# Helper to get activity per month
def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

