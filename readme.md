```markdown
# 🧠 CLIP Vector API (FastAPI)

A lightweight **FastAPI-based** microservice for generating text and image embeddings using **OpenAI's CLIP model**. This can be used to power AI search, recommendation, or similarity systems for content like jewelry, fashion, art, or any domain needing visual & textual understanding.


---

## 🚀 Features

- 🔤 Text & Image Embedding with CLIP  
- ⚡ FastAPI server for real-time vectorization  
- 🧩 Ready for integration with Solr or other vector databases  
- 💡 Modular structure (`model_loader.py`, `utils.py`, etc.)

---

## 📦 Project Structure

```
clip_vector_api/
├── fast-api-env/           # (Optional) Virtual environment
├── main.py                 # FastAPI app entry point
├── model_loader.py         # CLIP model loading
├── utils.py                # Image preprocessing & utilities
├── requirements.txt        # Python dependencies
└── __pycache__/            # Python bytecode cache
```

---

## 🧪 Setup & Installation

### 1. Clone the repository

```bash
git clone 
cd clip_vector_api
```

### 2. Create & activate virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> Note: You may need to install PyTorch manually with the correct CUDA version from https://pytorch.org if you're using a GPU.

---

## 📄 `requirements.txt`

```
fastapi
uvicorn
torch
ftfy
regex
tqdm
Pillow
git+https://github.com/openai/CLIP.git
```

---

## ▶️ Running the API Server

```bash
uvicorn main:app --reload
```

The API will be available at:  
📍 `http://127.0.0.1:8000`

---

## 📫 API Usage (Sample)

### 🔡 `/vectorize/text` – Generate text embedding

```http
POST /vectorize/text
Content-Type: application/json

{
  "text": "Elegant diamond pendant in rose gold"
}
```

### 🖼️ `/vectorize/image` – Generate image embedding

Send an image via `multipart/form-data` using a form upload.

---

## 💡 Notes

- You can use the generated embeddings directly with vector search engines like **Solr**, **Weaviate**, **FAISS**, or **Pinecone**.
- The embeddings are 512-dimensional vectors from the ViT-B/32 CLIP model.

---
