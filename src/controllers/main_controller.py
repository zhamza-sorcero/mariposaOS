import traceback
import os
import streamlit as st
from langchain_openai import ChatOpenAI
import pandas as pd

from src.models.data_model import (
    categorize_sentiment,
    get_hashtag_frequency,
    get_location_counts,
    get_sentiment,
    get_word_frequency,
    analyze_text_content,
    load_and_process_data,
)
from src.views.dashboard_view import (
    apply_custom_css,
    create_tabs,
    create_audio_player,
    create_video_player,
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
    # Set OpenAI API key from secrets to environment variable
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    
    st.set_page_config(
        page_title="MARIPOSA OS",
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

        tab1, tab3, tab4, tab5, tab6 = create_tabs()

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

        with tab3:
            col1, col2 = st.columns([0.6, 0.4])
            
            with col1:
                # Word frequency section
                st.markdown("### Phrase Analysis Settings")
                
                # Controls in a single row
                control_cols = st.columns([0.6, 0.4])
                with control_cols[0]:
                    word_range = st.slider(
                        "Phrase Length (words)",
                        min_value=2,
                        max_value=8,
                        value=(2, 5),
                        help="Control the minimum and maximum number of words in phrases"
                    )
                
                with control_cols[1]:
                    include_common = st.checkbox(
                        "Include common terms",
                        value=False,
                        help="Toggle to include/exclude common descriptive terms"
                    )
                
                # Process text data
                text_data = filtered_df['content'].fillna('').astype(str)
                non_empty_text = [text for text in text_data if text.strip()]
                
                if non_empty_text:
                    # Create and display chart using improved analysis
                    word_freq_chart = create_word_freq_chart(
                        pd.DataFrame({'content': non_empty_text}),
                        include_common=include_common,
                        min_words=word_range[0],
                        max_words=word_range[1]
                    )
                else:
                    st.warning("No text content available for analysis")
                    word_freq_chart = None
                
                if word_freq_chart is not None:
                    st.plotly_chart(
                        word_freq_chart,
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
            
        with tab4:
            create_audio_player()
            
        with tab5:
            create_video_player()
            
        with tab6:
            st.header("Mariposa Cocoon Chatbot 💬")
            
            # Custom CSS for chat interface
            st.markdown('''
                <style>
                .chat-message {
                    padding: 1rem;
                    border-radius: 4px;
                    margin-bottom: 1rem;
                    display: flex;
                }
                .chat-message.user {
                    background-color: #f0f0f0;
                }
                .chat-message.bot {
                    background-color: #e0e0e0;
                }
                .chat-message .avatar {
                    width: 10%;
                    min-width: 40px;
                }
                .chat-message .avatar img {
                    max-width: 40px;
                    max-height: 40px;
                    border-radius: 50%;
                    object-fit: cover;
                }
                .chat-message .message {
                    width: 90%;
                    padding: 0 1rem;
                    color: #333;
                    line-height: 1.4;
                }
                </style>
            ''', unsafe_allow_html=True)
            
            # HTML templates for chat messages
            bot_template = '''
            <div class="chat-message bot">
                <div class="avatar">
                    <img src="https://i.ibb.co/jMf7sB0/idea.png">
                </div>
                <div class="message">{{MSG}}</div>
            </div>
            '''

            user_template = '''
            <div class="chat-message user">
                <div class="avatar">
                    <img src="https://i.ibb.co/TcgRhzg/question-mark.png">
                </div>    
                <div class="message">{{MSG}}</div>
            </div>
            '''
            
            # Initialize session state for chat history
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            
            def load_data():
                df = pd.read_csv('Mariposa Cocoon OS X.csv')
                df = df.tail(40)  # Get last 40 lines
                formatted_data = []
                for _, row in df.iterrows():
                    text = f"Date: {row['date']}\nContent: {row['content']}"
                    if pd.notna(row['source']):
                        text += f"\nSource: {row['source']}"
                    if pd.notna(row['user name']):
                        text += f"\nAuthor: {row['user name']}"
                    if pd.notna(row['location']):
                        text += f"\nLocation: {row['location']}"
                    if pd.notna(row['tags']):
                        text += f"\nTags: {row['tags']}"
                    formatted_data.append(text)
                return "\n\n".join(formatted_data)
            
            def get_chatbot_response(user_question, context):
                llm = ChatOpenAI(
                    temperature=0.0,
                    model="gpt-4o-mini",
                    max_tokens=3000
                )
                
                prompt = f"""You are an expert medical chatbot analyzing data about lung cancer treatments, particularly focusing on EGFR mutations, clinical trials, and drug combinations. The following context contains recent discussions and findings about treatments like amivantamab, lazertinib, osimertinib, and related clinical trials like MARIPOSA.

                When answering questions:
                1. Focus on identifying specific drugs, their combinations, and treatment outcomes
                2. Highlight key findings from clinical trials
                3. Note any reported side effects or toxicity management
                4. Include relevant survival rates or statistics when available
                5. Mention the sources or experts cited in the data

                Context:
                {context}

                Question: {user_question}

                Provide a detailed but clear answer based on the data. If specific information isn't available in the context, explain what related information is available instead of saying you can't find it.
                """
                
                response = llm.predict(prompt)
                return response
            
            def handle_user_input(user_question):
                context = load_data()
                response = get_chatbot_response(user_question, context)
                
                st.session_state.chat_history.append(("user", user_question))
                st.session_state.chat_history.append(("bot", response))
                
                for role, message in st.session_state.chat_history:
                    if role == "user":
                        st.write(user_template.replace("{{MSG}}", message), unsafe_allow_html=True)
                    else:
                        st.write(bot_template.replace("{{MSG}}", message), unsafe_allow_html=True)
            
            # Text input for user question
            user_question = st.text_input("Ask a question about Mariposa Cocoon data:")
            if user_question:
                handle_user_input(user_question)
            
            # Sidebar info
            with st.sidebar:
                st.title("Chatbot Info")
                st.markdown("""
                This chatbot answers questions about:
                - EGFR mutations
                - Clinical trials
                - Drug combinations
                - Treatment outcomes
                - Patient experiences
                
                Based on the most recent data from Mariposa Cocoon OS X
                
                """)
                
                if st.button("Clear Chat"):
                    st.session_state.chat_history = []
                    st.rerun()

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.error(traceback.format_exc())
