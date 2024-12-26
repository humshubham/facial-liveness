import cv2
import numpy as np
from deepface import DeepFace
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Initialize FastAPI app
app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/check_liveness")
async def check_liveness(file: UploadFile = File(...)):
    """
    Endpoint to check liveness based on the uploaded image.
    """
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    try:
        output = DeepFace.extract_faces(img_path=frame, enforce_detection=False, anti_spoofing=True)
   
        confidence = round( output[0]['antispoof_score'], 2)

        # Define threshold for spoof detection
        threshold = 0.90
        is_live = True if confidence >= threshold else False
        message = f"Live person detected with confidence {confidence*100}%" if confidence >= threshold else f"Spoof detected with confidence {confidence*100}%, keep trying..."
        return JSONResponse(content={"is_live":is_live, "message": message})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500) 
    
