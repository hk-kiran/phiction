
from openai import OpenAI
import json

from utils import add_images, encode_image, fetch_and_encode_images, parse_caption_story_json, load_prompts
from Prompts import Prompt, ImageGenerationPrompt, StoryPrompt


import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import settings


class Generate:


    def get_test_images(self, dir):
        #Get from data directory
        return fetch_and_encode_images(dir)


    def image_descriptions(self, images):
        #Generate image descriptions from given images
        client = OpenAI()

        prompts = load_prompts("caption_generation", 'data/app/prompts.yaml')


        #prompt = Prompt(system=prompt)
                        
        messages = [
            {
            "role": "system",
            "content": [
                {
            "type": "text",
            "text": prompts['system'][0]['text']
                }
            ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type":"text",
                        "text": prompts['user'][0]['text']
                    }
                ]
            }
        ]

        add_images(messages, images)
        
        response = client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=messages,
                    max_tokens=512,
                    response_format={"type": "json_object"}
        )


        captions, story = parse_caption_story_json(response.json())

        return captions, story

    def demo_gen_local_images(self):

        curr_path = os.path.dirname(__file__)
        data_dir = os.path.join(curr_path, 'data/Kashmir-Sample')

        images = self.get_test_images(data_dir)
        captions, story = self.image_descriptions(images)

        print('Story', story)

        return captions, story



    def generate_description(self, image):
        #Generate a description from the image
        client = OpenAI()

        prompt = load_prompts("image_description", 'app/prompts.yaml')

        messages = [
            {
            "role": "system",
            "content": [
                {
            "type": "text",
            "text": prompt['system'][0]['text']
                }
            ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type":"text",
                        "text": prompt['user'][0]['text']
                    },

                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image[0]}"
                        }
                    }
                ]
            }
        ]
        
        response = client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=messages,
                    max_tokens=512,
                    response_format={"type": "json_object"}
        )
        
        if response.choices[0].message.content:
            return json.loads(response.choices[0].message.content)
        
        return None

    def generate_narration(self, language, description):
        #Generate a narration from the image description
        client = OpenAI()

        prompt = load_prompts("narration_generation", 'app/prompts.yaml')

        message = [{"role": "system", "content": prompt['system'][0]['text'] + language}, 
                                {"role":"user", "content": prompt['user'][0]['text'] + description }]
        
        response = client.chat.completions.create(
                        model="gpt-4-turbo",
                        messages=message,
                        max_tokens=256,
                        response_format={"type": "json_object"}
                    )
        if response.choices[0].message.content:
            return json.loads(response.choices[0].message.content)['narration']
        
        return None


    def demo_local_jewels(self):

        images = self.get_test_images('app/data')
        description = self.generate_description(images)

        return description['description']


    def generate_sd_prompt_human(self, description, gender):
        prompt = load_prompts("sd_ad_prompt", 'app/prompts.yaml')

        client = OpenAI()

        message = [{"role": "system", "content": prompt['system'][0]['text']}, 
                                {"role":"user", "content": prompt['user'][0]['text'] + 'Object description - ' + description + ' Gender - ' + gender }]
        
        print('Generating SD prompt')
        response = client.chat.completions.create(
                        model="gpt-4-turbo",
                        messages=message,
                        max_tokens=512,
                        response_format={"type": "json_object"}
                    )
        if response.choices[0].message.content:
            print(response.choices[0].message.content)
            return json.loads(response.choices[0].message.content)
        
        return None

    def generate_sd_prompt_object(self, description):
        prompt = load_prompts("sd_object_prompt", 'app/prompts.yaml')

        client = OpenAI()

        message = [{"role": "system", "content": prompt['system'][0]['text']}, 
                                {"role":"user", "content": prompt['user'][0]['text'] + 'Object description - ' + description }]
        
        print('Generating SD prompt')
        response = client.chat.completions.create(
                        model="gpt-4-turbo",
                        messages=message,
                        max_tokens=512,
                        response_format={"type": "json_object"}
                    )
        if response.choices[0].message.content:
            print(response.choices[0].message.content)
            return json.loads(response.choices[0].message.content)
        
        return None

if __name__ == '__main__':

    os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
    #generate_humans_description(eye_color='blue', skin_color='brown', hair_color='black', built='medium', age='25')
    #print(pipeline())
    gen = Generate()
    description = gen.demo_local_jewels()
    print(description)
    narration = gen.generate_narration('Spanish', description)
    print(narration)
    

    

