import torch
import numpy as np
from src.model.autoencoder import PriceAutoencoder, prepare_sequences

def load_model(path: str = "data/autoencoder.pth"):
    checkpoint = torch.load(path, weights_only=False)
    model = PriceAutoencoder(input_size=7)
    model.load_state_dict(checkpoint["model_state"])
    model.eval()
    return model, checkpoint["min_val"], checkpoint["max_val"]

def get_reconstruction_error(model, sequence: list, min_val: float, max_val: float) -> float:
    
    arr = np.array(sequence, dtype=np.float32)
    normalized = (arr - min_val) / (max_val - min_val)
    tensor = torch.FloatTensor(normalized).unsqueeze(0)
    
    with torch.no_grad():
        output = model(tensor)
    
    error = torch.nn.functional.mse_loss(output, tensor).item()
    return error

def detect_anomaly(sequence: list, threshold: float = None) -> dict:
    
    model, min_val, max_val = load_model()
    error = get_reconstruction_error(model, sequence, min_val, max_val)
    
    
    if threshold is None:
        threshold = 0.01
    
    return {
        "reconstruction_error": error,
        "is_anomaly": error > threshold,
        "threshold": threshold
    }