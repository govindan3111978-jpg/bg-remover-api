from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from rembg import remove, new_session
from io import BytesIO
from PIL import Image
import uvicorn

app = FastAPI()

# FIX 1: Robust CORS Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all domains (Blogger, local test, etc.)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FIX 2: Pre-load the SMALLER/FASTER model to prevent timeouts
# 'u2netp' is the lightweight model (fastest for Vercel)
session = new_session("u2netp")

@app.get("/")
def health_check():
    return {"message": "AI Background Remover is Online", "model": "u2netp"}

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    try:
        # Read file
        input_data = await file.read()
        
        # FIX 3: Process with the fast session
        # alpha_matting=False makes it much faster to avoid Vercel timeouts
        output_data = remove(input_data, session=session)
        
        return Response(content=output_data, media_type="image/png")
    except Exception as e:
        return {"error": str(e)}
