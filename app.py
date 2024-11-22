import streamlit as st
import pandas as pd
import plotly.express as px
from textblob import TextBlob
import re
from collections import Counter
import plotly.graph_objects as go
from datetime import datetime, timedelta

def apply_custom_css():
    st.markdown("""
        <style>
        .sentiment-metric {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            height: 150px;
            display: flex;
            flex-direction: column;
            justify-content: space-around;  /* Changed from center to space-around */
            align-items: center;
            text-align: center;
        }
        .metric-title {
            color: #1DA1F2;
            font-weight: 600;
            width: 100%;
            text-align: center;
            margin: 0;  /* Remove default margins */
            font-size: 1.2rem;  /* Standardize title size */
        }
        .metric-value {
            color: #14171A;
            font-weight: 600;
            width: 100%;
            text-align: center;
            margin: 0;  /* Remove default margins */
            font-size: 2rem;  /* Standardize value size */
        }
        /* Rest of the CSS remains the same */
        </style>
    """, unsafe_allow_html=True)

def load_and_process_data():
    df = pd.read_csv('matos2024.csv')
    df['date'] = pd.to_datetime(df['date'])

    numeric_columns = ['replies', 'reposts', 'likes', 'views', 'followers']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].fillna(0)

    return df


def get_sentiment(text):
    try:
        return TextBlob(str(text)).sentiment.polarity
    except:
        return 0


def categorize_sentiment(polarity):
    if polarity > 0:
        return 'Positive'
    elif polarity < 0:
        return 'Negative'
    return 'Neutral'


def get_word_frequency(text):
    text = str(text).lower()
    words = re.findall(r'\b\w+\b', text)
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    words = [word for word in words if word not in stopwords and len(word) > 2]
    return Counter(words)


def create_engagement_scatter(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['views'],
        y=df['likes'],
        mode='markers',
        marker=dict(
            size=df['followers'] / 1000 + 5,
            color=df['sentiment_score'],
            colorscale='RdYlBu',
            showscale=True,
            colorbar=dict(title='Sentiment')
        ),
        text=[f"@{user}: {content[:50]}..." for user, content in zip(df['user name'], df['content'])],
        hovertemplate="<b>User:</b> @%{text}<br>" +
                      "<b>Views:</b> %{x}<br>" +
                      "<b>Likes:</b> %{y}<br>" +
                      "<b>Followers:</b> %{marker.size}<br>" +
                      "<extra></extra>"
    ))

    fig.update_layout(
        title={
            'text': 'Engagement Analysis (bubble size = followers/1000)',
            'font': {'color': '#14171A', 'size': 20}
        },
        xaxis_title='Views',
        yaxis_title='Likes',
        template='plotly_white',
        height=500
    )

    return fig


def create_user_table(df):
    # Sort by views and select top 10 posts
    table_df = df.sort_values('views', ascending=False).head(10)

    # Prepare the dataframe for display
    display_df = pd.DataFrame({
        'Username': ['@' + str(username) for username in table_df['user name']],
        'Date': table_df['date'].dt.strftime('%Y-%m-%d'),
        'Content': [content[:100] + ('...' if len(content) > 100 else '') for content in table_df['content']],
        'Followers': [f"{int(followers):,}" for followers in table_df['followers']],
        'Views': [f"{int(views):,}" for views in table_df['views']]
    })

    # Apply custom CSS for the table
    st.markdown("""
        <style>
        .stDataFrame {
            background-color: black;
        }
        .stDataFrame table {
            width: 100%;
            color: white !important;
            background-color: black !important;
        }
        .stDataFrame th {
            background-color: #1DA1F2 !important;
            color: white !important;
            font-weight: bold !important;
            text-align: left !important;
            padding: 12px !important;
            border: 1px solid white !important;
        }
        .stDataFrame td {
            background-color: black !important;
            color: white !important;
            text-align: left !important;
            padding: 12px !important;
            border: 1px solid white !important;
        }
        .stDataFrame tr:hover td {
            background-color: #1a1a1a !important;
        }
        </style>
    """, unsafe_allow_html=True)

    return display_df


