import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def create_engagement_scatter(df):
    """Create engagement scatter plot with updated aesthetics"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['views'],
        y=df['likes'],
        mode='markers',
        marker=dict(
            size=df['followers'] / 1000 + 10,
            color=df['sentiment_score'],
            colorscale='RdYlBu',
            showscale=True,
            colorbar=dict(title='Sentiment Score')
        ),
        text=[f"@{user}: {content[:50]}..." for user, content in zip(df['user name'], df['content'])],
        hovertemplate=("<b>User:</b> @%{text}<br>"
                      "<b>Views:</b> %{x}<br>"
                      "<b>Likes:</b> %{y}<br>"
                      "<b>Followers:</b> %{marker.size}<br>"
                      "<extra></extra>")
    ))

    fig.update_layout(
        title={
            'text': 'Engagement Analysis',
            'font': {'color': '#14171A', 'size': 24}
        },
        annotations=[
            dict(
                text="Circle size indicates number of followers",
                xref="paper",
                yref="paper",
                x=0,
                y=1.05,
                showarrow=False,
                font=dict(size=14, color='gray'),
                xanchor='left'
            )
        ],
        xaxis_title='Views',
        yaxis_title='Likes',
        template='plotly_white',
        height=600,
        margin=dict(l=70, r=70, t=70, b=70),
        hovermode='closest'
    )
    return fig

def create_time_series(df, metric, chart_type='line'):
    """Create time series chart with specified metric and chart type"""
    daily_metric = df.groupby(df['date'].dt.date)[metric].sum().reset_index()
    
    if metric == 'engagement_rate':
        title = 'Daily Engagement Rate (%)'
        y_suffix = '%'
    else:
        title = f'Daily {metric.capitalize()}'
        y_suffix = ''
    
    if chart_type == 'line':
        fig = px.line(daily_metric, x='date', y=metric)
        fig.update_traces(line_color='#1DA1F2')
    else:  # bar
        fig = px.bar(daily_metric, x='date', y=metric)
        fig.update_traces(marker_color='#1DA1F2')
    
    fig.update_layout(
        title={
            'text': title,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Date',
        yaxis_title=metric.capitalize(),
        margin=dict(l=50, r=50, t=50, b=50),
        autosize=True,
        showlegend=False
    )
    
    # Add percentage formatting for engagement rate
    if metric == 'engagement_rate':
        fig.update_layout(
            yaxis=dict(
                tickformat='.2f',
                ticksuffix=y_suffix
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
        'Content': [content[:200] + ('...' if len(str(content)) > 200 else '')
                    for content in table_df['content']],
        'Followers': [f"{int(followers):,}" for followers in table_df['followers']],
        'Views': [f"{int(views):,}" for views in table_df['views']]
    })

    return display_df 

def get_sentiment_display(sentiment_score):
    """Convert sentiment score to visual display elements"""
    if sentiment_score > 0:
        return "#4ade80", "Positive"
    elif sentiment_score == 0:
        return "#94a3b8", "Neutral"
    else:
        return "#f87171", "Negative"

def display_metrics_with_icons(metrics):
    """Display metrics with improved sentiment visualization"""
    icons = {
        'Total Posts': '📄',
        'Total Views': '👁️',
        'Total Reposts': '🔄',
        'Total Followers': '👥'
    }
    
    sentiment_score = metrics.pop('Avg. Sentiment')
    color, label = get_sentiment_display(sentiment_score)
    
    cols = st.columns(len(metrics) + 1)
    
    # Display standard metrics
    for col, (metric, value) in zip(cols[:-1], metrics.items()):
        col.markdown(f"""
            <div class='sentiment-metric'>
                <h4 class='metric-title'>{icons.get(metric, '')} {metric}</h4>
                <h2 class='metric-value'>{value:,}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    # Display sentiment metric with improved formatting
    cols[-1].markdown(f"""
        <div class='sentiment-metric'>
            <h4 class='metric-title'>📊 Overall Sentiment</h4>
            <div style='padding-top: 0.6rem;'>
                <h2 class='metric-value' style='color: {color}; font-size: 2.75rem; margin: 0;'>
                    {label}
                </h2>
                <p style='color: var(--text-secondary); margin-top: -0.8rem; font-size: 1rem;'>
                    Score: {sentiment_score:.2f}
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True) 

def create_location_chart(location_counts):
    """Create bar chart for post locations"""
    # Limit to top 10 locations
    top_locations = location_counts.head(10)
    
    fig = px.bar(
        x=top_locations.values,
        y=top_locations.index,
        orientation='h',
        color=top_locations.values,
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        title={
            'text': 'Top Posting Locations',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        yaxis={'categoryorder': 'total ascending'},
        xaxis_title='Number of Posts',
        yaxis_title='Location',
        margin=dict(t=50, b=0, l=100, r=0),
        height=300,
        showlegend=False
    )
    return fig

def create_hashtag_chart(hashtag_freq):
    """Create bar chart for hashtag frequency"""
    # Get top 15 hashtags
    top_hashtags = hashtag_freq.most_common(15)
    
    fig = px.bar(
        x=[count for _, count in top_hashtags],
        y=[f"#{tag}" for tag, _ in top_hashtags],
        orientation='h',
        color=[count for _, count in top_hashtags],
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        title={
            'text': 'Top Hashtags',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        yaxis={'categoryorder': 'total ascending'},
        xaxis_title='Count',
        yaxis_title='Hashtag',
        margin=dict(t=50, b=0, l=100, r=0),
        height=300,
        showlegend=False
    )
    return fig 
