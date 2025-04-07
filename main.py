from utils import extract_text_features, extract_image_features
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

@app.post("/vector/text")
def vector_from_text(text: str = Form(...)):
    print(f"Received text: {text}")
    try:
        vector = extract_text_features(text)

        if hasattr(vector, 'tolist'):
            vector = vector.tolist()

        return {
            "status": "success",
            "data": {
                "vector": vector
            }
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "status": "error",
            "error": str(e)
        })


@app.post("/vector/image")
async def vector_from_image(image: UploadFile = File(...)):
    try:
        vector = extract_image_features(image.file)

        if hasattr(vector, 'tolist'):
            vector = vector.tolist()

        return {
            "status": "success",
            "data": {
                "vector": vector
            }
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "status": "error",
            "error": str(e)
        })


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
