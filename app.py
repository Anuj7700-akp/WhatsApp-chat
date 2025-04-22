import streamlit as st
from matplotlib.pyplot import subplots
from streamlit import columns
import seaborn as sns
import preprocesser,helper
import matplotlib.pyplot as plt

from helper import month_activity

st.sidebar.title('Whatsapp Chat Analysis')

upload_file = st.sidebar.file_uploader('Choose a file')
if upload_file is not None:
    bytes_data=upload_file.getvalue()
    data=bytes_data.decode("utf-8")     # to covert file into string
    df=preprocesser.preprocess(data)    # making connection b/w app.py and preprocessor.py
    st.dataframe(df)                    # to read file in data frame

    user_list=df['user'].unique().tolist()         # fetch unique users
    user_list.remove('group_notification')            # remove group_notification from user column
    user_list.sort()                                    # sort data column user
    user_list.insert(0,'Overall')                    # adding word Overall at position 0
    selected_user=st.sidebar.selectbox('Show analysis with respect to',user_list)  # indropdown usercolumn fetch

    if st.sidebar.button('Show Analysis'):   # button added


        num_message,word,num_media,num_links=helper.fetch_stats(selected_user,df)    # count total message,words

        st.title('Top Statistics of Whatsapp Chat')
        col1, col2, col3, col4=st.columns(4)  # creating columns
        with col1:
          st.header('Total Messages')
          st.title(num_message)

        with col2:
            st.header('Total Words')
            st.title(word)

        with col3:
           st.header('Total Media')
           st.title(num_media)

        with col4:
           st.header('Total Links Shared')
           st.title(num_links)


# -------==========most busy user
if selected_user!='Overall':
    st.title('Most Busy User')
    x,new_df=helper.most_busy_user(df)
    fig,ax = plt.subplots()

    col1,col2 = st.columns(2)

    # for bar graph most busy user
    with col1:
        ax.bar(x.index,x.values,color='red')
        st.pyplot(fig)

    # for table for most busy user
    with col2:
        st.dataframe(new_df)


#-------------=========== most common word used
most_common_df=helper.most_common_words(selected_user,df)
st.dataframe(most_common_df)

#--------- sub plot for most common word used
fig,ax=plt.subplots()
ax.bar(most_common_df[0],most_common_df[1],color='orange')
plt.xticks(rotation='vertical')
st.title('most common words')
st.pyplot(fig)


# ----===============emoji showing in table(df)
emoji_df=helper.emojis_helper(selected_user,df)
st.title('Emoji analysis')

col1,col2=st.columns(2)

# emoji in table most used
with col1:
    st.dataframe(emoji_df)

# emoji showing in pie chart
with col2:
    fig,ax=plt.subplots()
    ax.pie(emoji_df[1].head(5),labels=emoji_df[0].head(5),autopct='%0.2f')
    st.pyplot(fig)


# monthly analysis chat
st.title('Monthly Analysis')
timeline=helper.monthly(selected_user,df)

# graph of timeline variable
fig,ax=subplots()
ax.plot(timeline['time'],timeline['message'])
plt.xticks(rotation=20)
st.pyplot(fig)


# daily analysis chat
st.title('Daily Timeline Analysis')
# calling function from file helper
daily_timeline=helper.daily_timeline(selected_user,df)

# ploting graph daily chat
fig,ax=subplots()
ax.plot(daily_timeline['only_date'],daily_timeline['message'])
plt.xticks(rotation='vertical')
st.pyplot(fig)

# daily analysis day wise

st.title('activity map')
col1,col2=columns(2)

with col1:
    st.header('Most Busy Day')
    busy_day=helper.week_activity(selected_user,df)
    fig,ax=subplots()
    ax.bar(busy_day.index,busy_day.values,color='red')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

with col2:
    st.header('Most Busy Month')
    busy_month = month_activity(selected_user, df)
    fig, ax = subplots()
    ax.bar(busy_month.index, busy_month.values, color='red')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

 # online activity map
st.title('Oline Activity Heatmap Map')
user_heatmap=helper.activity(selected_user,df)
fig,ax=plt.subplots()
ax=sns.heatmap(user_heatmap)
st.pyplot(fig)
