import torch
from PIL import Image
from transformers import AutoProcessor, CLIPModel

# Load model and processor
device = "cuda" if torch.cuda.is_available() else "cpu"
model_name = "patrickjohncyh/fashion-clip"
model = CLIPModel.from_pretrained(model_name).to(device)
processor = AutoProcessor.from_pretrained(model_name)

def extract_text_features(text: str):
    inputs = processor(text=text, return_tensors="pt", padding=True).to(device)
    with torch.no_grad():
        outputs = model.get_text_features(**inputs)
    return outputs[0].cpu().numpy()

def extract_image_features(image_file):
    image = Image.open(image_file).convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.get_image_features(**inputs)
    return outputs[0].cpu().numpy()
