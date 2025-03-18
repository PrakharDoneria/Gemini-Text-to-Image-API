import os
import base64
import requests
from flask import Flask, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# Function to generate an image using Google Gemini API
def generate_image(prompt, api_key):
    client = genai.Client(api_key=api_key)
    model = "gemini-2.0-flash-exp-image-generation"

    contents = [
        types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_modalities=["image"],
    )

    # Stream the generated image
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if chunk.candidates and chunk.candidates[0].content.parts:
            image_data = chunk.candidates[0].content.parts[0].inline_data.data
            return image_data
    return None

# Function to upload image to ImgBB with custom filename
def upload_to_imgbb(image_data, prompt, api_key):
    encoded_image = base64.b64encode(image_data).decode("utf-8")
    url = "https://api.imgbb.com/1/upload"

    # Generate a valid filename
    filename = f"{prompt.replace(' ', '_')}.png"

    payload = {
        "key": api_key,
        "image": encoded_image,
        "name": filename  # Set custom filename
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        return response.json()["data"]["url"]
    return None

# Flask endpoint
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt")
    gemini_api_key = data.get("api")
    imgbb_api_key = os.getenv("IMGBB_API_KEY")  # Set this in your environment variables

    if not prompt or not gemini_api_key or not imgbb_api_key:
        return jsonify({"error": "Missing required parameters"}), 400

    # Generate image
    image_data = generate_image(prompt, gemini_api_key)
    if not image_data:
        return jsonify({"error": "Failed to generate image"}), 500

    # Upload to ImgBB with custom filename
    image_url = upload_to_imgbb(image_data, prompt, imgbb_api_key)
    if not image_url:
        return jsonify({"error": "Failed to upload image"}), 500

    return jsonify({"image_url": image_url})

if __name__ == "__main__":
    app.run(debug=True)
