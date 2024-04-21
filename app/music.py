"""
This class generates background music for voice over naration.
"""
#Instruction to run musicgen model
# # Best to make sure you have torch installed first, in particular before installing xformers.
# # Don't run this if you already have PyTorch installed.
# python -m pip install 'torch==2.1.0'
# # You might need the following before trying to install the packages
# python -m pip install setuptools wheel
# # Then proceed to one of the following
# python -m pip install -U audiocraft  # stable release
# python -m pip install -U git+https://git@github.com/facebookresearch/audiocraft#egg=audiocraft  # bleeding edge
# python -m pip install -e .  # or if you cloned the repo locally (mandatory if you want to train).


from audiocraft.models import MusicGen

# import streamit as st
import os
import torch
import torchaudio
import numpy as np
import base64

class generateMusic():
    def load_model(self):
        model = MusicGen.get_pretrained("facebook/musicgen-small")
        return model


    def generate_music_tensors(description, duration: int):
        print("Description: ", description)
        print("Duration: ", duration)
        model = load_model()

        model.set_generation_params(use_sampling=True, top_k=250, duration=duration)

        output = model.generate(
            descriptions=[description], progress=True, return_tokens=True
        )

        return output[0]


    def save_audio(self, samples: torch.Tensor):
        """Renders an audio player for the given audio samples and saves them to a local directory.

        Args:
            samples (torch.Tensor): a Tensor of decoded audio samples
                with shapes [B, C, T] or [C, T]
            sample_rate (int): sample rate audio should be displayed with.
            save_path (str): path to the directory where audio should be saved.
        """

        print("Samples (inside function): ", samples)
        sample_rate = 32000
        save_path = "audio_output/"
        assert samples.dim() == 2 or samples.dim() == 3

        samples = samples.detach().cpu()
        if samples.dim() == 2:
            samples = samples[None, ...]

        for idx, audio in enumerate(samples):
            audio_path = os.path.join(save_path, f"audio_{idx}.wav")
            torchaudio.save(audio_path, audio, sample_rate)


    def generate_music(self, text_prompt):

        time_slider = 12
        if text_area and time_slider:

            music_tensors = generate_music_tensors(text_area, time_slider)
            print("Music Tensors: ", music_tensors)
            save_music_file = save_audio(music_tensors)

