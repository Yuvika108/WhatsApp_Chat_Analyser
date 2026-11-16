import os
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(str(message).split())

    # fetch number of media messages
    num_media_messages = df[
        df['message'].astype(str).str.strip().eq('<Media omitted>')
    ].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(str(message)))

    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    percent_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    percent_df.columns = ['name', 'percent']
    return x, percent_df


def create_wordcloud(selected_user, df):
    _dir = os.path.dirname(os.path.abspath(__file__))
    stop_words_path = os.path.join(_dir, 'stop_hinglish.txt')

    with open(stop_words_path, 'r', encoding='utf-8') as f:
        stop_words = set(f.read().split())

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification'].copy()

    # Remove media messages regardless of trailing whitespace
    temp = temp[
        temp['message'].astype(str).str.strip() != '<Media omitted>'
    ]

    # Handle chats with no usable text
    if temp.empty:
        return None

    def remove_stop_words(message):
        words = str(message).lower().split()
        return " ".join(word for word in words if word not in stop_words)

    temp['message'] = temp['message'].fillna('').astype(str).apply(remove_stop_words)

    # Join messages without relying on Pandas .str accessor
    text = " ".join(temp['message'].tolist()).strip()

    if not text:
        return None

    wc = WordCloud(
        width=500,
        height=500,
        min_font_size=10,
        background_color='white'
    )

    return wc.generate(text)

def most_common_words(selected_user,df):

    _dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(_dir, 'stop_hinglish.txt'), 'r') as f:
        stop_words = set(f.read().splitlines())

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[
        temp['message'].astype(str).str.strip() != '<Media omitted>'
    ].copy()

    words = []

    for message in temp['message']:
        for word in str(message).lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(
        Counter(words).most_common(20),
        columns=['word', 'frequency']
    )
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in str(message) if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap















