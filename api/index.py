from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from rembg import remove, new_session
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use the 'u2netp' model - it's 10x faster and perfect for Vercel
session = new_session("u2netp")

@app.get("/")
def home():
    return {"status": "Fast AI Server Online"}

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    input_data = await file.read()
    # Process small image quickly (No alpha matting here to save time)
    output_data = remove(input_data, session=session)
    return Response(content=output_data, media_type="image/png")
