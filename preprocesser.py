def preprocess(data):
    import re
    import pandas as pd

    # now making dataframe from charts of whatsapp using re module pattern of date and time
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    # we split date and time from data
    messages = re.split(pattern, data)[1:]

    # getting data of pattern from data variable
    dates = re.findall(pattern, data)

    # now creating dataframe from txt file
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # formating date and time and its datatype
    df['message_date']=pd.to_datetime(df['message_date'],format="%d/%m/%y, %H:%M - ")

    # renaming column
    df.rename(columns={'message_date': 'Date'}, inplace=True)

    # this code working well for making columns for preprocessing the data(cleaning)

    import re

    user = []
    messages = []

    for message in df['user_message']:
        # Use raw string notation for regex pattern
        entry = re.split(r'([^:]+?):\s', message)

        if len(entry) > 1:
            user.append(entry[1].strip())  # Extracting the user name
            messages.append(" ".join(entry[2:]).strip())  # Extracting the message and combining any further parts
        else:
            # This case handles "group notification" or cases where there is no clear user
            user.append("group_notification")
            messages.append(entry[0].strip())

    df['user'] = user
    df['message'] = messages

    # now making columns further in dataframe

    # we added new column year
    df['Year'] = df['Date'].dt.year

    # we added new column month name
    df['Month'] = df['Date'].dt.month_name()

    # we added new column day name
    df['Day'] = df['Date'].dt.day

    # we added new column hour name
    df['Hour'] = df['Date'].dt.hour

    # we added new column minute name
    df['Minute'] = df['Date'].dt.minute

     # Added new column name month_num
    df['month_num'] = df['Date'].dt.month

    # added new column only_data
    df['only_date'] = df['Date'].dt.date

    # added a new column day_name
    df['day_name'] = df['Date'].dt.day_name()

    # drop column
    df.drop(columns='user_message', inplace=True)

    # making range of Hour column
    period = []
    for hour in df[['Day', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str("00"))
        elif hour == 0:
            period.append(str("00") + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    # new column added in df
    df['period'] = period

    return df