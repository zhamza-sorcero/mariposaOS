import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


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
        annotations=[
            dict(
                text="Circle size indicates number of followers",
                xref="paper",
                yref="paper",
                x=0,
                y=1.05,
                showarrow=False,
                font=dict(size=12, color='gray'),
                xanchor='left'
            )
        ],
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

def create_time_series(df, metric):
    daily_metric = df.groupby(df['date'].dt.date)[metric].sum().reset_index()
    fig = px.line(daily_metric, x='date', y=metric)
    fig.update_traces(line_color='#1DA1F2')
    fig.update_layout(
        title=f'Daily {metric.capitalize()}',
        xaxis_title='Date',
        yaxis_title=metric.capitalize(),
        margin=dict(l=50, r=50, t=50, b=50),
        autosize=True
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

def display_metrics_with_icons(metrics):
    icons = {
        'Total Posts': '📄',
        'Total Views': '👁️',
        'Total Reposts': '🔄',
        'Total Followers': '👥',
        'Avg. Sentiment': '😊'
    }

    cols = st.columns(len(metrics))
    for col, (metric, value) in zip(cols, metrics.items()):
        col.markdown(f"""
            <div class='sentiment-metric'>
                <h4 class='metric-title'>{icons.get(metric, '')} {metric}</h4>
                <h2 class='metric-value'>{value:,}</h2>
            </div>
        """, unsafe_allow_html=True) 