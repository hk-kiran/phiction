from elevenlabs.client import ElevenLabs
from elevenlabs import play, save



import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import settings

class GenerateAudio:

    def get_client(self):

        api_key = settings.ELEVEN_LABS_API_KEY
        client = ElevenLabs(
            api_key=api_key # Defaults to ELEVEN_API_KEY
        )

        return client

    def generate(self, client, voice, model, text):
        print(text)
        audio = client.generate(
                text=text,
                voice=voice,
                model=model
        )
        
        return audio

if __name__ == '__main__':

    aud = GenerateAudio()

    client = aud.get_client()
    
    text =  "Descubre el poder de la realeza con nuestra tiara. Elegancia y lujo en cada detalle."
    voice = 'Nicole'
    model = "eleven_multilingual_v2"

    audio = aud.generate(client, voice, model, text)

    print(audio)
    language = 'es'

    #play(audio)
    save(audio, f'/app/data/{language}_tiaras.mp3')



