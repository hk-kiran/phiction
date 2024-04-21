#Class to manage prompts for OpenAI API

class Prompt(object):
    def __init__(self, system):
        self.system_prompt = system

    def get_prompt(self):
        return self.system_prompt

    def __str__(self) -> str:
        return f"{self.system_prompt}"
    
class ImageGenerationPrompt(Prompt):

    def __init__(self, system, human_description, image_description, story=None):
        super().__init__(system)
        self.human_description = human_description
        self.image_description = image_description
        self.story = story

    def get_system_prompt(self):
        return self.system_prompt
    
    def get_human_description(self):
        return self.human_description
    
    def get_image_description(self):
        return self.image_description

    def __str__(self) -> str:
        return f"System Prompt: {self.system_prompt}\nHuman Description: {self.human_description}\nImage Description: {self.image_description}"
    
class StoryPrompt(Prompt):
    #Ask GPT4 to create a narration from the images
    
    def __init__(self, system, human_description, captions, story):
        super().__init__(system)
        self.human_description = human_description
        self.image_description = captions #List of image descriptions
        self.story = story

    def get_story(self):
        return self.story

    def __str__(self) -> str:
        return f"System Prompt: {self.system_prompt}\nHuman Description: {self.human_description}\nImage Description: {self.image_description}\nStory: {self.story}"