# Facial Liveness Detection App

This application demonstrates a sophisticated facial liveness detection system using a Python backend and a React-based frontend (powered by Vite). The backend performs advanced liveness detection using ONNX models, and the frontend allows users to upload images for liveness analysis.

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Setup Instructions](#setup-instructions)
    - [Backend](#backend)
    - [Frontend](#frontend)
4. [Running the Application](#running-the-application)
5. [How the App Works](#how-the-app-works)
6. [Acknowledgements](#acknowledgements)

---

## Features

- **Frontend**: User-friendly React-based interface for image upload.
- **Backend**: Python Flask app with ONNX Runtime for liveness detection.
- **Sophisticated Liveness Detection**: Uses machine learning models to determine if the input image is from a live person or a spoof.

---

## Prerequisites

1. **System Requirements**:
   - A machine with Python 3.11+ installed.
   - Node.js 19+ and npm.

2. **Libraries and Tools**:
   - `pip` for Python package management.
   - `git` for cloning the repository.

---

## Setup Instructions

### 1. Backend

#### Steps to Set Up:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/humshubham/facial-liveness.git
   cd facial-liveness/backend
   ```

2. **Create a Python Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For MacOS/Linux
   # On Windows:
   # venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
   pip3 install -r requirements.txt
   ```

4. **Download the ONNX Model**:
   - Place the ONNX model (`liveness_model.onnx`) in the `models/` directory.
   - Ensure the path in the backend script points to this file.
   - A default model has been uploaded in this repository.

5. **Run the Backend**:
   ```bash
   uvicorn main:app --reload
   ```
   The backend will run at `http://127.0.0.1:8000`.

#### Backend File Structure:
```
backend/
├── app.py               # Main backend script
├── requirements.txt     # Python dependencies
├── models/
│   └── liveness_model.onnx  # ONNX model file
└── venv/                # Python virtual environment
```

---

### 2. Frontend

#### Steps to Set Up:

1. **Navigate to the Frontend Directory**:
   ```bash
   cd ../frontend
   ```

2. **Install Dependencies**:
   ```bash
   nvm install
   npm install
   ```

3. **Start the Frontend**:
   ```bash
   npm run dev
   ```
   The frontend will run at `http://localhost:5173`.

#### Frontend File Structure:
```
frontend/
├── src/
│   ├── App.tsx         # Main React component
│   ├── index.tsx       # Entry point
│   └── styles.css      # Styling
├── vite.config.ts      # Vite configuration
└── package.json        # Node.js dependencies
```

---

## Running the Application

1. **Start the Backend**:
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn main:app --reload
   ```

2. **Start the Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the App**:
   Open a web browser and navigate to `http://localhost:5173`.

---

## How the App Works

1. **Frontend Interaction**:
   - Users upload an image via the React interface.
   - The image is sent to the backend API for processing.

2. **Backend Processing**:
   - The backend receives the image.
   - It preprocesses the image and passes it to the ONNX model for liveness detection.
   - The model outputs a matrix of predictions.
   - The backend applies post-processing to classify the input as "live" or "spoof".

3. **Result Display**:
   - The result is sent back to the frontend.
   - The user sees the detection result displayed on the page.

---

## Acknowledgements

- [React Documentation](https://reactjs.org/docs/getting-started.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [ONNX Runtime Documentation](https://onnxruntime.ai/docs/)

