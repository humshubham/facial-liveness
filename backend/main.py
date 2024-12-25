import numpy as np
import cv2
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import onnxruntime as ort
from PIL import Image

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

# Load ONNX Model
model_path = "models/liveness_model.onnx"  # Replace with your model path
session = ort.InferenceSession(model_path)

def preprocess_image(image: np.ndarray) -> np.ndarray:
    """
    Preprocess the input image for the model.
    Resize, normalize, and convert to the required input format.
    """
    image = cv2.resize(image, (224, 224))  # Resize to model input size
    image = image.astype(np.float32) / 255.0  # Normalize to [0, 1]
    image = (image - 0.5) / 0.5  # Standardize
    image = np.transpose(image, (2, 0, 1))  # Convert to CHW format
    return np.expand_dims(image, axis=0)  # Add batch dimension

def predict_liveness(image: np.ndarray) -> bool:
    """
    Predict whether the given image is live or spoof.
    """
    processed_image = preprocess_image(image)
    input_name = session.get_inputs()[0].name
    output = session.run(None, {input_name: processed_image})
    live_score = output[0][0][0]  # Adjust based on model's output format

    # Threshold for liveness (depends on the model, often around 0.5)
    return live_score > 0.5

@app.post("/check_liveness")
async def check_liveness(file: UploadFile = File(...)):
    """
    Endpoint to check liveness based on the uploaded image.
    """
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    try:
        is_live = predict_liveness(frame)

        # Calculate total True values
        true_count = np.sum(is_live)
        total_count = is_live.size
        true_percentage = true_count / total_count
        print(true_percentage)

        # Define threshold for liveness detection (e.g., 30% of the values should be True)
        threshold = 0.3
        live_status = True if true_percentage < threshold else False
        message = "Live person detected" if true_percentage < threshold else "Spoof detected"
        return JSONResponse(content={"is_live":live_status, "message": message})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
