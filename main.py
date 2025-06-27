from fastapi import FastAPI,Form,HTTPException,UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from threading import Thread, Lock
from queue import Queue
import time
import os
import signal
import pandas as pd
from joblib import load
import csv

from mainfunction.step_0 import check_file_size,validate_and_save_file
from mainfunction.step_1 import process_whatsapp_txt
from mainfunction.step_2 import clean_chat_file
from mainfunction.step_3 import extract_features_users
from mainfunction.step_4 import process_individual_outputs
from mainfunction.step_5 import extract_top_10_words_all_users
from mainfunction.model import predict_mbti
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 也可以写 ["*"] 测试阶段用
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 队列系统
task_queue = Queue()
status_data = {}  # filename: {"status": "queued" / "processing" / "completed", "log": []}
status_lock = Lock()


# 后台工作线程：持续监听队列
# 🔧 后台工作线程：持续监听队列
def worker():
    print("👷 Worker threat active, waiting for task...")
    while True:
        filename = task_queue.get()
        if filename is None:
            print("👋 filename empty terminal")
            break  # 用于优雅退出线程
        
        print(f"🚧 Worker start process: {filename}")
        with status_lock:
            status_data[filename]["status"] = "processing"
            status_data[filename]["step"] = "Queued"
            status_data[filename]["log"] = ["⚙️ start process..."]

        try:
            logs = []

            with status_lock:
                status_data[filename]["step"] = "Step 1: process_whatsapp_txt"
            logs.append("Step 1: process_whatsapp_txt start")
            process_whatsapp_txt(filename)
            logs.append("Step 1: done")

            with status_lock:
                status_data[filename]["step"] = "Step 2: clean_chat_file"
            logs.append("Step 2: clean_chat_file start")
            clean_chat_file(filename)
            logs.append("Step 2: done")

            with status_lock:
                status_data[filename]["step"] = "Step 3: extract_features_users"
            logs.append("Step 3: extract_features_users start")
            extract_features_users(filename)
            logs.append("Step 3: done")

            with status_lock:
                status_data[filename]["step"] = "Step 4: process_individual_outputs"
            logs.append("Step 4: process_individual_outputs start")
            process_individual_outputs(filename)
            logs.append("Step 4: done")
        

            with status_lock:
                status_data[filename]["status"] = "completed"
                status_data[filename]["step"] = "Done"
                status_data[filename]["log"] = logs

        except Exception as e:
            with status_lock:
                status_data[filename]["status"] = "error"
                status_data[filename]["step"] = "Error"
                status_data[filename]["log"] = [f"❌ Error: {str(e)}"]

        finally:
            task_queue.task_done()

            





# 启动后台线程
thread = Thread(target=worker, daemon=True)
thread.start()




@app.post("/queue")
async def handle_upload(filename: str = Form(...)):
    with status_lock:
        if filename not in status_data:
            # 初始化所有字段，包括 step
            status_data[filename] = {
                "status": "queued", 
                "step": "Queued",  # ✅ 初始化 step
                "log": ["⏳ waiting for process..."],
                "timestamp": time.time()
            }
            task_queue.put(filename)

        current_status = status_data[filename]["status"]
        return JSONResponse(content={
            "message": f"current status: {current_status}",
            "status": current_status,
            "step": status_data[filename].get("step", "未知"),
            "log": status_data[filename].get("log", [])
        })
    

@app.post("/model")
async def model(filename: str = Form(...)):
    result = predict_mbti(filename) 
    return JSONResponse(content={
        "status": "200",
        "data": result
    })


@app.api_route("/", methods=["GET", "POST"])
def root():
    return {"status": "FastAPI is active"}


SHUTDOWN_SECRET = "Abc12345"

@app.get("/shutdown")
async def shutdown(key: str):
    if key != SHUTDOWN_SECRET:
        raise HTTPException(status_code=403, detail="invalid")

    def stop():
        os.kill(os.getpid(), signal.SIGTERM)  # 用 SIGTERM 代替 SIGINT
    Thread(target=stop).start()

    return {"message": "server close"}

@app.get("/clean")
async def clean(key: str):
    if key != SHUTDOWN_SECRET:
        raise HTTPException(status_code=403, detail="无权访问")

    with status_lock:
        status_data.clear()

    while not task_queue.empty():
        try:
            task_queue.get_nowait()
        except:
            break

    task_queue.put(None)  # 通知后台线程退出
    return {"message": "✅ All Cleared"}

@app.post("/checkFile")
async def check_file(file: UploadFile = File(...),
                     filename: str = Form(...)):
    if not check_file_size(file.file):
        return {"success": False, "message": "File Size is over 2MB"}
    file.file.seek(0)
    if not validate_and_save_file(file.file,filename):
        return {"success": False, "message": "Invalid format or not WhatsApp history"}
    
    return {"success": True, "message": "File Valid you can proceed to next step"}


@app.post("/features")
async def get_features(filename: str = Form(...)):
    file_path = f"owndata/{filename}_user.csv"
    features = []

    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={
            "status": "404",
            "error": f"Feature file not found: {file_path}"
        })

    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                features.append(row)

    except Exception as e:
        return JSONResponse(status_code=500, content={
            "status": "500",
            "error": f"Error reading file: {str(e)}"
        })

    return {
        "status": "200",
        "features": features
    }


@app.post("/tfidf")
async def get_top_words(filename: str = Form(...)):
    base_name = filename.strip() + ".txt"
    try:
        results = extract_top_10_words_all_users(base_name)
        if not results:
            return JSONResponse(status_code=404, content={"status": "404", "error": "No data found for the given filename."})
        return {
            "status": "200",
            "tfidf": results
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "500", "error": str(e)})


