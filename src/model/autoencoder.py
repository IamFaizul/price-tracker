import torch
import torch.nn as nn
import numpy as np

class PriceAutoencoder(nn.Module):
    
    def __init__(self, input_size: int = 7):
        super(PriceAutoencoder, self).__init__()
        
        # Encoder — data compress করে
        self.encoder = nn.Sequential(
            nn.Linear(input_size, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 4),
            nn.ReLU()
        )
        
        # Decoder — compressed data থেকে reconstruct করে
        self.decoder = nn.Sequential(
            nn.Linear(4, 8),
            nn.ReLU(),
            nn.Linear(8, 16),
            nn.ReLU(),
            nn.Linear(16, input_size),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

def prepare_sequences(prices: list, window_size: int = 7) -> np.ndarray:
    """Price list থেকে sliding window sequences বানায়"""
    sequences = []
    for i in range(len(prices) - window_size + 1):
        sequences.append(prices[i:i + window_size])
    return np.array(sequences)

def normalize(sequences: np.ndarray):
    """Min-Max normalization"""
    min_val = sequences.min()
    max_val = sequences.max()
    if max_val == min_val:
        return sequences, min_val, max_val
    normalized = (sequences - min_val) / (max_val - min_val)
    return normalized, min_val, max_val

def denormalize(value, min_val, max_val):
    """Normalized value কে original scale এ ফিরিয়ে আনে"""
    return value * (max_val - min_val) + min_val