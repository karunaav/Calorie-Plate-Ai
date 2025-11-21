
import os

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from .vision import analyze_image_basic
from .gemini_client import analyze_calories_with_gemini
from .schemas import CalorieAnalysisRequest, CalorieAnalysisResponse

load_dotenv()

app = FastAPI(title="Calorie Plate AI Backend")

# CORS: allow local dev + Render frontend
origins = [
    # local dev (Vite)
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # production frontend on Render
    "https://calorie-plate-ai.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # you can temporarily use ["*"] while debugging
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/calc-image", response_model=CalorieAnalysisResponse)
async def calc_image(
    file: UploadFile = File(...),
    description: str = Form(""),
):
    """
    Accept an image + optional text description, run lightweight vision features,
    then call Gemini to estimate calories & macros.
    """
    if file.content_type is None or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image file.")

    # Ensure uploads directory exists (sibling of app/ folder)
    upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Run basic CV features
    img_features = analyze_image_basic(file_path)

    # Build prompt request for Gemini
    prompt_request = CalorieAnalysisRequest(
        description=description or "Unknown dish (user did not provide a description).",
        image_features=img_features,
    )

    try:
        analysis = analyze_calories_with_gemini(prompt_request)
    except Exception as e:
        # Print full traceback to logs on Render for debugging
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    # Combine everything into a structured response
    response = CalorieAnalysisResponse(
        image_features=img_features,
        model_name=analysis.get("model_name", "gemini"),
        total_calories=analysis.get("total_calories"),
        macros=analysis.get("macros"),
        reasoning=analysis.get("reasoning"),
        suggestions=analysis.get("suggestions"),
        raw_response=analysis.get("raw_response"),
    )

    return response

