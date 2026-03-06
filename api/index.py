from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from rembg import remove
from io import BytesIO
from PIL import Image
import uvicorn

app = FastAPI()

# Allow your Blogger site to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Change this to your blogger URL for security later
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def hello():
    return {"status": "AI Server is Running"}

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    # Read the uploaded image
    input_image = await file.read()
    
    # Process the image with Rembg (The AI part)
    # We use alpha_matting=True for better hair/edge detection
    output_image = remove(input_image, alpha_matting=True)
    
    # Return the processed image as a PNG
    return Response(content=output_image, media_type="image/png")
