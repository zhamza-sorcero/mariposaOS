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
    """Create an audio player using Streamlit's native audio component"""
    audio_path = "src/audio/Amivantamab & Lazertinib in EGFR-Mutated NSCLC (2).wav"
    
    st.markdown("""
        <h3 style='text-align: center; margin-bottom: 20px;'>
            Podcast: Amivantamab & Lazertinib in EGFR-Mutated NSCLC
        </h3>
    """, unsafe_allow_html=True)
    
    # Open and read the audio file
    audio_file = open(audio_path, "rb")
    audio_bytes = audio_file.read()
    
    # Display the audio player
    st.audio(audio_bytes, format="audio/wav")
    
    # Close the file after reading
    audio_file.close()
    
    # Add a download button
    st.download_button(
        label="Download Podcast",
        data=audio_bytes,
        file_name="Amivantamab_Lazertinib_EGFR-Mutated_NSCLC.wav",
        mime="audio/wav"
    )
    
    # Add source information
    st.markdown("""
        <div style='margin-top: 30px; padding: 20px; background-color: #f8f9fa; border-radius: 5px;'>
            <h4 style='color: #1e293b; margin-bottom: 10px;'>Source Information:</h4>
            <p><strong>Press Release:</strong> <a href='https://www.jnj.com/media-center/press-releases/rybrevant-amivantamab-vmjw-plus-lazcluze-lazertinib-shows-statistically-significant-and-clinically-meaningful-improvement-in-overall-survival-versus-osimertinib' target='_blank'>
            Johnson & Johnson Press Release - RYBREVANT® (amivantamab-vmjw) plus LAZCLUZE™ (lazertinib)</a></p>
            <p><strong>Data Source:</strong> Mariposa Cocoon OS X.csv - Social media engagement data related to the study</p>
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
    """Create a video player using Streamlit's native video component"""
    video_path = "src/audio/Advancements in EGFR-Mutated NSCLC Treatment.mp4"
    
    st.markdown("""
        <h3 style='text-align: center; margin-bottom: 20px;'>
            Video: Advancements in EGFR-Mutated NSCLC Treatment
        </h3>
    """, unsafe_allow_html=True)
    
    # Open and read the video file
    video_file = open(video_path, "rb")
    video_bytes = video_file.read()
    
    # Display the video player
    st.video(video_bytes)
    
    # Close the file after reading
    video_file.close()
    
    # Add a download button
    st.download_button(
        label="Download Video",
        data=video_bytes,
        file_name="Advancements_in_EGFR-Mutated_NSCLC_Treatment.mp4",
        mime="video/mp4"
    )

def create_tabs():
    return st.tabs(["📈 Engagement", "🔄 Time Series", "📊 Analysis", "🎧 Podcast", "🎥 Video"])
