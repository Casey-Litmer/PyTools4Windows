from menucmd import Menu, Bind as B
from moviepy.editor import *
import os


def main():

    result = Menu.result

    main_menu = Menu(name= "MoviePy")

    main_menu.append(
        ("r", "image + audio -> mp4", (
            album_upload, ()
        ))
    )

    main_menu()


#-------------------------------------------------------------------------------------------------

def album_upload() -> None:
    image_path = repr(input("image_path: ")).strip("\"'")
    audio_path = repr(input("audio_path: ")).strip("\"'")
    output_path = repr(input("output_path: ")).strip("\"'")

    output_path = output_path if output_path else r"C:\Users\litme\Desktop"
    output_path = os.path.join(output_path, input("file name: "))

    image_clip = ImageClip(image_path)
    audio_clip = AudioFileClip(audio_path)

    # Set the duration of the image clip to match the audio clip
    image_clip = image_clip.set_duration(audio_clip.duration)

    # Set the audio of the image clip
    video_clip = image_clip.set_audio(audio_clip)

    # Write the final video file
    video_clip.write_videofile(output_path, codec="libx264", audio_codec="libmp3lame", fps= 1)




###################################################################################################################

if __name__ == "__main__":
    main()