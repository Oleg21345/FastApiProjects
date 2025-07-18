from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse, StreamingResponse

router = APIRouter(tags=["Файли"])


@router.post("/files")
async def upload_file(upload_file: UploadFile):
    file = upload_file.file
    file_name = upload_file.filename
    with open(f"1_{file_name}", "wb") as f:
        f.write(file.read())


@router.post("/upload_files")
async def upload_file(upload_file: list[UploadFile]):
    for upload in upload_file:
        file = upload.file
        file_name = upload.filename
        with open(f"1_{file_name}", "wb") as f:
            f.write(file.read())


@router.get("/files{file_name}")
async def get_files(filename: str):
    return FileResponse(filename)

async def generator(filename):
    with open(filename, "rb") as f:
        while chunk:= f.read(1024 * 1024):
            yield chunk


@router.get("/stremeng_files")
async def stream_file(filename):
    return StreamingResponse(generator(filename), media_type="video/webm")


