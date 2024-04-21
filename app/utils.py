import json
import base64
import os
import yaml

class ImageGenerationPrompt():

    def __init__(self, system, human_description, image_description, story):
        self.set_system_prompt(system)
        self.set_human_description(human_description)
        self.set_image_description(image_description)
        self.set_story(story)

    #set system prompt attribute
    def set_system_prompt(self, system):
        self.system = system

    #set human description attribute
    def set_human_description(self, human_description):
        self.human_description = human_description

    #set image description attribute
    def set_image_description(self, image_description):
        self.image_description = image_description

    def set_story(self, story):
        self.story = story

    def get_prompt(self):
        return self

    def __str__(self):
        return f'''System Prompt: {self.system}\n
                    Human Description: {self.human_description}\n
                    Image Description: {self.image_description}\n
                    Story: {self.story}'''  


# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  

def fetch_and_encode_images(directory):
    encoded_images = []
    
    for file in os.listdir(directory):
        
        if file.lower().endswith(".jpg"):
            full_path = os.path.join(directory, file)  
            encoded = encode_image(full_path)  
            encoded_images.append(encoded) 
            print(f"Encoded {file} to base64.")

    return encoded_images
  
def add_images(message_data, new_urls):
    
    content_list = message_data[0]['content'] 

    for base64_img in new_urls:

        url = f"data:image/jpeg;base64,{base64_img}"

        new_image_content = {
            "type": "image_url",
            "image_url": {
                "url": url
            }
        }

        content_list.append(new_image_content)



def parse_caption_story_json(response):
    
    parsed_data = json.loads(response)

    content_string = parsed_data['choices'][0]['message']['content']

    content_data = json.loads(content_string)

    captions = content_data['captions']
    story = content_data['story']

    return captions, story


def load_prompts(prompt_type, file_path):
    curr_path = os.path.dirname(__file__)
    file_ = os.path.join(curr_path, file_path)

    with open(file_path, 'r') as file:
        prompts = yaml.safe_load(file)

    #print(prompts)
    
    return prompts[prompt_type]