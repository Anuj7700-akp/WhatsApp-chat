# -----------===========to extract url from dataset
from urlextract import URLExtract
extractor=URLExtract()
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import emoji
import seaborn as sns


def fetch_stats(selected_user,df):

    if selected_user=='Overall':
        # fetch no of messages
        num_message=df.shape[0]
        #num_of_words
        #----------========= counting no of words in message columns
        word = []
        for i in df['message']:
            word.extend(i.split())
            num_media=df[df['message']=='<Media omitted>\n'].shape[0]

        #---------======= now extracting url from data
        links = []
        for message in df['message']:
            links.extend(extractor.find_urls(message))  # extend() used for append list into list

        return num_message,len(word),num_media,len(links)
    else:
        new_df=df[df['user']==selected_user]
        num_message=new_df.shape[0]
        word = []
        for i in new_df['message']:
            word.extend(i.split())
            num_media = df[df['message'] == '<Media omitted>\n'].shape[0]

            # ==========----------now extracting url from data
            links = []
            for message in new_df['message']:
                links.extend(extractor.find_urls(message))  # extend() used for append list into list

            return num_message,len(word),num_media,len(links)


#----------======== to find most busy user
def most_busy_user(df):
    #--------====== most top 5 busy user find
    x = df['user'].value_counts().head(5)
    df=round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'count': 'percent', 'user': 'name'})
    return x,df


#-----------============ to find most common words used
def most_common_words(selected_user,df):
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()

    if selected_user!='Overall':
        df=df[df['user']==selected_user]
       # fetch no of messages
        num_message=df.shape[0]

    #---------====== removing group_notification and <meadia omitted>\n (and ,is etc.) only get proper word
    temp = df[df['user'] != 'group_notification']
    temp = df[df['message'] != '<media omitted>\n']

    #----------========= most used word by removing stock words(mai,and, ha etc )
    use_word = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                use_word.append(word)

    most_common_df=pd.DataFrame(Counter(use_word).most_common(25))

    return most_common_df

#----------========== to analysis emoji
def emojis_helper(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

        emojis = []
        for message in df['message']:
            emojis.extend([c for c in message if c in emoji.EMOJI_DATA])  # used to extract all emoji used in message

        # all emoji and its count converted into datafram
        emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
        return emoji_df
    else:
        emojis = []
        for message in df['message']:
            emojis.extend([c for c in message if c in emoji.EMOJI_DATA])  # used to extract all emoji used in message

        # all emoji and its count converted into datafram
        emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
        return emoji_df


# ========------------monthly chat analysis
def monthly(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

        timeline = df.groupby(['Year', 'month_num', 'Month'])['message'].size().reset_index()

        # to create anew column with year and month together
        time = []

        for i in range(timeline.shape[0]):
            time.append(timeline['Month'][i] + '-' + str(timeline['Year'][i]))

        # creating a new column
        timeline['time'] = time

    else:
        timeline = df.groupby(['Year', 'month_num', 'Month'])['message'].size().reset_index()

        # to create anew column with year and month together
        time = []

        for i in range(timeline.shape[0]):
            time.append(timeline['Month'][i] + '-' + str(timeline['Year'][i]))

        # creating a new column
        timeline['time'] = time

    return timeline

# --------==========daily chat analysis
def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

        daily_timeline = df.groupby('only_date')['message'].size().reset_index()
        return daily_timeline
    else:
        daily_timeline = df.groupby('only_date')['message'].size().reset_index()
        return daily_timeline

#====-------- day name wise chat analysis
def week_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        # to know which day was busy interms of message
        return df['day_name'].value_counts()
    else:
        return df['day_name'].value_counts()

# month name wise analysis
def month_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        return df['Month'].value_counts()
    else:
        return df['Month'].value_counts()


# activity by hours
def activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

        user_heatmap=(df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0))
        return user_heatmap
    else:
        user_heatmap = (df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0))
        return user_heatmap