def main():
    st.set_page_config(page_title="MaTOS 2024 - Chatter on X", layout="wide")
    apply_custom_css()

    st.markdown("""
        <h1 class='light-text' style='text-align: center;'>
        MaTOS 2024 - Social Media Analytics Dashboard
        </h1>
    """, unsafe_allow_html=True)

    try:
        df = load_and_process_data()
        df['sentiment_score'] = df['content'].apply(get_sentiment)
        df['sentiment'] = df['sentiment_score'].apply(categorize_sentiment)

        # Date range filter
        st.sidebar.markdown("<h3 class='light-text'>Filters</h3>", unsafe_allow_html=True)
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(df['date'].min().date(), df['date'].max().date()),
            min_value=df['date'].min().date(),
            max_value=df['date'].max().date()
        )

        # Apply date filter
        mask = (df['date'].dt.date >= date_range[0]) & (df['date'].dt.date <= date_range[1])
        filtered_df = df[mask]

        # Top metrics row with equal-sized tiles
        col1, col2, col3, col4, col5 = st.columns(5)

        metrics = {
            'Total Posts': len(filtered_df),
            'Total Views': int(filtered_df['views'].sum()),
            'Total Reposts': int(filtered_df['reposts'].sum()),
            'Total Followers': int(filtered_df['followers'].sum()),
            'Avg. Sentiment': round(filtered_df['sentiment_score'].mean(), 2)
        }

        for col, (metric, value) in zip([col1, col2, col3, col4, col5], metrics.items()):
            col.markdown(f"""
                <div class='sentiment-metric'>
                    <h4 class='metric-title'>{metric}</h4>
                    <h2 class='metric-value'>{value:,}</h2>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Interactive tabs
        tab1, tab2, tab3 = st.tabs(["📈 Engagement Analysis", "🔄 Time Series", "📊 Content Analysis"])

        with tab1:
            st.plotly_chart(create_engagement_scatter(filtered_df), use_container_width=True)

        with tab2:
            # Removed followers from metric options
            metric = st.selectbox("Select Metric", ['views', 'likes', 'reposts'])
            daily_metric = filtered_df.groupby(filtered_df['date'].dt.date)[metric].sum().reset_index()
            fig = px.line(daily_metric, x='date', y=metric)
            fig.update_traces(line_color='#1DA1F2')
            fig.update_layout(
                title={
                    'text': f'Daily {metric.capitalize()} Over Time',
                    'font': {'color': '#14171A', 'size': 20}
                },
                xaxis_title='Date',
                yaxis_title=metric.capitalize()
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            col1, col2 = st.columns(2)

            with col1:
                # Word frequency visualization
                all_text = ' '.join(filtered_df['content'].fillna('').astype(str))
                word_freq = get_word_frequency(all_text).most_common(15)
                fig = px.bar(
                    x=[count for _, count in word_freq],
                    y=[word for word, _ in word_freq],
                    orientation='h',
                    color=[count for _, count in word_freq],
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(
                    title={
                        'text': 'Top Words',
                        'font': {'color': '#14171A', 'size': 20}
                    },
                    yaxis={'categoryorder': 'total ascending'},
                    xaxis_title='Count',
                    yaxis_title='Word'
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Sentiment distribution
                sentiment_counts = filtered_df['sentiment'].value_counts()
                fig = px.pie(
                    values=sentiment_counts.values,
                    names=sentiment_counts.index,
                    color=sentiment_counts.index,
                    color_discrete_map={
                        'Positive': '#2ECC71',
                        'Neutral': '#95A5A6',
                        'Negative': '#E74C3C'
                    }
                )
                fig.update_layout(
                    title={
                        'text': 'Sentiment Distribution',
                        'font': {'color': '#14171A', 'size': 20}
                    }
                )
                st.plotly_chart(fig, use_container_width=True)

            # New table section for top viewed posts
            st.markdown("<h3 style='text-align: center; color: #ffffff; margin-top: 30px;'>📝 Top Viewed Posts</h3>",
                        unsafe_allow_html=True)
            table_df = create_user_table(filtered_df)
            st.dataframe(
                table_df,
                hide_index=True,
                use_container_width=True
            )

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        import traceback
        st.error(traceback.format_exc())


if __name__ == "__main__":
    main()