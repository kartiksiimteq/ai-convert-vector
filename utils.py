import torch
import clip
from PIL import Image
import io

# Load model only once
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def extract_text_features(text: str):
    with torch.no_grad():
        text_tokens = clip.tokenize([text]).to(device)
        text_features = model.encode_text(text_tokens)
        return text_features[0].cpu().numpy()

def extract_image_features(image_file):
    image = Image.open(image_file).convert("RGB")
    image_input = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image_input)
        return image_features[0].cpu().numpy()
