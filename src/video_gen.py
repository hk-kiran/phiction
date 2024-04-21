import websocket
import uuid
import json
import urllib.request
import urllib.parse
import io
import imageio


class AnimateLCM:
    def __init__(self, server, client_id, verbose=False) -> None:
        """
        server : Runpod endpoint where ComfyUI is hosted.
        verbose : Enables verbose mode."""
        self.server = server
        self.client_id = client_id
        self.verbose = verbose

    def queue_prompt(self, prompt):
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode("utf-8")
        req = urllib.request.Request("http://{}/prompt".format(self.server), data=data)
        return json.loads(urllib.request.urlopen(req).read())

    def get_image(self, filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen(
            "http://{}/view?{}".format(self.server, url_values)
        ) as response:
            return response.read()

    def get_history(self, prompt_id):
        with urllib.request.urlopen(
            "http://{}/history/{}".format(self.server, prompt_id)
        ) as response:
            return json.loads(response.read())

    def get_images(self, ws, prompt):
        prompt_id = self.queue_prompt(prompt)["prompt_id"]
        output_images = {}
        current_node = ""
        while True:
            out = ws.recv()
            if isinstance(out, str):
                if self.verbose:
                    print(out)
                message = json.loads(out)
                if message["type"] == "executing":
                    data = message["data"]
                    if data["prompt_id"] == prompt_id:
                        if data["node"] is None:
                            break  # Execution is done
                        else:
                            current_node = data["node"]
            else:
                if current_node == "save_image":
                    images_output = output_images.get(current_node, [])
                    images_output.append(out[8:])
                    output_images[current_node] = images_output

        return output_images

    def img2vid(self, model, prompt, vid_path, use_upscaler=False, seed=None):
        """
        model : Either 'helloyoung25d_V15j.safetensors' or 'helloobjects_V15evae.safetensors'
        prompt : prompt is a dict with 'positive_prompt' and 'negative_prompt' keys.
        vid_path : Path of the image with the video file name (.mp4 extension only)
        use_upscaler : Upscales generated videos to 1024
        seed : Random seed for noise generation
        """
        if use_upscaler:
            prompt_text = open(
                "src/workflows/animatelcm_phiction_ads_with_upscaler_api.json"
            ).read()
        else:
            prompt_text = open("src/workflows/animatelcm_phiction_ads_api.json").read()

        workflow = json.loads(prompt_text)

        workflow["pos_prompt"]["inputs"]["text"] = prompt["positive_prompt"]
        workflow["neg_prompt"]["inputs"]["text"] = prompt["negative_prompt"]
        workflow["load_ckpt"]["inputs"]["ckpt_name"] = model
        if seed is not None:
            workflow["58"]["inputs"]["noise_seed"] = seed
        ws = websocket.WebSocket()
        ws.connect("ws://{}/ws?clientId={}".format(self.server, self.client_id))
        images = self.get_images(ws, workflow)

        writer = imageio.get_writer(vid_path, fps=12, codec="libx264", quality=8)

        for byte_image in images["save_image"]:
            image = imageio.imread(io.BytesIO(byte_image))
            writer.append_data(image)

        writer.close()
