
# Backend – DeepSeek Computer Vision Calorie API

This FastAPI backend accepts a food image and an optional text description,
extracts some simple computer vision features (size, average color, brightness),
and then calls the DeepSeek Chat API to estimate calories and macronutrients.

## Setup

1. Create and activate a virtual environment (recommended):

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure your DeepSeek API key:

   - Sign up and create an API key on the DeepSeek platform.
   - Copy `.env.example` to `.env` and paste your key:

   ```bash
   cp .env.example .env
   # Then edit .env to put your DEEPSEEK_API_KEY
   ```

4. Start the backend server:

   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

The API will be live at `http://localhost:8000`.

### Key endpoints

- `GET /health` – simple health check.
- `POST /api/calc-image` – multipart/form-data with:
  - `file`: image file (jpeg/png/etc.)
  - `description` (optional): short text about the dish.

Returns a JSON payload with basic image features and DeepSeek's calorie analysis.
