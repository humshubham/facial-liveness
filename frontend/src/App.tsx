import React, { useRef, useState } from "react";
import axios from "axios";

const App = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isLivenessChecked, setLivenessChecked] = useState(false);
  const [message, setMessage] = useState("Initializing...");

  // Start webcam
  const startVideo = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
        setMessage("Webcam started. Looking for liveness...");
        startLivenessDetection();
      }
    } catch (error) {
      setMessage("Error accessing webcam. Please allow camera access.");
      console.error("Error starting webcam:", error);
    }
  };

  // Liveness detection logic
  const startLivenessDetection = () => {
    const interval = setInterval(async () => {
      if (isLivenessChecked) {
        clearInterval(interval); // Stop detection if liveness confirmed
        return;
      }

      if (videoRef.current) {
        const canvas = document.createElement("canvas");
        const video = videoRef.current;

        // Capture the current frame from the video
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext("2d");
        if (context) {
          context.drawImage(video, 0, 0, canvas.width, canvas.height);
          const dataURL = canvas.toDataURL("image/jpeg");
          const blob = await fetch(dataURL).then((res) => res.blob());
          const file = new File([blob], "frame.jpg", { type: "image/jpeg" });

          // Prepare form data
          const formData = new FormData();
          formData.append("file", file);

          try {
            // Send frame to backend
            const response = await axios.post(
              "http://127.0.0.1:8000/check_liveness",
              formData,
              {
                headers: { "Content-Type": "multipart/form-data" },
              }
            );

            // Handle response
            if (response.data.is_live) {
              setMessage(response.data.message);
              setLivenessChecked(true);
              clearInterval(interval);
            } else {
              setMessage(response.data.message);
            }
          } catch (error) {
            setMessage(
              "Error during detection. Check the console for details."
            );
            console.error("Error detecting liveness:", error);
          }
        }
      }
    }, 3000); // Capture every second
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Facial Liveness Detection</h1>
      <video
        ref={videoRef}
        style={{ border: "1px solid black", width: "500px", height: "auto" }}
      />
      <p>{message}</p>
      {!isLivenessChecked && (
        <button
          onClick={startVideo}
          style={{ padding: "10px 20px", fontSize: "16px" }}
        >
          Start Liveness Detection
        </button>
      )}
    </div>
  );
};

export default App;
