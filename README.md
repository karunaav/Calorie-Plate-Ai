
# Computer Vision Calorie Calculator

This project is a small full-stack demo:

- **Backend (FastAPI)**: accepts a meal image + optional text description, performs a
  lightweight computer vision pass (size, average color, brightness), and then
  calls **DeepSeek Chat API** to estimate calories and macros.
- **Frontend (React + Vite)**: modern UI with a 3D-ish gradient dashboard where you
  upload the photo and view results.

⚠️ **Disclaimer**: This is a demo / educational app. Calorie estimates are rough,
may be inaccurate, and are not medical or dietary advice.

## How to run everything

1. **Backend**

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env and paste your real DEEPSEEK_API_KEY
   uvicorn app.main:app --reload --port 8000
   ```

2. **Frontend**

   In another terminal:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

   Open the printed localhost URL (usually `http://localhost:5173`).

3. **Use the app**

   - Upload a clear meal photo.
   - Optionally describe the dish (e.g., "1 cup dal, 1.5 cups rice, 1 chapati").
   - The backend will:
     - Extract simple visual features via Pillow + NumPy.
     - Send a structured prompt to DeepSeek (`deepseek-chat` model).
     - Return estimated calories + macros, reasoning, and suggestions.

You can later swap the `analyze_image_basic` function with a real food-recognition
model (e.g., a CNN trained on Food-101 or a segmentation model for portion sizes).
