from generate import *
from audio import *

#Image description generation

#Audio ad narration multiple languages

#Close up prompt generation

#Video ad generation prompt

if __name__ == '__main__':

    gen = Generate()
    description = gen.demo_local_jewels()
    print(description)
    language = 'English'
    narration = gen.generate_narration(language, description)

    sd_prompt = gen.generate_sd_prompt_human(description, 'male') # Used for API call
    print('Ad prompt: ', sd_prompt)

    object_prompt = gen.generate_sd_prompt_object(description) # Used for API call
    print('Object prompt: ', object_prompt)
    
    voice = 'Nicole'
    model = "eleven_multilingual_v2"

    aud = GenerateAudio()

    client = aud.get_client()
    audio = aud.generate(client, voice, model, narration)

    save(audio, f'/app/{language}_tiaras.mp3') # Used for API call