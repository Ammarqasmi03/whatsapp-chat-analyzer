import re
import string
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
from sklearn.feature_extraction.text import CountVectorizer


def get_user_stats(df,selected_user):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch number of messages
    num_messages = df.shape[0]

    # fetch no of words
    words = []
    for message in df['messages']:
        words.extend(message.split())

    num_words = len(words)

    # fetch no of deleted messages
    num_del_messages = df[df['messages'].str.contains('This message was deleted\n')].shape[0]

    # fetch no of media messages
    num_media_messages = df[df['messages'].str.contains('<Media omitted>\n')].shape[0]

    num_emojis = sum(len(emoji.emoji_list(message)) for message in df['messages'])


    # fetch no of links shared
    extractor = URLExtract()
    links = []
    for message in df['messages']:
        links.extend(extractor.find_urls(message))

    num_links = len(links)

    # fetch most active users in group (group level)
    active_user_df = (
    df[df["user"] != "group_notification"]
      .groupby("user")
      .size()
      .reset_index(name="message_count")
      .sort_values("message_count", ascending=False)
    )

    return num_messages, num_words, num_emojis, num_links, active_user_df, num_media_messages, num_del_messages


def get_part_user_stats(df,selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_df = df[df["user"] != "group_notification"]

    user_counts = user_df["user"].value_counts()

    active_chatters = user_df["user"].nunique()

    most_active_user = user_counts.index[0]

    avg_messages = round(user_counts.mean())

    quiet_profiles = int((user_counts < 10).sum())

    return active_chatters, most_active_user, avg_messages, quiet_profiles
    
def all_user_stats_summary(df,selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]


    user_df = df[df["user"] != "group_notification"].copy()
    summary = pd.DataFrame()

    # No. of messages per user

    summary['Messages'] = user_df.groupby('user').size()

    # No of words per user
    user_df["word_count"] = user_df["messages"].apply(lambda x: len(str(x).split()))
    summary['Words'] = user_df.groupby("user")["word_count"].sum()

    # No of emojis per user
    user_df["emoji_count"] = user_df["messages"].apply(lambda x: sum(1 for c in str(x) if c in emoji.EMOJI_DATA))
    summary['Emojis'] = user_df.groupby("user")["emoji_count"].sum()

    # No of link per user
    extract = URLExtract()
    user_df["link_count"] = user_df["messages"].apply(lambda x: len(extract.find_urls(str(x))))
    summary['Links'] = user_df.groupby("user")["link_count"].sum()

    # Avg. word count per user
    user_df["message_length"] = user_df["messages"].str.len()
    summary['avg_length'] = (user_df.groupby("user")["message_length"].mean().round(1))


    return summary.reset_index()


def msg_len_distribution(df,selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df["word_count"] = df["messages"].apply(lambda x: len(str(x).split()))

    return df


def create_wordcloud(df,selected_user):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    temp = temp[temp['messages'] != 'This message was deleted\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if ((word not in stop_words) and (word != 'message' or word != 'edited')):
                y.append(word)
        return " ".join(y)


    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['messages'] = temp['messages'].apply(remove_stop_words)
    df_wc = wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc

def search_word_stats(df,selected_user,word):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # No of Occurences of this word
    total_occurrences = (df["messages"].str.lower().str.count(rf"\b{word}\b").sum())

    # first Date and Last date
    filtered = df[df["messages"].str.contains(rf"\b{word}\b",case=False,na=False,regex=True)]
    first_used = filtered["date"].min()
    last_used = filtered["date"].max()

    if pd.notna(first_used):
        first_used = first_used.strftime("%d %b %Y")
    else:
        first_used = "N/A"

    if pd.notna(last_used):
        last_used = last_used.strftime("%d %b %Y")
    else:
        last_used = "N/A"
    


    # percentage of the word in messages
    messages_with_word = len(filtered)
    percentage = round((messages_with_word / len(df)) * 100,2)

    return total_occurrences, first_used, last_used, percentage, filtered



translator = str.maketrans('', '', string.punctuation)

def clean_message(text):

    text = str(text).lower()

    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)

    # Remove <....>
    text = re.sub(r'<.*?>', '', text)

    # Remove emojis
    text = emoji.replace_emoji(text, replace='')

    # Remove punctuation
    text = text.translate(translator)

    # Remove numbers
    text = re.sub(r'\d+', '', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def most_common_words(df,selected_user):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    temp = temp[temp['messages'] != 'This message was deleted\n']



    words = []

    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_commom_df = pd.DataFrame(Counter(words).most_common(20))

    return most_commom_df 

def most_common_word_stats(df,selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    
    # Load stopwords
    with open("stop_hinglish.txt", "r", encoding="utf-8") as f:
        stop_words = set(f.read().splitlines())

    # Remove unwanted messages
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    temp = temp[temp['messages'] != 'This message was deleted\n']

    # Clean messages
    messages = temp['messages'].apply(clean_message)

    words = []
    word_users = {}

    # Count words and users
    for i, message in enumerate(messages):

        user = temp.iloc[i]["user"]

        # unique words in one message
        unique_words = set()

        for word in message.split():

            if word in stop_words or len(word) <= 1:
                continue

            words.append(word)
            unique_words.add(word)

        # Store which users used each word
        for word in unique_words:
            if word not in word_users:
                word_users[word] = set()

            word_users[word].add(user)

    # Frequency
    most_common_df = pd.DataFrame(
        Counter(words).most_common(50),
        columns=["Word", "Frequency"]
    )

    # Percentage
    total_words = len(words)

    most_common_df["Percentage"] = (
        most_common_df["Frequency"] / total_words * 100
    ).round(2)

    # Number of users who used the word
    most_common_df["Users"] = most_common_df["Word"].apply(
        lambda x: len(word_users.get(x, set()))
    )

    # Average per month
    months = temp["date"].dt.to_period("M").nunique()

    most_common_df["Avg/Month"] = (
        most_common_df["Frequency"] / months
    ).round(2)


    return most_common_df


def most_used_phase(df,selected_user):
    with open("stop_hinglish.txt", "r", encoding="utf-8") as f:
        stop_words = list(filter(None, f.read().split("\n")))

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]


    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    temp = temp[temp['messages'] != 'This message was deleted\n']

    vectorizer = CountVectorizer(
        ngram_range=(2,2),
         stop_words=stop_words
    )

    X = vectorizer.fit_transform(temp["messages"])

    phrase_counts = X.sum(axis=0).A1

    phrases = pd.DataFrame({
    "Phrase": vectorizer.get_feature_names_out(),
    "Frequency": phrase_counts
      })

    phrases = phrases.sort_values(
           "Frequency",
           ascending=False
          ).head(20)

    return phrases


def emojis_stats(df,selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    
    all_emojis = []

    for message in df["messages"]:
        all_emojis.extend(
            [char for char in str(message) if char in emoji.EMOJI_DATA]
        )

    emoji_counts = Counter(all_emojis)

    emoji_df = (
        pd.DataFrame(
            emoji_counts.items(),
            columns=["Emoji", "Count"]
        )
        .sort_values("Count", ascending=False)
        .reset_index(drop=True)
    )

    total_emojis = len(all_emojis)
    unique_emojis = emoji_df["Emoji"].nunique()
    top_emoji = emoji_df.iloc[0]["Emoji"] if not emoji_df.empty else ""
    

    return total_emojis,unique_emojis,top_emoji,emoji_df

def emojis_stats_summary(df,selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_df = df[df["user"] != "group_notification"].copy()

    table_data = []
    for user, group in user_df.groupby("user"):
        all_emojis = []
        for msg in group["messages"]:
            all_emojis.extend([char for char in str(msg) if char in emoji.EMOJI_DATA])

        emoji_count = len(all_emojis)
        if emoji_count > 0:
            favorite_emoji = pd.Series(all_emojis).value_counts().idxmax()
        else:
            favorite_emoji = "-"

        unique_emojis = len(set(all_emojis))
        emoji_per_message = round(emoji_count / len(group), 2) if len(group) > 0 else 0

        table_data.append({
            "User": user,
            "Emoji Count": emoji_count,
            "Favorite Emoji": favorite_emoji,
            "Emoji / Message": emoji_per_message,
            "Unique Emojis": unique_emojis
        })

    emoji_summary_df = pd.DataFrame(table_data)
    emoji_summary_df = emoji_summary_df.sort_values(
        "Emoji Count",
        ascending=False
    ).reset_index(drop=True)

    return emoji_summary_df

def time_stats(df,selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    first_msg = df['date'].min().strftime("%d %b %Y")

    last_msg = df['date'].max().strftime("%d %b %Y")

    peak_day = df['day_name'].value_counts().idxmax()

    active_months = df['date'].dt.to_period('M').nunique()

    return first_msg,last_msg,peak_day,active_months



def monthly_year_timeline(df, selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby([df['year'], df['month_name']]).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month_name'][i] + "-" + str(timeline['year'][i]))
    
    timeline['time'] = time

    return timeline

def daily_year_timeline(df, selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(df['only_date']).count()['messages'].reset_index()

    return timeline


def monthly_timeline(df, selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    monthly = df.groupby('month_name').size().reset_index(name='messages')

    return monthly

def daily_timeline(df, selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily = df.groupby('date').size().reset_index(name='messages')
    daily.rename(columns={"date":"Date"},inplace=True)

    return daily

def hourly_timeline(df,selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    hourly = df.groupby('hour').size().reset_index(name='messages')

    return hourly

def yearly_timeline(df,selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    yearly = df.groupby('year').size().reset_index(name='messages')

    return yearly


def day_activity(df,selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    day_act = df.groupby('day_name').size().reset_index(name='messages')

    return day_act

def hour_activity(df,selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    hour_act = df.groupby('hour').size().reset_index(name='messages')

    return hour_act

def user_trend(df,selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]


    user_trend_df = (
    df[df["user"] != "group_notification"]
    .groupby(["year", "month_name", "user"])
    .size()
    .reset_index(name="Messages")
)

    user_trend_df["month_num"] = (
    df[df["user"] != "group_notification"]
    .groupby(["year", "month_name"])["month"]
    .first()
    .reset_index()["month"]
     )

    user_trend_df["Period"] = (
       user_trend_df["month_name"] + " " + user_trend_df["year"].astype(str)
     )

    return user_trend_df

def year_month_summary(df,selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    summary_df = (
    df[df["user"] != "group_notification"]
    .groupby(["year", "month_name"])
    .agg(
        Messages=("messages", "count"),
        Active_Users=("user", "nunique")
    )
    .reset_index()
     )
    
    days = (
    df.groupby(["year", "month_name"])["day"]
    .nunique()
    .reset_index(name="Days")
    )

    summary_df = summary_df.merge(days, on=["year","month_name"])

    summary_df["Avg / Day"] = (
         summary_df["Messages"] /
         summary_df["Days"]
    ).round(1)

    peak_day = (
    df[df["user"] != "group_notification"]
    .groupby(["year","month_name","day_name"])
    .size()
    .reset_index(name="count")
)

    peak_day = (
        peak_day.sort_values("count", ascending=False)
            .drop_duplicates(["year","month_name"])
    )

    peak_day["Peak Day"] = peak_day["day_name"].astype(str)

    summary_df = summary_df.merge(
        peak_day[["year","month_name","Peak Day"]],
        on=["year","month_name"]
    )

    summary_df = summary_df.rename(columns={
    "year":"Year",
    "month_name":"Month",
    "Active_Users":"Active Users"
})

    summary_df = summary_df[
    ["Year",
     "Month",
     "Messages",
     "Active Users",
     "Avg / Day",
     "Peak Day"]
    ]

    return summary_df


def monthly_activity_map(df, selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month_name'].value_counts()


def weekly_activity_map(df, selected_user):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def hourly_activity_heatmap(df,selected_user):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    hour_heatmap = (
    df[df['user'] != 'group_notification']
        .pivot_table(
        index="month_name",
        columns="hour",
        values="messages",
        aggfunc="count",
        fill_value=0
         )
    )

    month_order = [
    "January","February","March","April",
    "May","June","July","August",
    "September","October","November","December"
    ]

    hour_heatmap = hour_heatmap.reindex(month_order)

    return hour_heatmap

def weekly_activity_heatmap(df,selected_user):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    week_heatmap = (
          df[df['user'] != 'group_notification'].pivot_table(
                index='day_name',
                columns='hour',
                values='messages',
                aggfunc='count',
                fill_value=0
            )
    )

    # Order weekdays
    week_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
     ]

    week_heatmap = week_heatmap.reindex(week_order)

    return week_heatmap