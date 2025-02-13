import streamlit as st
import pandas as pd


def apply_custom_css(css_path='src/styles/custom_css.css'):
    """Apply custom CSS styling"""
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def display_title():
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h1 style='font-size: 2.5rem; font-weight: 800; color: #1e293b; 
                      letter-spacing: -0.025em;'>
                MARIPOSA OS
            </h1>
            <h2 style='color: #64748b; font-size: 1.1rem;'>
                Press Release Social Sentiment
            </h2>
        </div>
    """, unsafe_allow_html=True)

def create_audio_player():
    """Create audio players using Streamlit's native audio component"""
    
    # First Podcast: MARIPOSA Trial Discussion
    st.markdown("""
        <h3 style='text-align: center; margin-bottom: 20px;'>
            Podcast: MARIPOSA Trial Results and Analysis
        </h3>
    """, unsafe_allow_html=True)
    
    audio_path_1 = "src/audio/podcast_pharmad.mp3"
    audio_file_1 = open(audio_path_1, "rb")
    audio_bytes_1 = audio_file_1.read()
    
    st.audio(audio_bytes_1, format="audio/mp3")
    audio_file_1.close()
    
    st.download_button(
        label="Download MARIPOSA Podcast",
        data=audio_bytes_1,
        file_name="MARIPOSA_Trial_Discussion.mp3",
        mime="audio/mp3"
    )
    
    # Add context for MARIPOSA podcast
    st.markdown("""
        <div style='margin: 20px 0; padding: 20px; background-color: #f8f9fa; border-radius: 5px;'>
            <h4 style='color: #1e293b; margin-bottom: 10px;'>Key Discussion Points:</h4>
            <ul>
                <li>Unprecedented median Overall Survival benefit exceeding 12 months compared to osimertinib</li>
                <li>Analysis of the combination therapy's dual targeting approach with amivantamab and lazertinib</li>
                <li>Discussion of pharmacological profiles and therapeutic management</li>
                <li>Examination of resistance patterns and biomarker data</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # Second Podcast: Original Amivantamab & Lazertinib
    st.markdown("""
        <h3 style='text-align: center; margin: 40px 0 20px 0;'>
            Podcast: Amivantamab & Lazertinib in EGFR-Mutated NSCLC
        </h3>
    """, unsafe_allow_html=True)
    
    audio_path_2 = "src/audio/Amivantamab & Lazertinib in EGFR-Mutated NSCLC (2).wav"
    audio_file_2 = open(audio_path_2, "rb")
    audio_bytes_2 = audio_file_2.read()
    
    st.audio(audio_bytes_2, format="audio/wav")
    audio_file_2.close()
    
    st.download_button(
        label="Download Amivantamab & Lazertinib Podcast",
        data=audio_bytes_2,
        file_name="Amivantamab_Lazertinib_EGFR-Mutated_NSCLC.wav",
        mime="audio/wav"
    )
    
    # Add combined source information
    st.markdown("""
        <div style='margin-top: 30px; padding: 20px; background-color: #f8f9fa; border-radius: 5px;'>
            <h4 style='color: #1e293b; margin-bottom: 10px;'>Source Information:</h4>
            <p><strong>Press Release:</strong> <a href='https://www.jnj.com/media-center/press-releases/rybrevant-amivantamab-vmjw-plus-lazcluze-lazertinib-shows-statistically-significant-and-clinically-meaningful-improvement-in-overall-survival-versus-osimertinib' target='_blank'>
            Johnson & Johnson Press Release - RYBREVANT® (amivantamab-vmjw) plus LAZCLUZE™ (lazertinib)</a></p>
            <p><strong>Data Sources:</strong></p>
            <ul>
                <li>Mariposa Cocoon OS X.csv - Social media engagement data related to the study</li>
                <li>MARIPOSA Trial Results and Clinical Analysis</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    # Add data preview
    st.markdown("""
        <h4 style='color: #1e293b; margin: 20px 0 10px 0;'>Data Preview (Top 10 Rows):</h4>
    """, unsafe_allow_html=True)
    
    # Read and display the CSV data
    df = pd.read_csv('Mariposa Cocoon OS X.csv')
    st.dataframe(
        df.head(10),
        hide_index=True,
        use_container_width=True
    )

def create_video_player():
    """Create video players using Streamlit's native video component"""
    
    # First Video: MARIPOSA Trial
    st.markdown("""
        <h3 style='text-align: center; margin-bottom: 20px;'>
            Video: The MARIPOSA Trial
        </h3>
    """, unsafe_allow_html=True)
    
    video_path_1 = "src/audio/The MARIPOSA Trial_ A New Era in Lung Cancer Treatment_.mp4"
    video_file_1 = open(video_path_1, "rb")
    video_bytes_1 = video_file_1.read()
    
    # Display the first video player
    st.video(video_bytes_1)
    
    # Close the file after reading
    video_file_1.close()
    
    # Add a download button for first video
    st.download_button(
        label="Download MARIPOSA Trial Video",
        data=video_bytes_1,
        file_name="MARIPOSA_Trial_New_Era.mp4",
        mime="video/mp4"
    )
    
    # Add spacing between videos
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Second Video: EGFR-Mutated NSCLC Treatment
    st.markdown("""
        <h3 style='text-align: center; margin-bottom: 20px;'>
            Video: Advancements in EGFR-Mutated NSCLC Treatment
        </h3>
    """, unsafe_allow_html=True)
    
    video_path_2 = "src/audio/Advancements in EGFR-Mutated NSCLC Treatment.mp4"
    video_file_2 = open(video_path_2, "rb")
    video_bytes_2 = video_file_2.read()
    
    # Display the second video player
    st.video(video_bytes_2)
    
    # Close the file after reading
    video_file_2.close()
    
    # Add a download button for second video
    st.download_button(
        label="Download NSCLC Treatment Video",
        data=video_bytes_2,
        file_name="Advancements_in_EGFR-Mutated_NSCLC_Treatment.mp4",
        mime="video/mp4"
    )

def create_tabs():
    return st.tabs(["📈 Engagement", "📊 Analysis", "🎧 Podcast", "🎥 Video", "💬 Chatbot"])
