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

```plaintext
mbti-api/
├── app.py                  # Main FastAPI server with all endpoints
├── mainfunction/           # Core NLP pipeline and feature extraction
│   ├── step_0.py           # Step 0: File validation & saving
│   ├── step_1.py           # Step 1: WhatsApp chat parsing
│   ├── step_2.py           # Step 2: Clean chat messages
│   ├── step_3.py           # Step 3: Extract linguistic features
│   ├── step_4.py           # Step 4: Generate per-user outputs
│   ├── step_5.py           # Step 5: TF-IDF keyword extraction
│   └── model.py            # MBTI prediction function using pre-trained model
├── model/                  # Folder for `.joblib` pre-trained model files
├── README.md               # Project documentation
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

