# 🧠 MBTI Personality Prediction API using WhatsApp Chat (FastAPI)

This is a backend-only **FastAPI-based MBTI personality prediction system**, built to analyze WhatsApp chat history and return psychological traits. The system uses a trained machine learning model to predict one of the 16 MBTI types (e.g., INFP, ESTJ, etc.) based on features extracted from chat content.

## 🚀 Project Overview

- 🧾 Input: WhatsApp `.txt` exported chat file  
- 🔎 Processing: Text cleaning → feature extraction → personality prediction  
- 🧠 Output: MBTI personality type (e.g., INTJ, ENFP)  
- 🧱 Architecture: FastAPI with background task queue and feature-serving endpoints  
- 📦 No training phase included — model is pre-trained and bundled

---

## 📁 File Structure

📦 mbti-api
├── app.py # Main FastAPI server with endpoints
├── mainfunction/ # Core NLP and feature extraction pipeline
│ ├── step_0.py # File validation & saving
│ ├── step_1.py # WhatsApp parsing
│ ├── step_2.py # Chat cleaning
│ ├── step_3.py # Feature extraction
│ ├── step_4.py # Individual user output
│ ├── step_5.py # TF-IDF keyword extraction
│ └── model.py # Pre-trained MBTI prediction model
├── model/ # Contains .joblib trained model files
└── README.md # This file


---

## 🛠️ API Endpoints

### 1. `POST /checkFile`
Check if the uploaded WhatsApp file is valid and under 2MB.

**Form data:**
- `file`: WhatsApp `.txt` file
- `filename`: Name to save under

**Returns:** `{ "success": True/False, "message": "..." }`

---

### 2. `POST /queue`
Begin processing the uploaded file via background queue.

**Form data:**
- `filename`: Previously uploaded file name

**Returns:** Task status and logs.

---

### 3. `POST /model`

**Description:**  
Run the MBTI prediction model on the processed chat file. This endpoint returns the predicted MBTI personality type only.

**Form Data:**

- `filename` (str): Target file to analyze

**Response:**

```json
{
  "status": "200",
  "data": {
    "MBTI": "INFP"
  }
}

