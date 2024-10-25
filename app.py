import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from helper import fetch_stats, create_wordcloud, most_busy_users, most_common_words, emoji_helper
from helper import most_busy_users_sentiment, create_sentiment_wordcloud, add_sentiment_column
from helper import monthly_timeline, daily_timeline , month_activity_map , week_activity_map, activity_heatmap  # Add these imports
from preprocessor import preprocess

# Set up the Streamlit app title
st.title("WhatsApp Chat Analyzer with Sentiment")

# Upload and preprocess the data
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # Preprocess the chat data
    data = uploaded_file.read().decode("utf-8")
    df = preprocess(data)

    # Add sentiment column
    df = add_sentiment_column(df)

    # Show statistics
    st.header("Overall Statistics")
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.selectbox("Show analysis for", user_list)

    # Preserve sentiment selection using Streamlit session state
    

    if st.button("Show Analysis"):
        # Fetch Stats
        num_messages, words, media_messages, links = fetch_stats(selected_user, df)
        st.write(f"Messages: {num_messages}, Words: {words}, Media: {media_messages}, Links: {links}")

        # Show Top Statistics
        st.header("Top Statistics")

        # Fetch Stats
        num_messages, total_words, media_messages, links = fetch_stats(selected_user, df)

        # Create columns for side by side display
        col1, col2, col3, col4 = st.columns(4)

        # Display statistics in columns with larger font size
        with col1:
            st.markdown(f"<h2 style='text-align: center;'>Total Messages</h2>", unsafe_allow_html=True)
            st.write(f"<h3 style='text-align: center;'>{num_messages}</h3>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"<h2 style='text-align: center;'>Total Words</h2>", unsafe_allow_html=True)
            st.write(f"<h3 style='text-align: center;'>{total_words}</h3>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<h2 style='text-align: center;'>Media Shared</h2>", unsafe_allow_html=True)
            st.write(f"<h3 style='text-align: center;'>{media_messages}</h3>", unsafe_allow_html=True)

        with col4:
            st.markdown(f"<h2 style='text-align: center;'>Links Shared</h2>", unsafe_allow_html=True)
            st.write(f"<h3 style='text-align: center;'>{links}</h3>", unsafe_allow_html=True)

        # Monthly Timeline and Daily Timeline side by side
        st.subheader("Monthly and Daily Timelines")

        # Create two columns
        col1, col2 = st.columns(2)

        # Monthly Timeline
        with col1:
            st.subheader("Monthly Message Count by Sentiment")
            monthly_df_positive = monthly_timeline(selected_user, df, sentiment_type="Positive")
            monthly_df_neutral = monthly_timeline(selected_user, df, sentiment_type="Neutral")
            monthly_df_negative = monthly_timeline(selected_user, df, sentiment_type="Negative")

            # Plot all three sentiments on the same monthly timeline
            fig, ax = plt.subplots()
            ax.plot(monthly_df_positive['time'], monthly_df_positive['message'], color='blue', label="Positive")
            ax.plot(monthly_df_neutral['time'], monthly_df_neutral['message'], color='black', label="Neutral")
            ax.plot(monthly_df_negative['time'], monthly_df_negative['message'], color='red', label="Negative")
            ax.set_title("Monthly Message Count by Sentiment")
            ax.set_xlabel("Month-Year")
            ax.set_ylabel("Number of Messages")
            ax.legend()
            ax.tick_params(axis='x', rotation=45)
            st.pyplot(fig)

        # Daily Timeline
        with col2:
            st.subheader("Daily Message Count by Sentiment")
            daily_df_positive = daily_timeline(selected_user, df, sentiment_type="Positive")
            daily_df_neutral = daily_timeline(selected_user, df, sentiment_type="Neutral")
            daily_df_negative = daily_timeline(selected_user, df, sentiment_type="Negative")

            # Plot all three sentiments on the same daily timeline
            fig, ax = plt.subplots()
            ax.plot(daily_df_positive['only_date'], daily_df_positive['message'], color='blue', label="Positive")
            ax.plot(daily_df_neutral['only_date'], daily_df_neutral['message'], color='black', label="Neutral")
            ax.plot(daily_df_negative['only_date'], daily_df_negative['message'], color='red', label="Negative")
            ax.set_title("Daily Message Count by Sentiment")
            ax.set_xlabel("Date")
            ax.set_ylabel("Number of Messages")
            ax.legend()
            ax.tick_params(axis='x', rotation=45)
            st.pyplot(fig)

        # Wordclouds for each sentiment
        st.subheader("Wordclouds by Sentiment")

        # Create word clouds for each sentiment type
        wordcloud_positive = create_sentiment_wordcloud(selected_user, df, "Positive")
        wordcloud_neutral = create_sentiment_wordcloud(selected_user, df, "Neutral")
        wordcloud_negative = create_sentiment_wordcloud(selected_user, df, "Negative")

        # Display word clouds side by side
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Positive")
            fig, ax = plt.subplots()
            ax.imshow(wordcloud_positive, interpolation="bilinear")
            ax.axis("off")  # Turn off axis
            st.pyplot(fig)

        with col2:
            st.subheader("Neutral")
            fig, ax = plt.subplots()
            ax.imshow(wordcloud_neutral, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)

        with col3:
            st.subheader("Negative")
            fig, ax = plt.subplots()
            ax.imshow(wordcloud_negative, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)
        # Add Activity Maps (Most Busy Month and Most Busy Day Activity Maps Side by Side)
        st.subheader("Most Busy Month and Most Busy Day Activity")

        col1, col2 = st.columns(2)

        with col1:
            st.write("Most Busy Month")
            busy_month_counts = month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month_counts.index, busy_month_counts.values, color='purple')
            ax.set_title("Messages per Month")
            ax.set_xlabel("Month")
            ax.set_ylabel("Message Count")
            ax.tick_params(axis='x', rotation=45)
            st.pyplot(fig)

        with col2:
            st.write("Most Busy Day")
            busy_day_counts = week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day_counts.index, busy_day_counts.values, color='orange')
            ax.set_title("Messages per Day of Week")
            ax.set_xlabel("Day")
            ax.set_ylabel("Message Count")
            st.pyplot(fig)

        # Weekly Activity Heatmap
        st.subheader("Weekly Activity Heatmap")
        activity_heatmap_df = activity_heatmap(selected_user, df)

        fig, ax = plt.subplots(figsize=(10, 6))
        # Custom color palette from white to orange to red to purple to black
        cmap = sns.color_palette(["black", "purple", "red", "orange", "white"])
        sns.heatmap(activity_heatmap_df, cmap=cmap, linewidths=0.3, annot=False,
                    ax=ax)  # Set annot=False to remove text
        ax.set_title("Weekly Activity Heatmap")
        st.pyplot(fig)

        # Busy users based on sentiment
        st.subheader("Most Busy Users by Sentiment")
        busy_sentiment_df = most_busy_users_sentiment(df)
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(busy_sentiment_df)

        # Most busy users histogram
        with col2:
            st.subheader("User Activity Histogram")
            user_counts = df['user'].value_counts().head(10)  # Adjust the count as needed
            fig3, ax3 = plt.subplots()
            ax3.bar(user_counts.index, user_counts.values, color='skyblue')
            ax3.set_title("Top 10 Most Active Users")
            ax3.set_xlabel("User")
            ax3.set_ylabel("Message Count")
            ax3.tick_params(axis='x', rotation=45)
            st.pyplot(fig3)

        # Emoji analysis
        st.subheader("Emoji Distribution")
        emoji_df = emoji_helper(selected_user, df)

        # Create two columns
        col1, col2 = st.columns(2)

        # Emoji Distribution Table in the first column
        with col1:
            st.dataframe(emoji_df)

        # Most Common Words in the second column
        with col2:
            st.subheader("Most Common Words")
            common_words_df = most_common_words(selected_user, df)

            # Create a horizontal bar graph
            fig, ax = plt.subplots(figsize=(12, 10))
            ax.barh(common_words_df[0], common_words_df[1], color='skyblue')
            ax.set_xlabel("Count")
            ax.set_ylabel("Words")
            ax.set_title("Most Common Words")

            # Display the horizontal bar graph
            st.pyplot(fig)

        # Sentiment pie chart
        st.subheader("Sentiment Distribution")
        sentiment_counts = df['sentiment'].value_counts()
        fig2, ax2 = plt.subplots()
        ax2.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%')
        st.pyplot(fig2)


