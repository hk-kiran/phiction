from flask import Flask, jsonify, request
from src.database import Database
from app import generate, audio, rungenerate
from os.path import join, dirname
from dotenv import load_dotenv
from src.video_gen import AnimateLCM
import uuid
import random 

app = Flask(__name__)

# get the prompt from the UI
@app.route('/api/send_prompt', methods=['POST'])
def get_prompt():
    # Logic to create a new user
    data = request.get_json()
    query = data['prompt']
    language = data['language']
    gender = data['gender']
    app.config['CONTEXT'] = {
        'query': query,
        'language': language,
        'gender': gender
    }
    return jsonify({'message': 'prompt recieved successfully'}), 201
    
    
# send the selected images to the UI
@app.route('/api/get_images', methods=['GET'])
def get_selected_images():
    prompt = app.config['CONTEXT']['query']
    db = Database()
    image_list = db.query_top_k_images(prompt, 1)
    app.config['CONTEXT']['selected_images'] = image_list
    return jsonify({'images': image_list}), 200

@app.route('/api/get_video', methods=['GET'])
def get_video():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    selected_images_paths = app.config['CONTEXT']['selected_images']
    gender = app.config['CONTEXT']['gender']
    # one image for now !!
    base_64_encoded_image = generate.encode_image(selected_images_paths[0])
    rungen = rungenerate.RunGenerate()
    rungen._generate_description(base_64_encoded_image)
    stable_diffusion_prompt = rungen.get_sd_human_prompt(gender)
    stable_diffusion_object_prompt = rungen.get_sd_object_prompt()
    # return jsonify({
    #     'stable_diffusion_prompt': stable_diffusion_prompt,
    #     'stable_diffusion_object_prompt': stable_diffusion_object_prompt
    # }), 200
    client_id = str(uuid.uuid4())
    vigen = AnimateLCM(server="213.173.110.106:15222", client_id=client_id, verbose=True)
    vigen.img2vid('helloyoung25d_V15j.safetensors',stable_diffusion_prompt, f"outputs/{client_id}_1.mp4")
    vigen.img2vid('helloyoung25d_V15j.safetensors',stable_diffusion_prompt, f"outputs/{client_id}_2.mp4", seed=random.randint(0,100000000))
    return jsonify({'message': 'video generated successfully'}), 200



if __name__ == '__main__':
    app.run()