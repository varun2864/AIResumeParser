import uuid
from pathlib import Path

UPLOAD_DIR = Path("uploads")

def upload_resume(file_bytes: bytes, filename: str) -> str:
    UPLOAD_DIR.mkdir(parents = True, exist_ok = True) #ensures directory exists

    name = f"{uuid.uuid4()}-{filename}" #ensures unique file names
    path = UPLOAD_DIR / name #file path

    path.write_bytes(file_bytes) #writes file to disk

    return f"http://127.0.0.1:8000/uploads/resumes/{name}" #returns file url