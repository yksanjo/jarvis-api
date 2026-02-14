"""
Jarvis API - Standalone REST API Server
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import os
from datetime import datetime

app = FastAPI(title="Jarvis API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data file
DATA_FILE = os.path.expanduser("~/.jarvis_api_data.json")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"tasks": [], "events": [], "messages": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Models
class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: str = ""
    status: str = "pending"
    priority: str = "medium"
    dueDate: Optional[str] = None

class Event(BaseModel):
    id: Optional[int] = None
    title: str
    description: str = ""
    startTime: str
    endTime: Optional[str] = None
    location: Optional[str] = None

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

# Routes
@app.get("/")
def root():
    return {"name": "Jarvis API", "version": "1.0.0", "status": "running"}

@app.get("/api/tasks")
def get_tasks():
    data = load_data()
    return data["tasks"]

@app.post("/api/tasks")
def create_task(task: Task):
    data = load_data()
    task.id = len(data["tasks"]) + 1
    task.createdAt = datetime.now().isoformat()
    data["tasks"].append(task.dict())
    save_data(data)
    return task

@app.put("/api/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    data = load_data()
    for i, t in enumerate(data["tasks"]):
        if t["id"] == task_id:
            task.id = task_id
            data["tasks"][i] = task.dict()
            save_data(data)
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    data = load_data()
    data["tasks"] = [t for t in data["tasks"] if t["id"] != task_id]
    save_data(data)
    return {"status": "deleted"}

@app.get("/api/events")
def get_events():
    data = load_data()
    return data["events"]

@app.post("/api/events")
def create_event(event: Event):
    data = load_data()
    event.id = len(data["events"]) + 1
    data["events"].append(event.dict())
    save_data(data)
    return event

@app.delete("/api/events/{event_id}")
def delete_event(event_id: int):
    data = load_data()
    data["events"] = [e for e in data["events"] if e["id"] != event_id]
    save_data(data)
    return {"status": "deleted"}

@app.post("/api/chat")
def chat(request: ChatRequest):
    # Get last user message
    user_msgs = [m for m in request.messages if m.role == "user"]
    if user_msgs:
        last_msg = user_msgs[-1].content
        response = f"I understand: '{last_msg}'. This is a demo response."
    else:
        response = "Hello! I'm Jarvis API."
    return {"message": response, "done": True}

@app.get("/api/llm/status")
def llm_status():
    return {"running": False, "model": "", "error": None}

@app.get("/api/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
