from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image
import io
import base64
import requests
from typing import List, Union

# Initialize the FastAPI app
app = FastAPI()

# Load the Hugging Face model and processor
model_name = "Qwen/Qwen2.5-VL-72B-Instruct"
processor = AutoProcessor.from_pretrained(model_name)
model = AutoModelForVision2Seq.from_pretrained(model_name)

# Define request and content models
class ImageContent(BaseModel):
    type: str
    text: Union[str, None] = None
    image_url: Union[dict, None] = None

class Message(BaseModel):
    role: str
    content: List[ImageContent]

class ChatRequest(BaseModel):
    messages: List[Message]

@app.post("/process_images")
async def process_images(request: ChatRequest):
    try:
        # Extract messages and process user input
        user_message = next((msg for msg in request.messages if msg.role == "user"), None)
        if not user_message:
            raise HTTPException(status_code=400, detail="No valid user message found.")

        content = user_message.content
        prompt = None
        images = []

        for item in content:
            if item.type == "text":
                prompt = item.text
            elif item.type == "image_url" and item.image_url:
                image_url = item.image_url.get("url")
                if image_url.startswith("data:image/"):  # Base64 image
                    header, base64_data = image_url.split(",", 1)
                    image_data = base64.b64decode(base64_data)
                    images.append(Image.open(io.BytesIO(image_data)))
                else:  # URL image
                    response = requests.get(image_url, stream=True)
                    response.raise_for_status()
                    images.append(Image.open(io.BytesIO(response.content)))

        if not prompt:
            raise HTTPException(status_code=400, detail="No prompt provided.")

        if not images:
            raise HTTPException(status_code=400, detail="No valid images provided.")

        # Preprocess images using the processor
        inputs = processor(images=images, text=prompt, return_tensors="pt")

        # Generate responses from the model
        outputs = model.generate(**inputs)
        responses = processor.batch_decode(outputs, skip_special_tokens=True)

        return JSONResponse(content={"responses": responses})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))