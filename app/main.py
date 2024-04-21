from generate import *
from audio import *

#Image description generation

#Audio ad narration multiple languages

#Close up prompt generation

#Video ad generation prompt

if __name__ == '__main__':
    description = demo_local_jewels()
    print(description)
    language = 'Chinese'
    narration = generate_narration(language, description)
    
    voice = 'Nicole'
    model = "eleven_multilingual_v2"

    client = get_client()
    audio = generate(client, voice, model, narration)

    save(audio, f'/app/{language}_tiaras.mp3')