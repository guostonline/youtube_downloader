import streamlit as st
from moviepy.editor import *
from pytube import YouTube


def download_youtube_video(url, output_path):
    try:
        yt = YouTube(url)
        video_stream = yt.streams.filter(only_audio=True).first()

        if not video_stream:
            print("No audio stream found for the given YouTube video.")
            return

        video_stream.download(output_path)
        return video_stream.default_filename
    except Exception as e:
        print("Error: ", str(e))
        return None


def convert_to_mp3(input_path, output_path):
    try:
        video_clip = AudioFileClip(input_path)
        video_clip.write_audiofile(output_path)
        video_clip.close()
    except Exception as e:
        print("Error: ", str(e))


if __name__ == "__main__":
    download_url = "mp3_output/"
    st.title("Youtube Downloader")

    video_url = st.text_input("Entree Youtube Url", help="copy url from youtube page")
    video_filename = download_youtube_video(video_url, download_url)

    isClicked = st.button("Convert")

    if isClicked:
        st.text("on progress..")
        if video_filename:
            mp4_path = download_url + video_filename
            mp3_filename = video_filename.replace(".mp4", ".mp3")
            mp3_path = download_url + mp3_filename

            convert_to_mp3(mp4_path, mp3_path)
            os.remove(mp4_path)
            st.text(f"you can download this file : {mp3_path}")
            with open(mp3_path, "rb") as f:
                btn = st.download_button(
                    label="Download file",
                    data=f,
                    file_name=mp3_path,
                    mime="sound/img"
                )
