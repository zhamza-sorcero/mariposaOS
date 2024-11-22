import traceback

import streamlit as st

from src.models.data_model import (
    categorize_sentiment,
    get_hashtag_frequency,
    get_location_counts,
    get_sentiment,
    get_word_frequency,
    load_and_process_data,
)
from src.views.dashboard_view import (
    apply_custom_css,
    create_tabs,
    display_title,
)
from src.views.filters_view import display_filters
from src.views.metrics_view import (
    create_engagement_scatter,
    create_hashtag_chart,
    create_location_chart,
    create_pie_chart,
    create_time_series,
    create_user_table,
    create_word_freq_chart,
    display_metrics_with_icons,
)


def main():
    st.set_page_config(
        page_title="MaTOS 2024 - Chatter on X",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    apply_custom_css()
    display_title()

    try:
        df = load_and_process_data()
        df['sentiment_score'] = df['content'].apply(get_sentiment)
        df['sentiment'] = df['sentiment_score'].apply(categorize_sentiment)

        filtered_df = display_filters(df)

        metrics = {
            'Total Posts': len(filtered_df),
            'Total Views': int(filtered_df['views'].sum()),
            'Total Reposts': int(filtered_df['reposts'].sum()),
            'Total Followers': int(filtered_df['followers'].sum()),
            'Avg. Sentiment': round(filtered_df['sentiment_score'].mean(), 2)
        }

        display_metrics_with_icons(metrics)

        tab1, tab2, tab3 = create_tabs()

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
            fig = create_time_series(filtered_df, metric)
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            col1, col2 = st.columns([0.6, 0.4])
            
            with col1:
                # Word frequency chart
                all_text = ' '.join(filtered_df['content'].fillna('').astype(str))
                word_freq = get_word_frequency(all_text).most_common(15)
                st.plotly_chart(
                    create_word_freq_chart(word_freq),
                    use_container_width=True,
                    config={'displayModeBar': False}
                )
                
                # Location chart
                location_counts = get_location_counts(filtered_df)
                st.plotly_chart(
                    create_location_chart(location_counts),
                    use_container_width=True,
                    config={'displayModeBar': False}
                )

            with col2:
                # Sentiment pie chart
                sentiment_counts = filtered_df['sentiment'].value_counts()
                st.plotly_chart(
                    create_pie_chart(sentiment_counts),
                    use_container_width=True,
                    config={'displayModeBar': False}
                )
                
                # Hashtag frequency chart
                hashtag_freq = get_hashtag_frequency(filtered_df['content'])
                st.plotly_chart(
                    create_hashtag_chart(hashtag_freq),
                    use_container_width=True,
                    config={'displayModeBar': False}
                )

            st.markdown("""
                <h3 style='text-align: center; margin: 2rem 0; 
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
        st.error(traceback.format_exc())