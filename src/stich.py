"""
This class takes the generated output of videos, music and narations and integrates it and creates final Ad video.
"""

from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout

from pydub import AudioSegment

# from pydub.effects import volume_normalize
from moviepy.editor import VideoFileClip, AudioFileClip


from skimage.filters import gaussian
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

import os
import sys

class stich():
    def video(self):
        clip_list = [
            "./videos/cocacola_1.mp4",
            "./videos/cocacola_2.mp4",
            "./videos/cocacola_3.mp4",
        ]  # List of video clip filenames
        transition_duration = 0.3  # 1 second transition duration

        # Initialize the final clips list
        final_clips = []

        # Iterate through the list of clips to apply transitions
        for i, clip_file in enumerate(clip_list):
            clip = VideoFileClip(clip_file)

            current_fps = clip.fps
            current_duration = clip.duration

            new_fps = (current_duration * current_fps) / 4
            print(clip.fps)
            # new_clip_duration = 4
            # new_clip_frame_rate = 60

            # new_num_frames = int(new_clip_duration * new_clip_frame_rate)

            clip = clip.set_fps(new_fps).subclip(0, 4)
            print(clip.duration)
            print(clip.fps)
            # Apply fade-out to the previous clip and fade-in to the current clip
            if i > 0:
                prev_clip_fadeout = fadeout(final_clips[-1], duration=transition_duration)
                current_clip_fadein = fadein(clip, duration=transition_duration)

                # Concatenate the faded clips with the current clip
                final_clips[-1] = prev_clip_fadeout
                final_clips.append(current_clip_fadein)
            else:
                final_clips.append(clip)

        # Concatenate all clips in the final_clips list
        self.final_clip = concatenate_videoclips(final_clips)
        final_clip_duration = self.final_clip.duration

        # Write the final video to a file
        self.final_clip.write_videofile("res8.mp4", codec="libx264")
        return final_clip


    def audio(self):
        naration = "./naration/English_coca_cola.mp3"
        music = "./music/bg_cocacola.wav"

        # Load the audio tracks using pydub
        audio1 = AudioSegment.from_file(naration)
        audio2 = AudioSegment.from_file(music)

        # Decrease the volume of audio2 by 6 dB
        decreased_audio2 = audio2 - 6

        # Superimpose (overlay) decreased_audio2 on top of audio1
        superimposed_audio = audio1.overlay(decreased_audio2)

        # Define the output path for the superimposed audio
        # output_path = os.path.join(audio_dir, "superimposed_increased_audio.mp3")

        # Export the superimposed audio to the output path
        superimposed_audio.export("audio_si_cocacola.mp3", format="mp3")

        print(
            "Superimposed and increased volume audio saved successfully at:",
            "audio_si_cocacola",
        )
        return superimposed_audio


    def merge(self, self.final_clip):
        superimposed_audio = AudioFileClip("audio_si_cocacola.mp3")
        final_ad = self.final_clip.set_audio(superimposed_audio)
        final_ad.write_videofile("cocacola_final_ad.mp4", codec="libx264", audio_codec="aac")


    #in this order
    # final_clip = video()
    # superimposed_audio = audio()
    # merge(final_clip)
