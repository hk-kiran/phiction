from flask import Flask, jsonify, request
from src.database import Database

app = Flask(__name__)

# get the prompt from the UI
@app.route('/api/send_prompt', methods=['POST'])
def get_prompt():
    # Logic to create a new user
    data = request.get_json()
    query = data['prompt']
    language = data['language']
    app.config['CONTEXT'] = {
        'query': query,
        'language': language
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
    selected_images_paths = app.config['CONTEXT']['selected_images']
    


if __name__ == '__main__':
    app.run()