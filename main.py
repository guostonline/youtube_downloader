import os

import streamlit as st
from st_keyup import st_keyup

import datetime
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


def convert_to_mp3(input_path, output_path, start, end):
    try:

        video_clip = AudioFileClip(input_path)
        new_video = video_clip.subclip(start, end)
        new_video.write_audiofile(output_path, )
        new_video.close()
        print('Converted')

    except Exception as e:
        print("Error: ", str(e))


if __name__ == "__main__":

    mp4_output = "mp4_output/"
    mp4_path = ""
    video_filename = ""

    duration = 0

    st.title("Youtube Downloader")

    video_url = st_keyup("Youtube url")
    # show info about video
    if video_url:
        st.session_state["test"] = "waw"
        yt = YouTube(video_url)
        duration = yt.length
        duration = str(datetime.timedelta(seconds=duration))
        st.image(yt.thumbnail_url, width=400)
        st.text(yt.title)
        st.text(f"La durée: {duration}")
    col1, col2 = st.columns(2)

    with col1:
        star_second = st.text_input("Start", value="0:0:0", help="start in second")
    with col2:
        end_second = st.text_input("End", value=duration, help="end in second")

    download_button = st.button("Download now")

    if download_button:
        with st.spinner('Wait for download...'):
            video_filename = download_youtube_video(video_url, mp4_output)
            mp4_path = mp4_output + video_filename
            mp3_path = mp4_path.replace(".mp4", ".mp3")
            mp3_output = "mp3_output/"
            convert_to_mp3(mp4_path, mp3_path, star_second, end_second)
            os.remove(mp4_path)
            st.success('Done!, you can download it.')
            with open(mp3_path, "rb") as f:
                btn = st.download_button(
                    label="Download file",
                    data=f,
                    file_name=video_filename.replace("mp4", "mp3"),
                    mime="sound/img")
