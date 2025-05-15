import os
from fastapi import UploadFile
from uuid import uuid4
from typing import Tuple


def save_uploaded_file(upload: UploadFile, upload_dir: str = "uploads") -> Tuple[str, str]:
    """
    Saves an uploaded resume file to the server with a unique filename.

    Args:
        upload (UploadFile): The file uploaded via FastAPI.
        upload_dir (str): Directory where the file will be saved. Defaults to 'uploads'.

    Returns:
        Tuple[str, str]: The full file path and the original filename.
    """
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    original_filename = upload.filename
    ext = os.path.splitext(original_filename)[-1]
    unique_filename = f"{uuid4().hex}{ext}"
    file_path = os.path.join(upload_dir, unique_filename)

    with open(file_path, "wb") as f:
        content = upload.file.read()
        f.write(content)

    return file_path, original_filename
