import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob
import re
from collections import Counter
from datetime import datetime, timedelta


def load_and_process_data():
    """
    Loads and processes the CSV data, converting date strings to datetime
    and handling numeric columns appropriately.
    """
    df = pd.read_csv('matos2024.csv')
    df['date'] = pd.to_datetime(df['date'])
    numeric_columns = ['replies', 'reposts', 'likes', 'views', 'followers']

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].fillna(0)

    return df


def apply_custom_css():
    """Apply custom CSS styling"""
    st.markdown("""
        <style>
        /* Combine all CSS styles */
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            max-width: 100%;
        }

        .sentiment-metric {
            background-color: #ffffff;
            padding: min(20px, 3vw);
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            min-height: 120px;
            height: auto;
            display: flex;
            flex-direction: column;
            justify-content: space-around;
            align-items: center;
            text-align: center;
            margin: 0.5rem 0;
        }

        .metric-title {
            color: #1DA1F2;
            font-weight: 600;
            font-size: clamp(0.8rem, 1.2vw, 1.2rem);
        }

        .metric-value {
            color: #14171A;
            font-weight: 600;
            font-size: clamp(1.2rem, 1.8vw, 2rem);
        }

        .stDataFrame {
            width: 100% !important;
        }

        .stDataFrame table {
            width: 100%;
            color: white !important;
            background-color: black !important;
            min-width: 800px;
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
            max-width: 300px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        @media screen and (max-width: 768px) {
            .sentiment-metric {
                padding: 10px;
                min-height: 100px;
            }
            .stDataFrame table {
                font-size: 14px;
            }
            .stDataFrame th, .stDataFrame td {
                padding: 8px !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)


def get_sentiment(text):
    """Calculate sentiment using TextBlob"""
    try:
        return TextBlob(str(text)).sentiment.polarity
    except:
        return 0


def categorize_sentiment(polarity):
    """Categorize sentiment score"""
    if polarity > 0:
        return 'Positive'
    elif polarity < 0:
        return 'Negative'
    return 'Neutral'


def get_word_frequency(text):
    """Analyze word frequency excluding stopwords"""
    text = str(text).lower()
    words = re.findall(r'\b\w+\b', text)
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
                 'for', 'of', 'with', 'by', 'from', 'up', 'about', 'into', 'over',
                 'after', 'is', 'are', 'was', 'were', 'this', 'that', 'these',
                 'those', 'has', 'have', 'had', 'what', 'when', 'where', 'who',
                 'which', 'why', 'how'}
    words = [word for word in words if word not in stopwords and len(word) > 2]
    return Counter(words)


def create_engagement_scatter(df):
    """Create engagement scatter plot"""
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
            'text': 'Engagement Analysis',
            'font': {'color': '#14171A', 'size': 20}
        },
        xaxis_title='Views',
        yaxis_title='Likes',
        template='plotly_white',
        height=500,
        margin=dict(l=50, r=50, t=50, b=50),
        autosize=True,
        hovermode='closest',
        width=None
    )
    return fig


def create_user_table(df):
    """Create formatted table of top posts"""
    table_df = df.sort_values('views', ascending=False).head(10)

    display_df = pd.DataFrame({
        'Username': ['@' + str(username) for username in table_df['user name']],
        'Date': table_df['date'].dt.strftime('%Y-%m-%d'),
        'Content': [content[:100] + ('...' if len(str(content)) > 100 else '')
                    for content in table_df['content']],
        'Followers': [f"{int(followers):,}" for followers in table_df['followers']],
        'Views': [f"{int(views):,}" for views in table_df['views']]
    })

    return display_df


def create_pie_chart(sentiment_counts):
    """Create pie chart for sentiment distribution"""
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
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        margin=dict(t=50, b=0, l=0, r=0),
        height=300,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    return fig


def create_word_freq_chart(word_freq):
    """Create word frequency bar chart"""
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
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        yaxis={'categoryorder': 'total ascending'},
        xaxis_title='Count',
        yaxis_title='Word',
        margin=dict(t=50, b=0, l=100, r=0),
        height=300,
        showlegend=False
    )
    return fig


def main():
    st.set_page_config(
        page_title="MaTOS 2024 - Chatter on X",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    apply_custom_css()

    st.markdown("""
        <h1 style='text-align: center; font-size: clamp(1.5rem, 2.5vw, 2.5rem); margin-bottom: 2rem;'>
        MaTOS 2024 - Social Media Analytics Dashboard
        </h1>
    """, unsafe_allow_html=True)

    try:
        df = load_and_process_data()
        df['sentiment_score'] = df['content'].apply(get_sentiment)
        df['sentiment'] = df['sentiment_score'].apply(categorize_sentiment)

        with st.sidebar:
            st.markdown("<h3 style='font-size: clamp(1rem, 1.5vw, 1.5rem);'>Filters</h3>", unsafe_allow_html=True)
            date_range = st.date_input(
                "Select Date Range",
                value=(df['date'].min().date(), df['date'].max().date()),
                min_value=df['date'].min().date(),
                max_value=df['date'].max().date()
            )

        mask = (df['date'].dt.date >= date_range[0]) & (df['date'].dt.date <= date_range[1])
        filtered_df = df[mask]

        metrics = {
            'Total Posts': len(filtered_df),
            'Total Views': int(filtered_df['views'].sum()),
            'Total Reposts': int(filtered_df['reposts'].sum()),
            'Total Followers': int(filtered_df['followers'].sum()),
            'Avg. Sentiment': round(filtered_df['sentiment_score'].mean(), 2)
        }

        cols = st.columns([1] * len(metrics))
        for col, (metric, value) in zip(cols, metrics.items()):
            col.markdown(f"""
                <div class='sentiment-metric'>
                    <h4 class='metric-title'>{metric}</h4>
                    <h2 class='metric-value'>{value:,}</h2>
                </div>
            """, unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["📈 Engagement", "🔄 Time Series", "📊 Analysis"])

        with tab1:
            st.plotly_chart(
                create_engagement_scatter(filtered_df),
                use_container_width=True,
                config={
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
                    'scrollZoom': True
                }
            )

        with tab2:
            metric = st.selectbox("Select Metric", ['views', 'likes', 'reposts'])
            daily_metric = filtered_df.groupby(filtered_df['date'].dt.date)[metric].sum().reset_index()
            fig = px.line(daily_metric, x='date', y=metric)
            fig.update_traces(line_color='#1DA1F2')
            fig.update_layout(
                title=f'Daily {metric.capitalize()}',
                xaxis_title='Date',
                yaxis_title=metric.capitalize(),
                margin=dict(l=50, r=50, t=50, b=50),
                autosize=True
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            col1, col2 = st.columns([0.6, 0.4])

            with col1:
                all_text = ' '.join(filtered_df['content'].fillna('').astype(str))
                word_freq = get_word_frequency(all_text).most_common(15)
                st.plotly_chart(
                    create_word_freq_chart(word_freq),
                    use_container_width=True,
                    config={'displayModeBar': False}
                )

            with col2:
                sentiment_counts = filtered_df['sentiment'].value_counts()
                st.plotly_chart(
                    create_pie_chart(sentiment_counts),
                    use_container_width=True,
                    config={'displayModeBar': False}
                )

            st.markdown("""
                <h3 style='text-align: center; color: #ffffff; margin: 2rem 0; 
                font-size: clamp(1.2rem, 1.8vw, 1.8rem);'>📝 Top Viewed Posts</h3>
            """, unsafe_allow_html=True)

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